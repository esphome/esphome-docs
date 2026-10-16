#!/usr/bin/env node
/**
 * Check component documentation against the ESPHome language schema.
 *
 * Parses the MDX with remark, routes every "Configuration variables" section
 * to a schema from the page path, the heading structure or an explicit
 * `{/* schema: <ref> *\/}` marker, and compares the documented keys with the
 * schema's keys in both directions.
 *
 * Usage:
 *   node script/check_schema_docs.mjs [--schema-dir DIR | --schema-url URL]
 *                                     [--file SUBSTR] [--json OUT]
 *                                     [--baseline FILE] [--check] [--verbose]
 */

import { existsSync, readFileSync, readdirSync, statSync, writeFileSync } from "node:fs";
import { basename, dirname, join, relative } from "node:path";
import { pathToFileURL } from "node:url";
import { parseArgs } from "node:util";
import { toString } from "mdast-util-to-string";
import remarkMath from "remark-math";
import remarkMdx from "remark-mdx";
import remarkParse from "remark-parse";
import { unified } from "unified";

const DOCS_ROOT = join("src", "content", "docs");
const COMPONENTS_ROOT = join(DOCS_ROOT, "components");
const DEFAULT_SCHEMA_URL = "https://schema.esphome.io/dev";
const DEFAULT_BASELINE = join("script", "schema_docs_baseline.json");

const CONFIG_VARS_RE = /^Configuration (variables|options):?$/i;
const MARKER_RE = /^\s*\/\*\s*schema:\s*(\S+)\s*\*\/\s*$/;
const REGISTRY_TYPES = new Set(["action", "condition", "filter", "effects"]);

// Bus and base schema keys that the extractor copies into every device schema;
// they are documented once on the bus page, not per component.
const INHERITED_KEYS = new Set([
  "id",
  "address",
  "i2c_id",
  "spi_id",
  "uart_id",
  "cs_pin",
  "data_rate",
  "spi_mode",
  "psram_dma",
  "release_device",
  "update_interval",
]);

// Platform registries documented as headings: [registry key, title suffix]
const REGISTRY_NAME_ODDITIES = {
  "light.effects": { automation_light: "automation", e_1_31: "e131" },
};

const COMPONENT_REGISTRIES = {
  light: [["effects", " Effect"]],
  binary_sensor: [["filter", null]],
  text_sensor: [["filter", null]],
  sensor: [["filter", " Filter"]],
};

const isMain = process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href;

const { values: args } = parseArgs({
  args: isMain ? undefined : [],
  options: {
    "schema-dir": { type: "string" },
    "schema-url": { type: "string", default: DEFAULT_SCHEMA_URL },
    file: { type: "string" },
    json: { type: "string" },
    baseline: { type: "string", default: DEFAULT_BASELINE },
    "update-baseline": { type: "boolean", default: false },
    check: { type: "boolean", default: false },
    verbose: { type: "boolean", short: "v", default: false },
    resolve: { type: "string" },
  },
});

// ---------------------------------------------------------------------------
// Schema access
// ---------------------------------------------------------------------------

export class SchemaStore {
  constructor({ dir, url }) {
    this.dir = dir;
    this.url = url;
    this.files = new Map();
    this.core = null;
  }

  async init() {
    const esphome = await this.file("esphome");
    this.core = esphome.core;
  }

  async file(name) {
    if (this.files.has(name)) return this.files.get(name);
    let doc = null;
    if (this.dir) {
      const path = join(this.dir, `${name}.json`);
      if (existsSync(path)) doc = JSON.parse(readFileSync(path, "utf8"));
    } else {
      const res = await fetch(`${this.url}/${name}.json`);
      if (res.ok) doc = await res.json();
    }
    this.files.set(name, doc);
    return doc;
  }

  isPlatform(name) {
    return Object.hasOwn(this.core.platforms, name);
  }

  isComponent(name) {
    return Object.hasOwn(this.core.components, name);
  }

