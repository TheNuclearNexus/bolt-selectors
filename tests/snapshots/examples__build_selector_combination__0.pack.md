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
give @e[distance=1..4, type=!zombie] diamond
give @s[distance=2..6, type=!skeleton] emerald
give @e[distance=1..6, type=!skeleton, type=!zombie] netherite_ingot
```
