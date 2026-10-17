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

test("a type annotation holding a link keeps the link and the whole description", async () => {
  const { docs } = await walk({
    schema: {
      esphome: core(["foo"]),
      foo: {
        foo: {
          schemas: {
            CONFIG_SCHEMA: schema({
              preset_change: { key: "Optional" },
              restore_from: { key: "Optional" },
              plain: { key: "Optional" },
            }),
          },
        },
      },
    },
    pages: {
      "foo.mdx": [
        "Foo.",
        "## Configuration variables",
        [
          "- **preset_change**: (*Optional*, [Action](/automations/actions/#all-actions)) Runs when the preset changes.",
          "- **restore_from**: (*Optional*, enum): Where to restore from.",
          "- **plain** (*Optional*, [Time](/guides/configuration-types/#time)): The interval.",
        ].join("\n"),
        "",
      ].join("\n\n"),
    },
  });
  const field = (k) => docs("foo", "foo", "schemas", "CONFIG_SCHEMA", "schema", "config_vars", k);
  assert.match(
    field("preset_change"),
    /^\*\*\[Action\]\(https:\/\/esphome\.io\/automations\/actions\/#all-actions\)\*\*: Runs when the preset changes\./,
  );
  assert.match(field("restore_from"), /^\*\*enum\*\*: Where to restore from\./);
  assert.match(
    field("plain"),
    /^\*\*\[Time\]\(https:\/\/esphome\.io\/guides\/configuration-types\/#time\)\*\*: The interval\./,
  );
});

test("a platform heading nested under the hub's options starts that platform's section", async () => {
  const { docs } = await walk({
    schema: {
      esphome: core(["mits"], { select: {} }),
      select: { select: { schemas: {}, components: { mits: {} } } },
      mits: {
        mits: { schemas: { CONFIG_SCHEMA: schema({ uart_id: { key: "Optional" } }) } },
        "mits.select": { schemas: { CONFIG_SCHEMA: schema({ vane: { key: "Optional" } }) } },
      },
    },
    pages: {
      "mits.mdx": [
        "Mits.",
        "## Configuration variables",
        "- **uart_id** (*Optional*, ID): The UART.",
        "### Select",
        "- **vane** (*Optional*, string): The vane select.",
        "",
      ].join("\n\n"),
    },
  });
  assert.match(docs("mits", "mits", "schemas", "CONFIG_SCHEMA", "schema", "config_vars", "uart_id"), /The UART/);
  assert.match(docs("mits", "mits.select", "schemas", "CONFIG_SCHEMA", "schema", "config_vars", "vane"), /vane select/);
});

test("a bare code heading on a top-level page does not switch to another component", async () => {
  const { docs, report } = await walk({
    schema: {
      esphome: core(["i2c", "host"]),
      i2c: { i2c: { schemas: { CONFIG_SCHEMA: schema({ device: { key: "Optional" } }) } } },
      host: { host: { schemas: { CONFIG_SCHEMA: schema({ board: { key: "Optional" } }) } } },
    },
    pages: {
      "i2c.mdx": [
        "I2C.",
        "## Configuration variables",
        "### `host`",
        "- **device** (*Optional*, string): The device path.",
        "",
      ].join("\n\n"),
    },
  });
  assert.match(docs("i2c", "i2c", "schemas", "CONFIG_SCHEMA", "schema", "config_vars", "device"), /device path/);
  assert.deepEqual(
    report.findings.filter((f) => f.kind === "unmatched_key"),
    [],
  );
});

test("options after a sub-schema heading fall back to the parent schema", async () => {
  const { docs, report } = await walk({
    schema: {
      esphome: core(["radar"]),
      radar: {
        radar: {
          schemas: {
            CONFIG_SCHEMA: schema({
              sensitivity: { key: "Optional", ...schema({ level: { key: "Optional" } }) },
              custom_mode: { key: "Optional" },
            }),
          },
        },
      },
    },
    pages: {
      "radar.mdx": [
        "Radar.",
        "## Configuration variables",
        "### Sensitivity",
        "- **level** (*Optional*, int): Sensitivity level.",
        "- **custom_mode** (*Optional*, int): Custom mode.",
        "",
      ].join("\n\n"),
    },
  });
  const cv = (...k) => docs("radar", "radar", "schemas", "CONFIG_SCHEMA", "schema", "config_vars", ...k);
  assert.match(cv("sensitivity", "schema", "config_vars", "level"), /Sensitivity level/);
  assert.match(cv("custom_mode"), /Custom mode/);
  assert.deepEqual(
    report.findings.filter((f) => f.kind === "unmatched_key"),
    [],
  );
});

test("enum bullets with a (Default) note before a hyphen keep their description", async () => {
  const { store } = await walk({
    schema: {
      esphome: core(["foo"]),
      foo: {
        foo: {
          schemas: {
            CONFIG_SCHEMA: schema({
              restore_mode: { key: "Optional", type: "enum", values: { RESTORE_DEFAULT_OFF: null, ALWAYS_ON: null } },
            }),
          },
        },
      },
    },
    pages: {
      "foo.mdx": [
        "Foo.",
        "## Configuration variables",
        "- **restore_mode** (*Optional*): Control how the switch attempts to restore state.\n  - `RESTORE_DEFAULT_OFF` (Default) - Attempt to restore state and default to OFF.\n  - `ALWAYS_ON`: Always initialize as ON.",
        "",
      ].join("\n\n"),
    },
  });
  const values = store.files.get("foo").foo.schemas.CONFIG_SCHEMA.schema.config_vars.restore_mode.values;
  assert.match(values.RESTORE_DEFAULT_OFF.docs, /^Attempt to restore state/);
  assert.equal(values.RESTORE_DEFAULT_OFF.default, true);
  assert.match(values.ALWAYS_ON.docs, /^Always initialize/);
  assert.equal(values.ALWAYS_ON.default, undefined);
});

test("an enum bullet that is only `VALUE` (Default) marks the default and writes no text", async () => {
  const { store } = await walk({
    schema: {
      esphome: core(["foo"]),
      foo: {
        foo: {
          schemas: { CONFIG_SCHEMA: schema({ mode: { key: "Optional", type: "enum", values: { A: null, B: null } } }) },
        },
      },
    },
    pages: {
      "foo.mdx": [
        "Foo.",
        "## Configuration variables",
        "- **mode** (*Optional*): The mode.\n  - `A` (Default)\n  - `B`: Mode B.",
        "",
      ].join("\n\n"),
    },
  });
  const values = store.files.get("foo").foo.schemas.CONFIG_SCHEMA.schema.config_vars.mode.values;
  assert.deepEqual(values.A, { default: true });
  assert.match(values.B.docs, /^Mode B/);
});

test("a sibling heading ends a heading-opened sub-schema section", async () => {
  const { docs } = await walk({
    schema: {
      esphome: core(["foo"]),
      foo: {
        foo: {
          schemas: {
            CONFIG_SCHEMA: schema({
              project: { key: "Optional", ...schema({ name: { key: "Required" } }) },
              area: { key: "Optional", ...schema({ name: { key: "Required" } }) },
            }),
          },
        },
      },
    },
    pages: {
      "foo.mdx": [
        "Foo.",
        "## Project information",
        "- **name** (**Required**, string): The project name.",
        "## Area Configuration",
        "- **name** (**Required**, string): Display name for the area.",
        "",
      ].join("\n\n"),
    },
  });
  const cv = (...k) => docs("foo", "foo", "schemas", "CONFIG_SCHEMA", "schema", "config_vars", ...k);
  assert.match(cv("project", "schema", "config_vars", "name"), /project name/);
  assert.match(cv("area", "schema", "config_vars", "name"), /Display name for the area/);
});

test("a `variant` Platform heading documents that typed variant of the page's platform", async () => {
  const { docs, report } = await walk({
    schema: {
      esphome: core(["vbus"], { sensor: {} }),
      sensor: { sensor: { schemas: {}, components: { vbus: {} } } },
      vbus: {
        vbus: { schemas: { CONFIG_SCHEMA: schema({ uart_id: { key: "Optional" } }) } },
        "vbus.sensor": {
          schemas: {
            CONFIG_SCHEMA: {
              type: "typed",
              typed_key: "model",
              types: {
                deltasol_c: { config_vars: { temperature_1: { key: "Optional" } } },
                custom: { config_vars: { sensors: { key: "Optional" } } },
              },
            },
          },
        },
      },
    },
    pages: {
      "vbus.mdx": [
        "VBus.",
        "## Sensor",
        "### Configuration variables",
        "- **model** (**Required**): The controller model.",
        "- **temperature_1** (*Optional*): Temperature sensor 1.",
        "## `custom` VBus sensors",
        "### Configuration variables",
        "- **sensors** (*Optional*): A list of sensor definitions with a lambda.",
        "",
      ].join("\n\n"),
    },
  });
  const types = (...k) => docs("vbus", "vbus.sensor", "schemas", "CONFIG_SCHEMA", "types", ...k);
  assert.match(types("deltasol_c", "config_vars", "temperature_1"), /Temperature sensor 1/);
  assert.match(types("custom", "config_vars", "sensors"), /sensor definitions/);
  assert.deepEqual(
    report.findings.filter((f) => f.kind === "unmatched_key" || (f.kind === "undocumented_key" && f.key === "model")),
    [],
  );
});

test("a typed platform joined with its hub keeps the discriminator and variant group", async () => {
  const { docs, report } = await walk({
    schema: {
      esphome: core(["ble"], { sensor: {} }),
      sensor: { sensor: { schemas: {}, components: { ble: {} } } },
      ble: {
        ble: {
          schemas: {
            CONFIG_SCHEMA: schema({ mac_address: { key: "Required" }, update_interval: { key: "Optional" } }),
          },
        },
        "ble.sensor": {
          schemas: {
            CONFIG_SCHEMA: {
              type: "typed",
              typed_key: "type",
              types: {
                rssi: { config_vars: { update_interval: { key: "Optional" } } },
                characteristic: { config_vars: { update_interval: { key: "Optional" }, notify: { key: "Optional" } } },
              },
            },
          },
        },
      },
    },
    pages: {
      "sensor/ble.mdx": [
        "BLE sensor.",
        "## Configuration variables",
        "- **type** (**Required**): One of `rssi`, `characteristic`.",
        "- **update_interval** (*Optional*): The interval to poll the device.",
        "- **notify** (*Optional*, boolean): Ask for notifications.",
        "- **mac_address** (**Required**): The hub's address.",
        "",
      ].join("\n\n"),
    },
  });
  const types = (...k) => docs("ble", "ble.sensor", "schemas", "CONFIG_SCHEMA", "types", ...k);
  const hub = (...k) => docs("ble", "ble", "schemas", "CONFIG_SCHEMA", "schema", "config_vars", ...k);
  assert.match(docs("ble", "ble.sensor", "schemas", "CONFIG_SCHEMA"), /^One of/);
  assert.match(types("rssi", "config_vars", "update_interval"), /interval to poll/);
  assert.match(types("characteristic", "config_vars", "update_interval"), /interval to poll/);
  assert.match(types("characteristic", "config_vars", "notify"), /notifications/);
  assert.equal(hub("update_interval"), undefined);
  assert.match(hub("mac_address"), /hub's address/);
  assert.deepEqual(
    report.findings.filter((f) => f.kind === "unmatched_key"),
    [],
  );
});

test("nested bullets under a key created from platform children are written to every child", async () => {
  const { docs, store } = await walk({
    schema: {
      esphome: core(["foo", "bar"], { sensor: {} }),
      sensor: {
        sensor: {
          schemas: { SENSOR_SCHEMA: schema({ name: { key: "Optional" } }) },
          components: { foo: {}, bar: {} },
        },
      },
      foo: {
        "foo.sensor": {
          schemas: {
            CONFIG_SCHEMA: schema({
              mode: { key: "Optional", type: "enum", values: { FAST: null, SLOW: null } },
            }),
          },
        },
      },
      bar: {
        "bar.sensor": {
          schemas: {
            CONFIG_SCHEMA: schema({
              mode: { key: "Optional", type: "enum", values: { FAST: null, SLOW: null } },
            }),
          },
        },
      },
    },
    pages: {
      "sensor/index.mdx": [
        "Sensors.",
        "## Base Sensor Configuration",
        "- **name** (*Optional*, string): The name.",
        "- **mode** (*Optional*, string): The sampling mode.\n  - `FAST`: Sample quickly.\n  - `SLOW`: Sample slowly.",
        "",
      ].join("\n\n"),
    },
  });
  assert.match(docs("sensor", "sensor", "schemas", "SENSOR_SCHEMA", "schema", "config_vars", "mode"), /sampling mode/);
  for (const comp of ["foo", "bar"]) {
    const values = store.files.get(comp)[`${comp}.sensor`].schemas.CONFIG_SCHEMA.schema.config_vars.mode.values;
    assert.match(values.FAST.docs, /^Sample quickly/);
    assert.match(values.SLOW.docs, /^Sample slowly/);
  }
});

test("an orphan list is reported even when its first bullet is prose", async () => {
  const { report } = await walk({
    schema: {
      esphome: core(["foo"]),
      foo: { foo: { schemas: { CONFIG_SCHEMA: schema({ name: { key: "Optional" } }) } } },
    },
    pages: {
      "foo.mdx": [
        "Foo.",
        "## Advanced",
        "{/* schema: foo.MISSING */}",
        "### Configuration variables",
        "- **Note**: read this first.\n- **name** (*Optional*, string): The name.\n- **pin** (*Optional*, pin): The pin.",
        "",
      ].join("\n\n"),
    },
  });
  assert.deepEqual(
    report.findings.map((f) => [f.kind, f.line, f.key, f.detail]),
    [
      ["unroutable_section", 11, undefined, "schema 'foo.MISSING' not found"],
      ["orphan_option_list", 13, "name", "2 option bullet(s) outside any schema section"],
    ],
  );
});

test("nested bullets under an inherited key refined on typed variants reach the base definition", async () => {
  const { docs, store, report } = await walk({
    schema: {
      esphome: core(["foo"]),
      foo: {
        foo: {
          schemas: {
            BASE_SCHEMA: schema({
              mode: { key: "Optional", type: "enum", values: { FAST: null, SLOW: null }, docs: "Base text." },
              filter: {
                key: "Optional",
                type: "schema",
                schema: { config_vars: { threshold: { key: "Optional" } } },
                docs: "Base filter.",
              },
            }),
            CONFIG_SCHEMA: {
              type: "typed",
              typed_key: "model",
              types: {
                a: { config_vars: { pin_a: { key: "Required" } }, extends: ["foo.BASE_SCHEMA"] },
                b: { config_vars: { pin_b: { key: "Required" } }, extends: ["foo.BASE_SCHEMA"] },
              },
            },
          },
        },
      },
    },
    pages: {
      "foo.mdx": [
        "Foo.",
        "## Configuration variables",
        "- **model** (**Required**): The model.",
        "- **mode** (*Optional*): The mode.\n  - `FAST`: Sample quickly.\n  - `SLOW`: Sample slowly.",
        "- **filter** (*Optional*): The filter.\n  - **threshold** (*Optional*, int): The threshold.",
        "",
      ].join("\n\n"),
    },
  });
  const types = (...k) => docs("foo", "foo", "schemas", "CONFIG_SCHEMA", "types", ...k);
  assert.match(types("a", "config_vars", "mode"), /^The mode/);
  assert.match(types("b", "config_vars", "mode"), /^The mode/);
  const base = store.files.get("foo").foo.schemas.BASE_SCHEMA.schema.config_vars;
  assert.equal(base.mode.docs, "Base text.");
  assert.match(base.mode.values.FAST.docs, /^Sample quickly/);
  assert.match(base.mode.values.SLOW.docs, /^Sample slowly/);
  assert.match(base.filter.schema.config_vars.threshold.docs, /The threshold/);
  assert.deepEqual(
    report.findings.filter((f) =>
      ["nested_list_ignored", "enum_values_without_enum", "unmatched_key"].includes(f.kind),
    ),
    [],
  );
});

test("nested enum values of a key one typed variant owns and another inherits reach both definitions", async () => {
  const { store, report } = await walk({
    schema: {
      esphome: core(["foo"]),
      foo: {
        foo: {
          schemas: {
            BASE_SCHEMA: schema({ mode: { key: "Optional", type: "enum", values: { FAST: null, SLOW: null } } }),
            CONFIG_SCHEMA: {
              type: "typed",
              typed_key: "model",
              types: {
                a: { config_vars: { mode: { key: "Optional", type: "enum", values: { FAST: null, SLOW: null } } } },
                b: { config_vars: { pin: { key: "Required" } }, extends: ["foo.BASE_SCHEMA"] },
              },
            },
          },
        },
      },
    },
    pages: {
      "foo.mdx": [
        "Foo.",
        "## Configuration variables",
        "- **model** (**Required**): The model.",
        "- **mode** (*Optional*): The mode.\n  - `FAST`: Sample quickly.\n  - `SLOW`: Sample slowly.",
        "",
      ].join("\n\n"),
    },
  });
  const own = store.files.get("foo").foo.schemas.CONFIG_SCHEMA.types.a.config_vars.mode;
  const base = store.files.get("foo").foo.schemas.BASE_SCHEMA.schema.config_vars.mode;
  for (const prop of [own, base]) {
    assert.match(prop.docs, /^The mode/);
    assert.match(prop.values.FAST.docs, /^Sample quickly/);
    assert.match(prop.values.SLOW.docs, /^Sample slowly/);
  }
  assert.deepEqual(
    report.findings.filter((f) => ["nested_list_ignored", "unmatched_key"].includes(f.kind)),
    [],
  );
});

test("bullets after a section that could not be routed are dropped and reported, not sent to the page schema", async () => {
  const { docs, report } = await walk({
    schema: {
      esphome: core(["foo"]),
      foo: { foo: { schemas: { CONFIG_SCHEMA: schema({ name: { key: "Optional" } }) } } },
    },
    pages: {
      "foo.mdx": [
        "Foo.",
        "## Configuration variables",
        "- **name** (*Optional*, string): The name.",
        "## Advanced",
        "{/* schema: foo.MISSING */}",
        "### Configuration variables",
        "- **name** (*Optional*, string): Text for another schema.",
        "#### Details",
        "- **name** (*Optional*, string): Text for another schema.",
        "",
      ].join("\n\n"),
    },
  });
  assert.match(docs("foo", "foo", "schemas", "CONFIG_SCHEMA", "schema", "config_vars", "name"), /: The name\./);
  assert.deepEqual(
    report.findings.map((f) => [f.kind, f.line]),
    [
      ["unroutable_section", 15],
      ["orphan_option_list", 17],
      ["orphan_option_list", 21],
    ],
  );
});

test("options of an action the schema does not have are dropped, not written to the component", async () => {
  const { docs, report } = await walk({
    schema: {
      esphome: core(["foo"]),
      foo: { foo: { schemas: { CONFIG_SCHEMA: schema({ name: { key: "Optional" } }) } }, action: {} },
    },
    pages: {
      "foo.mdx": [
        "Foo.",
        "## Configuration variables",
        "- **name** (*Optional*, string): The name.",
        "## `foo.missing` Action",
        "- **name** (*Optional*, string): Text for the action.",
        "### Configuration variables",
        "- **name** (*Optional*, string): Text for the action.",
        "## `foo.other` Action",
        "- **name** (*Optional*, string): Text for the other action.",
        "",
      ].join("\n\n"),
    },
  });
  assert.match(docs("foo", "foo", "schemas", "CONFIG_SCHEMA", "schema", "config_vars", "name"), /: The name\./);
  assert.deepEqual(
    report.findings.map((f) => [f.kind, f.line]),
    [
      ["unknown_registry_entry", 11],
      ["orphan_option_list", 13],
      ["unroutable_section", 15],
      ["orphan_option_list", 17],
      ["unknown_registry_entry", 19],
      ["orphan_option_list", 21],
    ],
  );
});

test("options under an effect or filter heading the schema lacks are dropped, not written to the platform", async () => {
  const { docs, report, store } = await walk({
    schema: {
      esphome: core([], { light: {} }),
      light: {
        light: {
          schemas: { LIGHT_SCHEMA: schema({ name: { key: "Optional" } }) },
          effects: { strobe: { schema: { config_vars: { name: { key: "Optional" } } } } },
        },
      },
    },
    pages: {
      "light/index.mdx": [
        "Lights.",
        "## Base Light Configuration",
        "- **name** (*Optional*, string): The light name.",
        "## Strobe Effect",
        "A strobe.",
        "- **name** (*Optional*, string): The effect name.",
        "## Missing Effect",
        "Not in the schema.",
        "- **name** (*Optional*, string): Text for the missing effect.",
        "### Configuration variables",
        "- **name** (*Optional*, string): Text for the missing effect.",
        "## Other Effect",
        "Also not in the schema.",
        "",
      ].join("\n\n"),
    },
  });
  assert.match(docs("light", "light", "schemas", "LIGHT_SCHEMA", "schema", "config_vars", "name"), /The light name/);
  assert.match(store.files.get("light").light.effects.strobe.schema.config_vars.name.docs, /The effect name/);
  assert.deepEqual(
    report.findings.map((f) => [f.kind, f.line]),
    [
      ["unknown_registry_entry", 17],
      ["orphan_option_list", 21],
      ["unroutable_section", 23],
      ["orphan_option_list", 25],
      ["unknown_registry_entry", 27],
    ],
  );
});

test("a nested typed schema that two outer variants define keeps its discriminator", async () => {
  const options = () => ({
    key: "Optional",
    type: "typed",
    typed_key: "kind",
    types: { fast: { config_vars: { speed: { key: "Optional" } } }, slow: { config_vars: {} } },
  });
  const { docs, report } = await walk({
    schema: {
      esphome: core(["foo"]),
      foo: {
        foo: {
          schemas: {
            CONFIG_SCHEMA: {
              type: "typed",
              typed_key: "model",
              types: { a: { config_vars: { options: options() } }, b: { config_vars: { options: options() } } },
            },
          },
        },
      },
    },
    pages: {
      "foo.mdx": [
        "Foo.",
        "## Configuration variables",
        "- **model** (**Required**): The model.",
        "- **options** (*Optional*): The options.",
        "## `options` Trigger",
        "- **kind** (**Required**): The kind.",
        "- **speed** (*Optional*, int): The speed.",
        "",
      ].join("\n\n"),
    },
  });
  const types = (...k) => docs("foo", "foo", "schemas", "CONFIG_SCHEMA", "types", ...k);
  for (const model of ["a", "b"]) {
    assert.match(types(model, "config_vars", "options"), /^The kind/);
    assert.match(types(model, "config_vars", "options", "types", "fast", "config_vars", "speed"), /The speed/);
  }
  assert.deepEqual(
    report.findings.filter((f) => f.kind === "unmatched_key").map((f) => f.key),
    [],
  );
});

test("a nested key only one typed variant has is matched, not reported unmatched on the others", async () => {
  const options = (extra = {}) => ({
    key: "Optional",
    type: "schema",
    schema: { config_vars: { x: { key: "Optional" }, ...extra } },
  });
  const { docs, report } = await walk({
    schema: {
      esphome: core(["foo"]),
      foo: {
        foo: {
          schemas: {
            CONFIG_SCHEMA: {
              type: "typed",
              typed_key: "model",
              types: {
                a: { config_vars: { options: options() } },
                b: { config_vars: { options: options({ extra: { key: "Optional" } }) } },
              },
            },
          },
        },
      },
    },
    pages: {
      "foo.mdx": [
        "Foo.",
        "## Configuration variables",
        "- **model** (**Required**): The model.",
        "- **options** (*Optional*): The options.\n  - **x** (*Optional*, int): The x.\n  - **extra** (*Optional*, int): The extra.",
        "",
      ].join("\n\n"),
    },
  });
  const types = (...k) => docs("foo", "foo", "schemas", "CONFIG_SCHEMA", "types", ...k);
  assert.match(types("a", "config_vars", "options", "schema", "config_vars", "x"), /The x/);
  assert.match(types("b", "config_vars", "options", "schema", "config_vars", "x"), /The x/);
  assert.match(types("b", "config_vars", "options", "schema", "config_vars", "extra"), /The extra/);
  assert.deepEqual(
    report.findings.filter((f) => f.kind === "unmatched_key"),
    [],
  );
});

test("a top-level <EnumValues> block reaches every typed variant that has the option before it", async () => {
  const typed = (extra = {}) => ({
    config_vars: { mode: { key: "Optional", type: "enum", values: { FAST: null, SLOW: null } }, ...extra },
  });
  const { store } = await walk({
    schema: {
      esphome: core(["foo"]),
      foo: {
        foo: {
          schemas: {
            CONFIG_SCHEMA: {
              type: "typed",
              typed_key: "model",
              types: { a: typed(), b: typed({ pin: { key: "Required" } }) },
            },
          },
        },
      },
    },
    pages: {
      "foo.mdx": [
        "Foo.",
        "## Configuration variables",
        "- **model** (**Required**): The model.",
        "- **mode** (*Optional*): The mode.",
        '<EnumValues values={[{ value: "FAST", default: true, description: "Sample quickly" }, { value: "SLOW", description: "Sample slowly" }]} />',
        "",
      ].join("\n\n"),
    },
  });
  for (const variant of ["a", "b"]) {
    const values = store.files.get("foo").foo.schemas.CONFIG_SCHEMA.types[variant].config_vars.mode.values;
    assert.deepEqual(values.FAST, { default: true, docs: "Sample quickly" });
    assert.equal(values.SLOW.docs, "Sample slowly");
  }
});

test("a variant's own Required key is not excused by an inherited Optional one", async () => {
  const { report } = await walk({
    schema: {
      esphome: core(["foo"]),
      foo: {
        foo: {
          schemas: {
            BASE_SCHEMA: schema({ mode: { key: "Optional" } }),
            CONFIG_SCHEMA: {
              type: "schema",
              schema: { config_vars: { mode: { key: "Required" } }, extends: ["foo.BASE_SCHEMA"] },
            },
          },
        },
      },
    },
    pages: {
      "foo.mdx": ["Foo.", "## Configuration variables", "- **mode** (*Optional*, string): The mode.", ""].join("\n\n"),
    },
  });
  assert.deepEqual(
    report.findings.map((f) => [f.kind, f.key, f.detail]),
    [["optionality_mismatch", "mode", "docs say optional, schema says required"]],
  );
});

test("a Hub Component heading is the page's own hub, not an unresolved component", async () => {
  const { docs, report } = await walk({
    schema: {
      esphome: core(["foo"], { sensor: {} }),
      sensor: { sensor: { schemas: {}, components: { foo: {} } } },
      foo: {
        foo: { schemas: { CONFIG_SCHEMA: schema({ uart_id: { key: "Optional" } }) } },
        "foo.sensor": { schemas: { CONFIG_SCHEMA: schema({ distance: { key: "Optional" } }) } },
      },
    },
    pages: {
      "foo.mdx": [
        "Foo.",
        "## Hub Component",
        "The hub.",
        "### Configuration variables",
        "- **uart_id** (*Optional*, ID): The UART.",
        "## Sensor",
        "### Configuration variables",
        "- **distance** (*Optional*): Distance.",
        "",
      ].join("\n\n"),
    },
  });
  assert.match(docs("foo", "foo", "schemas", "CONFIG_SCHEMA", "schema", "config_vars", "uart_id"), /The UART/);
  assert.match(docs("foo", "foo.sensor", "schemas", "CONFIG_SCHEMA", "schema", "config_vars", "distance"), /Distance/);
  assert.deepEqual(
    report.findings.filter((f) => f.kind === "unresolved_component_heading"),
    [],
  );
});

test("a platform index without a base schema does not get platform keys created on a derived schema", async () => {
  const { store, report } = await walk({
    schema: {
      esphome: core(["foo"], { gizmo: {} }),
      gizmo: {
        gizmo: {
          schemas: { BASIC_GIZMO_SCHEMA: schema({ name: { key: "Optional" } }) },
          components: { foo: {} },
        },
      },
      foo: { "foo.gizmo": { schemas: { CONFIG_SCHEMA: schema({ speed: { key: "Optional" } }) } } },
    },
    pages: {
      "gizmo/index.mdx": [
        "Gizmos.",
        "## Base Gizmo Configuration",
        "- **name** (*Optional*, string): The name.",
        "- **speed** (*Optional*, int): The speed.",
        "",
      ].join("\n\n"),
    },
  });
  const basic = store.files.get("gizmo").gizmo.schemas.BASIC_GIZMO_SCHEMA.schema.config_vars;
  assert.match(basic.name.docs, /The name/);
  assert.equal(basic.speed, undefined);
  assert.deepEqual(
    report.findings.map((f) => [f.kind, f.key]),
    [
      ["missing_base_schema", undefined],
      ["unmatched_key", "speed"],
    ],
  );
});

test("options under a Component heading the schema lacks are dropped, not written to the page component", async () => {
  const { docs, report } = await walk({
    schema: {
      esphome: core(["foo"]),
      foo: {
        foo: { schemas: { CONFIG_SCHEMA: schema({ id: { key: "GeneratedID" }, address: { key: "Optional" } }) } },
      },
    },
    pages: {
      "foo.mdx": [
        "Foo.",
        "## Configuration variables",
        "- **address** (*Optional*, int): The hub address.",
        "## Lambda Hook Component",
        "A helper.",
        "### Configuration variables",
        "- **id** (**Required**, ID): The ID to use in lambdas.",
        "- **address** (**Required**, int): The address every call targets.",
        "## Other",
        "",
      ].join("\n\n"),
    },
  });
  assert.match(docs("foo", "foo", "schemas", "CONFIG_SCHEMA", "schema", "config_vars", "address"), /The hub address/);
  assert.equal(docs("foo", "foo", "schemas", "CONFIG_SCHEMA", "schema", "config_vars", "id"), undefined);
  assert.deepEqual(
    report.findings.map((f) => [f.kind, f.line]),
    [
      ["unresolved_component_heading", 11],
      ["unroutable_section", 15],
      ["orphan_option_list", 17],
    ],
  );
});

test("an Over SPI heading on a component typed by bus documents that variant", async () => {
  const { docs, report } = await walk({
    schema: {
      esphome: core(["foo"]),
      foo: {
        foo: {
          schemas: {
            CONFIG_SCHEMA: {
              type: "typed",
              typed_key: "type",
              types: {
                gpio: { config_vars: { data_pin: { key: "Required" }, sr_count: { key: "Optional" } } },
                spi: { config_vars: { spi_id: { key: "Optional" }, sr_count: { key: "Optional" } } },
              },
            },
          },
        },
      },
    },
    pages: {
      "foo.mdx": [
        "Foo.",
        "## Over GPIO",
        "### Configuration variables",
        "- **type** (**Required**): `gpio` or `spi`.",
        "- **data_pin** (**Required**, pin): The data pin.",
        "- **sr_count** (*Optional*, int): Chained registers.",
        "## Over SPI",
        "### Configuration variables",
        "- **spi_id** (*Optional*, ID): The SPI bus.",
        "- **sr_count** (*Optional*, int): Chained registers over SPI.",
        "## Pin configuration",
        "",
      ].join("\n\n"),
    },
  });
  const types = (...k) => docs("foo", "foo", "schemas", "CONFIG_SCHEMA", "types", ...k);
  assert.match(types("gpio", "config_vars", "data_pin"), /The data pin/);
  assert.match(types("gpio", "config_vars", "sr_count"), /Chained registers\./);
  assert.match(types("spi", "config_vars", "spi_id"), /The SPI bus/);
  assert.match(types("spi", "config_vars", "sr_count"), /over SPI/);
  assert.deepEqual(report.findings, []);
});

test("a trigger section reaches that trigger in every typed variant", async () => {
  const trigger = () => ({ key: "Optional", type: "schema", schema: { config_vars: { then: { key: "Optional" } } } });
  const { store } = await walk({
    schema: {
      esphome: core(["foo"]),
      foo: {
        foo: {
          schemas: {
            CONFIG_SCHEMA: {
              type: "typed",
              typed_key: "model",
              types: {
                a: { config_vars: { on_event: trigger() } },
                b: { config_vars: { on_event: trigger(), pin: { key: "Required" } } },
              },
            },
          },
        },
      },
    },
    pages: {
      "foo.mdx": [
        "Foo.",
        "## Configuration variables",
        "- **model** (**Required**): The model.",
        "- **pin** (**Required**, pin): The pin.",
        "## `on_event` Trigger",
        "Fires on an event.",
        "### Configuration variables",
        "- **then** (*Optional*, Automation): What to run.",
        "",
      ].join("\n\n"),
    },
  });
  for (const variant of ["a", "b"]) {
    const onEvent = store.files.get("foo").foo.schemas.CONFIG_SCHEMA.types[variant].config_vars.on_event;
    assert.match(onEvent.schema.config_vars.then.docs, /What to run/);
  }
});

test("a trigger section reaches an inherited trigger through a docs-only copy on the child", async () => {
  const { store, report } = await walk({
    schema: {
      esphome: core(["foo"]),
      foo: {
        foo: {
          schemas: {
            BASE_SCHEMA: schema({
              on_event: { key: "Optional", type: "schema", schema: { config_vars: { then: { key: "Optional" } } } },
            }),
            // An earlier page refined the inherited trigger into a copy that holds only docs
            CONFIG_SCHEMA: {
              type: "schema",
              schema: { config_vars: { on_event: { key: "Optional", docs: "x" } }, extends: ["foo.BASE_SCHEMA"] },
            },
          },
        },
      },
    },
    pages: {
      "foo.mdx": [
        "Foo.",
        "## `on_event` Trigger",
        "Fires on an event.",
        "### Configuration variables",
        "- **then** (*Optional*, Automation): What to run.",
        "",
      ].join("\n\n"),
    },
  });
  const base = store.files.get("foo").foo.schemas.BASE_SCHEMA.schema.config_vars.on_event;
  assert.match(base.schema.config_vars.then.docs, /What to run/);
  assert.deepEqual(
    report.findings.filter((f) => ["unmatched_key", "unroutable_section", "unresolved_trigger"].includes(f.kind)),
    [],
  );
});

test("a trigger heading the schema cannot place is reported and routes as before", async () => {
  const { docs, report } = await walk({
    schema: {
      esphome: core(["foo"]),
      foo: { foo: { schemas: { CONFIG_SCHEMA: schema({ id: { key: "GeneratedID" }, name: { key: "Optional" } }) } } },
    },
    pages: {
      "foo.mdx": [
        "Foo.",
        "## Configuration variables",
        "- **name** (*Optional*, string): The name.",
        "## `foo.on_missing` Trigger",
        "- **then** (*Optional*, Automation): What to run.",
        "",
      ].join("\n\n"),
    },
  });
  assert.match(docs("foo", "foo", "schemas", "CONFIG_SCHEMA", "schema", "config_vars", "name"), /The name/);
  assert.deepEqual(
    report.findings.map((f) => [f.kind, f.line]),
    [
      ["unresolved_trigger", 11],
      ["unmatched_key", 13],
    ],
  );
});

test("a platform key documented on the base page is not created on the base schema without docs", async () => {
  const { store, report } = await walk({
    schema: {
      esphome: core(["foo"], { gizmo: {} }),
      gizmo: { gizmo: { schemas: { GIZMO_SCHEMA: schema({ name: { key: "Optional" } }) }, components: { foo: {} } } },
      foo: {
        "foo.gizmo": { schemas: { CONFIG_SCHEMA: schema({ speed: { key: "Optional" }, mode: { key: "Optional" } }) } },
      },
    },
    pages: {
      "gizmo/index.mdx": [
        "Gizmos.",
        "## Configuration variables",
        "- **speed** (*Optional*, int): The speed.",
        "- **mode**: (*Optional*, string)",
        "",
      ].join("\n\n"),
    },
  });
  const base = store.files.get("gizmo").gizmo.schemas.GIZMO_SCHEMA.schema.config_vars;
  assert.match(base.speed.docs, /The speed/);
  assert.equal(base.mode, undefined);
  assert.deepEqual(
    report.findings.filter((f) => f.kind === "unmatched_key"),
    [],
  );
});

test("a sibling-schema heading keeps its section through a nested configuration heading", async () => {
  const { docs, report } = await walk({
    schema: {
      esphome: core(["foo"]),
      foo: {
        foo: {
          schemas: {
            CONFIG_SCHEMA: schema({ name: { key: "Optional" } }),
            LIGHT_STATE_SCHEMA: schema({ brightness: { key: "Optional" } }),
          },
        },
      },
    },
    pages: {
      "foo.mdx": [
        "Foo.",
        "## Configuration variables",
        "- **name** (*Optional*, string): The name.",
        "## Light state",
        "A light state has these variables:",
        "### Configuration variables",
        "- **brightness** (*Optional*, percentage): The brightness.",
        "## Unrelated",
        "### Configuration variables",
        "- **name** (*Optional*, string): Still the name.",
        "",
      ].join("\n\n"),
    },
  });
  assert.match(
    docs("foo", "foo", "schemas", "LIGHT_STATE_SCHEMA", "schema", "config_vars", "brightness"),
    /The brightness/,
  );
  assert.match(docs("foo", "foo", "schemas", "CONFIG_SCHEMA", "schema", "config_vars", "name"), /Still the name/);
  assert.deepEqual(
    report.findings.filter((f) => f.kind === "unmatched_key"),
    [],
  );
});

test("a bold configuration label stays inside the sub-schema section it follows", async () => {
  const { docs, report } = await walk({
    schema: {
      esphome: core(["foo"]),
      foo: {
        foo: {
          schemas: {
            CONFIG_SCHEMA: schema({
              name: { key: "Optional" },
              legend: { key: "Optional", type: "schema", schema: { config_vars: { border: { key: "Optional" } } } },
            }),
          },
        },
      },
    },
    pages: {
      "foo.mdx": [
        "Foo.",
        "## Configuration variables",
        "- **name** (*Optional*, string): The name.",
        "### Legend Options",
        "**Configuration variables:**",
        "- **border** (*Optional*, boolean): Draw a border.",
        "",
      ].join("\n\n"),
    },
  });
  assert.match(
    docs(
      "foo",
      "foo",
      "schemas",
      "CONFIG_SCHEMA",
      "schema",
      "config_vars",
      "legend",
      "schema",
      "config_vars",
      "border",
    ),
    /Draw a border/,
  );
  assert.deepEqual(
    report.findings.filter((f) => f.kind === "unmatched_key"),
    [],
  );
});

test("a nested key only one typed variant has is still audited", async () => {
  const options = (extra = {}) => ({
    key: "Optional",
    type: "schema",
    schema: { config_vars: { x: { key: "Optional" }, ...extra } },
  });
  const { report } = await walk({
    schema: {
      esphome: core(["foo"]),
      foo: {
        foo: {
          schemas: {
            CONFIG_SCHEMA: {
              type: "typed",
              typed_key: "model",
              types: {
                a: { config_vars: { options: options() } },
                b: { config_vars: { options: options({ extra: { key: "Optional" } }) } },
              },
            },
          },
        },
      },
    },
    pages: {
      "foo.mdx": [
        "Foo.",
        "## Configuration variables",
        "- **model** (**Required**): The model.",
        "- **options** (*Optional*): The options.\n  - **x** (*Optional*, int): X.",
        "",
      ].join("\n\n"),
    },
  });
  assert.deepEqual(
    report.findings.filter((f) => f.kind === "undocumented_key").map((f) => [f.schema, f.key]),
    [["foo.CONFIG_SCHEMA/options", "extra"]],
  );
});

test("nested audits two levels down are kept apart per branch", async () => {
  const branch = (...keys) => ({
    key: "Optional",
    type: "schema",
    schema: {
      config_vars: {
        options: {
          key: "Optional",
          type: "schema",
          schema: { config_vars: Object.fromEntries(keys.map((k) => [k, { key: "Optional" }])) },
        },
      },
    },
  });
  const { report } = await walk({
    schema: {
      esphome: core(["foo"]),
      foo: { foo: { schemas: { CONFIG_SCHEMA: schema({ left: branch("a"), right: branch("b", "c") }) } } },
    },
    pages: {
      "foo.mdx": [
        "Foo.",
        "## Configuration variables",
        "- **left** (*Optional*): Left.\n  - **options** (*Optional*): Options.\n    - **a** (*Optional*, int): A.",
        "- **right** (*Optional*): Right.\n  - **options** (*Optional*): Options.\n    - **c** (*Optional*, int): C.",
        "",
      ].join("\n\n"),
    },
  });
  assert.deepEqual(
    report.findings.filter((f) => f.kind === "undocumented_key").map((f) => [f.schema, f.key]),
    [["foo.CONFIG_SCHEMA/right/options", "b"]],
  );
});
