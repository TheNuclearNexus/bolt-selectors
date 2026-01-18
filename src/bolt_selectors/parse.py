from dataclasses import fields
from functools import partial
from mecha import AstNode, AstSelector, AstSelectorArgument, AstString
from tokenstream import set_location
from .selector import Selector
from .types import ExactOrRangeArgument
from mecha import (
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
)
from mecha.ast import (
    AstChildren,
    AstNode,
    AstRange,
    AstSelector,
    AstSelectorArgument,
    AstSelectorAdvancements,
)


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


def parse_range(range: AstRange, _: bool = False):
    if range.exact:
        return range.min

    return (range.min, range.max)


def parse_exact(node: AstNode, _: bool = False):
    if hasattr(node, "value"):
        return getattr(node, "value")
    elif isinstance(node, AstResourceLocation):
        return node.get_value()
    elif isinstance(node, AstNbtCompound):
        return node.evaluate()

    return None


def parse_scores(value: AstSelectorScores, _: bool = False):
    new_value = {}
    for score in value.scores:
        new_value[score.key.value] = parse_range(score.value)
    return new_value


def parse_advancements(value: AstSelectorAdvancements, _: bool = False):
    new_value = {}
    for advancement in value.advancements:
        path = advancement.key.get_value()

        if isinstance(advancement.value, AstBool):
            new_value[path] = advancement.value.value
        else:
            new_value[path] = {n.key.value: n.value.value for n in advancement.value}

    return new_value


def parse_list_arg(value: AstNode, inverted: bool, factory=set):
    return factory([(inverted, parse_exact(value))])


FIELD_TO_AST = {
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

AST_TO_FIELD = {
    "x": parse_exact,
    "y": parse_exact,
    "z": parse_exact,
    "distance": parse_range,
    "dx": parse_exact,
    "dy": parse_exact,
    "dz": parse_exact,
    "x_rotation": parse_range,
    "y_rotation": parse_range,
    "scores": parse_scores,
    "tag": parse_list_arg,
    "team": parse_list_arg,
    "name": parse_list_arg,
    "type": parse_list_arg,
    "predicate": parse_list_arg,
    "nbt": partial(parse_list_arg, factory=list),
    "level": parse_range,
    "gamemode": parse_list_arg,
    "advancements": parse_advancements,
    "limit": parse_exact,
    "sort": parse_exact,
}


def selector_to_ast(selector: "Selector", node: AstNode):
    args = []

    for field in fields(selector):
        if (
            field_value := getattr(selector, field.name)
        ) is None or field.name == "variable":
            continue

        factory = FIELD_TO_AST[field.name]

        if isinstance(field_value, set):
            field_value = sorted(list(field_value), key=lambda e: e[1])

        if isinstance(field_value, list):
            for entry in field_value:
                args.append(selector_arg(field.name[:-1], factory(entry[1]), entry[0]))
        elif not isinstance(field_value, dict) or len(field_value.keys()) > 1:
            args.append(selector_arg(field.name, factory(field_value)))

    return set_location(
        AstSelector(variable=selector.variable, arguments=args),
        node.location,
        node.end_location,
    )


def ast_to_selector(selector: AstSelector):
    arguments = {}

    for argument in selector.arguments:
        key = argument.key.value

        converter = AST_TO_FIELD[key]

        value = converter(argument.value, argument.inverted)

        if value is None:
            continue

        # Map single names to their plural versions
        if isinstance(value, set) or isinstance(value, list):
            key += "s"

        # Combine matching arguments, overide single values
        if key in arguments and isinstance(arguments[key], set):
            arguments[key] = arguments[key].union(value)
        elif key in arguments and isinstance(arguments[key], list):
            arguments[key] += value
        else:
            arguments[key] = value

    return Selector(selector.variable, **arguments)
