# log21.Argparse.py
# CodeWriter21

from __future__ import annotations

import re as _re
import sys as _sys
import types as _types
import typing as _typing
import argparse as _argparse
from enum import Enum as _Enum
from typing import (Tuple as _Tuple, Mapping as _Mapping, Optional as _Optional,
                    Sequence as _Sequence)
from gettext import gettext as _gettext
from textwrap import TextWrapper as _TextWrapper
from collections import OrderedDict as _OrderedDict

import log21 as _log21
from log21.Colors import get_colors as _gc
from log21.Formatters import DecolorizingFormatter as _Formatter

__all__ = [
    'ColorizingArgumentParser', 'ColorizingHelpFormatter', 'ColorizingTextWrapper',
    'Literal'
]


class Literal:
    """A class for representing literals in argparse arguments."""

    def __init__(self, literal: _typing._LiteralGenericAlias):
        self.literal = literal
        # Only str arguments are allowed
        if not all(map(lambda x: isinstance(x, str), self.literal.__args__)):
            raise TypeError('Only str arguments are allowed for Literal.')

    def __repr__(self):
        return f'Literal[{", ".join(map(str, self.literal.__args__))}]'

    def __str__(self):
        return self.__repr__()

    def __call__(self, value):
        if value not in self.literal.__args__:
            raise ValueError(
                f'Value must be one of [{", ".join(map(str, self.literal.__args__))}]'
            )
        return value


