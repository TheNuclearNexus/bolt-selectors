from typing import TypeVar


T = TypeVar("T")
N = TypeVar("N", int, float)
ExactOrRangeArgument = N | tuple[N | None, N | None]
NegatableArgument = tuple[bool, T]
