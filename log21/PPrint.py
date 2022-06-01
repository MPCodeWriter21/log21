# log21.PPrint.py
# CodeWriter21

import re as _re
import sys as _sys
import types as _types
import collections as _collections
import dataclasses as _dataclasses

from typing import Dict as _Dict, Union as _Union
from pprint import PrettyPrinter as _PrettyPrinter

from log21.Colors import get_colors as _gc

_builtin_scalars = frozenset({str, bytes, bytearray, float, complex, bool, type(None)})


def _recursion(obj):
    return f"<Recursion on {type(obj).__name__} with id={id(obj)}>"


def _safe_tuple(t):
    """Helper function for comparing 2-tuples"""
    return _SafeKey(t[0]), _SafeKey(t[1])


def _wrap_bytes_repr(obj, width, allowance):
    current = b''
    last = len(obj) // 4 * 4
    for i in range(0, len(obj), 4):
        part = obj[i: i + 4]
        candidate = current + part
        if i == last:
            width -= allowance
        if len(repr(candidate)) > width:
            if current:
                yield repr(current)
            current = part
        else:
            current = candidate
    if current:
        yield repr(current)


class _SafeKey:
    """Helper function for key functions when sorting unorderable objects.

    The wrapped-object will fallback to a Py2.x style comparison for
    unorderable types (sorting first comparing the type name and then by
    the obj ids).  Does not work recursively, so dict.items() must have
    _safe_key applied to both the key and the value.

    """

    __slots__ = ['obj']

    def __init__(self, obj):
        self.obj = obj

    def __lt__(self, other):
        try:
            return self.obj < other.obj
        except TypeError:
            return (str(type(self.obj)), id(self.obj)) < (str(type(other.obj)), id(other.obj))


