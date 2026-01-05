# log21.TreePrint.py
# CodeWriter21

from __future__ import annotations

from typing import (List as _List, Union as _Union, Mapping as _Mapping,
                    Optional as _Optional, Sequence as _Sequence)

from log21.Colors import get_colors as _gc


class TreePrint:
    """A class to help you print objects in a tree-like format."""

    class Node:
        """A class to represent a node in a tree."""

        def __init__(
            self,
            value: _Union[str, int],
            children: _Optional[_List[TreePrint.Node]] = None,
            indent: int = 4,
            colors: _Optional[_Mapping[str, str]] = None,
            mode: str = '-'
        ):
            """Initialize a node.

            :param value: The value of the node.
            :param children: The children of the node.
            :param indent: Number of spaces to indent the node.
            :param colors: Colors to use for the node.
            :param mode: Choose between '-' and '='.
            """
            self.value = str(value)
            if children:
                self._children = children
            else:
                self._children = []
            self.indent = indent
            self.colors = {
                'branches': _gc('Green'),
                'fruit': _gc('LightMagenta'),
            }

            if colors:
                for key, value_ in colors.items():
                    if key in self.colors:
                        self.colors[key] = _gc(value_)
            if not mode:
                self.mode = 1
            else:
                self.mode = self._get_mode(mode)
                if self.mode == -1:
                    raise ValueError('`mode` must be - or =')

        def _get_mode(self, mode: _Optional[_Union[str, int]] = None) -> int:
            if not mode:
                mode = self.mode
            if isinstance(mode, int):
                if mode in [1, 2]:
                    return mode
            elif isinstance(mode, str):
                if mode in '-_─┌│|└┬├└':
                    return 1
                if mode in '=═╔║╠╚╦╚':
                    return 2
            return -1

        def __str__(self, level=0, prefix='', mode=None):
            mode = self._get_mode(mode)
            if mode == -1:
                raise ValueError('`mode` must be - or =')
            chars = '─┌│└┬├└'
            if mode == 2:
                chars = '═╔║╚╦╠╚'

            text = _gc(self.colors['branches']) + prefix
            if level == 0:
                text += chars[0]  # ─ OR ═
                prefix += ' '

            if self.has_child():
                text += chars[4]  # ┬ OR ╦
            else:
                text += chars[0]  # ─ OR ═

            text += ' ' + _gc(self.colors['fruit']) + str(self.value) + '\n'

            for i, child in enumerate(self._children):
                prefix_ = ''
                for part in prefix:
                    if part in '┌│├┬╔║╠╦':
                        prefix_ += chars[2]  # │ OR ║
                    elif part in chars:
                        prefix_ += ' '
                    else:
                        prefix_ += part

                if i + 1 == len(self._children):
                    prefix_ += chars[6]  # └ OR ╚
                else:
                    prefix_ += chars[5]  # ├ OR ╠
                prefix_ += chars[0] * (self.indent - 1)  # ─ OR ═
                prefix_ = prefix_[:len(prefix)] + _gc(self.colors['branches']
                                                      ) + prefix_[len(prefix):]
                text += child.__str__(level=level + 1, prefix=prefix_, mode=mode)

            return text

        def has_child(self):
            """Return True if node has children, False otherwise."""
            return len(self._children) > 0

        def add_child(self, child: TreePrint.Node):
            """Add a child to the node."""
            if not isinstance(child, TreePrint.Node):
                raise TypeError('`child` must be TreePrint.Node')
            self._children.append(child)

        def get_child(self, value: _Optional[str] = None, index: _Optional[int] = None):
            """Get a child by value or index."""
            if value and index:
                raise ValueError('`value` and `index` can not be both set')
            if not value and not index:
                raise ValueError('`value` or `index` must be set')
            if value:
                for child in self._children:
                    if child.value == value:
                        return child
            if index:
                return self._children[index]
            raise ValueError(f'Failed to find child: {value = }, {index = }')

        def add_to(
            self: TreePrint.Node,
            data: _Union[_Mapping, _Sequence, str, int],
            indent: int = 4,
            colors: _Optional[_Mapping[str, str]] = None,
            mode='-'
        ):  # pylint: disable=too-many-branches
            """Add data to the node."""
            if isinstance(data, _Mapping):
                if len(data) == 1:
                    child = TreePrint.Node(
                        list(data.keys())[0], indent=indent, colors=colors, mode=mode
                    )
                    child.add_to(
                        list(data.values())[0], indent=indent, colors=colors, mode=mode
                    )
                    self.add_child(child)
                else:
                    for key, value in data.items():
                        child = TreePrint.Node(
                            key, indent=indent, colors=colors, mode=mode
                        )
                        child.add_to(value, indent=indent, colors=colors, mode=mode)
                        self.add_child(child)
            elif isinstance(data, _Sequence) and not isinstance(data, str):
                if len(data) == 1:
                    self.add_child(
                        TreePrint.Node(
                            data[0], indent=indent, colors=colors, mode=mode
                        )
                    )
                else:
                    for value in data:
                        if isinstance(value, _Mapping):
                            for key, dict_value in value.items():
                                child = TreePrint.Node(
                                    key, indent=indent, colors=colors, mode=mode
                                )
                                child.add_to(
                                    dict_value, indent=indent, colors=colors, mode=mode
                                )
                                self.add_child(child)
                        elif isinstance(value, _Sequence):
                            child = TreePrint.Node(
                                '>', indent=indent, colors=colors, mode=mode
                            )
                            child.add_to(value, indent=indent, colors=colors, mode=mode)
                            self.add_child(child)
                        else:
                            child = TreePrint.Node(
                                str(value), indent=indent, colors=colors, mode=mode
                            )
                            self.add_child(child)
            else:
                child = TreePrint.Node(
                    str(data), indent=indent, colors=colors, mode=mode
                )
                self.add_child(child)

    def __init__(
        self,
        data: _Union[_Mapping, _Sequence, str, int],
        indent: int = 4,
        colors: _Optional[_Mapping[str, str]] = None,
        mode='-'
    ):
        self.indent = indent
        self.mode = mode
        if isinstance(data, _Mapping):
            if len(data) == 1:
                self.root = self.Node(
                    list(data.keys())[0], indent=indent, colors=colors
                )
                self.add_to_root(list(data.values()), colors=colors)
            else:
                self.root = self.Node('root', indent=indent, colors=colors)
                self.add_to_root(data, colors=colors)
        elif isinstance(data, _Sequence):
            self.root = self.Node('root', indent=indent, colors=colors)
            self.add_to_root(data, colors=colors)
        else:
            self.root = self.Node(str(data), indent=indent, colors=colors)

    def add_to_root(
        self,
        data: _Union[_Mapping, _Sequence, str, int],
        colors: _Optional[_Mapping[str, str]] = None
    ):
        """Add data to root node."""
        self.root.add_to(data, indent=self.indent, colors=colors, mode=self.mode)

    def __str__(self, mode=None):
        if not mode:
            mode = self.mode
        return self.root.__str__(mode=mode)


def tree_format(
    data: _Union[_Mapping, _Sequence, str, int],
    indent: int = 4,
    mode='-',
    colors: _Optional[_Mapping[str, str]] = None
) -> str:
    """Return a tree representation of data.

    :param data: data to be represented as a tree (dict, list, str, int)
    :param indent: number of spaces to indent each level of the tree
    :param mode: mode of tree representation ('-', '=')
    :param colors: colors to use for each level of the tree
    :return: tree representation of data
    """
    return str(TreePrint(data, indent=indent, colors=colors, mode=mode))
