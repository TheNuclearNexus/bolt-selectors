from dataclasses import dataclass, fields
from functools import partial
from typing import Any, Callable, Optional, TypeVar, cast
from beet import Context
from beet.core.utils import extra_field
from bolt import AstValue, InterpolationParser, Runtime
from nbtlib import (
    Compound,
    Byte,
    Int,
    Short,
    Long,
    Float,
    Double,
    List,
    String,
    Array,
    IntArray,
    LongArray,
    ByteArray,
)

from mecha import (
    AlternativeParser,
    AstAdvancementPredicate,
    AstBool,
    AstNbtCompound,
    AstNumber,
    AstObjective,
    AstResourceLocation,
    AstSelectorAdvancementMatch,
    AstSelectorAdvancementPredicateMatch,
    AstSelectorScoreMatch,
    AstSelectorScores,
    AstSortOrder,
    AstString,
    Mecha,
    Parser,
)
from mecha.ast import (
    AstChildren,
    AstNode,
    AstRange,
    AstSelector,
    AstSelectorArgument,
    AstSelectorAdvancements,
)
from tokenstream import TokenStream, set_location

NBT_GLOBALS = [
    Compound,
    Byte,
    Int,
    Short,
    Long,
    List,
    Float,
    Double,
    String,
    Array,
    IntArray,
    LongArray,
    ByteArray,
]


def beet_default(ctx: Context):
    mc = ctx.inject(Mecha)
    runtime = ctx.inject(Runtime)
    runtime.globals.update({"Selector": Selector})
    runtime.globals.update({t.__name__: t for t in NBT_GLOBALS})
    mc.spec.parsers["bolt:literal"] = SelectorParser(
        literal_parser=mc.spec.parsers["bolt:literal"],
        selector_parser=mc.spec.parsers["selector"],
    )

    mc.spec.parsers["selector"] = AlternativeParser(
        [mc.spec.parsers["selector"], InterpolationParser("selector")]
    )

    runtime.helpers["interpolate_entity"] = SelectorConverter(
        runtime.helpers["interpolate_entity"]
    )


T = TypeVar("T")
N = TypeVar("N", int, float)
ExactOrRangeArgument = N | tuple[N | None, N | None]
NegatableArgument = tuple[bool, T]


@dataclass
class SelectorConverter:
    base_converter: Callable[[Any, AstNode], AstNode]

    def __call__(self, obj: Any, node: AstNode) -> AstNode:
        if isinstance(obj, Selector):
            return obj.to_ast(node)

        return self.base_converter(obj, node)


def selector_arg(key: str, value: AstNode, inverted: bool = False):
    return AstSelectorArgument(
        key=AstString.from_value(key), value=value, inverted=inverted
    )


def score_field_to_ast(scores: dict[str, ExactOrRangeArgument[int]]):
    score_nodes = []
    for objective, range in scores.items():
        score_nodes.append(
            AstSelectorScoreMatch(
                key=AstObjective.from_value(objective),
                value=AstRange.from_value(range),
            )
        )
    return AstSelectorScores(scores=AstChildren(score_nodes))


def advancements_field_to_ast(advancements: dict[str, bool | dict[str, bool]]):
    advancement_nodes = []
    for path, value in advancements.items():
        if isinstance(value, bool):
            value_node = AstBool.from_value(value)
        else:
            criteria_nodes = []
            for criteria, state in value.items():
                criteria_nodes.append(
                    AstSelectorAdvancementPredicateMatch(
                        key=AstAdvancementPredicate.from_value(criteria),
                        value=AstBool.from_value(state),
                    )
                )
            value_node = AstChildren(criteria_nodes)

        advancement_nodes.append(
            AstSelectorAdvancementMatch(
                key=AstResourceLocation.from_value(path), value=value_node
            )
        )
    return AstSelectorAdvancements(advancements=AstChildren(advancement_nodes))


FIELD_TO_FACTORY = {
    "x": AstNumber.from_value,
    "y": AstNumber.from_value,
    "z": AstNumber.from_value,
    "distance": AstRange.from_value,
    "dx": AstNumber.from_value,
    "dy": AstNumber.from_value,
    "dz": AstNumber.from_value,
    "x_rotation": AstRange.from_value,
    "y_rotation": AstRange.from_value,
    "scores": score_field_to_ast,
    "tags": AstString.from_value,
    "teams": AstString.from_value,
    "names": AstString.from_value,
    "types": AstResourceLocation.from_value,
    "predicates": AstResourceLocation.from_value,
    "nbts": AstNbtCompound.from_value,
    "level": AstRange.from_value,
    "gamemodes": AstString.from_value,
    "advancements": advancements_field_to_ast,
    "limit": AstNumber.from_value,
    "sort": AstSortOrder.from_value,
}