  /**
   * Resolve a schema reference to its inner schema.
   *   comp.NAME                 -> file comp, top comp, schemas.NAME
   *   comp.platform.NAME        -> file comp, top comp.platform, schemas.NAME
   *   comp.action.x[.y]        -> registry entry
   *   comp.platform.action.x   -> registry entry on a platform component
   *   core.action.x             -> esphome.json core registry
   *   ref[VARIANT]              -> one variant of a typed schema
   */
  async resolve(ref) {
    if (ref.includes("/")) {
      const [base, ...props] = ref.split("/");
      let inner = await this.resolve(base);
      for (const prop of props) inner = propInner(await this.findProp(inner, prop));
      return inner;
    }
    if (ref.includes("+")) {
      const inners = await Promise.all(ref.split("+").map((r) => this.resolve(r)));
      const variants = inners.filter(Boolean).flatMap((i) => i.variants);
      return variants.length ? { variants } : null;
    }
    if (ref.endsWith(".*")) {
      // Every schema of a platform base page (sensor/index.mdx documents
      // SENSOR_SCHEMA and the derived schemas that add filters, triggers, ...)
      const top = ref.slice(0, -2);
      const doc = await this.file(top.split(".")[0]);
      const variants = Object.values(doc ?? {})
        .filter((body) => body && typeof body === "object" && body.schemas)
        .flatMap((body) => Object.values(body.schemas))
        .map((entry) => toInner(entry))
        .filter(Boolean)
        .flatMap((inner) => inner.variants);
      return variants.length ? { variants } : null;
    }
    let variant = null;
    const m = ref.match(/^(.*)\[([^\]]+)\]$/);
    if (m) [, ref, variant] = m;
    const parts = ref.split(".");
    if (parts[0] === "core") {
      const entry = REGISTRY_TYPES.has(parts[1])
        ? this.core?.[parts[1]]?.[parts.slice(2).join(".")]
        : this.core?.schemas?.[parts[1]];
      if (!entry) return null;
      return toInner(entry, variant) ?? (REGISTRY_TYPES.has(parts[1]) ? { variants: [{}] } : null);
    }
    const doc = await this.file(parts[0]);
    if (!doc) return null;
    for (const topLen of [1, 2]) {
      const top = doc[parts.slice(0, topLen).join(".")];
      if (!top) continue;
      const rest = parts.slice(topLen);
      if (rest.length === 0) continue;
      if (REGISTRY_TYPES.has(rest[0])) {
        const entry = top[rest[0]]?.[rest.slice(1).join(".")];
        if (entry) return toInner(entry, variant) ?? { variants: [{}] };
      } else if (rest.length === 1) {
        const entry = top.schemas?.[rest[0]];
        if (entry) return toInner(entry, variant);
      }
    }
    return null;
  }

  async exists(ref) {
    return (await this.resolve(ref)) !== null;
  }

  async schemaNames(topRef) {
    const parts = topRef.split(".");
    const doc = await this.file(parts[0]);
    return Object.keys(doc?.[topRef]?.schemas ?? {});
  }

  /** Find a config var by name, following extends. */
  async findProp(inner, name, seen = new Set()) {
    if (!inner) return null;
    if (inner.typedKey === name) return { key: "Required", type: "enum" };
    for (const variantInner of inner.variants) {
      if (variantInner.config_vars && Object.hasOwn(variantInner.config_vars, name)) {
        return variantInner.config_vars[name];
      }
      for (const ext of variantInner.extends ?? []) {
        if (seen.has(ext)) continue;
        seen.add(ext);
        const found = await this.findProp(await this.resolve(ext), name, seen);
        if (found) return found;
      }
    }
    return null;
  }

  /** Every definition of a key across typed variants and extends. */
  async findProps(inner, name) {
    const props = [];
    if (!inner) return props;
    if (inner.typedKey === name) props.push({ key: "Required", type: "enum" });
    for (const variantInner of inner.variants) {
      const own = variantInner.config_vars?.[name];
      if (own) props.push(own);
      for (const ext of variantInner.extends ?? []) {
        props.push(...(await this.findProps(await this.resolve(ext), name)));
      }
    }
    return props;
  }

  /** Look for a key one or two levels below this schema (documented flat). */
  async findNestedProp(inner, name, depth = 2) {
    if (!inner || depth === 0) return null;
    for (const variantInner of inner.variants) {
      for (const child of Object.values(variantInner.config_vars ?? {})) {
        const childInner = propInner(child);
        if (!childInner) continue;
        const direct = await this.findProp(childInner, name);
        if (direct) return direct;
        const deeper = await this.findNestedProp(childInner, name, depth - 1);
        if (deeper) return deeper;
      }
    }
    return null;
  }

  /** `target_N` / `gX` in the docs stand for target_1, target_2, ... in the schema. */
  numberedFamily(inner, name) {
    const m = name.match(/^(.*?)_?[NX]$/);
    if (!m || !m[1]) return [];
    const re = new RegExp(`^${m[1]}_?\\d+$`);
    const keys = [];
    for (const variantInner of inner.variants) {
      for (const k of Object.keys(variantInner.config_vars ?? {})) if (re.test(k)) keys.push(k);
    }
    return keys;
  }

  /** Keys declared directly on this schema (not inherited), excluding generated ids. */
  ownKeys(inner) {
    const keys = new Set();
    for (const variantInner of inner.variants) {
      for (const [k, v] of Object.entries(variantInner.config_vars ?? {})) {
        if (v.key !== "Required" && v.key !== "Optional") continue;
        if (v.visibility === "yaml_only") continue;
        if (INHERITED_KEYS.has(k)) continue;
        keys.add(k);
      }
    }
    if (inner.typedKey) keys.add(inner.typedKey);
    return keys;
  }
}

