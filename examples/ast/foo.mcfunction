
# this should not be affected
if entity @e[type=armor_stand]

entity = "minecraft:zombie"
dist = 5

self = @s[
    x=0,
    y=0,
    z=0,

    distance=(None, dist),

    dx=1,
    dy=1,
    dz=1,

    x_rotation=..90,
    y_rotation=90..,

    scores={foo=1,bar=..1,baz=1..},

    tag=foo.bar.baz,
    tag=!foo.baz.bar,

    team=fooBar,
    team=!fooBaz,

    name=BazBarFoo,
    name=!BarFooBaz,

    type=entity,
    type=!skeleton,

    predicate=./foo,
    predicate=!./bar,

    nbt={Health:20f},
    nbt=!{Health:19f},

    level=1..,
    gamemode=!adventure,
    gamemode=!survival,
    advancements={
        ./foo=true,
        ./bar={baz=true}
    },

    limit=1,
    sort=nearest
]

give self stick