@dataclass
class Selector:
    variable: str

    x: Optional[int | float] = extra_field(default=None)
    y: Optional[int | float] = extra_field(default=None)
    z: Optional[int | float] = extra_field(default=None)

    distance: Optional[ExactOrRangeArgument[int | float]] = extra_field(default=None)

    dx: Optional[int | float] = extra_field(default=None)
    dy: Optional[int | float] = extra_field(default=None)
    dz: Optional[int | float] = extra_field(default=None)

    x_rotation: Optional[ExactOrRangeArgument[int | float]] = extra_field(default=None)
    y_rotation: Optional[ExactOrRangeArgument[int | float]] = extra_field(default=None)

    scores: Optional[dict[str, ExactOrRangeArgument[int]]] = extra_field(default=None)
    tags: Optional[set[NegatableArgument[str]]] = extra_field(default=None)
    teams: Optional[set[NegatableArgument[str]]] = extra_field(default=None)

    names: Optional[set[NegatableArgument[str]]] = extra_field(default=None)
    types: Optional[set[NegatableArgument[str]]] = extra_field(default=None)
    predicates: Optional[set[NegatableArgument[str]]] = extra_field(default=None)

    nbts: Optional[list[NegatableArgument[Compound]]] = extra_field(default=None)

    level: Optional[ExactOrRangeArgument[int]] = extra_field(default=None)
    gamemodes: Optional[set[NegatableArgument[str]]] = extra_field(default=None)
    advancements: Optional[dict[str, bool | dict[str, bool]]] = extra_field(
        default=None
    )

    limit: Optional[int] = extra_field(default=None)
    sort: Optional[str] = extra_field(default=None)

    def __repr__(self):
        field_values = {k: v for k, v in self.__dict__.items() if v is not None}
        field_str = ", ".join(f"{k}={repr(v)}" for k, v in field_values.items())
        return f"{self.__class__.__name__}({field_str})"

    def positioned(
        self, value: tuple[int | float, int | float, int | float] | None
    ) -> "Selector":
        if value is None:
            value = (None, None, None)

        self.x = value[0]
        self.y = value[1]
        self.z = value[2]

        return self

    def bounded(
        self, value: tuple[int | float, int | float, int | float] | None
    ) -> "Selector":
        if value is None:
            value = (None, None, None)

        self.dx = value[0]
        self.dy = value[1]
        self.dz = value[2]

        return self

    def within(self, value: ExactOrRangeArgument[int | float] | None) -> "Selector":
        self.distance = value
        return self

    def rotated(
        self,
        value: (
            tuple[ExactOrRangeArgument[int | float], ExactOrRangeArgument[int | float]]
            | None
        ),
    ) -> "Selector":
        if value is None:
            value = (None, None)

        self.x_rotation = value[0]
        self.y_rotation = value[1]

        return self

    def score(self, objective: str, value: ExactOrRangeArgument[int] | None):
        if value is None:
            del self.scores[objective]
        else:
            self.scores[objective] = value

        return self
    
    def _toggle_value(self, value: T, state: bool | None, values: set[NegatableArgument[T]]) -> "Selector":
        if state is None:
            if (True, value) in values:
                values.remove((True, value))
            if (False, value) in values:
                values.remove((False, value))

            return self

        if (not state, value) in values:
            values.remove(not state, value)

        values.add((state, value))

        return self

    def tag(self, tag: str, state: bool | None = False) -> "Selector":
        return self._toggle_value(tag, state, self.tags)
        
    def team(self, team: str, state: bool | None = False) -> "Selector":
        return self._toggle_value(team, state, self.teams)
   
    def name(self, name: str, state: bool | None = False) -> "Selector":
        return self._toggle_value(name, state, self.names) 

    def type(self, type: str, state: bool | None = False) -> "Selector":
        return self._toggle_value(type, state, self.types)
    
    def predicate(self, predicate: str, state: bool | None = False) -> "Selector":
        return self._toggle_value(predicate, state, self.predicates)
 
    def nbt(self, nbt: Compound, state: bool | None = False) -> "Selector":
        return self._toggle_value(nbt, state, self.nbts)
    
    def at_level(self, value: ExactOrRangeArgument[int] | None) -> "Selector":
        self.level = value
        return self
    
    def gamemode(self, gamemode: str, state: bool | None = False) -> "Selector":
        return self._toggle_value(gamemode, state, self.gamemodes)
    
    def advancement(self, advancement: str, state: bool | dict[str, bool | None] | None) -> "Selector":
        if state is None:
            if advancement in self.advancements:
                del self.advancements[advancement]
            return self 

        if not (cur_value := self.advancements.get(advancement)) or (isinstance(state, bool) or isinstance(cur_value, bool)):
            self.advancements[advancement] = state
            return self

        for criteria, new_state in state.items():
            if new_state is None:
                del cur_value[criteria]
            else:
                cur_value[criteria] = new_state
            
        return self
    
    def limit_to(self, limit: int|None) -> "Selector":
        self.limit = limit
        return self
    
    def sorted_by(self, sort: str | None) -> "Selector":
        self.sort = sort
        return self

    def to_ast(self, node: AstNode):
        args = []

        for field in fields(self):
            if (
                field_value := getattr(self, field.name)
            ) is None or field.name == "variable":
                continue

            factory = FIELD_TO_FACTORY[field.name]

            if isinstance(field_value, list) or isinstance(field_value, set):
                for entry in field_value:
                    args.append(
                        selector_arg(field.name[:-1], factory(entry[1]), entry[0])
                    )
            else:
                args.append(selector_arg(field.name, factory(field_value)))

        return set_location(
            AstSelector(variable=self.variable, arguments=args),
            node.location,
            node.end_location,
        )


