from dataclasses import dataclass
from typing import Any, Callable, Generator, Optional
from beet import Context
from mecha import AlternativeParser, AstNode, AstSelector, Mecha, Parser, Visitor, rule
from bolt import Accumulator, Runtime, visit_generic

from bolt import InterpolationParser, Runtime

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


@dataclass(frozen=True, slots=True)
class AstSelectorLiteral(AstSelector): ...


@dataclass
class SelectorParser:

    literal_parser: Parser
    selector_parser: Parser

    def __call__(self, stream: TokenStream):
        with stream.checkpoint() as commit:
            # Try to parse literal as a selector
            node: AstSelector = self.selector_parser(stream)

            commit()
            return set_location(
                AstSelectorLiteral(variable=node.variable, arguments=node.arguments),
                node,
            )

        return self.literal_parser(stream)


class SelectorCodegen(Visitor):
    @rule(AstSelectorLiteral)
    def literal_selector(
        self, node: AstSelectorLiteral, acc: Accumulator
    ) -> Generator[AstNode, Optional[List[str]], Optional[List[str]]]:
        # This takes the AstSelectorLiteral node, generates all the code
        # for interpolating the arguments, then returns the name of
        # the variable holding the interpolated AstSelectorLiteral object
        result = yield from visit_generic(node, acc)

        # Just use the original node if there are no interpolations
        if result is None:
            result = acc.make_ref(node)

        # Generates the code for calling the function that converts
        # the ast node into a Selector object
        result = acc.helper("ast_to_selector", result)

        # Returns the Selector object
        return [result]


def beet_default(ctx: Context):
    mc = ctx.inject(Mecha)
    runtime = ctx.inject(Runtime)

    # Override the bolt:literal parser to enable selectors
    mc.spec.parsers["bolt:literal"] = SelectorParser(
        literal_parser=mc.spec.parsers["bolt:literal"],
        selector_parser=mc.spec.parsers["selector"],
    )

    # Enable interpolation for selectors
    mc.spec.parsers["selector"] = AlternativeParser(
        [mc.spec.parsers["selector"], InterpolationParser("selector")]
    )

    # Extends codegen to generate Selector objects from the ast
    runtime.modules.codegen.extend(SelectorCodegen())
    runtime.helpers["ast_to_selector"] = ast_to_selector

    # Patch entity interpolation to support handling Selector objects
    runtime.helpers["interpolate_entity"] = SelectorConverter(
        runtime.helpers["interpolate_entity"]
    )