class PrettyPrinter(_PrettyPrinter):
    signs_colors: _Dict[str, str] = {
        'square-brackets': _gc('LightCyan'),
        'curly-braces': _gc('LightBlue'),
        'parenthesis': _gc('LightGreen'),
        'comma': _gc('LightRed'),
        'colon': _gc('LightRed'),
        '...': _gc('LightMagenta'),
        'data': _gc('Green')
    }

    def __init__(self, indent=1, width=80, depth=None, stream=None, signs_colors: _Dict[str, str] = None, *,
                 compact=False, sort_dicts=True, underscore_numbers=False):
        super().__init__(indent=indent, width=width, depth=depth, stream=stream, compact=compact,
                         sort_dicts=sort_dicts, underscore_numbers=underscore_numbers)
        self._depth = depth
        self._indent_per_level = indent
        self._width = width
        if stream is not None:
            self._stream = stream
        else:
            self._stream = _sys.stdout
        self._compact = bool(compact)
        self._sort_dicts = sort_dicts
        self._underscore_numbers = underscore_numbers
        if signs_colors:
            for sign, color in signs_colors.items():
                self.signs_colors[sign.lower()] = _gc(color)

    def _format(self, obj, stream, indent, allowance, context, level):
        objid = id(obj)
        if objid in context:
            stream.write(_recursion(obj))
            self._recursive = True
            self._readable = False
            return
        rep = self._repr(obj, context, level)
        max_width = self._width - indent - allowance
        if len(rep) > max_width:
            p = self._dispatch.get(type(obj).__repr__, None)
            if p is not None:
                context[objid] = 1
                p(self, obj, stream, indent, allowance, context, level + 1)
                del context[objid]
                return
            elif (_dataclasses.is_dataclass(obj) and
                  not isinstance(obj, type) and
                  obj.__dataclass_params__.repr and
                  # Check dataclass has generated repr method.
                  hasattr(obj.__repr__, "__wrapped__") and
                  "__create_fn__" in obj.__repr__.__wrapped__.__qualname__):
                context[objid] = 1
                self._pprint_dataclass(obj, stream, indent, allowance, context, level + 1)
                del context[objid]
                return
        stream.write(rep)

    def _pprint_dataclass(self, obj, stream, indent, allowance, context, level):
        cls_name = obj.__class__.__name__
        indent += len(cls_name) + 1
        items = [(f.name, getattr(obj, f.name)) for f in _dataclasses.fields(obj) if f.repr]
        stream.write(cls_name + '(')
        self._format_namespace_items(items, stream, indent, allowance, context, level)
        stream.write(')')

    def _repr(self, obj, context, level):
        repr, readable, recursive = self.format(obj, context.copy(),
                                                self._depth, level)
        if not readable:
            self._readable = False
        if recursive:
            self._recursive = True
        return repr

    def _safe_repr(self, object_, context, max_levels, level):
        # Return triple (repr_string, isreadable, isrecursive).
        type_ = type(object_)
        if type_ in _builtin_scalars:
            return repr(object_), True, False

        representation = getattr(type_, "__repr__", None)

        if issubclass(type_, int) and representation is int.__repr__:
            if self._underscore_numbers:
                return f"{object_:_d}", True, False
            else:
                return repr(object_), True, False

        if issubclass(type_, dict) and representation is dict.__repr__:
            if not object_:
                return self.signs_colors.get('curly-braces') + "{}" + self.signs_colors.get('data'), True, False
            object_id = id(object_)
            if max_levels and level >= max_levels:
                return self.signs_colors.get('curly-braces') + "{" + self.signs_colors.get('...') + "..." + \
                       self.signs_colors.get('curly-braces') + "}" + self.signs_colors.get('data'), \
                       False, object_id in context
            if object_id in context:
                return _recursion(object_), False, True
            context[object_id] = 1
            readable = True
            recursive = False
            components = []
            append = components.append
            level += 1
            if self._sort_dicts:
                items = sorted(object_.items(), key=_safe_tuple)
            else:
                items = object_.items()
            for k, v in items:
                krepr, kreadable, krecur = self.format(k, context, max_levels, level)
                vrepr, vreadable, vrecur = self.format(v, context, max_levels, level)
                append(f"{krepr}{self.signs_colors.get('colon')}:{self.signs_colors.get('data')} {vrepr}")
                readable = readable and kreadable and vreadable
                if krecur or vrecur:
                    recursive = True
            del context[object_id]
            return self.signs_colors.get('curly-braces') + "{" + self.signs_colors.get('data') + \
                   (self.signs_colors.get('comma') + ", " + self.signs_colors.get('data')).join(components) + \
                   self.signs_colors.get('data'), readable, recursive

        if (issubclass(type_, list) and representation is list.__repr__) or \
                (issubclass(type_, tuple) and representation is tuple.__repr__):
            if issubclass(type_, list):
                if not object_:
                    return self.signs_colors.get('square-brackets') + "[]" + self.signs_colors.get('data'), True, False
                format_ = self.signs_colors.get('square-brackets') + "[" + self.signs_colors.get('data') + "%s" + \
                          self.signs_colors.get('square-brackets') + "]" + self.signs_colors.get('data')
            elif len(object_) == 1:
                format_ = self.signs_colors.get('parenthesis') + "(" + self.signs_colors.get('data') + "%s" + \
                          self.signs_colors.get('comma') + "," + self.signs_colors.get('parenthesis') + ")" + \
                          self.signs_colors.get('data')
            else:
                if not object_:
                    return self.signs_colors.get('parenthesis') + "()" + self.signs_colors.get('data'), True, False
                format_ = self.signs_colors.get('parenthesis') + "(" + self.signs_colors.get('data') + "%s" + \
                          self.signs_colors.get('parenthesis') + ")" + self.signs_colors.get('data')
            object_id = id(object_)
            if max_levels and level >= max_levels:
                return format_ % self.signs_colors.get('...') + "...", False, object_id in context
            if object_id in context:
                return _recursion(object_), False, True
            context[object_id] = 1
            readable = True
            recursive = False
            components = []
            append = components.append
            level += 1
            for o in object_:
                orepr, oreadable, orecur = self.format(o, context, max_levels, level)
                append(orepr)
                if not oreadable:
                    readable = False
                if orecur:
                    recursive = True
            del context[object_id]
            return format_ % (self.signs_colors.get('comma') + ", " + self.signs_colors.get('data')).join(components), \
                   readable, recursive

        rep = repr(object_)
        return rep, (rep and not rep.startswith('<')), False

    _dispatch = {}

    def _pprint_dict(self, obj, stream, indent, allowance, context, level):
        write = stream.write
        write(self.signs_colors.get('curly-braces') + '{' + self.signs_colors.get('data'))
        if self._indent_per_level > 1:
            write((self._indent_per_level - 1) * ' ')
        length = len(obj)
        if length:
            if self._sort_dicts:
                items = sorted(obj.items(), key=_safe_tuple)
            else:
                items = obj.items()
            self._format_dict_items(items, stream, indent, allowance + 1,
                                    context, level)
        write(self.signs_colors.get('curly-braces') + '}' + self.signs_colors.get('data'))

    _dispatch[dict.__repr__] = _pprint_dict

    def _pprint_ordered_dict(self, obj, stream, indent, allowance, context, level):
        if not len(obj):
            stream.write(repr(obj))
            return
        cls = obj.__class__
        stream.write(cls.__name__ + self.signs_colors.get('parenthesis') + '(' + self.signs_colors.get('data'))
        self._format(list(obj.items()), stream,
                     indent + len(cls.__name__) + 1, allowance + 1,
                     context, level)
        stream.write(self.signs_colors.get('parenthesis') + ')' + self.signs_colors.get('data'))

    _dispatch[_collections.OrderedDict.__repr__] = _pprint_ordered_dict

    def _pprint_list(self, obj, stream, indent, allowance, context, level):
        stream.write(self.signs_colors.get('square-brackets') + '[' + self.signs_colors.get('data'))
        self._format_items(obj, stream, indent, allowance + 1,
                           context, level)
        stream.write(self.signs_colors.get('square-brackets') + ']' + self.signs_colors.get('data'))

    _dispatch[list.__repr__] = _pprint_list

    def _pprint_tuple(self, obj, stream, indent, allowance, context, level):
        stream.write(self.signs_colors.get('parenthesis') + '(' + self.signs_colors.get('data'))
        endchar = self.signs_colors.get('comma') + ',' + self.signs_colors.get('parenthesis') + ')' + \
                  self.signs_colors.get('data') if len(obj) == 1 else self.signs_colors.get('parenthesis') + ')' + \
                                                                      self.signs_colors.get('data')
        self._format_items(obj, stream, indent, allowance + len(endchar),
                           context, level)
        stream.write(endchar)

    _dispatch[tuple.__repr__] = _pprint_tuple

    def _pprint_set(self, obj, stream, indent, allowance, context, level):
        if not len(obj):
            stream.write(repr(obj))
            return
        typ = obj.__class__
        if typ is set:
            stream.write(self.signs_colors.get('curly-braces') + '{' + self.signs_colors.get('data'))
            endchar = self.signs_colors.get('curly-braces') + '}' + self.signs_colors.get('data')
        else:
            stream.write(typ.__name__ + self.signs_colors.get('parenthesis') + '(' +
                         self.signs_colors.get('curly-braces') + '{' + self.signs_colors.get('data'))
            endchar = self.signs_colors.get('curly-braces') + '}' + self.signs_colors.get('parenthesis') + ')' \
                      + self.signs_colors.get('data')
            indent += len(typ.__name__) + 1
        obj = sorted(obj, key=_SafeKey)
        self._format_items(obj, stream, indent, allowance + len(endchar),
                           context, level)
        stream.write(endchar)

    _dispatch[set.__repr__] = _pprint_set
    _dispatch[frozenset.__repr__] = _pprint_set

    def _pprint_str(self, object_, stream, indent, allowance, context, level):
        write = stream.write
        if not len(object_):
            write(repr(object_))
            return
        chunks = []
        lines = object_.splitlines(True)
        if level == 1:
            indent += 1
            allowance += 1
        max_width1 = max_width = self._width - indent
        representation = ''
        for i, line in enumerate(lines):
            representation = repr(line)
            if i == len(lines) - 1:
                max_width1 -= allowance
            if len(representation) <= max_width1:
                chunks.append(representation)
            else:
                # A list of alternating (non-space, space) strings
                parts = _re.findall(r'\S*\s*', line)
                assert parts
                assert not parts[-1]
                parts.pop()  # drop empty last part
                max_width2 = max_width
                current = ''
                for j, part in enumerate(parts):
                    candidate = current + part
                    if j == len(parts) - 1 and i == len(lines) - 1:
                        max_width2 -= allowance
                    if len(repr(candidate)) > max_width2:
                        if current:
                            chunks.append(repr(current))
                        current = part
                    else:
                        current = candidate
                if current:
                    chunks.append(repr(current))
        if len(chunks) == 1:
            write(representation)
            return
        if level == 1:
            write(self.signs_colors.get('parenthesis') + '(' + self.signs_colors.get('data'))
        for i, representation in enumerate(chunks):
            if i > 0:
                write('\n' + ' ' * indent)
            write(representation)
        if level == 1:
            write(self.signs_colors.get('parenthesis') + ')' + self.signs_colors.get('data'))

    _dispatch[str.__repr__] = _pprint_str

    def _pprint_bytes(self, obj, stream, indent, allowance, context, level):
        write = stream.write
        if len(obj) <= 4:
            write(repr(obj))
            return
        parens = level == 1
        if parens:
            indent += 1
            allowance += 1
            write(self.signs_colors.get('parenthesis') + '(' + self.signs_colors.get('data'))
        delim = ''
        for rep in _wrap_bytes_repr(obj, self._width - indent, allowance):
            write(delim)
            write(rep)
            if not delim:
                delim = '\n' + ' ' * indent
        if parens:
            write(self.signs_colors.get('parenthesis') + ')' + self.signs_colors.get('data'))

    _dispatch[bytes.__repr__] = _pprint_bytes

    def _pprint_bytearray(self, obj, stream, indent, allowance, context, level):
        write = stream.write
        write('bytearray' + self.signs_colors.get('parenthesis') + '(' + self.signs_colors.get('data'))
        self._pprint_bytes(bytes(obj), stream, indent + 10,
                           allowance + 1, context, level + 1)
        write(self.signs_colors.get('parenthesis') + ')' + self.signs_colors.get('data'))

    _dispatch[bytearray.__repr__] = _pprint_bytearray

    def _pprint_mappingproxy(self, obj, stream, indent, allowance, context, level):
        stream.write('mappingproxy' + self.signs_colors.get('parenthesis') + '(' + self.signs_colors.get('data'))
        self._format(obj.copy(), stream, indent + 13, allowance + 1,
                     context, level)
        stream.write(self.signs_colors.get('parenthesis') + ')' + self.signs_colors.get('data'))

    _dispatch[_types.MappingProxyType.__repr__] = _pprint_mappingproxy

    def _pprint_simplenamespace(self, obj, stream, indent, allowance, context, level):
        if type(obj) is _types.SimpleNamespace:
            # The SimpleNamespace repr is "namespace" instead of the class
            # name, so we do the same here. For subclasses; use the class name.
            cls_name = 'namespace'
        else:
            cls_name = obj.__class__.__name__
        indent += len(cls_name) + 1
        items = obj.__dict__.items()
        stream.write(cls_name + self.signs_colors.get('parenthesis') + '(' + self.signs_colors.get('data'))
        self._format_namespace_items(items, stream, indent, allowance, context, level)
        stream.write(self.signs_colors.get('parenthesis') + ')' + self.signs_colors.get('data'))

    _dispatch[_types.SimpleNamespace.__repr__] = _pprint_simplenamespace

    def _format_dict_items(self, items, stream, indent, allowance, context, level):
        write = stream.write
        indent += self._indent_per_level
        delimnl = self.signs_colors.get('comma') + ',\n' + self.signs_colors.get('data') + ' ' * indent
        last_index = len(items) - 1
        for i, (key, ent) in enumerate(items):
            last = i == last_index
            rep = self._repr(key, context, level)
            write(rep)
            write(self.signs_colors.get('colon') + ': ' + self.signs_colors.get('data'))
            self._format(ent, stream, indent + len(rep) + 2,
                         allowance if last else 1,
                         context, level)
            if not last:
                write(delimnl)

    def _format_namespace_items(self, items, stream, indent, allowance, context, level):
        write = stream.write
        delimnl = self.signs_colors.get('comma') + ',\n' + self.signs_colors.get('data') + ' ' * indent
        last_index = len(items) - 1
        for i, (key, ent) in enumerate(items):
            last = i == last_index
            write(key)
            write('=')
            if id(ent) in context:
                # Special-case representation of recursion to match standard
                # recursive dataclass repr.
                write(self.signs_colors.get('...') + "..." + self.signs_colors.get('data'))
            else:
                self._format(ent, stream, indent + len(key) + 1, allowance if last else 1, context, level)
            if not last:
                write(delimnl)

    def _format_items(self, items, stream, indent, allowance, context, level):
        write = stream.write
        indent += self._indent_per_level
        if self._indent_per_level > 1:
            write((self._indent_per_level - 1) * ' ')
        delimnl = self.signs_colors.get('comma') + ',\n' + self.signs_colors.get('data') + ' ' * indent
        delim = ''
        width = max_width = self._width - indent + 1
        it = iter(items)
        try:
            next_ent = next(it)
        except StopIteration:
            return
        last = False
        while not last:
            ent = next_ent
            try:
                next_ent = next(it)
            except StopIteration:
                last = True
                max_width -= allowance
                width -= allowance
            if self._compact:
                rep = self._repr(ent, context, level)
                w = len(rep) + 2
                if width < w:
                    width = max_width
                    if delim:
                        delim = delimnl
                if width >= w:
                    width -= w
                    write(delim)
                    delim = self.signs_colors.get('comma') + ', ' + self.signs_colors.get('data')
                    write(rep)
                    continue
            write(delim)
            delim = delimnl
            self._format(ent, stream, indent, allowance if last else 1, context, level)

    def _pprint_default_dict(self, obj, stream, indent, allowance, context, level):
        if not len(obj):
            stream.write(repr(obj))
            return
        rdf = self._repr(obj.default_factory, context, level)
        cls = obj.__class__
        indent += len(cls.__name__) + 1
        stream.write(cls.__name__ + self.signs_colors.get('parenthesis') + '(' + self.signs_colors.get('data') + rdf +
                     self.signs_colors.get('comma') + ',\n' + self.signs_colors.get('data') + (' ' * indent))
        self._pprint_dict(obj, stream, indent, allowance + 1, context, level)
        stream.write(self.signs_colors.get('parenthesis') + ')' + self.signs_colors.get('data'))

    _dispatch[_collections.defaultdict.__repr__] = _pprint_default_dict

    def _pprint_counter(self, obj, stream, indent, allowance, context, level):
        if not len(obj):
            stream.write(repr(obj))
            return
        cls = obj.__class__
        stream.write(cls.__name__ + self.signs_colors.get('parenthesis') + '(' +
                     self.signs_colors.get('curly-braces') + '{' + self.signs_colors.get('data'))
        if self._indent_per_level > 1:
            stream.write((self._indent_per_level - 1) * ' ')
        items = obj.most_common()
        self._format_dict_items(items, stream,
                                indent + len(cls.__name__) + 1, allowance + 2,
                                context, level)
        stream.write(self.signs_colors.get('curly-braces') + '}' +
                     self.signs_colors.get('parenthesis') + ')' + self.signs_colors.get('data'))

    _dispatch[_collections.Counter.__repr__] = _pprint_counter

    def _pprint_chain_map(self, obj, stream, indent, allowance, context, level):
        if not len(obj.maps):
            stream.write(repr(obj))
            return
        cls = obj.__class__
        stream.write(cls.__name__ + self.signs_colors.get('parenthesis') + '(' + self.signs_colors.get('data'))
        indent += len(cls.__name__) + 1
        for i, m in enumerate(obj.maps):
            if i == len(obj.maps) - 1:
                self._format(m, stream, indent, allowance + 1, context, level)
                stream.write(self.signs_colors.get('parenthesis') + ')' + self.signs_colors.get('data'))
            else:
                self._format(m, stream, indent, 1, context, level)
                stream.write(self.signs_colors.get('comma') + ',\n' + self.signs_colors.get('data') + ' ' * indent)

    _dispatch[_collections.ChainMap.__repr__] = _pprint_chain_map

    def _pprint_deque(self, obj, stream, indent, allowance, context, level):
        if not len(obj):
            stream.write(repr(obj))
            return
        cls = obj.__class__
        stream.write(cls.__name__ + self.signs_colors.get('parenthesis') + '(' + self.signs_colors.get('data'))
        indent += len(cls.__name__) + 1
        stream.write(self.signs_colors.get('square-brackets') + '[' + self.signs_colors.get('data'))
        if obj.maxlen is None:
            self._format_items(obj, stream, indent, allowance + 2,
                               context, level)
            stream.write(self.signs_colors.get('square-brackets') + ']' + self.signs_colors.get('parenthesis') + ')' +
                         self.signs_colors.get('data'))
        else:
            self._format_items(obj, stream, indent, 2,
                               context, level)
            rml = self._repr(obj.maxlen, context, level)
            stream.write(self.signs_colors.get('square-brackets') + ']' + self.signs_colors.get('comma') +
                         ',' + self.signs_colors.get('data') + '\n' + (' ' * indent) + 'maxlen=' + rml +
                         self.signs_colors.get('parenthesis') + ')')

    _dispatch[_collections.deque.__repr__] = _pprint_deque

    def _pprint_user_dict(self, obj, stream, indent, allowance, context, level):
        self._format(obj.data, stream, indent, allowance, context, level - 1)

    _dispatch[_collections.UserDict.__repr__] = _pprint_user_dict

    def _pprint_user_list(self, obj, stream, indent, allowance, context, level):
        self._format(obj.data, stream, indent, allowance, context, level - 1)

    _dispatch[_collections.UserList.__repr__] = _pprint_user_list

    def _pprint_user_string(self, obj, stream, indent, allowance, context, level):
        self._format(obj.data, stream, indent, allowance, context, level - 1)

    _dispatch[_collections.UserString.__repr__] = _pprint_user_string


def pformat(obj, indent=1, width=80, depth=None, signs_colors: _Dict[str, str] = None, *, compact=False,
            sort_dicts=True, underscore_numbers=False):
    """Format a Python object into a pretty-printed representation."""
    return PrettyPrinter(indent=indent, width=width, depth=depth, compact=compact, signs_colors=signs_colors,
                         sort_dicts=sort_dicts, underscore_numbers=underscore_numbers).pformat(obj)
