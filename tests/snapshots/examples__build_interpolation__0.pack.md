# Lectern snapshot

## Data pack

`@data_pack pack.mcmeta`

```json
{
  "pack": {
    "min_format": [
      94,
      1
    ],
    "max_format": [
      94,
      1
    ],
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
