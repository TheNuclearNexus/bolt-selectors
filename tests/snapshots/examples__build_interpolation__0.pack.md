# Lectern snapshot

## Data pack

`@data_pack pack.mcmeta`

```json
{
  "pack": {
    "pack_format": 61,
    "description": ""
  }
}
```

### test

`@function test:foo`

```mcfunction
tellraw @s "hi"
kill @e[tag=foobar.test, type=minecraft:cow]
```
