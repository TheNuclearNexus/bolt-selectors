from dataclasses import dataclass
from typing import Any, Callable
from beet import Context
from mecha import AlternativeParser, AstNode, AstSelector, Mecha, Parser
from bolt import Runtime

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
from tokenstream import TokenStream, set_location

from bolt_selectors.parse import ast_to_selector, selector_to_ast
from bolt_selectors.selector import Selector

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

__all__ = ["SelectorConverter", "SelectorParser", "beet_default"]


@dataclass
class SelectorConverter:
    base_converter: Callable[[Any, AstNode], AstNode]

    def __call__(self, obj: Any, node: AstNode) -> AstNode:
        if isinstance(obj, Selector):
            return selector_to_ast(obj, node)

        return self.base_converter(obj, node)


@dataclass
class SelectorParser:

    literal_parser: Parser
    selector_parser: Parser

    def __call__(self, stream: TokenStream):
        with stream.checkpoint() as commit:
            # Try to parse literal as a selector
            node: AstSelector = self.selector_parser(stream)

            # If it was successful, convert to a Selector object
            selector = ast_to_selector(node)

            commit()
            return set_location(AstValue(value=selector), stream.current)
        return self.literal_parser(stream)


def beet_default(ctx: Context):
    mc = ctx.inject(Mecha)
    runtime = ctx.inject(Runtime)

    # Make Selector and NBT types globally available due to limitations with AstValue
    runtime.globals.update({"Selector": Selector})
    runtime.globals.update({t.__name__: t for t in NBT_GLOBALS})

    # Override the bolt:literal parser to enable selectors
    mc.spec.parsers["bolt:literal"] = SelectorParser(
        literal_parser=mc.spec.parsers["bolt:literal"],
        selector_parser=mc.spec.parsers["selector"],
    )

    # Enable interpolation for selectors
    mc.spec.parsers["selector"] = AlternativeParser(
        [mc.spec.parsers["selector"], InterpolationParser("selector")]
    )

    # Patch entity interpolation to support handling Selector objects
    runtime.helpers["interpolate_entity"] = SelectorConverter(
        runtime.helpers["interpolate_entity"]
    )
