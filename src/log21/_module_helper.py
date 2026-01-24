# log21._module_helper.py
# CodeWriter21

from types import ModuleType
from typing import Any, Callable

ModuleAttribute = Any


class FakeModule(ModuleType):

    def __init__(self, real_module: ModuleType, on_call: Callable) -> None:
        super().__init__(real_module.__name__)
        self.__dict__.update(real_module.__dict__)
        self.__real_module = real_module
        self.__on_call = on_call

    def __getattr__(self, name: str) -> ModuleAttribute:
        return getattr(self.__real_module, name)

    def __call__(self, *args, **kwargs):  # noqa
        return self.__on_call(*args, **kwargs)
