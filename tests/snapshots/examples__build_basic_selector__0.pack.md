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
give @s[x=0, y=0, z=0, distance=..1, dx=1, dy=1, dz=1, x_rotation=..90, y_rotation=90.., scores={foo=1, bar=..1, baz=1..}, tag=foo.bar.baz, tag=!foo.baz.bar, team=fooBar, team=!fooBaz, name=!BarFooBaz, name=BazBarFoo, type=!skeleton, type=zombie, predicate=!test:bar, predicate=test:foo, nbt={Health: 20.0f}, nbt=!{Health: 19.0f}, level=1.., gamemode=!adventure, gamemode=!survival, advancements={test:foo=true, test:bar={baz=true}}, limit=1, sort=nearest] stick
```
