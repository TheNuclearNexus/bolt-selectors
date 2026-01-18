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
<class 'mecha.ast.AstRoot'>
  commands:
    <class 'mecha.ast.AstCommand'>
      identifier: 'execute:subcommand'
      arguments:
        <class 'mecha.ast.AstCommand'>
          identifier: 'execute:if:entity:entities'
          arguments:
            <class 'mecha.ast.AstSelector'>
              variable: 'e'
              arguments:
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: False
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'type'
                  value:
                    <class 'mecha.ast.AstResourceLocation'>
                      is_tag: False
                      namespace: None
                      path: 'armor_stand'
    <class 'bolt.ast.AstStatement'>
      identifier: 'mecha:sentinel'
      arguments:
        <class 'bolt.ast.AstAssignment'>
          operator: '='
          target:
            <class 'bolt.ast.AstTargetIdentifier'>
              value: 'entity'
              rebind: False
          value:
            <class 'bolt.ast.AstValue'>
              value: 'minecraft:zombie'
          type_annotation: None
    <class 'bolt.ast.AstStatement'>
      identifier: 'mecha:sentinel'
      arguments:
        <class 'bolt.ast.AstAssignment'>
          operator: '='
          target:
            <class 'bolt.ast.AstTargetIdentifier'>
              value: 'dist'
              rebind: False
          value:
            <class 'bolt.ast.AstValue'>
              value: 5
          type_annotation: None
    <class 'bolt.ast.AstStatement'>
      identifier: 'mecha:sentinel'
      arguments:
        <class 'bolt.ast.AstAssignment'>
          operator: '='
          target:
            <class 'bolt.ast.AstTargetIdentifier'>
              value: 'self'
              rebind: False
          value:
            <class 'bolt_selectors.plugin.AstSelectorLiteral'>
              variable: 's'
              arguments:
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: False
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'x'
                  value:
                    <class 'mecha.ast.AstNumber'>
                      value: 0
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: False
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'y'
                  value:
                    <class 'mecha.ast.AstNumber'>
                      value: 0
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: False
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'z'
                  value:
                    <class 'mecha.ast.AstNumber'>
                      value: 0
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: False
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'distance'
                  value:
                    <class 'bolt.ast.AstInterpolation'>
                      prefix: None
                      unpack: None
                      converter: 'range'
                      value:
                        <class 'bolt.ast.AstTuple'>
                          items:
                            <class 'bolt.ast.AstValue'>
                              value: None
                            <class 'bolt.ast.AstIdentifier'>
                              value: 'dist'
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: False
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'dx'
                  value:
                    <class 'mecha.ast.AstNumber'>
                      value: 1
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: False
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'dy'
                  value:
                    <class 'mecha.ast.AstNumber'>
                      value: 1
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: False
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'dz'
                  value:
                    <class 'mecha.ast.AstNumber'>
                      value: 1
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: False
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'x_rotation'
                  value:
                    <class 'mecha.ast.AstRange'>
                      min: None
                      max: 90
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: False
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'y_rotation'
                  value:
                    <class 'mecha.ast.AstRange'>
                      min: 90
                      max: None
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: False
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'scores'
                  value:
                    <class 'mecha.ast.AstSelectorScores'>
                      scores:
                        <class 'mecha.ast.AstSelectorScoreMatch'>
                          key:
                            <class 'mecha.ast.AstObjective'>
                              value: 'foo'
                          value:
                            <class 'mecha.ast.AstRange'>
                              min: 1
                              max: 1
                        <class 'mecha.ast.AstSelectorScoreMatch'>
                          key:
                            <class 'mecha.ast.AstObjective'>
                              value: 'bar'
                          value:
                            <class 'mecha.ast.AstRange'>
                              min: None
                              max: 1
                        <class 'mecha.ast.AstSelectorScoreMatch'>
                          key:
                            <class 'mecha.ast.AstObjective'>
                              value: 'baz'
                          value:
                            <class 'mecha.ast.AstRange'>
                              min: 1
                              max: None
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: False
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'tag'
                  value:
                    <class 'mecha.ast.AstWord'>
                      value: 'foo.bar.baz'
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: True
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'tag'
                  value:
                    <class 'mecha.ast.AstWord'>
                      value: 'foo.baz.bar'
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: False
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'team'
                  value:
                    <class 'mecha.ast.AstTeam'>
                      value: 'fooBar'
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: True
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'team'
                  value:
                    <class 'mecha.ast.AstTeam'>
                      value: 'fooBaz'
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: False
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'name'
                  value:
                    <class 'mecha.ast.AstString'>
                      value: 'BazBarFoo'
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: True
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'name'
                  value:
                    <class 'mecha.ast.AstString'>
                      value: 'BarFooBaz'
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: False
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'type'
                  value:
                    <class 'bolt.ast.AstInterpolation'>
                      prefix: None
                      unpack: None
                      converter: 'resource_location'
                      value:
                        <class 'bolt.ast.AstIdentifier'>
                          value: 'entity'
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: True
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'type'
                  value:
                    <class 'mecha.ast.AstResourceLocation'>
                      is_tag: False
                      namespace: None
                      path: 'skeleton'
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: False
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'predicate'
                  value:
                    <class 'mecha.ast.AstResourceLocation'>
                      is_tag: False
                      namespace: 'test'
                      path: 'foo'
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: True
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'predicate'
                  value:
                    <class 'mecha.ast.AstResourceLocation'>
                      is_tag: False
                      namespace: 'test'
                      path: 'bar'
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: False
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'nbt'
                  value:
                    <class 'mecha.ast.AstNbtCompound'>
                      entries:
                        <class 'mecha.ast.AstNbtCompoundEntry'>
                          key:
                            <class 'mecha.ast.AstNbtCompoundKey'>
                              value: 'Health'
                          value:
                            <class 'mecha.ast.AstNbtValue'>
                              value: Float(20.0)
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: True
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'nbt'
                  value:
                    <class 'mecha.ast.AstNbtCompound'>
                      entries:
                        <class 'mecha.ast.AstNbtCompoundEntry'>
                          key:
                            <class 'mecha.ast.AstNbtCompoundKey'>
                              value: 'Health'
                          value:
                            <class 'mecha.ast.AstNbtValue'>
                              value: Float(19.0)
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: False
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'level'
                  value:
                    <class 'mecha.ast.AstRange'>
                      min: 1
                      max: None
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: True
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'gamemode'
                  value:
                    <class 'mecha.ast.AstGamemode'>
                      value: 'adventure'
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: True
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'gamemode'
                  value:
                    <class 'mecha.ast.AstGamemode'>
                      value: 'survival'
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: False
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'advancements'
                  value:
                    <class 'mecha.ast.AstSelectorAdvancements'>
                      advancements:
                        <class 'mecha.ast.AstSelectorAdvancementMatch'>
                          key:
                            <class 'mecha.ast.AstResourceLocation'>
                              is_tag: False
                              namespace: 'test'
                              path: 'foo'
                          value:
                            <class 'mecha.ast.AstBool'>
                              value: True
                        <class 'mecha.ast.AstSelectorAdvancementMatch'>
                          key:
                            <class 'mecha.ast.AstResourceLocation'>
                              is_tag: False
                              namespace: 'test'
                              path: 'bar'
                          value:
                            <class 'mecha.ast.AstSelectorAdvancementPredicateMatch'>
                              key:
                                <class 'mecha.ast.AstAdvancementPredicate'>
                                  value: 'baz'
                              value:
                                <class 'mecha.ast.AstBool'>
                                  value: True
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: False
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'limit'
                  value:
                    <class 'mecha.ast.AstNumber'>
                      value: 1
                <class 'mecha.ast.AstSelectorArgument'>
                  inverted: False
                  key:
                    <class 'mecha.ast.AstString'>
                      value: 'sort'
                  value:
                    <class 'mecha.ast.AstSortOrder'>
                      value: 'nearest'
          type_annotation: None
    <class 'mecha.ast.AstCommand'>
      identifier: 'give:targets:item'
      arguments:
        <class 'bolt.ast.AstInterpolation'>
          prefix: None
          unpack: None
          converter: 'entity'
          value:
            <class 'bolt.ast.AstIdentifier'>
              value: 'self'
        <class 'mecha.ast.AstItemStack'>
          identifier:
            <class 'mecha.ast.AstResourceLocation'>
              is_tag: False
              namespace: None
              path: 'stick'
          arguments:
            <empty>
          data_tags: None
```
