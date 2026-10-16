import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";

import { parseMdx, Report, SchemaStore, Walker } from "../script/schema_doc.mjs";

/** A tiny schema bundle and docs tree on disk; returns what a walk emitted. */
async function walk({ schema, pages }) {
  const root = mkdtempSync(join(tmpdir(), "schema-doc-"));
  const schemaDir = join(root, "schema");
  const docsRoot = join(root, "docs");
  const componentsRoot = join(docsRoot, "components");
  mkdirSync(schemaDir);
  for (const [name, doc] of Object.entries(schema)) {
    writeFileSync(join(schemaDir, `${name}.json`), JSON.stringify(doc));
  }
  for (const [rel, body] of Object.entries(pages)) {
    const path = join(componentsRoot, rel);
    mkdirSync(join(path, ".."), { recursive: true });
    writeFileSync(path, `---\ntitle: Test Page\n---\n\n${body}`);
  }
  const store = new SchemaStore({ dir: schemaDir });
  await store.init();
  await store.loadAll();
  const report = new Report();
  for (const rel of Object.keys(pages)) {
    const walker = new Walker(store, report, join(componentsRoot, rel), { emit: true, docsRoot, componentsRoot });
    await walker.init();
    await walker.walk(parseMdx(join(componentsRoot, rel)));
  }
  return { store, report, docs: (file, ...path) => path.reduce((o, k) => o?.[k], store.files.get(file))?.docs };
}

const core = (components, platforms = {}) => ({
  core: {
    components: Object.fromEntries(components.map((c) => [c, {}])),
    platforms,
    action: {},
    condition: {},
    schemas: {},
  },
});
const schema = (config_vars, extra = {}) => ({ type: "schema", schema: { config_vars }, ...extra });

test("a bus heading re-targets only its own subtree", async () => {
  const { docs, report } = await walk({
    schema: {
      esphome: core(["bmp581_i2c", "bmp581_spi"], { sensor: {} }),
      sensor: { sensor: { schemas: {}, components: { bmp581_i2c: {}, bmp581_spi: {} } } },
      bmp581_i2c: { "bmp581_i2c.sensor": { schemas: { CONFIG_SCHEMA: schema({ address: { key: "Optional" } }) } } },
      bmp581_spi: { "bmp581_spi.sensor": { schemas: { CONFIG_SCHEMA: schema({ cs_pin: { key: "Required" } }) } } },
    },
    pages: {
      "sensor/bmp581.mdx": [
        "The BMP581 sensor.",
        "## Over SPI",
        "- **cs_pin** (**Required**, pin): Chip select.",
        "## Configuration variables",
        "- **address** (*Optional*, int): The I²C address.",
        "",
      ].join("\n\n"),
    },
  });
  assert.match(
    docs("bmp581_spi", "bmp581_spi.sensor", "schemas", "CONFIG_SCHEMA", "schema", "config_vars", "cs_pin"),
    /Chip select/,
  );
  assert.match(
    docs("bmp581_i2c", "bmp581_i2c.sensor", "schemas", "CONFIG_SCHEMA", "schema", "config_vars", "address"),
    /I²C address/,
  );
  assert.deepEqual(
    report.findings.filter((f) => f.kind === "unmatched_key"),
    [],
  );
});

test("a heading naming two actions documents the options of both", async () => {
  const { docs } = await walk({
    schema: {
      esphome: core(["lvgl"]),
      lvgl: {
        lvgl: {
          schemas: { CONFIG_SCHEMA: schema({}) },
          action: {
            "page.next": schema({ animation: { key: "Optional" } }),
            "page.previous": schema({ animation: { key: "Optional" } }),
          },
        },
      },
    },
    pages: {
      "lvgl/index.mdx": [
        "LVGL.",
        "## `lvgl.page.next` / `lvgl.page.previous` Action",
        "Flip pages.",
        "- **animation** (*Optional*, string): The animation.",
        "",
      ].join("\n\n"),
    },
  });
  for (const name of ["page.next", "page.previous"]) {
    assert.match(docs("lvgl", "lvgl", "action", name, "schema", "config_vars", "animation"), /The animation/);
    assert.equal(docs("lvgl", "lvgl", "action", name), "Flip pages.");
  }
});

test("nested options left out of the docs are reported", async () => {
  const { report } = await walk({
    schema: {
      esphome: core(["graph"]),
      graph: {
        graph: {
          schemas: {
            CONFIG_SCHEMA: schema({
              legend: { key: "Optional", ...schema({ name_font: { key: "Required" }, border: { key: "Optional" } }) },
            }),
          },
        },
      },
    },
    pages: {
      "graph.mdx": [
        "A graph.",
        "## Configuration variables",
        "- **legend** (*Optional*, mapping): Legend options.\n  - **border** (*Optional*, boolean): Draw a border.",
        "",
      ].join("\n\n"),
    },
  });
  const missing = report.findings.filter((f) => f.kind === "undocumented_key").map((f) => `${f.schema}:${f.key}`);
  assert.deepEqual(missing, ["graph.CONFIG_SCHEMA/legend:name_font"]);
});

test("an unused schema marker is reported", async () => {
  const { report } = await walk({
    schema: {
      esphome: core(["foo"]),
      foo: { foo: { schemas: { CONFIG_SCHEMA: schema({ bar: { key: "Optional" } }) } } },
    },
    pages: {
      "foo.mdx": ["Foo.", "{/* schema: foo.CONFIG_SCHEMA */}", "## Notes", "Nothing here.", "## See Also", ""].join(
        "\n\n",
      ),
    },
  });
  assert.equal(report.findings.filter((f) => f.kind === "unused_schema_marker").length, 1);
});

test("a key both bus variants declare is documented in both", async () => {
  const { docs } = await walk({
    schema: {
      esphome: core(["foo_i2c", "foo_spi"], { sensor: {} }),
      sensor: { sensor: { schemas: {}, components: { foo_i2c: {}, foo_spi: {} } } },
      foo_i2c: { "foo_i2c.sensor": { schemas: { CONFIG_SCHEMA: schema({ temperature: { key: "Optional" } }) } } },
      foo_spi: { "foo_spi.sensor": { schemas: { CONFIG_SCHEMA: schema({ temperature: { key: "Optional" } }) } } },
    },
    pages: {
      "sensor/foo.mdx": [
        "Foo.",
        "## Configuration variables",
        "- **temperature** (*Optional*): The temperature sensor.",
        "",
      ].join("\n\n"),
    },
  });
  for (const bus of ["foo_i2c", "foo_spi"]) {
    assert.match(
      docs(bus, `${bus}.sensor`, "schemas", "CONFIG_SCHEMA", "schema", "config_vars", "temperature"),
      /temperature sensor/,
    );
  }
});

test("text after a colon-before-type annotation is kept as the description", async () => {
  const { docs } = await walk({
    schema: {
      esphome: core(["foo"]),
      foo: { foo: { schemas: { CONFIG_SCHEMA: schema({ restore_value: { key: "Optional" } }) } } },
    },
    pages: {
      "foo.mdx": [
        "Foo.",
        "## Configuration variables",
        "- **restore_value**: (*Optional*, bool) Restore the value on boot.",
        "",
      ].join("\n\n"),
    },
  });
  assert.match(
    docs("foo", "foo", "schemas", "CONFIG_SCHEMA", "schema", "config_vars", "restore_value"),
    /^\*\*bool\*\*: Restore the value on boot/,
  );
});
