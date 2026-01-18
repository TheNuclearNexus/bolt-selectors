from bolt_selectors.selector import Selector


def test_create_selector():
    selector = Selector("a")


def test_chaining_selector():
    selector = Selector("a").type("zombie").sorted_by("nearest").limit_to(1)
