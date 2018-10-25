# -*- coding: utf-8 -*-

from collections import OrderedDict

from ipywidgets import Widget, Tab


class ExtendedTab(Tab):
    """
    A Tab subclass that allows to add/access/select/replace/remove children by name.

    There can be only one tab for any given name.

    Example:

        import time
        t = ExtendedTab([])
        t.add_child_named(Text('Some text'), 'A')
        t.selected_index = 0
        time.sleep(1)
        t.get_child_named('A').value = 'Some real text'
        time.sleep(1)
        t.replace_child_named('A', Button())
        t.selected_index = 0
        time.sleep(1)
        t.remove_child_named('A')
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.children_dict = OrderedDict()
        if 'selected_index' in kwargs:
            selected_index = kwargs['selected_index']
            self.selected_index = selected_index
        if 'titles' in kwargs:
            num_titles = len(titles)
            for i, child in enumerate(self.children):
                self.children_dict[titles[i]] = child
                if i >= num_titles:
                    break
                self.set_title(i, titles[i])

    def add_child_named(self, child: Widget, name: str) -> None:
        "Add a new child widget under some name to the compound one."

        self.children_dict[name] = child
        self.children = tuple(self.children_dict.values())
        self.set_title(len(self.children) - 1, name)

    def get_child_named(self, name: str) -> Widget:
        "Get child widget with given name."

        return self.children_dict[name]

    def remove_child_named(self, name: str) -> None:
        "Remove a child widget with some name from the compound one."

        titles = self.children_dict.keys()
        if name not in titles:
            return
        del self.children_dict[name]
        self.children = tuple(self.children_dict.values())
        for i, title in enumerate(self.children_dict.keys()):
            self.set_title(i, title)

    def select_child_named(self, name: str) -> None:
        "Select the one child widget with given name."

        for i, n in enumerate(self.children_dict):
            if n == name:
                self.selected_index = i
                break

    def replace_child_named(self, name: str, child: Widget) -> None:
        "Replace a child widget with some name in the compound one."

        self.children_dict[name] = child
        self.children = tuple(self.children_dict.values())
