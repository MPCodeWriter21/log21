# log21.TreePrint.py
# CodeWriter21

from typing import Union as _Union

from log21.Colors import get_colors as _gc


class TreePrint:
    class Node:
        colors = {
            'branches': _gc('Green'),
            'fruit': _gc('LightMagenta'),
        }

        def __init__(self, value: _Union[str, int], children: list = None, indent: int = 4, colors: dict = None,
                     mode='-'):
            self.value = str(value)
            if children:
                self._children = children
            else:
                self._children = []
            self.indent = indent
            self.colors = self.colors.copy()
            if colors:
                for key, value in colors.items():
                    if key in self.colors:
                        self.colors[key] = _gc(value)
            if not mode:
                self.mode = 1
            else:
                self.mode = self._get_mode(mode)
                if self.mode == -1:
                    raise ValueError('`mode` must be - or =')

        def _get_mode(self, mode=None) -> int:
            if not mode:
                mode = self.mode
            if isinstance(mode, int):
                if mode in [1, 2]:
                    return mode
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
                for j in range(len(prefix)):
                    if prefix[j] in '┌│├┬╔║╠╦':
                        prefix_ += chars[2]  # │ OR ║
                    elif prefix[j] in chars:
                        prefix_ += ' '
                    else:
                        prefix_ += prefix[j]

                if i + 1 == len(self._children):
                    prefix_ += chars[6]  # └ OR ╚
                else:
                    prefix_ += chars[5]  # ├ OR ╠
                prefix_ += chars[0] * (self.indent - 1)  # ─ OR ═
                prefix_ = prefix_[:len(prefix)] + _gc(self.colors['branches']) + prefix_[len(prefix):]
                text += child.__str__(level=level + 1, prefix=prefix_, mode=mode)

            return text

        def has_child(self):
            return len(self._children) > 0

        def add_child(self, child: 'TreePrint.Node'):
            if not isinstance(child, TreePrint.Node):
                raise TypeError('`child` must be TreePrint.Node')
            self._children.append(child)

        def get_child(self, value: str = None, index: int = None):
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

        @staticmethod
        def add_to(node: 'TreePrint.Node', data: _Union[dict, list, str, int], indent: int = 4, colors: dict = None,
                   mode='-'):
            if isinstance(data, dict):
                if len(data) == 1:
                    child = TreePrint.Node(list(data.keys())[0], indent=indent, colors=colors, mode=mode)
                    TreePrint.Node.add_to(child, list(data.values())[0], indent=indent, colors=colors, mode=mode)
                    node.add_child(child)
                else:
                    for key, value in data.items():
                        child = TreePrint.Node(key, indent=indent, colors=colors, mode=mode)
                        TreePrint.Node.add_to(child, value, indent=indent, colors=colors, mode=mode)
                        node.add_child(child)
            elif isinstance(data, list):
                for value in data:
                    if isinstance(value, dict):
                        for key, dict_value in value.items():
                            child = TreePrint.Node(key, indent=indent, colors=colors, mode=mode)
                            TreePrint.Node.add_to(child, dict_value, indent=indent, colors=colors, mode=mode)
                            node.add_child(child)
                    elif isinstance(value, list):
                        child = TreePrint.Node('>', indent=indent, colors=colors, mode=mode)
                        TreePrint.Node.add_to(child, value, indent=indent, colors=colors, mode=mode)
                        node.add_child(child)
                    else:
                        child = TreePrint.Node(str(value), indent=indent, colors=colors, mode=mode)
                        node.add_child(child)
            else:
                child = TreePrint.Node(str(data), indent=indent, colors=colors, mode=mode)
                node.add_child(child)

    def __init__(self, data: _Union[dict, list, str, int], indent: int = 4, colors: dict = None, mode='-'):
        self.indent = indent
        self.mode = mode
        if isinstance(data, dict):
            if len(data) == 1:
                self.root = self.Node(list(data.keys())[0], indent=indent, colors=colors)
                self.add_to_root(list(data.values()), colors=colors)
            else:
                self.root = self.Node('root', indent=indent, colors=colors)
                self.add_to_root(data, colors=colors)
        elif isinstance(data, list):
            self.root = self.Node('root', indent=indent, colors=colors)
            self.add_to_root(data, colors=colors)
        else:
            self.root = self.Node(str(data), indent=indent, colors=colors)

    def add_to_root(self, data: _Union[dict, list, str, int], colors: dict = None):
        self.Node.add_to(self.root, data, indent=self.indent, colors=colors, mode=self.mode)

    def __str__(self, mode=None):
        if not mode:
            mode = self.mode
        return self.root.__str__(mode=mode)


def tree_format(data: _Union[dict, list, str, int], indent: int = 4, mode='-', colors: dict = None):
    return str(TreePrint(data, indent=indent, colors=colors, mode=mode))