/** Normalise a config var / schema entry to { variants: [{config_vars, extends}] }. */
export function toInner(entry, variant = null) {
  if (!entry || typeof entry !== "object") return null;
  if (entry.type === "typed") {
    const types = variant ? { [variant]: entry.types?.[variant] } : (entry.types ?? {});
    const variants = Object.values(types).filter(Boolean);
    return variants.length ? { variants, typedKey: entry.typed_key ?? "type" } : null;
  }
  if (entry.schema && typeof entry.schema === "object") {
    return { variants: [entry.schema] };
  }
  if (entry.config_vars || entry.extends) {
    return { variants: [entry] };
  }
  return null;
}

function propInner(prop) {
  if (!prop) return null;
  if (prop.type === "enum") return null;
  return toInner(prop);
}

// ---------------------------------------------------------------------------
// Doc walking
// ---------------------------------------------------------------------------

function listMdx(dir) {
  const out = [];
  for (const name of readdirSync(dir).sort()) {
    const path = join(dir, name);
    if (statSync(path).isDirectory()) out.push(...listMdx(path));
    else if (name.endsWith(".mdx")) out.push(path);
  }
  return out;
}

export function parseMdx(path) {
  let src = readFileSync(path, "utf8");
  // Frontmatter is not markdown; drop it but keep line numbers stable.
  src = src.replace(/^---\n[\s\S]*?\n---\n/, (fm) => fm.replace(/[^\n]/g, ""));
  return unified().use(remarkParse).use(remarkMath).use(remarkMdx).parse(src);
}

function slug(text) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "_")
    .replace(/^_+|_+$/g, "");
}

/** `name` Action -> {name, type} using the inlineCode node, not the text. */
export function registryHeading(node) {
  const code = node.children.find((c) => c.type === "inlineCode");
  if (!code) return null;
  const rest = toString({ children: node.children.filter((c) => c !== code) }).trim();
  const m = rest.match(/^(Action|Condition)$/i);
  if (!m) return null;
  return { name: code.value, type: m[1].toLowerCase() };
}

function bareCodeHeading(node) {
  const c = node.children;
  if (c.length === 1 && c[0].type === "inlineCode") return c[0].value;
  if (c.length >= 1 && c[0].type === "inlineCode" && c.slice(1).every((n) => n.type === "text" && !n.value.trim())) {
    return c[0].value;
  }
  return null;
}