EXACT_VALUES = ["x", "y", "z", "dx", "dy", "dz", "limit", "sort"]

RANGE_VALUES = set(["distance", "x_rotation", "y_rotation", "level"])

STRING_LIST_VALUES = set(["tag", "team", "name", "gamemode"])
RESOURCE_LOCATION_VALUES = set(["type", "predicate"])


def parse_range(range: AstRange):
    if range.exact:
        return range.min

    return (range.min, range.max)


def parse_exact(node: AstNode):
    if hasattr(node, "value"):
        return getattr(node, "value")

    return None


def parse_invertable(inverted: bool, node: AstNode, parser: Callable[[AstNode], Any]):
    value = parser(node)
    if value is None:
        return None

    return (inverted, value)


def parse_value(key: str, value: AstNode, inverted: bool):
    if value is None:
        return None

    if key in EXACT_VALUES:
        return parse_exact(value)

    if key in RANGE_VALUES and isinstance(value, AstRange):
        return parse_range(value)

    if key in STRING_LIST_VALUES:
        value = parse_invertable(inverted, value, parse_exact)

        return set([value]) if value is not None else None

    if key in RESOURCE_LOCATION_VALUES and isinstance(value, AstResourceLocation):
        return set([(inverted, value.get_value())])

    if key == "advancements" and isinstance(value, AstSelectorAdvancements):
        return parse_advancements(value)

    if key == "scores" and isinstance(value, AstSelectorScores):
        return parse_scores(value)

    if key == "nbt" and isinstance(value, AstNbtCompound):
        return [(inverted, value.evaluate())]

    return None


def parse_scores(value: AstSelectorScores):
    new_value = {}
    for score in value.scores:
        new_value[score.key.value] = parse_range(score.value)
    return new_value


def parse_advancements(value: AstSelectorAdvancements):
    new_value = {}
    for advancement in value.advancements:
        path = advancement.key.get_value()

        if isinstance(advancement.value, AstBool):
            new_value[path] = advancement.value.value
        else:
            new_value[path] = {n.key.value: n.value.value for n in advancement.value}

    return new_value


@dataclass
class SelectorParser:

    literal_parser: Parser
    selector_parser: Parser

    def handle_arguments(self, selector_arguments: AstChildren[AstSelectorArgument]):
        arguments = {}

        for argument in selector_arguments:
            key = argument.key.value
            value = parse_value(key, argument.value, argument.inverted)

            if value is None:
                continue

            if isinstance(value, set) or isinstance(value, list):
                key += "s"

            if key in arguments and isinstance(arguments[key], set):
                arguments[key] = arguments[key].union(value)
            elif key in arguments and isinstance(arguments[key], list):
                arguments[key] += value
            else:
                arguments[key] = value

        return arguments

    def __call__(self, stream: TokenStream):
        with stream.checkpoint() as commit:
            node: AstSelector = self.selector_parser(stream)

            arguments = self.handle_arguments(node.arguments)

            selector = Selector(node.variable, **arguments)

            commit()
            return set_location(AstValue(value=selector), stream.current)
        return self.literal_parser(stream)
