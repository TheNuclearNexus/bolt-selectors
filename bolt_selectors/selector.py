from dataclasses import dataclass
from typing import Optional
from beet.core.utils import extra_field
from nbtlib import Compound

from .types import ExactOrRangeArgument, NegatableArgument, T, N

__all__ = ["Selector"]


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
