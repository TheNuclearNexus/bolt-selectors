from dataclasses import dataclass, fields
from typing import Any, Optional
from beet.core.utils import extra_field
from nbtlib import Compound

from .types import ExactOrRangeArgument, NegatableArgument, T, N

__all__ = ["Selector"]

OP_ERROR = "Cannot '{}' non-None {}"


def union_single(field: str, op: str):
    def err(a, b):
        if a == b:
            return a

        raise ValueError(OP_ERROR.format(op, field))

    return err


def union_range(field: str):
    def union(a: ExactOrRangeArgument[N], b: ExactOrRangeArgument[N]):
        if a == b:
            return a

        if isinstance(a, N.__constraints__) and isinstance(b, N.__constraints__):
            raise ValueError(f"Cannot '|' between exact {field}s")
        elif isinstance(a, N.__constraints__):
            if a >= b[0] or a <= b[1]:
                return b
        elif isinstance(b, N.__constraints__):
            if b >= a[0] or b <= a[1]:
                return a

        # One of the ranges has no lower bound
        # Return the no lower bound and the max upper bound
        if a[0] is None and b[0] is not None:
            return (None, max(a[1], b[1]))
        elif b[0] is None and a[0] is not None:
            return (None, max(a[1], b[1]))

        # One of the ranges has no upper bound
        # Return the no upper bound and the min lower bound
        if a[1] is None and b[1] is not None:
            return (max(a[0], b[0]), None)
        elif b[1] is None and a[1] is not None:
            return (max(a[0], b[0]), None)

        # The ranges have no overlapping bound so cannot be merged
        if a[1] < b[0]:
            raise ValueError(f"Cannot '|' between {field}s with no overlap")
        elif b[1] < b[0]:
            raise ValueError(f"Cannot '|' between {field}s with no overlap")
        elif a[0] > b[1]:
            raise ValueError(f"Cannot '|' between {field}s with no overlap")
        elif b[0] > a[1]:
            raise ValueError(f"Cannot '|' between {field}s with no overlap")

        # At least one bound is overlapping,
        # so take the min lower and max upper
        min_bound = min(a[0], b[0])
        max_bound = max(a[1], b[1])

        return (min_bound, max_bound)

    return union


def union_scores(
    a: dict[str, ExactOrRangeArgument[int]], b: dict[str, ExactOrRangeArgument[int]]
):
    new_scores = {}

    for objective in a:
        if objective in b:
            new_scores[objective] = union_range("scores." + objective)(
                a[objective], b[objective]
            )
        else:
            new_scores[objective] = a[objective]

    for objective in b:
        if objective in new_scores:
            continue
        new_scores[objective] = b[objective]

    return new_scores


def union_advancements(a: dict[str, bool | dict[str]], b: dict[str, bool | dict[str]]):
    new_advancements = {}

    for path in a:
        if path in b:
            if a[path] == b[path]:
                new_advancements[path] = a[path]
            elif a[path] == True or b[path] == True:
                new_advancements[path] = True
            elif isinstance(a[path], bool) or isinstance(b[path], bool):
                new_advancements[path] = a[path] or b[path]
            else:
                raise ValueError(
                    f"Cannot '|' between advancement.{path} with no overlap"
                )
        else:
            new_advancements[path] = a[path]

    for path in b:
        if path in new_advancements:
            continue
        new_advancements[path] = b[path]

    return new_advancements


def union_negatable_set(a: set[NegatableArgument[T]], b: set[NegatableArgument[T]]):
    return a.union(b)


FIELD_UNION = {
    "x": union_single("x", "|"),
    "y": union_single("y", "|"),
    "z": union_single("z", "|"),
    "distance": union_range("distance"),
    "dx": union_single("dx", "|"),
    "dy": union_single("dy", "|"),
    "dz": union_single("dz", "|"),
    "x_rotation": union_range("x_rotation"),
    "y_rotation": union_range("y_rotation"),
    "scores": union_scores,
    "tags": union_negatable_set,
    "teams": union_negatable_set,
    "names": union_negatable_set,
    "types": union_negatable_set,
    "predicates": union_negatable_set,
    "nbts": lambda a, b: a + b,
    "level": union_range("level"),
    "gamemodes": union_negatable_set,
    "advancements": union_advancements,
    "limit": union_single("limit", "|"),
    "sort": union_single("sort", "|"),
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

    scores: Optional[dict[str, ExactOrRangeArgument[int]]] = extra_field(
        default_factory=dict
    )
    tags: Optional[set[NegatableArgument[str]]] = extra_field(default_factory=set)
    teams: Optional[set[NegatableArgument[str]]] = extra_field(default_factory=set)

    names: Optional[set[NegatableArgument[str]]] = extra_field(default_factory=set)
    types: Optional[set[NegatableArgument[str]]] = extra_field(default_factory=set)
    predicates: Optional[set[NegatableArgument[str]]] = extra_field(default_factory=set)

    nbts: Optional[list[NegatableArgument[Compound]]] = extra_field(
        default_factory=list
    )

    level: Optional[ExactOrRangeArgument[int]] = extra_field(default=None)
    gamemodes: Optional[set[NegatableArgument[str]]] = extra_field(default_factory=set)
    advancements: Optional[dict[str, bool | dict[str, bool]]] = extra_field(
        default_factory=dict
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

    def _toggle_value(
        self, value: T, state: bool | None, values: set[NegatableArgument[T]]
    ) -> "Selector":
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

    def advancement(
        self, advancement: str, state: bool | dict[str, bool | None] | None
    ) -> "Selector":
        if state is None:
            if advancement in self.advancements:
                del self.advancements[advancement]
            return self

        if not (cur_value := self.advancements.get(advancement)) or (
            isinstance(state, bool) or isinstance(cur_value, bool)
        ):
            self.advancements[advancement] = state
            return self

        for criteria, new_state in state.items():
            if new_state is None:
                del cur_value[criteria]
            else:
                cur_value[criteria] = new_state

        return self

    def limit_to(self, limit: int | None) -> "Selector":
        self.limit = limit
        return self

    def sorted_by(self, sort: str | None) -> "Selector":
        self.sort = sort
        return self

    @property
    def single_target(self) -> bool:
        return self.variable == "n" or self.variable == "s" or self.limit == 1

    def __or__(self, other: Any):
        if not isinstance(other, Selector):
            raise ValueError(f"Cannot '|' between Selector and {type(other).__name__}")

        if self.variable != other.variable and not (
            self.variable == "s" or other.variable == "s"
        ):
            raise ValueError(
                f"Cannot '|' between @{self.variable} and @{other.variable}"
            )

        new_variable = self.variable if self.variable != "s" else other.variable

        new_selector = Selector(new_variable)

        for field in fields(self):
            if field.name == "variable":
                continue

            a = getattr(self, field.name)
            b = getattr(other, field.name)

            if a is not None and b is not None:
                setattr(new_selector, field.name, FIELD_UNION[field.name](a, b))
            else:
                setattr(new_selector, field.name, a or b)

        return new_selector
