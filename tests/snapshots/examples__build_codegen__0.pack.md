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
_bolt_lineno = [1, 11, 13, 15, 18, 20, 21], [1, 5, 6, 13, 33, 8, 54]
_bolt_helper_interpolate_range = _bolt_runtime.helpers['interpolate_range']
_bolt_helper_replace = _bolt_runtime.helpers['replace']
_bolt_helper_interpolate_resource_location = _bolt_runtime.helpers['interpolate_resource_location']
_bolt_helper_children = _bolt_runtime.helpers['children']
_bolt_helper_ast_to_selector = _bolt_runtime.helpers['ast_to_selector']
_bolt_helper_interpolate_entity = _bolt_runtime.helpers['interpolate_entity']
with _bolt_runtime.scope() as _bolt_var7:
    _bolt_runtime.commands.append(_bolt_refs[0])
    _bolt_var0 = 'minecraft:zombie'
    entity = _bolt_var0
    _bolt_var1 = 5
    dist = _bolt_var1
    _bolt_var2 = None
    _bolt_var3 = dist
    _bolt_var4 = (_bolt_var2,_bolt_var3,)
    _bolt_var4 = _bolt_helper_interpolate_range(_bolt_var4, _bolt_refs[1])
    _bolt_var5 = entity
    _bolt_var5 = _bolt_helper_interpolate_resource_location(_bolt_var5, _bolt_refs[6])
    self = _bolt_helper_ast_to_selector(_bolt_helper_replace(_bolt_refs[31], arguments=_bolt_helper_children([_bolt_refs[3], _bolt_refs[4], _bolt_refs[5], _bolt_helper_replace(_bolt_refs[2], value=_bolt_var4), _bolt_refs[8], _bolt_refs[9], _bolt_refs[10], _bolt_refs[11], _bolt_refs[12], _bolt_refs[13], _bolt_refs[14], _bolt_refs[15], _bolt_refs[16], _bolt_refs[17], _bolt_refs[18], _bolt_refs[19], _bolt_helper_replace(_bolt_refs[7], value=_bolt_var5), _bolt_refs[20], _bolt_refs[21], _bolt_refs[22], _bolt_refs[23], _bolt_refs[24], _bolt_refs[25], _bolt_refs[26], _bolt_refs[27], _bolt_refs[28], _bolt_refs[29], _bolt_refs[30]])))
    _bolt_var6 = self
    _bolt_var6 = _bolt_helper_interpolate_entity(_bolt_var6, _bolt_refs[32])
    _bolt_runtime.commands.append(_bolt_helper_replace(_bolt_refs[34], arguments=_bolt_helper_children([_bolt_var6, _bolt_refs[33]])))
_bolt_var8 = _bolt_helper_replace(_bolt_refs[35], commands=_bolt_helper_children(_bolt_var7))
```
