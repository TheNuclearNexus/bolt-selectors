from bolt_selectors.selector import Selector


def test_create_selector():
    _selector = Selector("a")


def test_chaining_selector():
    _selector = Selector("a").type("zombie").sorted_by("nearest").limit_to(1)