class ColorizingHelpFormatter(_argparse.HelpFormatter):
    """A help formatter that supports colorizing help messages."""

    def __init__(
        self,
        prog,
        indent_increment=2,
        max_help_position=24,
        width=None,
        colors: _Optional[_Mapping[str, str]] = None
    ):
        super().__init__(prog, indent_increment, max_help_position, width)

        self.colors = {
            'usage': 'Cyan',
            'brackets': 'LightRed',
            'switches': 'LightCyan',
            'values': 'Green',
            'colons': 'LightRed',
            'commas': 'LightRed',
            'section headers': 'LightGreen',
            'help': 'LightWhite',
            'choices': 'LightGreen'
        }

        if colors:
            for key, value in colors.items():
                if key in self.colors:
                    self.colors[key] = value

    class _Section(object):

        def __init__(self, formatter, parent, heading=None):
            self.formatter = formatter
            self.parent = parent
            self.heading = heading
            self.items = []

        def format_help(self):
            # format the indented section
            if self.parent is not None:
                self.formatter._indent()
            join = self.formatter._join_parts
            item_help = join([func(*args) for func, args in self.items])
            if self.parent is not None:
                self.formatter._dedent()

            # return nothing if the section was empty
            if not item_help:
                return ''

            # add the heading if the section was non-empty
            if self.heading is not _argparse.SUPPRESS and self.heading is not None:
                current_indent = self.formatter._current_indent
                heading = (
                    '%*s%s' % (current_indent, '', self.heading) +
                    _gc(self.formatter.colors['colons']) + ':\033[0m\n'
                )
            else:
                heading = ''

            # join the section-initial newline, the heading and the help
            return join(
                ['\n', heading,
                 _gc(self.formatter.colors['help']), item_help, '\n']
            )

    def _add_item(self, func, args):
        self._current_section.items.append((func, args))

    def _fill_text(self, text, width, indent):
        text = self._whitespace_matcher.sub(' ', text).strip()
        return ColorizingTextWrapper(
            width=width, initial_indent=indent, subsequent_indent=indent
        ).fill(text)

    def _split_lines(self, text, width):
        text = self._whitespace_matcher.sub(' ', text).strip()
        return ColorizingTextWrapper(width=width).wrap(text)

    def start_section(self, heading):
        self._indent()
        section = self._Section(
            self, self._current_section,
            _gc(self.colors['section headers']) + str(heading) + '\033[0m'
        )
        self._add_item(section.format_help, [])
        self._current_section = section

    def _format_action(self, action):
        # determine the required width and the entry label
        help_position = min(self._action_max_length + 2, self._max_help_position)
        help_width = max(self._width - help_position, 11)
        action_width = help_position - self._current_indent - 2
        action_header = _gc('rst') + self._format_action_invocation(action)

        indent_first = 0
        # no help; start on same line and add a final newline
        if not action.help:
            action_header = self._current_indent * ' ' + action_header + '\n'
        # short action name; start on the same line and pad two spaces
        elif len(action_header) <= action_width:
            action_header = '%*s%-*s  ' % (
                self._current_indent, '', action_width, action_header
            )
        # long action name; start on the next line
        else:
            action_header = self._current_indent * ' ' + action_header + '\n'
            indent_first = help_position

        # collect the pieces of the action help
        parts = [action_header]

        # if there was help for the action, add lines of help text
        if action.help:
            help_text = _gc(self.colors['help']) + self._expand_help(action)
            help_lines = self._split_lines(help_text, help_width)
            parts.append('%*s%s\n' % (indent_first, '', help_lines[0]))
            for line in help_lines[1:]:
                parts.append('%*s%s\n' % (help_position, '', line))

        # or add a newline if the description doesn't end with one
        elif not action_header.endswith('\n'):
            parts.append('\n')

        # if there are any sub-actions, add their help as well
        for subaction in self._iter_indented_subactions(action):
            parts.append(self._format_action(subaction))

        # return a single string
        return self._join_parts(parts)

    # modified upstream code, not going to refactor for complexity.
    def _format_usage(self, usage, actions, groups, prefix):  # noqa: C901
        if prefix is None:
            prefix = _gettext('usage: ')

        # if usage is specified, use that
        if usage is not None:
            usage = usage % dict(prog=self._prog)

        # if no optionals or positionals are available, usage is just prog
        elif usage is None and not actions:
            usage = '%(prog)s' % dict(prog=self._prog)

        # if optionals and positionals are available, calculate usage
        elif usage is None:
            prog = '%(prog)s' % dict(prog=self._prog)

            # split optionals from positionals
            optionals = []
            positionals = []
            for action in actions:
                if action.option_strings:
                    optionals.append(action)
                else:
                    positionals.append(action)

            # build full usage string
            action_usage = self._format_actions_usage(optionals + positionals, groups)
            usage = ' '.join([s for s in [prog, action_usage] if s])

            # wrap the usage parts if it's too long
            text_width = self._width - self._current_indent
            if len(prefix) + len(_Formatter.decolorize(usage)) > text_width:

                # break usage into wrappable parts
                part_regexp = r'\(.*?\)+|\[.*?\]+|\S+'
                opt_usage = self._format_actions_usage(optionals, groups)
                pos_usage = self._format_actions_usage(positionals, groups)
                opt_parts = _re.findall(part_regexp, opt_usage)
                pos_parts = _re.findall(part_regexp, pos_usage)
                assert ' '.join(opt_parts) == opt_usage
                assert ' '.join(pos_parts) == pos_usage

                # helper for wrapping lines
                def get_lines(parts, indent, prefix=None):
                    lines = []
                    line = []
                    if prefix is not None:
                        line_len = len(prefix) - 1
                    else:
                        line_len = len(indent) - 1
                    for part in parts:
                        if line_len + 1 + len(_Formatter.decolorize(part)
                                              ) > text_width and line:
                            lines.append(indent + ' '.join(line))
                            line = []
                            line_len = len(indent) - 1
                        line.append(part)
                        line_len += len(_Formatter.decolorize(part)) + 1
                    if line:
                        lines.append(indent + ' '.join(line))
                    if prefix is not None:
                        lines[0] = lines[0][len(indent):]
                    return lines

                # if prog is short, follow it with optionals or positionals
                len_prog = len(_Formatter.decolorize(prog))
                if len(prefix) + len_prog <= 0.75 * text_width:
                    indent = ' ' * (len(prefix) + len_prog + 1)
                    if opt_parts:
                        lines = get_lines([prog] + opt_parts, indent, prefix)
                        lines.extend(get_lines(pos_parts, indent))
                    elif pos_parts:
                        lines = get_lines([prog] + pos_parts, indent, prefix)
                    else:
                        lines = [prog]

                # if prog is long, put it on its own line
                else:
                    indent = ' ' * len(prefix)
                    parts = opt_parts + pos_parts
                    lines = get_lines(parts, indent)
                    if len(lines) > 1:
                        lines = []
                        lines.extend(get_lines(opt_parts, indent))
                        lines.extend(get_lines(pos_parts, indent))
                    lines = [prog] + lines

                # join lines into usage
                usage = '\n'.join(lines)

        # prefix with 'usage:'
        return prefix + usage + '\n\n'

    def _format_actions_usage(self, actions: list, groups):
        # find group indices and identify actions in groups
        group_actions = set()
        inserts = {}
        for group in groups:
            try:
                start = actions.index(group._group_actions[0])
            except ValueError:
                continue
            else:
                end = start + len(group._group_actions)
                if actions[start:end] == group._group_actions:
                    for action in group._group_actions:
                        group_actions.add(action)
                    if not group.required:
                        if start in inserts:
                            inserts[start] += ' ['
                        else:
                            inserts[start] = '['
                        if end in inserts:
                            inserts[end] += ']'
                        else:
                            inserts[end] = ']'
                    else:
                        if start in inserts:
                            inserts[start] += ' ('
                        else:
                            inserts[start] = '('
                        if end in inserts:
                            inserts[end] += ')'
                        else:
                            inserts[end] = ')'
                    for i in range(start + 1, end):
                        inserts[i] = '|'

        # collect all actions format strings
        parts = []
        for i, action in enumerate(actions):

            # suppressed arguments are marked with None
            # remove | separators for suppressed arguments
            if action.help is _argparse.SUPPRESS:
                parts.append(None)
                if inserts.get(i) == '|':
                    inserts.pop(i)
                elif inserts.get(i + 1) == '|':
                    inserts.pop(i + 1)

            # produce all arg strings
            elif not action.option_strings:
                default = self._get_default_metavar_for_positional(action)
                part = self._format_args(action, default)

                # if it's in a group, strip the outer []
                if action in group_actions:
                    if part[0] == '[' and part[-1] == ']':
                        part = part[1:-1]

                # add the action string to the list
                parts.append(part)

            # produce the first way to invoke the option in brackets
            else:
                option_string = action.option_strings[0]

                # if the Optional doesn't take a value, format is:
                #    -s or --long
                if action.nargs == 0:
                    part = _gc(self.colors['switches']) + action.format_usage()

                # if the Optional takes a value, format is:
                #    -s ARGS or --long ARGS
                else:
                    default = self._get_default_metavar_for_optional(action)
                    args_string = self._format_args(action, default)
                    part = _gc(self.colors['switches']) + '%s %s%s' % (
                        option_string, _gc(self.colors['values']), args_string
                    )

                # make it look optional if it's not required or in a group
                if not action.required and action not in group_actions:
                    part = _gc(self.colors['brackets']) + '[' + part + _gc(
                        self.colors['brackets']
                    ) + ']\033[0m'

                # add the action string to the list
                parts.append(part)

        # insert things at the necessary indices
        for i in sorted(inserts, reverse=True):
            parts[i:i] = [inserts[i]]

        # join all the action items with spaces
        text = ' '.join([item for item in parts if item is not None])

        # clean up separators for mutually exclusive groups
        open = r'[\[(]'
        close = r'[\])]'
        text = _re.sub(r'(%s) ' % open, r'\1', text)
        text = _re.sub(r' (%s)' % close, r'\1', text)
        text = _re.sub(r'%s *%s' % (open, close), r'', text)
        text = _re.sub(r'\(([^|]*)\)', r'\1', text)
        text = text.strip()

        # return the text
        return text

    def _format_action_invocation(self, action):
        if not action.option_strings:
            default = self._get_default_metavar_for_positional(action)
            metavar, = self._metavar_formatter(action, default)(1)
            return metavar

        else:
            parts = []

            # if the Optional doesn't take a value, format is:
            #    -s, --long
            if action.nargs == 0:
                for option_string in action.option_strings:
                    parts.append(_gc(self.colors['switches']) + option_string)

            # if the Optional takes a value, format is:
            #    -s ARGS, --long ARGS
            else:
                default = self._get_default_metavar_for_optional(action)
                args_string = self._format_args(action, default)
                for option_string in action.option_strings:
                    parts.append(
                        _gc(self.colors['switches']) + '%s %s%s' %
                        (option_string, _gc(self.colors['values']), args_string)
                    )

            return _gc(self.colors['commas']) + ', '.join(parts)

    def _metavar_formatter(self, action, default_metavar):
        if action.metavar is not None:
            result = action.metavar
        elif action.choices is not None:
            choice_strs = [str(choice) for choice in action.choices]
            result = (
                _gc(self.colors['brackets']) + '{ ' +
                (_gc(self.colors['commas']) + ', ').join(
                    _gc(self.colors['choices']) + choice_str
                    for choice_str in choice_strs
                ) + _gc(self.colors['brackets']) + ' }'
            )
        else:
            result = default_metavar

        def format(tuple_size):
            if isinstance(result, tuple):
                return result
            else:
                return (result, ) * tuple_size

        return format


