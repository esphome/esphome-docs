#!/usr/bin/env node
/**
 * Check component documentation against the ESPHome language schema, or
 * (with --emit) write the documentation into the schema for the editors.
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
 *   node script/check_schema_docs.mjs --schema-dir DIR --emit OUT_DIR
 *                                     [--deploy-url https://esphome.io]
 */

import { existsSync, readFileSync, readdirSync, statSync, writeFileSync } from "node:fs";
import { basename, dirname, join, relative } from "node:path";
import { pathToFileURL } from "node:url";
import { parseArgs } from "node:util";
import Slugger from "github-slugger";
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
  "light.effects": { automation_light: "automation", e1_31: "e131" },
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
    emit: { type: "string" },
    "deploy-url": { type: "string", default: "https://esphome.io" },
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
      const inners = (await Promise.all(ref.split("+").map((r) => this.resolve(r)))).filter(Boolean);
      const variants = inners.flatMap((i) => i.variants);
      return variants.length ? { variants, primaryCount: inners[0].variants.length } : null;
    }
    if (ref.endsWith(".*")) {
      // Every schema of a platform base page (sensor/index.mdx documents
      // SENSOR_SCHEMA and the derived schemas that add filters, triggers, ...)
      const top = ref.slice(0, -2);
      const doc = await this.file(top.split(".")[0]);
      const upper = top.toUpperCase();
      const rank = (topName, schemaName) => {
        if (topName === top && (schemaName === `${upper}_SCHEMA` || schemaName === `_${upper}_SCHEMA`)) return 0;
        if (/_(ACTION|CONDITION)_SCHEMA$/.test(schemaName)) return 3;
        return topName === top ? 1 : 2;
      };
      const variants = Object.entries(doc ?? {})
        .filter(([, body]) => body && typeof body === "object" && body.schemas)
        .flatMap(([topName, body]) =>
          Object.entries(body.schemas).map(([schemaName, entry]) => [rank(topName, schemaName), entry]),
        )
        .filter(([r]) => r < 3)
        .sort((a, b) => a[0] - b[0]);
      const inners = variants.map(([r, entry]) => [r, toInner(entry)]).filter(([, i]) => i);
      const flat = inners.flatMap(([, i]) => i.variants);
      const primaryCount = inners.filter(([r]) => r === 0).reduce((n, [, i]) => n + i.variants.length, 0);
      return flat.length ? { variants: flat, primaryCount: primaryCount || flat.length, baseRef: top } : null;
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

  /** The raw JSON object a plain (non-union) reference points at. */
  async entry(ref) {
    const parts = ref.replace(/\[[^\]]+\]$/, "").split(".");
    if (parts[0] === "core") {
      return REGISTRY_TYPES.has(parts[1])
        ? (this.core?.[parts[1]]?.[parts.slice(2).join(".")] ?? null)
        : (this.core?.schemas?.[parts[1]] ?? null);
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
        if (entry) return entry;
      } else if (rest.length === 1 && top.schemas?.[rest[0]]) {
        return top.schemas[rest[0]];
      }
    }
    return null;
  }

  loadAll() {
    for (const name of readdirSync(this.dir)) {
      if (name.endsWith(".json")) this.file(basename(name, ".json"));
    }
  }

  save(dir) {
    for (const [name, doc] of this.files) {
      if (doc) writeFileSync(join(dir, `${name}.json`), `${JSON.stringify(doc, null, 2)}\n`);
    }
  }

  /** Like findProp but also says which schema object holds the key. */
  async findPropOwner(inner, name, inherited = false, seen = new Set()) {
    if (!inner) return null;
    if (inner.typedKey === name) {
      return { prop: { key: "Required", type: "enum" }, owner: null, inherited, typedEntry: inner.entry };
    }
    for (const variantInner of inner.variants) {
      if (variantInner.config_vars && Object.hasOwn(variantInner.config_vars, name)) {
        return { prop: variantInner.config_vars[name], owner: variantInner, inherited };
      }
      for (const ext of variantInner.extends ?? []) {
        if (seen.has(ext)) continue;
        seen.add(ext);
        const found = await this.findPropOwner(await this.resolve(ext), name, true, seen);
        if (found) return found;
      }
    }
    return null;
  }

  /** Every holder of a key across typed variants (own keys only). */
  propHolders(inner, name) {
    const out = [];
    for (const variantInner of inner?.variants ?? []) {
      if (variantInner.config_vars && Object.hasOwn(variantInner.config_vars, name)) {
        out.push({ prop: variantInner.config_vars[name], owner: variantInner, inherited: false });
      }
    }
    return out;
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

  /** Platform component schemas (loaded files only) that extend a platform base schema. */
  childrenOf(baseTop) {
    const children = [];
    for (const doc of this.files.values()) {
      for (const [top, body] of Object.entries(doc ?? {})) {
        if (!top.endsWith(`.${baseTop}`)) continue;
        const inner = toInner(body?.schemas?.CONFIG_SCHEMA);
        if (inner) children.push(...inner.variants);
      }
    }
    return children;
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
    for (const variantInner of inner.variants.slice(0, inner.primaryCount ?? inner.variants.length)) {
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
    return variants.length ? { variants, typedKey: entry.typed_key ?? "type", entry } : null;
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
  let title = null;
  // Frontmatter is not markdown; blank it but keep offsets and line numbers stable.
  src = src.replace(/^---\n([\s\S]*?)\n---\n/, (fm, body) => {
    const m = body.match(/^title:\s*(.+)$/m);
    if (m) title = m[1].trim().replace(/^(["'])(.*)\1$/, "$2");
    return fm.replace(/[^\n]/g, " ");
  });
  const tree = unified().use(remarkParse).use(remarkMath).use(remarkMdx).parse(src);
  tree.source = src;
  tree.title = title;
  return tree;
}

// ---------------------------------------------------------------------------
// Emitting docs into the schema (what script/schema_doc.py used to do)
// ---------------------------------------------------------------------------

export function slugify(text) {
  return text
    .normalize("NFKD")
    .replace(/[\u0080-\uffff]/g, "")
    .toLowerCase()
    .replace(/[^\w\s-]/g, "")
    .replace(/[-\s]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

/** Site path of a doc page: /components/sensor/bme280 */
export function pageUrl(file) {
  const rel = relative(DOCS_ROOT, file)
    .replace(/\\/g, "/")
    .replace(/\.mdx$/, "");
  return `/${rel.replace(/\/index$/, "")}`;
}

export function convertLinks(text, url, deployUrl) {
  if (text == null) return text;
  return text.replace(/\[([^\]]*)\]\(([^)]*)\)/g, (all, title, href) => {
    if (/^https?:\/\//.test(href)) return all;
    if (href.startsWith("/")) return `[${title}](${deployUrl}${href})`;
    if (href.startsWith("#")) return `[${title}](${deployUrl}${url}${href})`;
    return all;
  });
}

/** Source text of a node with line breaks collapsed, as the Python walker produced it. */
function nodeText(tree, node) {
  return tree.source
    .slice(node.position.start.offset, node.position.end.offset)
    .split("\n")
    .map((l) => l.trim())
    .join(" ")
    .trim();
}

/** Text of a list item: all of its paragraphs, not its nested lists. */
function itemText(tree, item) {
  return item.children
    .filter((c) => c.type === "paragraph")
    .map((c) => nodeText(tree, c))
    .join(" ");
}

const PROP_RE = /^\*\*(\w+)\*\*(?: \((.*?)\))?: (.*)$/;
const ENUM_RE = /^(?:`([^`]*)`|\*\*([^*]*)\*\*)(?:(?: -|:) (.*)| \(([^)]*)\)(?:: (.*))?)?$/;

/** <EnumValues values={[ {value: "X", default: true, description: "Y"}, … ]} /> */
export function parseEnumValues(node) {
  const attr = node.attributes?.find((a) => a.name === "values");
  const raw = attr?.value?.value ?? attr?.value;
  if (typeof raw !== "string") return null;
  const body = raw.replace(/\b(value|description|default)\s*:/g, '"$1":').replace(/,(\s*[\]}])/g, "$1");
  try {
    const entries = JSON.parse(body);
    return Array.isArray(entries) && entries.every((e) => e && typeof e === "object" && "value" in e) ? entries : null;
  } catch {
    return null;
  }
}

function slug(text) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "_")
    .replace(/^_+|_+$/g, "");
}

/** `name` Action -> {name, type} using the inlineCode node, not the text. */
export function registryHeading(node) {
  const codes = node.children.filter((c) => c.type === "inlineCode");
  if (!codes.length) return null;
  const rest = toString({ children: node.children.filter((c) => c.type !== "inlineCode") })
    .replace(/\s*\/\s*/g, " ")
    .trim();
  const m = rest.match(/^(Action|Condition)$/i);
  if (!m) return null;
  return { name: codes[0].value, names: codes.map((c) => c.value), type: m[1].toLowerCase() };
}

/** `time.on_time` Trigger -> on_time */
function triggerHeading(node) {
  const code = node.children.find((c) => c.type === "inlineCode");
  if (!code) return null;
  const rest = toString({ children: node.children.filter((c) => c.type !== "inlineCode") }).trim();
  if (!/^Trigger$/i.test(rest)) return null;
  return code.value.split(".").pop();
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
  const hasParen = rest[0]?.type === "text" && /^\s*\(/.test(rest[0].value);
  if (rest[0]?.type === "text" && /^\s*\(\s*$/.test(rest[0].value)) {
    const marker = rest[1];
    if (marker && (marker.type === "strong" || marker.type === "emphasis")) {
      const word = toString(marker).trim().toLowerCase();
      if (word === "required" || word === "optional") optionality = word;
    }
  }
  return { key, optionality, hasParen, line: para.position.start.line };
}

export class Report {
  constructor() {
    this.findings = [];
    this.sections = [];
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
      emitted: {
        props: 0,
        propsRefined: 0,
        propsSkipped: 0,
        enumDocs: 0,
        actionDocs: 0,
        conditionDocs: 0,
        registryDocs: 0,
        componentDocs: 0,
        platformDocs: 0,
        platformIndexDocs: 0,
        keyChanged: 0,
      },
    };
  }

  add(kind, file, line, detail) {
    this.findings.push({ kind, file, line, ...detail });
  }
}

export class Walker {
  constructor(store, report, file, { emit = false, deployUrl = "https://esphome.io" } = {}) {
    this.store = store;
    this.report = report;
    this.file = file;
    this.emit = emit;
    this.deployUrl = deployUrl;
    this.url = pageUrl(file);
    this.lastHeadingSlug = null;
    this.lastEnumProp = null;
    this.slugger = new Slugger();
    this.tree = null;
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
      const hubRef = await this.componentSchemaRef(this.stem);
      if (hubRef) {
        // sensor/bh1745.mdx documents the bh1745 hub and its sensor platform in one page
        this.defaultRef = this.defaultRef ? `${this.defaultRef}+${hubRef}` : hubRef;
        this.componentRef = this.stem;
      }
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
    this.section = { ref, inner, depth, documented: new Set(), line, continued: false };
    report.sections.push({ file: this.rel, line, ref, source });
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

  // -- emit helpers ---------------------------------------------------------

  links(text) {
    return convertLinks(text, this.url, this.deployUrl);
  }

  withSeeAlso(text) {
    const anchor = this.lastHeadingSlug ? `#${this.lastHeadingSlug}` : "";
    return `${this.links(text)}\n\n*See also: [${this.tree.title}](${this.deployUrl}${this.url}${anchor})*`;
  }

  /** First paragraph after index in the top-level children, or null if a code block comes first. */
  leadParagraph(children, index) {
    for (let i = index; i < children.length; i++) {
      const n = children[i];
      if (["mdxjsEsm", "mdxJsxFlowElement", "mdxFlowExpression", "heading", "html", "blockquote"].includes(n.type)) {
        continue;
      }
      if (n.type === "paragraph") return nodeText(this.tree, n);
      return null;
    }
    return null;
  }

  /** Write the page/section intro for the component or platform entry the docs describe. */
  async emitComponentDocs(name, platform, text) {
    if (!this.emit || !text) return;
    const { store, report } = this;
    if (platform) {
      const doc = await store.file(platform);
      const entry = doc?.[platform]?.components?.[name];
      if (entry) {
        entry.docs = this.withSeeAlso(text);
        report.stats.emitted.platformDocs++;
      }
      return;
    }
    const entry = store.core.components[name];
    if (entry && !("docs" in entry)) {
      entry.docs = this.withSeeAlso(text);
      report.stats.emitted.componentDocs++;
    }
  }

  async emitRegistryDocs(ref, type, text) {
    if (!this.emit || !text) return;
    const entry = await this.store.entry(ref);
    if (!entry) return;
    entry.docs = this.links(text);
    const e = this.report.stats.emitted;
    if (type === "action") e.actionDocs++;
    else if (type === "condition") e.conditionDocs++;
    else e.registryDocs++;
  }

  emitEnumEntries(prop, entries) {
    if (!this.emit || !prop || prop.type !== "enum" || !prop.values) return;
    for (const entry of entries) {
      if (!Object.hasOwn(prop.values, entry.value)) continue;
      prop.values[entry.value] = prop.values[entry.value] || {};
      if (entry.description) prop.values[entry.value].docs = this.links(entry.description);
      if (entry.default) prop.values[entry.value].default = true;
      this.report.stats.emitted.enumDocs++;
    }
  }

  emitEnumList(prop, listNode) {
    if (!this.emit || !prop || prop.type !== "enum" || !prop.values) return;
    for (const item of listNode.children) {
      if (!item.children.some((c) => c.type === "paragraph")) continue;
      const m = ENUM_RE.exec(itemText(this.tree, item));
      if (!m) continue;
      const value = m[1] ?? m[2];
      const desc = m[3] ?? m[5] ?? m[4];
      if (!desc || !Object.hasOwn(prop.values, value)) continue;
      prop.values[value] = prop.values[value] || {};
      prop.values[value].docs = this.links(desc);
      this.report.stats.emitted.enumDocs++;
    }
  }

  /** Attach a config bullet's description to the schema, mirroring schema_doc.py. */
  emitPropDocs(found, sectionInner, item, parsed) {
    if (!this.emit || !found) return;
    const m = PROP_RE.exec(itemText(this.tree, item));
    if (!m) return;
    if (found.typedEntry) {
      found.typedEntry.docs = m[3];
      this.report.stats.emitted.props++;
      return;
    }
    if (sectionInner.typedKey && sectionInner.variants.length > 1) {
      // A typed schema: document the key in every variant that accepts it
      return this.emitPropDocsTyped(sectionInner, item, parsed);
    }
    const { prop, owner, inherited } = found;
    const e = this.report.stats.emitted;
    let converted = this.withSeeAlso(m[3]);
    if (m[2]) {
      const typeParts = m[2].split(",").map((t) => t.trim());
      if (
        parsed.optionality &&
        parsed.key !== "id" &&
        prop.key !== "GeneratedID" &&
        prop.key?.toLowerCase() !== parsed.optionality &&
        !parsed.optionalityAgrees
      ) {
        prop.key = parsed.optionality[0].toUpperCase() + parsed.optionality.slice(1);
        e.keyChanged++;
      }
      if (typeParts.length > 1 && !/\[templatable\]/.test(typeParts[1])) {
        converted = `**${this.links(typeParts[1])}**: ${converted}`;
      }
    }
    if (prop.docs === converted) {
      e.propsSkipped++;
      return;
    }
    if (inherited && "docs" in prop) {
      // The base schema already carries different docs: describe it at this level instead
      const target = sectionInner.variants[0];
      target.config_vars ??= {};
      const refined = (target.config_vars[parsed.key] ??= {});
      if ("key" in prop && !("key" in refined)) refined.key = prop.key;
      refined.docs = converted;
      e.propsRefined++;
      return;
    }
    prop.docs = converted;
    e.props++;
    void owner;
  }

  async emitPropDocsTyped(sectionInner, item, parsed) {
    for (const variant of sectionInner.variants) {
      const single = { variants: [variant] };
      const found = await this.store.findPropOwner(single, parsed.key);
      if (found) this.emitPropDocs(found, single, item, parsed);
    }
  }

  // -- walking --------------------------------------------------------------

  async walk(tree) {
    this.tree = tree;
    this.report.stats.files++;
    if (this.emit) {
      const text = this.leadParagraph(tree.children, 0);
      const platform = this.folder !== "components" && this.store.isPlatform(this.folder) ? this.folder : null;
      if (platform && this.stem === "index") {
        if (text && this.store.core.platforms[platform]) {
          this.store.core.platforms[platform].docs = this.links(text);
          this.report.stats.emitted.platformIndexDocs++;
        }
      } else if (platform) {
        await this.emitComponentDocs(this.stem, platform, text);
        if (this.store.isComponent(this.stem)) await this.emitComponentDocs(this.stem, null, text);
      } else if (this.stem !== "index" || this.folder !== "components") {
        await this.emitComponentDocs(this.stem === "index" ? this.folder : this.stem, null, text);
      }
    }
    for (let i = 0; i < tree.children.length; i++) {
      const node = tree.children[i];
      if (node.type === "heading") await this.heading(node, tree.children, i);
      else if (node.type === "paragraph") await this.paragraph(node);
      else if (node.type === "list") await this.list(node);
      else if (node.type === "mdxFlowExpression") this.expression(node);
      else if (node.type === "mdxJsxFlowElement" && node.name === "EnumValues") {
        const entries = parseEnumValues(node);
        if (entries) this.emitEnumEntries(this.lastEnumProp, entries);
      }
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

  async heading(node, siblings = [], index = 0) {
    const { store } = this;
    const text = toString(node).trim();
    const line = node.position.start.line;
    this.lastHeadingSlug = this.slugger.slug(toString(node).replace(/\./g, "-"));
    this.lastHeadingDepth = node.depth;
    const intro = () => this.leadParagraph(siblings, index + 1);

    if (CONFIG_VARS_RE.test(text)) {
      await this.openConfigSection(node.depth, line);
      return;
    }

    if (this.section) this.section.enumProp = null;
    // Leave `prop` sub-sections that this heading is not nested under
    while (this.section?.parent && node.depth <= this.section.depth) this.section = this.section.parent;
    if (this.pendingRegistry && node.depth <= this.pendingRegistryDepth) this.pendingRegistry = null;
    const lastWord = slug(text).split("_").pop();
    const isBreak =
      /^see also$/i.test(text) ||
      store.isPlatform(lastWord) ||
      ["action", "condition", "component", "components", "hub"].includes(lastWord) ||
      bareCodeHeading(node) !== null ||
      (this.section?.depth >= node.depth && node.depth <= 1);
    if (this.section && isBreak && node.depth <= this.section.depth) await this.closeSection();
    else if (this.section && !CONFIG_VARS_RE.test(text)) this.section.continued = true;

    const trig = triggerHeading(node);
    if (trig && this.defaultRef) {
      const base = await store.resolve(this.defaultRef);
      const prop = await store.findProp(base, trig);
      if (propInner(prop)) {
        await this.openSection(`${this.defaultRef}/${trig}`, node.depth, line, "heading");
        return;
      }
    }

    const reg = registryHeading(node);
    if (reg) {
      const ref = await this.registryRef(reg.name, reg.type);
      for (const extra of reg.names.slice(1)) {
        const extraRef = await this.registryRef(extra, reg.type);
        if (extraRef) await this.emitRegistryDocs(extraRef, reg.type, intro());
      }
      if (ref) {
        await this.emitRegistryDocs(ref, reg.type, intro());
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
      await this.emitRegistryDocs(registryEntry, "registry", intro());
      await this.openSection(registryEntry, node.depth, line, "registry");
      this.pendingRegistry = registryEntry;
      this.pendingRegistryDepth = node.depth;
      return;
    }

    const switched = async (name) => {
      if (!(await this.switchComponent(name))) return false;
      const [comp, platform] = this.componentRef.split(".");
      await this.emitComponentDocs(comp, platform ?? null, intro());
      return true;
    };
    if (/ Component$/.test(text)) {
      const name = slug(text.replace(/ Component$/, "").replace(/\./g, ""));
      if (await switched(name)) return;
    }
    if (text === "Component/Hub" || text === "Hub Component") {
      if (await switched(this.stem)) return;
    }
    if (/Over SPI$/i.test(text) && (await switched(`${this.stem}_spi`))) return;
    if (/Over I²C$/i.test(text) && (await switched(`${this.stem}_i2c`))) return;
    if (this.stem !== "index") {
      let platformName = slug(text);
      const prefix = `${slug(this.componentRef?.split(".")[0] ?? "")}_`;
      if (platformName.startsWith(prefix)) platformName = platformName.slice(prefix.length);
      if (store.isPlatform(platformName)) {
        const ref = await this.componentSchemaRef(this.stem, platformName);
        if (ref) {
          this.defaultRef = ref;
          this.componentRef = `${this.stem}.${platformName}`;
          await this.emitComponentDocs(this.stem, platformName, intro());
          return;
        }
      }
      // "## Clockless" in fastled.mdx -> fastled_clockless
      if (await switched(`${this.stem}_${slug(text)}`)) return;
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
    if (code && /^[a-z0-9_]+$/.test(code) && !(this.section && (await store.findProp(this.section.inner, code)))) {
      if (await this.componentSchemaRef(code, store.isPlatform(this.folder) ? this.folder : null)) {
        await this.closeSection();
        if (await switched(code)) return;
      }
    }

    // "## Legend Options" documents the `legend` sub-schema of the current schema
    const baseRef = this.section?.ref ?? this.defaultRef;
    if (baseRef && !baseRef.includes("/")) {
      const first = slug(text).split("_")[0];
      const base = await store.resolve(baseRef);
      const prop = first && (await store.findProp(base, first));
      if (prop && propInner(prop) && !(await store.findProp(base, slug(text)))) {
        if (this.section && !this.section.parent) {
          // keep the parent open so later headings fall back to it
          this.section.documented.add(first);
          this.section = {
            ...this.section,
            inner: propInner(prop),
            ref: `${this.section.ref}/${first}`,
            depth: node.depth,
            documented: new Set(),
            parent: this.section,
            line,
          };
        } else {
          await this.openSection(`${baseRef}/${first}`, node.depth, line, "heading");
        }
        return;
      }
    }

    // `prop` sub-heading inside an open section: describe a nested schema
    if (code && this.section && node.depth > this.section.depth) {
      const prop = await store.findProp(this.section.inner, code);
      const inner = propInner(prop);
      if (prop?.type === "enum") {
        this.lastEnumProp = prop;
        this.section.enumProp = prop;
        this.section.documented.add(code);
        return;
      }
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
    if (!this.section && this.defaultRef) {
      // "## Base Fan Configuration" / "## A4988 Component" go straight into the
      // option list without a "Configuration variables" heading
      const first = node.children[0] && parseItem(node.children[0]);
      if (first?.hasParen && !first.prose) {
        await this.openSection(this.defaultRef, this.lastHeadingDepth ?? 2, node.position.start.line, "implicit");
      }
    }
    if (!this.section) return;
    if (this.section.enumProp) {
      this.emitEnumList(this.section.enumProp, node);
      return;
    }
    await this.items(node, this.section.inner, this.section.documented);
  }

  async items(listNode, inner, documented) {
    const { store, report } = this;
    for (const item of listNode.children) {
      const parsed = parseItem(item);
      if (!parsed) continue;
      if (parsed.prose || (this.section?.continued && inner === this.section.inner && !parsed.hasParen)) {
        report.stats.proseBullets++;
        continue;
      }
      let found = await store.findPropOwner(inner, parsed.key);
      let prop = found?.prop ?? null;
      if (!prop) {
        const family = store.numberedFamily(inner, parsed.key);
        if (family.length) {
          report.stats.keysMatched++;
          for (const k of family) {
            documented.add(k);
            this.emitPropDocs(await store.findPropOwner(inner, k), inner, item, { ...parsed, key: k });
          }
          continue;
        }
        prop = await store.findNestedProp(inner, parsed.key);
        if (prop) {
          report.stats.keysMatchedNested++;
          this.emitPropDocs({ prop, owner: null, inherited: false }, inner, item, parsed);
          continue;
        }
        if (inner.baseRef && this.emit) {
          // Documented on the platform page, declared only by platform components:
          // describe it on the base schema so every platform shows the hover text
          const child = store.childrenOf(inner.baseRef).find((v) => v.config_vars?.[parsed.key]);
          if (child) {
            const base = inner.variants[0];
            base.config_vars ??= {};
            const created = (base.config_vars[parsed.key] ??= {});
            if ("key" in child.config_vars[parsed.key]) created.key ??= child.config_vars[parsed.key].key;
            report.stats.keysMatched++;
            documented.add(parsed.key);
            this.emitPropDocs({ prop: created, owner: base, inherited: false }, inner, item, parsed);
            continue;
          }
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
        parsed.optionalityAgrees = marked.includes(parsed.optionality);
        if (marked.length && !marked.includes(parsed.optionality)) {
          report.stats.optionalityMismatch++;
          report.add("optionality_mismatch", this.rel, parsed.line, {
            schema: this.section?.ref,
            key: parsed.key,
            detail: `docs say ${parsed.optionality}, schema says ${marked[0]}`,
          });
        }
      }
      await this.emitPropDocs(found, inner, item, parsed);
      if (prop.type === "enum") this.lastEnumProp = prop;
      const nested = item.children.find((c) => c.type === "list");
      if (nested) {
        const nestedInner = propInner(prop);
        if (nestedInner) await this.items(nested, nestedInner, new Set());
        else if (prop.type === "enum") this.emitEnumList(prop, nested);
      }
      for (const jsx of item.children.filter((c) => c.type === "mdxJsxFlowElement" && c.name === "EnumValues")) {
        const entries = parseEnumValues(jsx);
        if (entries) this.emitEnumEntries(prop, entries);
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
  if (args.emit && !args["schema-dir"]) {
    console.error("--emit needs --schema-dir");
    return 2;
  }
  const store = new SchemaStore({ dir: args["schema-dir"], url: args["schema-url"] });
  await store.init();
  if (args.emit) store.loadAll();
  if (args.resolve) {
    const inner = await store.resolve(args.resolve);
    console.log(inner ? JSON.stringify([...store.ownKeys(inner)]) : "not found");
    return inner ? 0 : 1;
  }
  const report = new Report();

  let files = listMdx(COMPONENTS_ROOT);
  files.push(join(DOCS_ROOT, "automations", "actions.mdx"));
  if (args.file) files = files.filter((f) => f.includes(args.file));

  // Platform index pages first so base-schema docs are in place before the
  // platform components refine them (same order as schema_doc.py).
  const fileOrder = (f) => {
    if (basename(f) === "index.mdx") return 0;
    return dirname(f) === COMPONENTS_ROOT ? 1 : 2;
  };
  files.sort((a, b) => fileOrder(a) - fileOrder(b) || a.localeCompare(b));
  for (const file of files) {
    let tree;
    try {
      tree = parseMdx(file);
    } catch (err) {
      report.add("parse_error", relative(COMPONENTS_ROOT, file), err.line ?? 0, { detail: err.message });
      continue;
    }
    const walker = new Walker(store, report, file, { emit: Boolean(args.emit), deployUrl: args["deploy-url"] });
    await walker.init();
    await walker.walk(tree);
  }

  if (args.emit) {
    store.save(args.emit);
    console.log(JSON.stringify(report.stats.emitted, null, 2));
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
    writeFileSync(
      args.json,
      JSON.stringify({ stats: report.stats, sections: report.sections, findings: report.findings }, null, 2),
    );
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