/** Extract {key, optionality, line} from a list item's first paragraph. */
export function parseItem(item) {
  const para = item.children.find((c) => c.type === "paragraph");
  if (!para) return null;
  const [first, ...rest] = para.children;
  if (!first || first.type !== "strong") return null;
  const key = toString(first).trim();
  // YAML keys are lower snake_case; `target_N` / `gX` stand for numbered families
  if (!/^[a-z0-9_]+[NX]?$/.test(key)) return { prose: true, key, line: para.position.start.line };
  let optionality = null;
  // Expected shape: **key** (**Required**, type): ...  /  **key** (*Optional*, type): ...
  if (rest[0]?.type === "text" && /^\s*\(\s*$/.test(rest[0].value)) {
    const marker = rest[1];
    if (marker && (marker.type === "strong" || marker.type === "emphasis")) {
      const word = toString(marker).trim().toLowerCase();
      if (word === "required" || word === "optional") optionality = word;
    }
  }
  return { key, optionality, line: para.position.start.line };
}

export class Report {
  constructor() {
    this.findings = [];
    this.stats = {
      files: 0,
      sections: 0,
      sectionsUnroutable: 0,
      sectionsByMarker: 0,
      keysMatched: 0,
      keysMatchedNested: 0,
      keysUnmatched: 0,
      keysUndocumented: 0,
      optionalityMismatch: 0,
      proseBullets: 0,
    };
  }

  add(kind, file, line, detail) {
    this.findings.push({ kind, file, line, ...detail });
  }
}

export class Walker {
  constructor(store, report, file) {
    this.store = store;
    this.report = report;
    this.file = file;
    this.rel = relative(COMPONENTS_ROOT, file).replace(/\\/g, "/");
    this.stem = basename(file, ".mdx");
    this.folder = basename(dirname(file));
    this.section = null; // { inner, ref, depth, documented:Set, subStack:[] }
    this.pendingMarker = null;
    this.pendingRegistry = null; // ref set by a `x.y` Action heading
    this.defaultRef = null;
    this.componentRef = null; // top ref like "uart" or "template.sensor" for named-schema lookup
  }

  async init() {
    const { store } = this;
    const inComponents = this.file.startsWith(COMPONENTS_ROOT);
    if (!inComponents) {
      this.defaultRef = null;
      this.componentRef = "core";
      return;
    }
    const folderIsPlatform = this.folder !== "components" && store.isPlatform(this.folder);
    if (this.stem === "index" && this.folder === "components") return;
    if (folderIsPlatform && this.stem === "index") {
      this.defaultRef = `${this.folder}.*`;
      this.componentRef = this.folder;
    } else if (folderIsPlatform) {
      this.componentRef = `${this.stem}.${this.folder}`;
      this.defaultRef = await this.componentSchemaRef(this.stem, this.folder);
    } else if (this.folder === "filter" && store.isPlatform(basename(dirname(dirname(this.file))))) {
      const platform = basename(dirname(dirname(this.file)));
      this.componentRef = platform;
      this.defaultRef = `${platform}.filter.${this.stem}`;
    } else {
      const comp = this.stem === "index" ? this.folder : this.stem;
      this.componentRef = comp;
      this.defaultRef = await this.componentSchemaRef(comp);
    }
  }

  /** foo.CONFIG_SCHEMA, or the union of foo_i2c/foo_spi when foo itself has none. */
  async componentSchemaRef(name, platform = null) {
    const { store } = this;
    const suffix = platform ? `.${platform}.CONFIG_SCHEMA` : ".CONFIG_SCHEMA";
    if (await store.exists(`${name}${suffix}`)) return `${name}${suffix}`;
    const buses = [];
    for (const bus of ["i2c", "spi"]) {
      if (await store.exists(`${name}_${bus}${suffix}`)) buses.push(`${name}_${bus}${suffix}`);
    }
    return buses.length ? buses.join("+") : null;
  }

  async switchComponent(name) {
    // A heading such as "FooBar Component" / "Sensor" re-targets the rest of the page
    const platform = this.folder !== "components" && this.store.isPlatform(this.folder) ? this.folder : null;
    for (const ref of [
      await this.componentSchemaRef(name),
      platform && (await this.componentSchemaRef(name, platform)),
    ]) {
      if (ref) {
        this.defaultRef = ref;
        this.componentRef = ref.split("+")[0].replace(/\.CONFIG_SCHEMA$/, "");
        return true;
      }
    }
    return false;
  }

  async registryRef(name, type) {
    const { store } = this;
    const parts = name.split(".");
    const candidates = [];
    if (parts.length === 1) {
      candidates.push(`${this.componentRef}.${type}.${name}`);
      candidates.push(`core.${type}.${name}`);
    } else if (parts.length === 2) {
      candidates.push(`${parts[0]}.${type}.${parts[1]}`);
    } else if (store.isPlatform(parts[0])) {
      candidates.push(`${parts[1]}.${parts[0]}.${type}.${parts.slice(2).join(".")}`);
    } else {
      candidates.push(`${parts[0]}.${type}.${parts.slice(1).join(".")}`);
    }
    for (const ref of candidates) if (await store.exists(ref)) return ref;
    return null;
  }

  async findRegistryEntry(headingText) {
    const { store } = this;
    const platform = store.isPlatform(this.folder) ? this.folder : this.componentRef;
    for (const [registry, suffix] of COMPONENT_REGISTRIES[platform] ?? []) {
      let name = null;
      if (suffix === null) {
        const m = headingText.match(/^`(.+)`$/);
        if (m) name = m[1];
      } else if (headingText.endsWith(suffix)) {
        name = slug(headingText.slice(0, -suffix.length));
        name = REGISTRY_NAME_ODDITIES[`${platform}.${registry}`]?.[name] ?? name;
      }
      if (name) {
        const ref = `${platform}.${registry}.${name}`;
        if (await store.exists(ref)) return ref;
      }
    }
    return null;
  }

  async openSection(ref, depth, line, source) {
    const { store, report } = this;
    if (this.section && this.section.ref === ref) {
      this.section.depth = Math.max(this.section.depth, depth);
      return;
    }
    await this.closeSection();
    report.stats.sections++;
    if (source === "marker") report.stats.sectionsByMarker++;
    const inner = ref ? await store.resolve(ref) : null;
    if (!inner) {
      report.stats.sectionsUnroutable++;
      report.add("unroutable_section", this.rel, line, {
        detail: ref ? `schema '${ref}' not found` : "no schema for this page section",
      });
      this.section = null;
      return;
    }
    this.section = { ref, inner, depth, documented: new Set(), line };
  }

  async closeSection() {
    const s = this.section;
    if (!s) return;
    this.section = null;
    for (const key of this.store.ownKeys(s.inner)) {
      if (!s.documented.has(key)) {
        this.report.stats.keysUndocumented++;
        this.report.add("undocumented_key", this.rel, s.line, { schema: s.ref, key });
      }
    }
  }

  async walk(tree) {
    this.report.stats.files++;
    for (const node of tree.children) {
      if (node.type === "heading") await this.heading(node);
      else if (node.type === "paragraph") await this.paragraph(node);
      else if (node.type === "list") await this.list(node);
      else if (node.type === "mdxFlowExpression") this.expression(node);
    }
    await this.closeSection();
  }

  expression(node) {
    const m = node.value.match(MARKER_RE);
    if (m) this.pendingMarker = m[1];
  }

  async paragraph(node) {
    const text = toString(node).trim();
    if (CONFIG_VARS_RE.test(text) && node.children.length === 1 && node.children[0].type === "strong") {
      // **Configuration variables:** used as a pseudo heading under an action
      await this.openConfigSection(this.section?.depth ?? 2, node.position.start.line);
    }
  }

  async openConfigSection(depth, line) {
    if (this.pendingMarker) {
      const ref = this.pendingMarker;
      this.pendingMarker = null;
      await this.openSection(ref, depth, line, "marker");
    } else if (this.pendingRegistry) {
      const ref = this.pendingRegistry;
      this.pendingRegistry = null;
      await this.openSection(ref, depth, line, "registry");
    } else {
      await this.openSection(this.defaultRef, depth, line, "default");
    }
  }

  async heading(node) {
    const { store } = this;
    const text = toString(node).trim();
    const line = node.position.start.line;

    if (CONFIG_VARS_RE.test(text)) {
      await this.openConfigSection(node.depth, line);
      return;
    }

    // Any other heading ends a section at the same or higher level
    if (this.section && node.depth <= this.section.depth) await this.closeSection();
    if (this.pendingRegistry && node.depth <= this.pendingRegistryDepth) this.pendingRegistry = null;

    const reg = registryHeading(node);
    if (reg) {
      const ref = await this.registryRef(reg.name, reg.type);
      if (ref) {
        // Many action docs list options directly under the heading
        await this.openSection(ref, node.depth, line, "registry");
        this.pendingRegistry = ref;
        this.pendingRegistryDepth = node.depth;
      } else {
        this.report.add("unknown_registry_entry", this.rel, line, {
          detail: `${reg.type} '${reg.name}' not in schema`,
        });
        this.pendingRegistry = null;
      }
      return;
    }

    const registryEntry = await this.findRegistryEntry(
      node.children.some((c) => c.type === "inlineCode") ? `\`${bareCodeHeading(node) ?? ""}\`` : text,
    );
    if (registryEntry) {
      this.pendingRegistry = registryEntry;
      this.pendingRegistryDepth = node.depth;
      return;
    }

    if (/ Component$/.test(text)) {
      const name = slug(text.replace(/ Component$/, "").replace(/\./g, ""));
      if (await this.switchComponent(name)) return;
    }
    if (text === "Component/Hub" || text === "Hub Component") {
      if (await this.switchComponent(this.stem)) return;
    }
    if (/Over SPI$/i.test(text) && (await this.switchComponent(`${this.stem}_spi`))) return;
    if (/Over I²C$/i.test(text) && (await this.switchComponent(`${this.stem}_i2c`))) return;
    if (this.stem !== "index") {
      let platformName = slug(text);
      const prefix = `${slug(this.componentRef?.split(".")[0] ?? "")}_`;
      if (platformName.startsWith(prefix)) platformName = platformName.slice(prefix.length);
      if (store.isPlatform(platformName)) {
        const ref = await this.componentSchemaRef(this.stem, platformName);
        if (ref) {
          this.defaultRef = ref;
          this.componentRef = `${this.stem}.${platformName}`;
          return;
        }
      }
      // "## Clockless" in fastled.mdx -> fastled_clockless
      if (await this.switchComponent(`${this.stem}_${slug(text)}`)) return;
    }

    // A heading naming a sibling schema, e.g. "Light state" -> LIGHT_STATE_SCHEMA
    if (this.componentRef && this.componentRef !== "core") {
      const candidate = `${slug(text).toUpperCase()}_SCHEMA`;
      if ((await store.schemaNames(this.componentRef)).includes(candidate)) {
        await this.openSection(`${this.componentRef}.${candidate}`, node.depth, line, "heading");
        return;
      }
    }

    const code = bareCodeHeading(node);
    if (code && !this.section && /^[a-z0-9_]+$/.test(code) && (await this.switchComponent(code))) return;

    // "## Legend Options" documents the `legend` sub-schema of the page's schema
    if (this.defaultRef && !this.section) {
      const first = slug(text).split("_")[0];
      const base = await store.resolve(this.defaultRef);
      const prop = first && (await store.findProp(base, first));
      if (prop && propInner(prop) && !(await store.findProp(base, slug(text)))) {
        await this.openSection(`${this.defaultRef}/${first}`, node.depth, line, "heading");
        return;
      }
    }

    // `prop` sub-heading inside an open section: describe a nested schema
    if (code && this.section && node.depth > this.section.depth) {
      const prop = await store.findProp(this.section.inner, code);
      const inner = propInner(prop);
      if (inner) {
        this.section.documented.add(code);
        this.section = {
          ...this.section,
          inner,
          depth: node.depth,
          documented: new Set(),
          parent: this.section,
          line,
        };
        this.section.closeToParent = true;
      }
    }
  }

  async list(node) {
    if (!this.section) return;
    await this.items(node, this.section.inner, this.section.documented);
  }

  async items(listNode, inner, documented) {
    const { store, report } = this;
    for (const item of listNode.children) {
      const parsed = parseItem(item);
      if (!parsed) continue;
      if (parsed.prose) {
        report.stats.proseBullets++;
        continue;
      }
      let prop = await store.findProp(inner, parsed.key);
      if (!prop) {
        const family = store.numberedFamily(inner, parsed.key);
        if (family.length) {
          report.stats.keysMatched++;
          for (const k of family) documented.add(k);
          continue;
        }
        prop = await store.findNestedProp(inner, parsed.key);
        if (prop) {
          report.stats.keysMatchedNested++;
          continue;
        }
      }
      if (!prop) {
        report.stats.keysUnmatched++;
        report.add("unmatched_key", this.rel, parsed.line, {
          schema: this.section?.ref,
          key: parsed.key,
        });
        continue;
      }
      report.stats.keysMatched++;
      documented.add(parsed.key);
      if (parsed.optionality) {
        // With typed schemas a key may be Required in one variant and Optional
        // in another; only report when no variant agrees with the docs.
        const marked = (await store.findProps(inner, parsed.key))
          .map((p) => p.key?.toLowerCase())
          .filter((k) => k === "required" || k === "optional");
        if (marked.length && !marked.includes(parsed.optionality)) {
          report.stats.optionalityMismatch++;
          report.add("optionality_mismatch", this.rel, parsed.line, {
            schema: this.section?.ref,
            key: parsed.key,
            detail: `docs say ${parsed.optionality}, schema says ${marked[0]}`,
          });
        }
      }
      const nested = item.children.find((c) => c.type === "list");
      if (nested) {
        const nestedInner = propInner(prop);
        if (nestedInner) await this.items(nested, nestedInner, new Set());
      }
    }
  }
}

// Sub-sections opened by `prop` headings must fall back to the parent on close.
const originalClose = Walker.prototype.closeSection;
Walker.prototype.closeSection = async function () {
  while (this.section?.parent) {
    this.section = this.section.parent;
  }
  await originalClose.call(this);
};

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
  const store = new SchemaStore({ dir: args["schema-dir"], url: args["schema-url"] });
  await store.init();
  if (args.resolve) {
    const inner = await store.resolve(args.resolve);
    console.log(inner ? JSON.stringify([...store.ownKeys(inner)]) : "not found");
    return inner ? 0 : 1;
  }
  const report = new Report();

  let files = listMdx(COMPONENTS_ROOT);
  files.push(join(DOCS_ROOT, "automations", "actions.mdx"));
  if (args.file) files = files.filter((f) => f.includes(args.file));

  for (const file of files) {
    let tree;
    try {
      tree = parseMdx(file);
    } catch (err) {
      report.add("parse_error", relative(COMPONENTS_ROOT, file), err.line ?? 0, { detail: err.message });
      continue;
    }
    const walker = new Walker(store, report, file);
    await walker.init();
    await walker.walk(tree);
  }

  const baselinePath = args.baseline;
  const findingKey = (f) => `${f.kind}|${f.file}|${f.schema ?? ""}|${f.key ?? f.detail ?? ""}`;
  if (args["update-baseline"]) {
    const keys = [...new Set(report.findings.map(findingKey))].sort();
    writeFileSync(baselinePath, `${JSON.stringify(keys, null, 2)}\n`);
    console.log(`Wrote ${keys.length} entries to ${baselinePath}`);
    return 0;
  }
  const baseline = new Set(
    args.check && existsSync(baselinePath) ? JSON.parse(readFileSync(baselinePath, "utf8")) : [],
  );

  if (args.json) {
    writeFileSync(args.json, JSON.stringify({ stats: report.stats, findings: report.findings }, null, 2));
  }

  let newFindings = 0;
  const order = [
    "parse_error",
    "unroutable_section",
    "unknown_registry_entry",
    "unmatched_key",
    "optionality_mismatch",
    "undocumented_key",
  ];
  const shown = new Set(args.verbose ? order : order.slice(0, 5));
  for (const f of report.findings.sort((a, b) => a.file.localeCompare(b.file) || a.line - b.line)) {
    if (baseline.has(findingKey(f))) continue;
    newFindings++;
    if (!shown.has(f.kind)) continue;
    const what = f.key ? `'${f.key}'` : "";
    console.log(
      `${f.file}:${f.line}: ${f.kind} ${what} ${f.schema ? `[${f.schema}]` : ""} ${f.detail ?? ""}`
        .replace(/\s+/g, " ")
        .trim(),
    );
  }

  const s = report.stats;
  console.log(
    [
      `files ${s.files}`,
      `sections ${s.sections} (unroutable ${s.sectionsUnroutable}, by marker ${s.sectionsByMarker})`,
      `keys matched ${s.keysMatched} (+${s.keysMatchedNested} via nested schema), not in schema ${s.keysUnmatched}, in schema but undocumented ${s.keysUndocumented}`,
      `optionality mismatches ${s.optionalityMismatch}`,
      `prose bullets skipped ${s.proseBullets}`,
    ].join("\n"),
  );
  if (args.check) {
    console.log(`${newFindings} findings not in baseline`);
    return newFindings ? 1 : 0;
  }
  return 0;
}

if (isMain) process.exitCode = await main();
