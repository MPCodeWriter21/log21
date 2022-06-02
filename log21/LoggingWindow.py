# log21.LoggingWindow.py
# CodeWriter21
import re as _re
import subprocess as _subprocess

from uuid import uuid4 as _uuid4
from typing import Union as _Union
from string import printable as _printable
from logging import FileHandler as _FileHandler

from log21.Levels import NOTSET as _NOTSET
from log21.Logger import Logger as _Logger
from log21.StreamHandler import StreamHandler as _StreamHandler
from log21.Colors import ansi_escape as _ansi_escape, hex_escape as _hex_escape

__all__ = ['LoggingWindow', 'LoggingWindowHandler']

try:
    import tkinter as _tkinter
except ImportError:
    class LoggingWindow:
        def __init__(self, *args, **kwargs):
            raise ImportError('LoggingWindow requires tkinter to be installed.')


    class LoggingWindowHandler:
        def __init__(self, *args, **kwargs):
            raise ImportError('LoggingWindow requires tkinter to be installed.')
else:
    ansi_to_hex_color_map = {  # https://chrisyeh96.github.io/2020/03/28/terminal-colors.html
        '30': ('#000000', 'foreground'),  # Black foreground
        '31': ('#cc0000', 'foreground'),  # Red foreground
        '32': ('#4e9a06', 'foreground'),  # Green foreground
        '33': ('#c4a000', 'foreground'),  # Yellow foreground
        '34': ('#729fcf', 'foreground'),  # Blue foreground
        '35': ('#75507b', 'foreground'),  # Magenta foreground
        '36': ('#06989a', 'foreground'),  # Cyan foreground
        '37': ('#d3d7cf', 'foreground'),  # White foreground
        '90': ('#555753', 'foreground'),  # Bright black foreground
        '91': ('#ef2929', 'foreground'),  # Bright red foreground
        '92': ('#8ae234', 'foreground'),  # Bright green foreground
        '93': ('#fce94f', 'foreground'),  # Bright yellow foreground
        '94': ('#32afff', 'foreground'),  # Bright blue foreground
        '95': ('#ad7fa8', 'foreground'),  # Bright magenta foreground
        '96': ('#34e2e2', 'foreground'),  # Bright cyan foreground
        '97': ('#ffffff', 'foreground'),  # Bright white foreground
        '40': ('#000000', 'background'),  # Black background
        '41': ('#cc0000', 'background'),  # Red background
        '42': ('#4e9a06', 'background'),  # Green background
        '43': ('#c4a000', 'background'),  # Yellow background
        '44': ('#729fcf', 'background'),  # Blue background
        '45': ('#75507b', 'background'),  # Magenta background
        '46': ('#06989a', 'background'),  # Cyan background
        '47': ('#d3d7cf', 'background'),  # White background
        '100': ('#555753', 'background'),  # Bright black background
        '101': ('#ef2929', 'background'),  # Bright red background
        '102': ('#8ae234', 'background'),  # Bright green background
        '103': ('#fce94f', 'background'),  # Bright yellow background
        '104': ('#32afff', 'background'),  # Bright blue background
        '105': ('#ad7fa8', 'background'),  # Bright magenta background
        '106': ('#34e2e2', 'background'),  # Bright cyan background
        '107': ('#ffffff', 'background'),  # Bright white background
    }


    class LoggingWindowHandler(_StreamHandler):
        def __init__(self, logging_window: 'LoggingWindow', handle_carriage_return: bool = True,
                     handle_new_line: bool = True):
            self.HandleCR = handle_carriage_return
            self.HandleNL = handle_new_line
            self.__carriage_return: bool = False
            self.LoggingWindow = logging_window
            super().__init__(stream=None)

        def emit(self, record):
            try:
                if self.HandleCR:
                    self.check_cr(record)
                if self.HandleNL:
                    self.check_nl(record)
                msg = self.format(record)
                self.write(msg)
                self.write(self.terminator)
            except Exception:
                self.handleError(record)

        def write(self, message):
            if self.LoggingWindow is not None:
                # Sets the element's state to normal so that it can be modified.
                self.LoggingWindow.logs.config(state=_tkinter.NORMAL)

                # Handles carriage return
                parts = _re.split(r'(\r)', message)

                while parts:
                    part = parts.pop(0)

                    if self.__carriage_return:
                        # Checks if the part is printable
                        if any((char in _printable[:-6]) for char in _hex_escape.sub('', _ansi_escape.sub('', part))):
                            # Removes the last line
                            self.LoggingWindow.logs.delete('end - 1 lines', _tkinter.END)
                            if self.LoggingWindow.logs.count('0.0', 'end')[0] != 1:
                                self.LoggingWindow.logs.insert('end', '\n')
                            self.__carriage_return = False

                    tags = []
                    # Handles ANSI color codes
                    ansi_parts = _ansi_escape.split(part)
                    while ansi_parts:
                        ansi_text = ansi_parts.pop(0)

                        if ansi_text:
                            # Handles HEX color codes
                            hex_parts = _hex_escape.split(ansi_text)
                            while hex_parts:
                                hex_text = hex_parts.pop(0)

                                if hex_text:
                                    self.LoggingWindow.logs.insert(_tkinter.END, hex_text)

                                if hex_parts:
                                    hex_color = hex_parts.pop(0)

                                    tag = str(_uuid4())
                                    # Foreground color
                                    if hex_parts.pop(0) == 'f':
                                        tags.append({'name': tag, 'start': self.LoggingWindow.logs.index('end-1c'),
                                                     'config': {'foreground': hex_color}})
                                    # Background color
                                    else:
                                        tags.append({'name': tag, 'start': self.LoggingWindow.logs.index('end-1c'),
                                                     'config': {'background': hex_color}})

                        if ansi_parts:
                            ansi_params = ansi_parts.pop(0).split(';')
                            ansi_color = {'foreground': None, 'background': None}

                            for part in ansi_params:
                                if part in ansi_to_hex_color_map:
                                    color_ = ansi_to_hex_color_map[part]
                                    ansi_color[color_[1]] = color_[0]
                                elif part == '0':
                                    ansi_color['foreground'] = self.LoggingWindow.default_foreground_color
                                    ansi_color['background'] = self.LoggingWindow.default_background_color
                                else:
                                    pass  # error condition ignored
                            if ansi_color['foreground'] or ansi_color['background']:
                                tags.append({'name': str(_uuid4()), 'start': self.LoggingWindow.logs.index('end-1c'),
                                             'config': ansi_color})

                    # Applies the color tags
                    for tag in tags:
                        self.LoggingWindow.logs.tag_add(tag['name'], tag['start'], 'end')
                        self.LoggingWindow.logs.tag_config(tag['name'], **tag['config'])

                    if parts:
                        parts.pop(0)
                        self.__carriage_return = True

                self.LoggingWindow.logs.config(state=_tkinter.DISABLED)
                self.LoggingWindow.logs.see(_tkinter.END)


    class LoggingWindow(_Logger):
        def __init__(self, name, level=_NOTSET, width: int = 80, height: int = 20, default_foreground_color='white',
                     default_background_color='black', font=('Courier', 10), allow_python: bool = False,
                     allow_shell: bool = False, command_history_buffer_size: int = 100):
            """
            Creates a new LoggingWindow object.

            >>> # Manual creation
            >>> # Imports the LoggingWindow and LoggingWindowHandler classes
            >>> from log21 import LoggingWindow, LoggingWindowHandler
            >>> # Creates a new LoggingWindow object
            >>> window = LoggingWindow('Test Window', level='DEBUG')
            >>> # Creates a new LoggingWindowHandler object and adds it to the LoggingWindow object
            >>> window.addHandler(LoggingWindowHandler(window))
            >>> window.debug('A debug message')
            >>> window.info('An info message')
            >>> # Run these lines to see the messages in the window
            >>>
            >>> # Automatic creation
            >>> # Imports log21 and time modules
            >>> import log21, time
            >>> # Creates a new LoggingWindow object
            >>> window = log21.get_logging_window('Test Window')
            >>> # Use it without any additional steps to add handlers and formatters
            >>> window.info('This works properly!')
            >>> # ANSI colors usage:
            >>> window.info('This is a \033[91mred\033[0m message.')
            >>> window.info('\033[102mThis is a message with green background.')
            >>> # HEX colors usage:
            >>> window.info('\033#00FFFFhfThis is a message with cyan foreground.')
            >>> window.info('\033#0000FFhbThis is a message with blue background.')
            >>> # Progressbar usage:
            >>> for i in range(100):
            >>>     window.print_progress(i + 1, 100)
            >>>     time.sleep(0.1)
            >>> # Gettig input from the user:
            >>> name: str = window.input('Enter your name: ')
            >>> window.print('Hello, ' + name + '!')
            >>> # Run these lines to see the messages in the window
            >>>

            :param name: The name of the logger.
            :param level: The level of the logger.
            :param width: The width of the LoggingWindow.
            :param height: The height of the LoggingWindow.
            :param default_foreground_color: The default foreground color of the LoggingWindow.
            :param default_background_color: The default background color of the LoggingWindow.
            :param font: The font of the LoggingWindow.
            """
            super().__init__(name, level)
            self.window = _tkinter.Tk()
            self.window.title(name)
            # Hides window instead of closing it
            self.window.protocol("WM_DELETE_WINDOW", self.hide)

            self.window.resizable(False, False)

            self.logs = _tkinter.Text(self.window)
            self.logs.grid(row=0, column=0, sticky='nsew')
            self.logs.config(state=_tkinter.DISABLED)
            self.logs.config(wrap=_tkinter.NONE)

            # Commands entry
            self.command_entry = _tkinter.Entry(self.window)
            self.command_entry.grid(row=1, column=0, sticky='nsew')
            self.command_entry.bind('<Return>', self.execute_command)
            self.command_entry.bind('<Up>', self.history_up)
            self.command_entry.bind('<Down>', self.history_down)
            self.command_history = []
            self.command_history_index = 0
            if not isinstance(command_history_buffer_size, (int, float)):
                raise TypeError('command_history_buffer_size must be a number')
            self.command_history_buffer_size = command_history_buffer_size if command_history_buffer_size > 0 else 0
            # Hides the command entry if allow_python and allow_shell are False
            if not allow_python and not allow_shell:
                self.command_entry.grid_remove()
            if allow_python:
                raise NotImplementedError('Python commands are not supported yet!')
            self.__allow_python = False
            self.__allow_shell = allow_shell

            # Scroll bars
            self.logs.config(xscrollcommand=_tkinter.Scrollbar(self.window, orient=_tkinter.HORIZONTAL).set)
            self.logs.config(yscrollcommand=_tkinter.Scrollbar(self.window).set)

            # Input related lines
            self.getting_input = False
            self.input_text = ''
            # cursor counter is used for making a nice blinking cursor
            self.__cursor_counter = 1
            self._cursor_position = None
            self.cursor_position = 0
            # KeyPress event for self.logs
            self.logs.bind('<KeyPress>', self.key_press)

            self.font = font
            self.width = width
            self.height = height
            self.default_foreground_color = default_foreground_color
            self.default_background_color = default_background_color

        def addHandler(self, handler: _Union[_FileHandler, LoggingWindowHandler]):
            if not (isinstance(handler, LoggingWindowHandler) or isinstance(handler, _FileHandler)):
                raise TypeError("Handler must be a FileHandler or LoggingWindowHandler")
            super().addHandler(handler)

        def hide(self):
            """
            Hides the LoggingWindow.
            :return:
            """
            self.window.withdraw()

        def show(self):
            """
            Shows the LoggingWindow.
            :return:
            """
            self.window.deiconify()

        def clear(self):
            """
            Clears the LoggingWindow.
            :return:
            """
            self.logs.config(state=_tkinter.NORMAL)
            self.logs.delete('1.0', _tkinter.END)
            self.logs.config(state=_tkinter.DISABLED)

        def input(self, *msg, args: tuple = (), end='\033[0m', **kwargs) -> str:
            """
            Prints a message and waits for input.

            :param msg: The message to print.
            :param args: The arguments to pass to the message.
            :param end: The end of the message.
            :param kwargs:
            :return: The input.
            """
            msg = ' '.join([str(m) for m in msg]) + end
            self._log(self.level if self.level >= _NOTSET else _NOTSET, msg, args, **kwargs)
            self.input_text = ''
            self.getting_input = True
            self.cursor_position = 0
            self.logs.focus()
            try:
                while self.getting_input:
                    self.cursor_position = self.cursor_position
                    self.window.update()
                    self.window.after(10)
            except KeyboardInterrupt:
                self.input_text = ''
                self.getting_input = False
            return self.input_text

        def key_press(self, event):
            """
            KeyPress event callback for self.logs.
            """
            if self.getting_input:
                # Handles Enter key
                if event.keysym == 'Return':
                    self.getting_input = False
                    self.cursor_position = 0
                    self.logs.config(state=_tkinter.NORMAL)
                    self.logs.insert(_tkinter.END, '\n')
                    self.logs.config(state=_tkinter.DISABLED)
                    self.logs.see(_tkinter.END)
                # Handles Backspace key
                elif event.keysym == 'BackSpace':
                    if self.input_text:
                        self.logs.config(state=_tkinter.NORMAL)
                        self.logs.delete(f'end-{len(self.input_text) + 1}c', 'end-1c')
                        self.input_text = self.input_text[:self.cursor_position - 1] + \
                                          self.input_text[self.cursor_position:]
                        self.logs.insert(_tkinter.END, self.input_text)
                        self.logs.config(state=_tkinter.DISABLED)
                        self.cursor_position -= 1
                # Handles Right Arrow
                elif event.keysym == 'Right':
                    if self.cursor_position < len(self.input_text):
                        self.cursor_position += 1
                # Handles Left Arrow
                elif event.keysym == 'Left':
                    if self.cursor_position > 0:
                        self.cursor_position -= 1
                # Handles other keys
                elif event.char:
                    self.logs.config(state=_tkinter.NORMAL)
                    self.logs.delete(f'end-{len(self.input_text) + 1}c', 'end-1c')
                    self.input_text = self.input_text[:self.cursor_position] + event.char + \
                                      self.input_text[self.cursor_position:]
                    self.logs.insert(_tkinter.END, self.input_text)
                    self.logs.config(state=_tkinter.DISABLED)
                    self.cursor_position += 1

        def execute_command(self, event):
            """
            Executes the command in self.command_entry.
            """
            command = self.command_entry.get()
            self.command_entry.delete(0, _tkinter.END)
            self.command_history.append(command)
            self.command_history = self.command_history[-self.command_history_buffer_size:]
            # FIXME: It doesn't support multiline commands yet
            # Shell commands:
            if command.startswith('!'):
                if self.allow_shell:
                    try:
                        # TODO: Add the support of interactive programmes such as python shell and bash
                        output = _subprocess.check_output(command[1:].strip(), shell=False)
                        self.print(output.decode('utf-8').strip('\r\n'))
                    except _subprocess.CalledProcessError as e:
                        self.error('Error code:', e.returncode, e.output.decode('utf-8').strip('\r\n'))
                    except FileNotFoundError:
                        self.error('File not found: Unrecognized command.')
                    except Exception as e:
                        self.error(e)
                else:
                    self.error('Shell commands are not allowed!')
            # Python commands:
            else:
                if self.allow_python:
                    try:
                        # TODO: Add the support of python commands
                        raise NotImplementedError
                    except Exception as e:
                        self.error(e)
                else:
                    try:
                        output = _subprocess.check_output(command.strip(), shell=False)
                        self.print(output.decode('utf-8').strip('\r\n'))
                    except _subprocess.CalledProcessError as e:
                        self.error('Error code:', e.returncode, e.output.decode('utf-8').strip('\r\n'))
                    except FileNotFoundError:
                        self.error('File not found: Unrecognized command.')
                    except Exception as e:
                        self.error(e)
            self.command_history_index = len(self.command_history)

        def history_up(self, event):
            """
            Moves up the command history.
            """
            if self.command_history_index > 0:
                self.command_history_index -= 1
                self.command_entry.delete(0, _tkinter.END)
                self.command_entry.insert(0, self.command_history[self.command_history_index])

        def history_down(self, event):
            """
            Moves down the command history.
            """
            if self.command_history_index < len(self.command_history) - 1:
                self.command_history_index += 1
                self.command_entry.delete(0, _tkinter.END)
                self.command_entry.insert(0, self.command_history[self.command_history_index])
            else:
                self.command_entry.delete(0, _tkinter.END)

        @property
        def allow_python(self):
            return self.__allow_python

        @allow_python.setter
        def allow_python(self, value):
            raise NotImplementedError('Python commands are not supported yet!')
            self.__allow_python = value
            # Hides the command entry if allow_python and allow_shell are False
            if not self.__allow_python and not self.__allow_shell:
                self.command_entry.grid_remove()
            # Shows the command entry if allow_python or allow_shell are True
            else:
                self.command_entry.grid(row=1, column=0, sticky='nsew')

        @property
        def allow_shell(self):
            return self.__allow_shell

        @allow_shell.setter
        def allow_shell(self, value):
            self.__allow_shell = value
            # Hides the command entry if allow_python and allow_shell are False
            if not self.__allow_python and not self.__allow_shell:
                self.command_entry.grid_remove()
            # Shows the command entry if allow_python or allow_shell are True
            else:
                self.command_entry.grid(row=1, column=0, sticky='nsew')

        @property
        def cursor_position(self):
            return self._cursor_position

        @cursor_position.setter
        def cursor_position(self, value):
            new_value = self.cursor_position != value

            # Removes the cursor from the last position
            if self.cursor_position is not None and (self.__cursor_counter % 50 == 0 or new_value):
                index = self.logs.index(f'end-{len(self.input_text) - self.cursor_position + 2}c')
                self.logs.tag_add(index, index, f'end-{len(self.input_text) - self.cursor_position + 1}c')
                self.logs.tag_config(index, background=self.default_background_color,
                                     foreground=self.default_foreground_color)
            self._cursor_position = value

            self.__cursor_counter += 1
            # Places the new cursor
            if self.getting_input and (self.__cursor_counter % 100 == 0 or new_value):
                self.__cursor_counter = 1
                index = self.logs.index(f'end-{len(self.input_text) - self.cursor_position + 2}c')
                self.logs.tag_add(index, index, f'end-{len(self.input_text) - self.cursor_position + 1}c')
                self.logs.tag_config(index, background=self.default_foreground_color,
                                     foreground=self.default_background_color)

        @property
        def default_foreground_color(self):
            return self._default_foreground_color

        @default_foreground_color.setter
        def default_foreground_color(self, value):
            self._default_foreground_color = value
            self.logs.config(foreground=value)

        @property
        def default_background_color(self):
            return self._default_background_color

        @default_background_color.setter
        def default_background_color(self, value):
            self._default_background_color = value
            self.logs.config(background=value)

        @property
        def font(self):
            return self.logs.config()['font']

        @font.setter
        def font(self, value):
            self.logs.config(font=value)

        @property
        def width(self):
            return self.logs.config()['width'][-1]

        @width.setter
        def width(self, value):
            self.logs.config(width=value)

        @property
        def height(self):
            return self.logs.config()['height'][-1]

        @height.setter
        def height(self, value):
            self.logs.config(height=value)

        @property
        def progress_bar(self):
            if not self._progress_bar:
                from log21.ProgressBar import ProgressBar
                self._progress_bar = ProgressBar(logger=self, width=self.width)
            self.window.update()
            return self._progress_bar

        def __del__(self):
            self.window.withdraw()
            self.window.destroy()
            del self.window
