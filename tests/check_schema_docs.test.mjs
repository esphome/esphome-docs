import assert from "node:assert/strict";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";
import { unified } from "unified";
import remarkMdx from "remark-mdx";
import remarkParse from "remark-parse";

import { parseItem, registryHeading, SchemaStore, toInner } from "../script/check_schema_docs.mjs";

const parse = (md) => unified().use(remarkParse).use(remarkMdx).parse(md);

test("parseItem reads key and optionality from a config bullet", () => {
  const tree = parse("- **baud_rate** (**Required**, int): The baud rate.\n- **tx_pin** (*Optional*, pin): TX.\n");
  const [a, b] = tree.children[0].children.map(parseItem);
  assert.deepEqual([a.key, a.optionality], ["baud_rate", "required"]);
  assert.deepEqual([b.key, b.optionality], ["tx_pin", "optional"]);
});

test("parseItem marks non-key bullets as prose", () => {
  const tree = parse("- **Side** (wall mounted): angle is measured from +X.\n- plain text bullet\n");
  const [a, b] = tree.children[0].children.map(parseItem);
  assert.equal(a.prose, true);
  assert.equal(b, null);
});

test("registryHeading uses the inline code, not the heading text", () => {
  const tree = parse("## `uart.write` Action\n");
  assert.deepEqual(registryHeading(tree.children[0]), { name: "uart.write", type: "action" });
  assert.equal(registryHeading(parse("## Debugging\n").children[0]), null);
});

test("toInner exposes the typed key and all variants", () => {
  const inner = toInner({
    type: "typed",
    typed_key: "role",
    types: { client: { config_vars: { host: { key: "Required" } } }, server: { config_vars: {} } },
  });
  assert.equal(inner.typedKey, "role");
  assert.equal(inner.variants.length, 2);
  assert.equal(toInner({ type: "typed", typed_key: "role", types: { client: {} } }, "server"), null);
});

test("SchemaStore resolves components, platforms, registries and extends", async () => {
  const dir = mkdtempSync(join(tmpdir(), "schema-"));
  writeFileSync(
    join(dir, "esphome.json"),
    JSON.stringify({
      core: {
        components: { foo: {} },
        platforms: { sensor: {} },
        action: { delay: { schema: { config_vars: { delay: { key: "Required" } } } } },
        schemas: { COMPONENT_SCHEMA: { schema: { config_vars: { setup_priority: { key: "Optional" } } } } },
      },
    }),
  );
  writeFileSync(
    join(dir, "foo.json"),
    JSON.stringify({
      foo: {
        schemas: {
          CONFIG_SCHEMA: {
            type: "schema",
            schema: {
              config_vars: { id: { key: "GeneratedID" }, pin: { key: "Required" } },
              extends: ["core.COMPONENT_SCHEMA"],
            },
          },
        },
        action: { toggle: {} },
      },
      "foo.sensor": {
        schemas: {
          CONFIG_SCHEMA: {
            type: "schema",
            schema: { config_vars: { target_1: { key: "Optional" }, target_2: { key: "Optional" } } },
          },
        },
      },
    }),
  );
  const store = new SchemaStore({ dir });
  await store.init();

  const foo = await store.resolve("foo.CONFIG_SCHEMA");
  assert.ok(await store.findProp(foo, "pin"));
  assert.ok(await store.findProp(foo, "setup_priority"), "follows extends into core");
  assert.deepEqual([...store.ownKeys(foo)], ["pin"], "ids are not reported as undocumented");

  assert.ok(await store.resolve("core.action.delay"));
  assert.ok(await store.resolve("foo.action.toggle"), "an empty registry entry still exists");
  assert.equal(await store.resolve("foo.action.missing"), null);

  const sensor = await store.resolve("foo.sensor.CONFIG_SCHEMA");
  assert.deepEqual(store.numberedFamily(sensor, "target_N"), ["target_1", "target_2"]);
  assert.equal((await store.resolve("foo.*")).variants.length, 2, "wildcard unions every schema in the file");
});