class ColorizingTextWrapper(_TextWrapper):
    # modified upstream code, not going to refactor for complexity.
    def _wrap_chunks(self, chunks):  # noqa: C901
        """_wrap_chunks(chunks : [string]) -> [string]

        Wrap a sequence of text chunks and return a list of lines of
        length 'self.width' or less.  (If 'break_long_words' is false,
        some lines may be longer than this.)  Chunks correspond roughly
        to words and the whitespace between them: each chunk is
        indivisible (modulo 'break_long_words'), but a line break can
        come between any two chunks.  Chunks should not have internal
        whitespace; i.e. a chunk is either all whitespace or a "word".
        Whitespace chunks will be removed from the beginning and end of
        lines, but apart from that whitespace is preserved.
        """
        lines = []
        if self.width <= 0:
            raise ValueError("invalid width %r (must be > 0)" % self.width)
        if self.max_lines is not None:
            if self.max_lines > 1:
                indent = self.subsequent_indent
            else:
                indent = self.initial_indent
            if len(indent) + len(self.placeholder.lstrip()) > self.width:
                raise ValueError("placeholder too large for max width")

        # Arrange in reverse order so items can be efficiently popped
        # from a stack of chucks.
        chunks.reverse()

        while chunks:

            # Start the list of chunks that will make up the current line.
            # current_len is just the length of all the chunks in current_line.
            current_line = []
            current_len = 0

            # Figure out which static string will prefix this line.
            if lines:
                indent = self.subsequent_indent
            else:
                indent = self.initial_indent

            # Maximum width for this line.
            width = self.width - len(indent)

            # First chunk on the line is whitespace -- drop it, unless this
            # is the very beginning of the text (i.e. no lines started yet).
            if self.drop_whitespace and _Formatter.decolorize(chunks[-1]
                                                              ).strip() == '' and lines:
                del chunks[-1]

            while chunks:
                # modified upstream code, not going to refactor for ambiguous variable
                # name.
                length = len(_Formatter.decolorize(chunks[-1]))  # noqa: E741

                # Can at least squeeze this chunk onto the current line.
                # Modified upstream code, not going to refactor for ambiguous variable
                # name.
                if current_len + length <= width:  # noqa: E741
                    current_line.append(chunks.pop())
                    current_len += length
                # Nope, this line is full.
                else:
                    break

            # The current line is full, and the next chunk is too big to
            # fit on *any* line (not just this one).
            if chunks and len(_Formatter.decolorize(chunks[-1])) > width:
                self._handle_long_word(chunks, current_line, current_len, width)
                current_len = sum(map(len, current_line))

            # If the last chunk on this line is all whitespace, drop it.
            if self.drop_whitespace and current_line and _Formatter.decolorize(
                    current_line[-1]).strip() == '':
                current_len -= len(_Formatter.decolorize(current_line[-1]))
                del current_line[-1]

            if current_line:
                if (self.max_lines is None or len(lines) + 1 < self.max_lines
                        or (not chunks or self.drop_whitespace and len(chunks) == 1
                            and not chunks[0].strip()) and current_len <= width):
                    # Convert current line back to a string and store it in
                    # list of all lines (return value).
                    lines.append(indent + ''.join(current_line))
                else:
                    while current_line:
                        if _Formatter.decolorize(
                                current_line[-1]
                        ).strip() and current_len + len(self.placeholder) <= width:
                            current_line.append(self.placeholder)
                            lines.append(indent + ''.join(current_line))
                            break
                        current_len -= len(_Formatter.decolorize(current_line[-1]))
                        del current_line[-1]
                    else:
                        if lines:
                            prev_line = lines[-1].rstrip()
                            if len(_Formatter.decolorize(prev_line)) + len(
                                    self.placeholder) <= self.width:
                                lines[-1] = prev_line + self.placeholder
                                break
                        lines.append(indent + self.placeholder.lstrip())
                    break

        return lines


