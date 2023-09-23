# log21.Argparse.py
# CodeWriter21

import re as _re
import string as _string
import asyncio as _asyncio
import inspect as _inspect
from typing import (Any as _Any, Set as _Set, Dict as _Dict, List as _List,
                    Tuple as _Tuple, Union as _Union, Callable as _Callable,
                    Optional as _Optional, Awaitable as _Awaitable,
                    Coroutine as _Coroutine, OrderedDict as _OrderedDict)
from dataclasses import field as _field, dataclass as _dataclass

from docstring_parser import Docstring as _Docstring, parse as _parse

import log21.Argparse as _Argparse

__all__ = [
    'argumentify', 'ArgumentifyError', 'ArgumentTypeError', 'FlagGenerationError',
    'RESERVED_FLAGS', 'Callable', 'Argument', 'FunctionInfo', 'generate_flag',
    'normalize_name', 'normalize_name_to_snake_case'
]

Callable = _Union[_Callable[..., _Any], _Callable[..., _Coroutine[_Any, _Any, _Any]]]
RESERVED_FLAGS = {'--help', '-h'}


class ArgumentifyError(Exception):
    """Base class for exceptions in this module."""


class ArgumentTypeError(ArgumentifyError, TypeError):
    """Exception raised when a function has an unsupported type of argument.

    e.g: a function has a VAR_KEYWORD argument.
    """

    def __init__(
        self, message: _Optional[str] = None, unsupported_arg: _Optional[str] = None
    ):
        """Initialize the exception.

        :param message: The message to display.
        :param unsupported_arg: The name of the unsupported argument.
        """
        if message is None:
            if unsupported_arg is None:
                message = 'Unsupported argument type.'
            else:
                message = f'Unsupported argument type: {unsupported_arg}'
        self.message = message
        self.unsupported_arg = unsupported_arg


class FlagGenerationError(ArgumentifyError, RuntimeError):
    """Exception raised when an error occurs while generating a flag.

    Most likely raised when there are arguments with the same name.
    """

    def __init__(self, message: _Optional[str] = None, arg_name: _Optional[str] = None):
        """Initialize the exception.

        :param message: The message to display.
        :param arg_name: The name of the argument that caused the error.
        """
        if message is None:
            if arg_name is None:
                message = 'An error occurred while generating a flag.'
            else:
                message = (
                    'An error occurred while generating a flag for argument: '
                    f'{arg_name}'
                )
        self.message = message
        self.arg_name = arg_name


def normalize_name_to_snake_case(name: str, sep_char: str = '_') -> str:
    """Returns the normalized name a class.

    >>> normalize_name_to_snake_case('main')
    'main'
    >>> normalize_name_to_snake_case('MyClassName')
    'my_class_name'
    >>> normalize_name_to_snake_case('HelloWorld')
    'hello_world'
    >>> normalize_name_to_snake_case('myVar')
    'my_var'
    >>> normalize_name_to_snake_case("It's cool")
    'it_s_cool'
    >>> normalize_name_to_snake_case("test-name")
    'test_name'

    :param name: The name to normalize.
    :param sep_char: The character that will replace space and separate words
    :return: The normalized name.
    """
    for char in _string.punctuation:
        name = name.replace(char, sep_char)
    name = _re.sub(rf'([\s{sep_char}]+)|(([a-zA-z])([A-Z]))', rf'\3{sep_char}\4',
                   name).lower()
    return name


def normalize_name(name: str, sep_char: str = '_') -> str:
    """Returns the normalized name a class.

    >>> normalize_name('main')
    'main'
    >>> normalize_name('MyFunction')
    'MyFunction'
    >>> normalize_name('HelloWorld')
    'HelloWorld'
    >>> normalize_name('myVar')
    'myVar'
    >>> normalize_name("It's cool")
    'It_s_cool'
    >>> normalize_name("test-name")
    'test_name'

    :param name: The name to normalize.
    :param sep_char: The character that will replace space and separate words
    :return: The normalized name.
    """
    for char in _string.punctuation:
        name = name.replace(char, sep_char)
    name = _re.sub(rf'([\s{sep_char}]+)', sep_char, name)
    return name


@_dataclass
class Argument:
    """Represents a function argument."""
    name: str
    kind: _inspect._ParameterKind
    annotation: _Any = _inspect._empty
    default: _Any = _inspect._empty
    help: _Optional[str] = None

    def __post_init__(self):
        """Sets the some values to None if they are empty."""
        if self.annotation == _inspect._empty:
            self.annotation = None
        if self.default == _inspect._empty:
            self.default = None


