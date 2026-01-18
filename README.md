# Bolt Selectors
> Lets you work with selectors in a pythonic way

## Configuration
1. Setup `beet.yml`/`beet.json`
```yml
pipeline:
 - mecha

require:
 - bolt
 - bolt_selectors
```
2. Start using macros
```mcfunction
self = @s
if score self id matches 0 run say me
```
```mcfunction
if score @s id matches 0 run say me
```