class _ActionsContainer(_argparse._ActionsContainer):
    """Container for the actions for a single command line option."""

    # pylint: disable=too-many-branches
    def _validate_func_type(self, action, func_type, kwargs, level: int = 0) -> _Tuple:
        # raise an error if the action type is not callable
        if (hasattr(_types, 'UnionType') and not callable(func_type)
                and not isinstance(func_type, (_types.UnionType, tuple))):
            raise ValueError(f'{func_type} is not callable; level={level}')

        # Handle `UnionType` as a type (e.g. `int|str`)
        if hasattr(_types, 'UnionType') and isinstance(func_type, _types.UnionType):
            func_type = func_type.__args__  # type: ignore

        # Handle `Literal` as a type (e.g. `Literal[1, 2, 3]`)
        elif (hasattr(_typing, '_LiteralGenericAlias')
              and isinstance(func_type, _typing._LiteralGenericAlias)):  # type: ignore
            func_type = Literal(func_type)

        # Handle `List` as a type (e.g. `List[int]`)
        elif (hasattr(_typing, '_GenericAlias')
              and isinstance(func_type, _typing._GenericAlias)  # type: ignore
              and func_type.__origin__ is list):
            func_type = func_type.__args__[0]
            if kwargs.get('nargs') is None:
                action.nargs = '+'

        # Handle `Required` as a type (e.g. `Required[int]`)
        elif (hasattr(_typing, 'Required') and hasattr(_typing, '_GenericAlias')
              and isinstance(func_type, _typing._GenericAlias)  # type: ignore
              and func_type.__origin__ is _typing.Required
              ):
            func_type = func_type.__args__[0]
            action.required = True

        # Handle `Union` and `Optional` as a type (e.g. `Union[int, str]` and
        # `Optional[int]`)
        elif (hasattr(_types, 'NoneType') and hasattr(_typing, '_UnionGenericAlias')
              and isinstance(func_type, _typing._UnionGenericAlias)):  # type: ignore
            # Optional[T] is just Union[T, NoneType]
            # Optional
            if (len(func_type.__args__) == 2
                    and func_type.__args__[1] is _types.NoneType):
                action.required = False
                func_type = func_type.__args__[0]
            # Union
            else:
                func_type = func_type.__args__  # type: ignore

        # Handle Enum as a type
        elif callable(func_type) and isinstance(func_type, type) and issubclass(
                func_type, _Enum) and action.choices is None and level == 0:
            action.choices = tuple(
                map(lambda x: x.value, func_type.__members__.values())
            )

        # Handle SpecialForms
        elif isinstance(func_type, _typing._SpecialForm):
            if func_type is _typing.Any:
                func_type = None
            elif func_type is _typing.ClassVar:
                func_type = None
            elif func_type is _typing.Union:
                func_type = None
            elif func_type is _typing.Optional:
                func_type = None
                action.required = False
            elif func_type is _typing.Type:
                func_type = None
            elif func_type is _typing.TypeVar:
                func_type = None
            else:
                raise ValueError(f'Unknown special form {func_type}')

        elif func_type is _argparse.FileType:
            raise ValueError(
                f'{func_type} is a FileType class object, instance of it must be passed'
            )

        if isinstance(func_type, _Sequence):
            temp = []
            for type_ in _OrderedDict(zip(func_type, [0] * len(func_type))):
                temp.extend(self._validate_func_type(action, type_, kwargs, level + 1))
            func_type = tuple(temp)
        else:
            if (hasattr(_types, 'UnionType') and hasattr(_typing, '_GenericAlias')
                    and hasattr(_typing, '_UnionGenericAlias')
                    and hasattr(_typing, '_LiteralGenericAlias') and isinstance(
                        func_type,
                        (
                            _typing._GenericAlias,  # type: ignore
                            _typing._UnionGenericAlias,  # type: ignore
                            _typing._LiteralGenericAlias,  # type: ignore
                            _types.UnionType,
                        ))):
                func_type = self._validate_func_type(
                    action, func_type, kwargs, level + 1
                )
            else:
                func_type = (func_type, )

        return func_type

    # Override the default add_argument method defined in argparse._ActionsContainer
    # to add the support for different type annotations
    def add_argument(self, *args, **kwargs):
        """Add an argument to the parser.

        Signature:
            add_argument(dest, ..., name=value, ...)
            add_argument(option_string, option_string, ..., name=value, ...)
        """

        # if no positional args are supplied or only one is supplied and
        # it doesn't look like an option string, parse a positional
        # argument
        chars = self.prefix_chars
        if not args or len(args) == 1 and args[0][0] not in chars:
            if args and 'dest' in kwargs:
                raise ValueError('dest supplied twice for positional argument')
            kwargs = self._get_positional_kwargs(*args, **kwargs)

        # otherwise, we're adding an optional argument
        else:
            kwargs = self._get_optional_kwargs(*args, **kwargs)

        # if no default was supplied, use the parser-level default
        if 'default' not in kwargs:
            dest = kwargs['dest']
            if dest in self._defaults:
                kwargs['default'] = self._defaults[dest]
            elif self.argument_default is not None:
                kwargs['default'] = self.argument_default

        # create the action object, and add it to the parser
        action_class = self._pop_action_class(kwargs)
        if not callable(action_class):
            raise ValueError(f'unknown action "{action_class}"')
        action = action_class(**kwargs)

        func_type = self._registry_get('type', action.type, action.type)
        action.type = self._validate_func_type(
            action, func_type, kwargs
        )  # type: ignore
        if len(action.type) == 1:
            action.type = action.type[0]
        elif len(action.type) == 0:
            action.type = None

        # raise an error if the metavar does not match the type
        if hasattr(self, "_get_formatter"):
            try:
                self._get_formatter()._format_args(action, None)
            except TypeError:
                raise ValueError(
                    "length of metavar tuple does not match nargs"
                ) from None

        return self._add_action(action)

    def add_argument_group(self, *args, **kwargs):
        group = _ArgumentGroup(self, *args, **kwargs)
        self._action_groups.append(group)
        return group

    def add_mutually_exclusive_group(self, **kwargs):
        group = _MutuallyExclusiveGroup(self, **kwargs)
        self._mutually_exclusive_groups.append(group)
        return group