@_dataclass
class FunctionInfo:
    """Represents a function."""
    function: Callable
    name: str = _field(init=False)
    arguments: _OrderedDict[str, Argument] = _field(init=False)
    docstring: _Docstring = _field(init=False)
    parser: _Argparse.ColorizingArgumentParser = _field(init=False)

    def __post_init__(self):
        self.name = normalize_name_to_snake_case(
            self.function.__init__.__name__
        ) if isinstance(self.function,
                        type) else normalize_name(self.function.__name__)
        self.function = self.function.__init__ if isinstance(
            self.function, type
        ) else self.function

        self.arguments: _OrderedDict[str, Argument] = _OrderedDict()
        for parameter in _inspect.signature(self.function).parameters.values():
            self.arguments[parameter.name] = Argument(
                name=parameter.name,
                kind=parameter.kind,
                default=parameter.default,
                annotation=parameter.annotation,
            )

        self.docstring = _parse(self.function.__doc__ or '')
        for parameter in self.docstring.params:
            if parameter.arg_name in self.arguments:
                self.arguments[parameter.arg_name].help = parameter.description


def generate_flag(  # pylint: disable=too-many-branches
    argument: Argument,
    no_dash: bool = False,
    reserved_flags: _Optional[_Set[str]] = None
) -> _List[str]:
    """Generates one or more flags for an argument based on its attributes.

    :param argument: The argument to generate flags for.
    :param no_dash: Whether to generate flags without dashes as
        prefixes.
    :param reserved_flags: A set of flags that are reserved. (Default: `RESERVED_FLAGS`)
    :raises FlagGenerationError: If all the suitable flags are reserved.
    :return: A list of flags for the argument.
    """
    if reserved_flags is None:
        reserved_flags = RESERVED_FLAGS
    flags: _List[str] = []
    flag1_base = ('' if no_dash else '--')
    flag1 = flag1_base + normalize_name_to_snake_case(argument.name, '-')
    if flag1 in reserved_flags:
        flag1 = flag1_base + normalize_name(argument.name, sep_char='-')
    if flag1 in reserved_flags:
        flag1 = flag1_base + argument.name
    if flag1 in reserved_flags:
        flag1 = flag1_base + normalize_name(
            ' '.join(normalize_name_to_snake_case(argument.name, '-').split('-')
                     ).capitalize(),
            sep_char='-'
        )
    if flag1 in reserved_flags:
        flag1 = flag1_base + normalize_name(argument.name, sep_char='-').upper()
    if flag1 in reserved_flags:
        if no_dash:
            raise FlagGenerationError(
                f"Failed to generate a flag for argument: {argument}"
            )
    else:
        flags.append(flag1)

    if not no_dash:
        flag2 = '-' + argument.name[:1].lower()
        if flag2 in reserved_flags:
            flag2 = flag2.upper()
        if flag2 in reserved_flags:
            flag2 = '-' + ''.join(
                part[:1]
                for part in normalize_name_to_snake_case(argument.name).split('_')
            )
        if flag2 in reserved_flags:
            flag2 = flag2.capitalize()
        if flag2 in reserved_flags:
            flag2 = flag2.upper()
        if flag2 not in reserved_flags:
            flags.append(flag2)

    if not flags:
        raise FlagGenerationError(f"Failed to generate a flag for argument: {argument}")

    reserved_flags.update(flags)

    return flags


def _add_arguments(
    parser: _Union[_Argparse.ColorizingArgumentParser, _Argparse._ArgumentGroup],
    info: FunctionInfo,
    reserved_flags: _Optional[_Set[str]] = None
) -> None:
    """Add the arguments to the parser.

    :param parser: The parser to add the arguments to.
    :param info: The function info.
    :param reserved_flags: The reserved flags.
    """
    if reserved_flags is None:
        reserved_flags = RESERVED_FLAGS.copy()
    # Add the arguments
    for argument in info.arguments.values():
        config: _Dict[str, _Any] = {
            'action': 'store',
            'dest': argument.name,
            'help': argument.help
        }
        if isinstance(argument.annotation, type):
            config['type'] = argument.annotation
        if argument.annotation == bool:
            config['action'] = 'store_true'
            config.pop('type')
        if argument.kind == _inspect._ParameterKind.POSITIONAL_ONLY:
            config['required'] = True
        if argument.kind == _inspect._ParameterKind.VAR_POSITIONAL:
            config['nargs'] = '*'
        if argument.default:
            config['default'] = argument.default
        parser.add_argument(
            *generate_flag(argument, reserved_flags=reserved_flags), **config
        )


