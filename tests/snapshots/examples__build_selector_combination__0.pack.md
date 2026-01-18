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
give @e[distance=1..4, type=!zombie] diamond
give @s[distance=2..6, type=!skeleton] emerald
give @e[distance=1..6, type=!skeleton, type=!zombie] netherite_ingot
```