class ColorizingArgumentParser(_argparse.ArgumentParser, _ActionsContainer):
    """An ArgumentParser that colorizes its output and more."""

    def __init__(
        self,
        formatter_class=ColorizingHelpFormatter,
        colors: _Optional[_Mapping[str, str]] = None,
        **kwargs
    ):
        self.logger = _log21.Logger('ArgumentParser')
        self.colors = colors
        super().__init__(formatter_class=formatter_class, **kwargs)

    def _print_message(self, message, file=None):
        if message:
            self.logger.handlers.clear()
            handler = _log21.ColorizingStreamHandler(stream=file)
            self.logger.addHandler(handler)
            self.logger.info(message + _gc('rst'))

    def exit(self, status=0, message=None):
        if message:
            self._print_message(_gc('lr') + message + _gc('rst'), _sys.stderr)
        _sys.exit(status)

    def error(self, message):
        self.print_usage(_sys.stderr)
        args = {'prog': self.prog, 'message': message}
        self.exit(
            2,
            _gettext(
                f'%(prog)s: {_gc("r")}error{_gc("lr")}:{_gc("rst")} %(message)s\n'
            ) % args
        )

    def _get_formatter(self):
        if hasattr(self.formatter_class, 'colors'):
            return self.formatter_class(prog=self.prog, colors=self.colors)
        else:
            return self.formatter_class(prog=self.prog)

    def _get_value(self, action, arg_string):
        """Override _get_value to add support for types such as Union and
        Literal."""

        func_type = self._registry_get('type', action.type, action.type)
        if not callable(func_type) and not isinstance(func_type, tuple):
            raise _argparse.ArgumentError(
                action, _gettext(f'{func_type!r} is not callable')
            )

        name = getattr(action.type, '__name__', repr(action.type))

        # convert the value to the appropriate type
        try:
            if callable(func_type):
                result = func_type(arg_string)
            else:
                exception = ValueError()
                for type_ in func_type:
                    name = getattr(type_, '__name__', repr(type_))
                    try:
                        result = type_(arg_string)
                        break
                    except (ValueError, TypeError) as ex:
                        exception = ex
                else:
                    raise exception

        # ArgumentTypeErrors indicate errors
        except _argparse.ArgumentTypeError as ex:
            msg = str(ex)
            raise _argparse.ArgumentError(action, msg)

        # TypeErrors or ValueErrors also indicate errors
        except (TypeError, ValueError):
            raise _argparse.ArgumentError(
                action, _gettext(f'invalid {name!s} value: {arg_string!r}')
            ) from None

        # return the converted value
        return result

    def __convert_type(self, func_type, arg_string):
        result = None
        if callable(func_type):
            try:
                result = func_type(arg_string)
            except Exception:
                pass
        else:
            for type_ in func_type:
                try:
                    result = type_(arg_string)
                    break
                except Exception:
                    pass

        return result

    def _check_value(self, action, choice):
        # converted value must be one of the choices (if specified)
        if action.choices is not None:
            choices = set(action.choices)

            func_type = self._registry_get('type', action.type, action.type)
            if not callable(func_type) and not isinstance(func_type, tuple):
                raise _argparse.ArgumentError(
                    action, _gettext(f'{func_type!r} is not callable')
                )

            for value in action.choices:
                choices.add(self.__convert_type(func_type, value))

            if choice not in choices:
                raise _argparse.ArgumentError(
                    action,
                    _gettext(
                        f'invalid choice: {choice!r} '
                        f'(choose from {", ".join(map(repr, action.choices))})'
                    )
                )

    def _read_args_from_files(self, arg_strings):
        # expand arguments referencing files
        new_arg_strings = []
        for arg_string in arg_strings:

            # for regular arguments, just add them back into the list
            if not arg_string or arg_string[0] not in self.fromfile_prefix_chars:
                new_arg_strings.append(arg_string)

            # replace arguments referencing files with the file content
            else:
                try:
                    with open(arg_string[1:]) as args_file:
                        arg_strings = []
                        for arg_line in args_file.read().splitlines():
                            for arg in self.convert_arg_line_to_args(arg_line):
                                arg_strings.append(arg)
                        arg_strings = self._read_args_from_files(arg_strings)
                        new_arg_strings.extend(arg_strings)
                except OSError as err:
                    self.error(str(err))

        # return the modified argument list
        return new_arg_strings

    def _parse_known_args(self, arg_strings, namespace):
        # replace arg strings that are file references
        if self.fromfile_prefix_chars is not None:
            arg_strings = self._read_args_from_files(arg_strings)

        # map all mutually exclusive arguments to the other arguments
        # they can't occur with
        action_conflicts = {}
        for mutex_group in self._mutually_exclusive_groups:
            group_actions = mutex_group._group_actions
            for i, mutex_action in enumerate(mutex_group._group_actions):
                conflicts = action_conflicts.setdefault(mutex_action, [])
                conflicts.extend(group_actions[:i])
                conflicts.extend(group_actions[i + 1:])

        # find all option indices, and determine the arg_string_pattern
        # which has an 'O' if there is an option at an index,
        # an 'A' if there is an argument, or a '-' if there is a '--'
        option_string_indices = {}
        arg_string_pattern_parts = []
        arg_strings_iter = iter(arg_strings)
        for i, arg_string in enumerate(arg_strings_iter):

            # all args after -- are non-options
            if arg_string == '--':
                arg_string_pattern_parts.append('-')
                for arg_string in arg_strings_iter:
                    arg_string_pattern_parts.append('A')

            # otherwise, add the arg to the arg strings
            # and note the index if it was an option
            else:
                option_tuple = self._parse_optional(arg_string)
                if option_tuple is None:
                    pattern = 'A'
                else:
                    option_string_indices[i] = option_tuple
                    pattern = 'O'
                arg_string_pattern_parts.append(pattern)

        # join the pieces together to form the pattern
        arg_strings_pattern = ''.join(arg_string_pattern_parts)

        # converts arg strings to the appropriate and then takes the action
        seen_actions = set()
        seen_non_default_actions = set()

        def take_action(action, argument_strings, option_string=None):
            seen_actions.add(action)
            argument_values = self._get_values(action, argument_strings)

            # error if this argument is not allowed with other previously
            # seen arguments, assuming that actions that use the default
            # value don't really count as "present"
            if argument_values is not action.default:
                seen_non_default_actions.add(action)
                for conflict_action in action_conflicts.get(action, []):
                    if conflict_action in seen_non_default_actions:
                        action_name = _argparse._get_action_name(conflict_action)
                        msg = _gettext(f'not allowed with argument {action_name}')
                        raise _argparse.ArgumentError(action, msg)

            # take the action if we didn't receive a SUPPRESS value
            # (e.g. from a default)
            if argument_values is not _argparse.SUPPRESS:
                action(self, namespace, argument_values, option_string)

        # function to convert arg_strings into an optional action
        def consume_optional(start_index):

            # get the optional identified at this index
            option_tuple = option_string_indices[start_index]
            action, option_string, explicit_arg = option_tuple

            # identify additional optionals in the same arg string
            # (e.g. -xyz is the same as -x -y -z if no args are required)
            match_argument = self._match_argument
            action_tuples = []
            while True:

                # if we found no optional action, skip it
                if action is None:
                    extras.append(arg_strings[start_index])
                    return start_index + 1

                # if there is an explicit argument, try to match the
                # optional's string arguments to only this
                if explicit_arg is not None:
                    arg_count = match_argument(action, 'A')

                    # if the action is a single-dash option and takes no
                    # arguments, try to parse more single-dash options out
                    # of the tail of the option string
                    chars = self.prefix_chars
                    if arg_count == 0 and option_string[1] not in chars:
                        action_tuples.append((action, [], option_string))
                        char = option_string[0]
                        option_string = char + explicit_arg[0]
                        new_explicit_arg = explicit_arg[1:] or None
                        optionals_map = self._option_string_actions
                        if option_string in optionals_map:
                            action = optionals_map[option_string]
                            explicit_arg = new_explicit_arg
                        else:
                            msg = _gettext(
                                f'ignored explicit argument {explicit_arg!r}'
                            )
                            raise _argparse.ArgumentError(action, msg)

                    # if the action expect exactly one argument, we've
                    # successfully matched the option; exit the loop
                    elif arg_count == 1:
                        stop = start_index + 1
                        args = [explicit_arg]
                        action_tuples.append((action, args, option_string))
                        break

                    # error if a double-dash option did not use the
                    # explicit argument
                    else:
                        msg = _gettext(f'ignored explicit argument {explicit_arg!r}')
                        raise _argparse.ArgumentError(action, msg)

                # if there is no explicit argument, try to match the
                # optional's string arguments with the following strings
                # if successful, exit the loop
                else:
                    start = start_index + 1
                    selected_patterns = arg_strings_pattern[start:]
                    arg_count = match_argument(action, selected_patterns)
                    stop = start + arg_count
                    args = arg_strings[start:stop]
                    action_tuples.append((action, args, option_string))
                    break

            # add the Optional to the list and return the index at which
            # the Optional's string args stopped
            assert action_tuples
            for action, args, option_string in action_tuples:
                take_action(action, args, option_string)
            return stop

        # the list of Positionals left to be parsed; this is modified
        # by consume_positionals()
        positionals = self._get_positional_actions()

        # function to convert arg_strings into positional actions
        def consume_positionals(start_index):
            # match as many Positionals as possible
            match_partial = self._match_arguments_partial
            selected_pattern = arg_strings_pattern[start_index:]
            arg_counts = match_partial(positionals, selected_pattern)

            # slice off the appropriate arg strings for each Positional
            # and add the Positional and its args to the list
            for action, arg_count in zip(positionals, arg_counts):
                args = arg_strings[start_index:start_index + arg_count]
                start_index += arg_count
                take_action(action, args)

            # slice off the Positionals that we just parsed and return the
            # index at which the Positionals' string args stopped
            positionals[:] = positionals[len(arg_counts):]
            return start_index

        # consume Positionals and Optionals alternately, until we have
        # passed the last option string
        extras = []
        start_index = 0
        if option_string_indices:
            max_option_string_index = max(option_string_indices)
        else:
            max_option_string_index = -1
        while start_index <= max_option_string_index:

            # consume any Positionals preceding the next option
            next_option_string_index = min(
                [index for index in option_string_indices if index >= start_index]
            )
            if start_index != next_option_string_index:
                positionals_end_index = consume_positionals(start_index)

                # only try to parse the next optional if we didn't consume
                # the option string during the positionals parsing
                if positionals_end_index > start_index:
                    start_index = positionals_end_index
                    continue
                else:
                    start_index = positionals_end_index

            # if we consumed all the positionals we could and we're not
            # at the index of an option string, there were extra arguments
            if start_index not in option_string_indices:
                strings = arg_strings[start_index:next_option_string_index]
                extras.extend(strings)
                start_index = next_option_string_index

            # consume the next optional and any arguments for it
            start_index = consume_optional(start_index)

        # consume any positionals following the last Optional
        stop_index = consume_positionals(start_index)

        # if we didn't consume all the argument strings, there were extras
        extras.extend(arg_strings[stop_index:])

        # make sure all required actions were present and also convert
        # action defaults which were not given as arguments
        required_actions = []
        for action in self._actions:
            if action not in seen_actions:
                if action.required:
                    required_actions.append(_argparse._get_action_name(action))
                else:
                    # Convert action default now instead of doing it before
                    # parsing arguments to avoid calling convert functions
                    # twice (which may fail) if the argument was given, but
                    # only if it was defined already in the namespace
                    if (action.default is not None and isinstance(action.default, str)
                            and hasattr(namespace, action.dest)
                            and action.default is getattr(namespace, action.dest)):
                        setattr(
                            namespace, action.dest,
                            self._get_value(action, action.default)
                        )

        if required_actions:
            self.error(
                _gettext(
                    'the following arguments are required: ' +
                    ", ".join(required_actions)
                )
            )

        # make sure all required groups had one option present
        for group in self._mutually_exclusive_groups:
            if group.required:
                for action in group._group_actions:
                    if action in seen_non_default_actions:
                        break

                # if no actions were used, report the error
                else:
                    names = [
                        _argparse._get_action_name(action)
                        for action in group._group_actions
                        if action.help is not _argparse.SUPPRESS
                    ]
                    self.error(
                        _gettext(f'one of the arguments {" ".join(names)} is required')
                    )

        for group in self._action_groups:
            if isinstance(group, _ArgumentGroup) and group.required:
                for action in group._group_actions:
                    if action in seen_non_default_actions:
                        break

                # if no actions were used, report the error
                else:
                    names = [
                        _argparse._get_action_name(action)
                        for action in group._group_actions
                        if action.help is not _argparse.SUPPRESS
                    ]
                    self.error(
                        _gettext(f'one of the arguments {" ".join(names)} is required')
                    )

        # return the updated namespace and the extra arguments
        return namespace, extras


class _ArgumentGroup(_argparse._ArgumentGroup, _ActionsContainer):

    def __init__(
        self,
        container,
        title=None,
        description=None,
        required: bool = False,
        **kwargs
    ):
        super().__init__(container, title=title, description=description, **kwargs)

        self.required = required


class _MutuallyExclusiveGroup(_argparse._MutuallyExclusiveGroup, _ArgumentGroup):
    pass