def _argumentify_one(func: Callable):
    """This function argumentifies one function as the entry point of the
    script.

    :param function: The function to argumentify.
    """
    info = FunctionInfo(func)

    # Check if the function has a VAR_KEYWORD argument
    # Raises a ArgumentTypeError if it does
    for argument in info.arguments.values():
        if argument.kind == _inspect._ParameterKind.VAR_KEYWORD:
            raise ArgumentTypeError(
                f"The function has a `**{argument.name}` argument, "
                "which is not supported.",
                unsupported_arg=argument.name
            )

    # Create the parser
    parser = _Argparse.ColorizingArgumentParser(
        description=info.docstring.short_description
    )
    # Add the arguments
    _add_arguments(parser, info)
    cli_args = parser.parse_args()
    args = []
    kwargs = {}
    for argument in info.arguments.values():
        if argument.kind in (_inspect._ParameterKind.POSITIONAL_ONLY,
                             _inspect._ParameterKind.POSITIONAL_OR_KEYWORD):
            args.append(getattr(cli_args, argument.name))
        elif argument.kind == _inspect._ParameterKind.VAR_POSITIONAL:
            args.extend(getattr(cli_args, argument.name) or [])
        else:
            kwargs[argument.name] = getattr(cli_args, argument.name)
    result = func(*args, **kwargs)
    # Check if the result is a coroutine
    if isinstance(result, (_Coroutine, _Awaitable)):
        _asyncio.run(result)


def _argumentify(functions: _Dict[str, Callable]):
    """This function argumentifies one or more functions as the entry point of
    the script.

    :param functions: A dictionary of functions to argumentify.
    :raises RuntimeError:
    """
    functions_info: _Dict[str, _Tuple[Callable, FunctionInfo]] = {}
    for name, function in functions.items():
        functions_info[name] = (function, FunctionInfo(function))

        # Check if the function has a VAR_KEYWORD argument
        # Raises a ArgumentTypeError if it does
        for argument in functions_info[name][1].arguments.values():
            if argument.kind == _inspect._ParameterKind.VAR_KEYWORD:
                raise ArgumentTypeError(
                    f"Function {name} has `**{argument.name}` argument, "
                    "which is not supported.",
                    unsupported_arg=argument.name
                )
    parser = _Argparse.ColorizingArgumentParser()
    subparsers = parser.add_subparsers(required=True)
    for name, (_, info) in functions_info.items():
        subparser = subparsers.add_parser(name, help=info.docstring.short_description)
        _add_arguments(subparser, info)
        subparser.set_defaults(func=info.function)
    cli_args = parser.parse_args()
    args = []
    kwargs = {}
    info = None
    for name, (function, info) in functions_info.items():
        if function == cli_args.func:
            break
    else:
        raise RuntimeError('No function found for the given arguments.')
    for argument in info.arguments.values():
        if argument.kind in (_inspect._ParameterKind.POSITIONAL_ONLY,
                             _inspect._ParameterKind.POSITIONAL_OR_KEYWORD):
            args.append(getattr(cli_args, argument.name))
        elif argument.kind == _inspect._ParameterKind.VAR_POSITIONAL:
            args.extend(getattr(cli_args, argument.name) or [])
        else:
            kwargs[argument.name] = getattr(cli_args, argument.name)
    result = function(*args, **kwargs)
    # Check if the result is a coroutine
    if isinstance(result, (_Coroutine, _Awaitable)):
        _asyncio.run(result)


def argumentify(entry_point: _Union[Callable, _List[Callable], _Dict[str, Callable]]):
    """This function argumentifies one or more functions as the entry point of
    the script.

     1 #!/usr/bin/env python
     2 # argumentified.py
     3 from log21 import argumentify
     4
     5
     6 def main(first_name: str, last_name: str, /, *, age: int = None) -> None:
     7     if age is not None:
     8         print(f'{first_name} {last_name} is {age} years old.')
     9     else:
    10         print(f'{first_name} {last_name} is not yet born.')
    11
    12 if __name__ == '__main__':
    13     argumentify(main)

    $ python argumentified.py Ahmad Ahmadi --age 20
    Ahmad Ahmadi is 20 years old.
    $ python argumentified.py Mehrad Pooryoussof
    Mehrad Pooryoussof is not yet born.

    :param entry_point: The function(s) to argumentify.
    :raises TypeError: A function must be a function or a list of functions or a
        dictionary of functions.
    """

    functions = {}
    # Check the types
    if callable(entry_point):
        _argumentify_one(entry_point)
        return entry_point
    if isinstance(entry_point, _List):
        for func in entry_point:
            if not callable(func):
                raise TypeError(
                    "argumentify: func must be a function or a list of functions or a "
                    "dictionary of functions."
                )
            functions[func.__name__] = func
    elif isinstance(entry_point, _Dict):
        for func in entry_point.values():
            if not callable(func):
                raise TypeError(
                    "argumentify: func must be a function or a list of functions or a "
                    "dictionary of functions."
                )
        functions = entry_point
    else:
        raise TypeError(
            "argumentify: func must be a function or a list of functions or a "
            "dictionary of functions."
        )

    _argumentify(functions)
    return entry_point
