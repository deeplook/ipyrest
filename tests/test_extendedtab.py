from ipywidgets import Text, Button

from ipyrest.extendedtab import ExtendedTab


def test_extended_tab():
    "Test ExtendedTab class."

    t = ExtendedTab([])

    key, val = 'A', 'Foo'
    t.add_child_named(Text(val), key)
    assert t.children[0].value == val
    assert t.children_dict[key].value == val

    val1 = t.get_child_named(key).value
    assert val1 == val

    val2 = 'Click'
    t.replace_child_named(key, Button(description=val2))
    assert t.children[0].description == val2

    t.remove_child_named(key)
    assert len(t.children) == 0
    assert len(t.children_dict) == 0
