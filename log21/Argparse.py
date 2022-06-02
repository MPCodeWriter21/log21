# log21.Argparse.py
# CodeWriter21

import re as _re
import sys as _sys
import log21 as _log21
import argparse as _argparse
from typing import Dict as _Dict
from gettext import gettext as _gettext
from textwrap import TextWrapper as _TextWrapper
from log21.Colors import get_colors as _gc
from log21.Formatters import DecolorizingFormatter as _Formatter

__all__ = ['ColorizingArgumentParser', 'ColorizingHelpFormatter', 'ColorizingTextWrapper']


class ColorizingHelpFormatter(_argparse.HelpFormatter):
    colors = {
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

    def __init__(self, prog, indent_increment=2, max_help_position=24, width=None, colors: _Dict[str, str] = None):
        super().__init__(prog, indent_increment, max_help_position, width)
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
                heading = '%*s%s' % (current_indent, '', self.heading) + _gc(self.formatter.colors['colons']) + \
                          ':\033[0m\n'
            else:
                heading = ''

            # join the section-initial newline, the heading and the help
            return join(['\n', heading, _gc(self.formatter.colors['help']), item_help, '\n'])

    def _add_item(self, func, args):
        self._current_section.items.append((func, args))

    def _fill_text(self, text, width, indent):
        text = self._whitespace_matcher.sub(' ', text).strip()
        return ColorizingTextWrapper(width=width, initial_indent=indent, subsequent_indent=indent).fill(text)

    def _split_lines(self, text, width):
        text = self._whitespace_matcher.sub(' ', text).strip()
        return ColorizingTextWrapper(width=width).wrap(text)

    def start_section(self, heading):
        self._indent()
        section = self._Section(self, self._current_section,
                                _gc(self.colors['section headers']) + str(heading) + '\033[0m')
        self._add_item(section.format_help, [])
        self._current_section = section

    def _format_action(self, action):
        # determine the required width and the entry label
        help_position = min(self._action_max_length + 2,
                            self._max_help_position)
        help_width = max(self._width - help_position, 11)
        action_width = help_position - self._current_indent - 2
        action_header = _gc('rst') + self._format_action_invocation(action)

        indent_first = 0
        # no help; start on same line and add a final newline
        if not action.help:
            action_header = self._current_indent * ' ' + action_header + '\n'
        # short action name; start on the same line and pad two spaces
        elif len(action_header) <= action_width:
            action_header = '%*s%-*s  ' % (self._current_indent, '', action_width, action_header)
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
                        if line_len + 1 + len(_Formatter.decolorize(part)) > text_width and line:
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
                    part = _gc(self.colors['switches']) + '%s %s%s' % (option_string, _gc(self.colors['values']),
                                                                       args_string)

                # make it look optional if it's not required or in a group
                if not action.required and action not in group_actions:
                    part = _gc(self.colors['brackets']) + '[' + part + _gc(
                        self.colors['brackets']) + ']\033[0m'

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
                    parts.append(_gc(self.colors['switches']) + '%s %s%s' % (option_string, _gc(self.colors['values']),
                                                                             args_string))

            return _gc(self.colors['commas']) + ', '.join(parts)

    def _metavar_formatter(self, action, default_metavar):
        if action.metavar is not None:
            result = action.metavar
        elif action.choices is not None:
            choice_strs = [str(choice) for choice in action.choices]
            result = _gc(self.colors['brackets']) + '{ ' + (_gc(self.colors['commas']) + ', ').join(
                _gc(self.colors['choices']) + choice_str for choice_str in choice_strs) + \
                     _gc(self.colors['brackets']) + ' }'
        else:
            result = default_metavar

        def format(tuple_size):
            if isinstance(result, tuple):
                return result
            else:
                return (result,) * tuple_size

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
            if self.drop_whitespace and _Formatter.decolorize(chunks[-1]).strip() == '' and lines:
                del chunks[-1]

            while chunks:
                # modified upstream code, not going to refactor for ambiguous variable name.
                length = len(_Formatter.decolorize(chunks[-1]))  # noqa: E741

                # Can at least squeeze this chunk onto the current line.
                # Modified upstream code, not going to refactor for ambiguous variable name.
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
            if self.drop_whitespace and current_line and _Formatter.decolorize(current_line[-1]).strip() == '':
                current_len -= len(_Formatter.decolorize(current_line[-1]))
                del current_line[-1]

            if current_line:
                if (self.max_lines is None or
                        len(lines) + 1 < self.max_lines or
                        (not chunks or
                         self.drop_whitespace and
                         len(chunks) == 1 and
                         not chunks[0].strip()) and current_len <= width):
                    # Convert current line back to a string and store it in
                    # list of all lines (return value).
                    lines.append(indent + ''.join(current_line))
                else:
                    while current_line:
                        if _Formatter.decolorize(current_line[-1]).strip() and current_len + len(
                                self.placeholder) <= width:
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


class ColorizingArgumentParser(_argparse.ArgumentParser):
    def __init__(self, formatter_class=ColorizingHelpFormatter, colors: _Dict[str, str] = None, **kwargs):
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
        self.exit(2, _gettext(f'%(prog)s: {_gc("r")}error{_gc("lr")}:{_gc("rst")} %(message)s\n') % args)

    def _get_formatter(self):
        if hasattr(self.formatter_class, 'colors'):
            return self.formatter_class(prog=self.prog, colors=self.colors)
        else:
            return self.formatter_class(prog=self.prog)
