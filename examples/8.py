# Common Section
import log21


class ReversedText:

    def __init__(self, text: str):
        self._text = text[::-1]

    def __str__(self):
        return self._text

    def __repr__(self):
        return f"<{self.__class__.__name__}(text='{self._text}') at {hex(id(self))}>"


# New way
def main(
    positional_arg: int,
    /,
    optional_arg: ReversedText,
    arg_with_default: int = 21,
    additional_arg=None,
    verbose: bool = False,
    quiet: bool = False
):
    """Some description.

    :param positional_arg: This argument is positional!
    :param optional_arg: Whatever you pass here will be REVERSED!
    :param arg_with_default: The default value is 21
    :param additional_arg: This one is extra.
    :param verbose: Increase verbosity
    :param quiet: Make the script quiet
    """
    if verbose and quiet:
        raise log21.IncompatibleArgumentsError(
            '--verbose',
            '--quiet',
            message="You can not make the script quiet and except it to be more verbose!"
        )
    if verbose:
        log21.basic_config(level='DEBUG')
    if quiet:
        log21.basic_config(level='WARN')

    log21.info(f"{positional_arg = }")
    log21.info(f"{optional_arg = !s}")
    log21.warn("THIS IS IMPORTANT!!!")
    log21.debug(f"{arg_with_default = }")
    log21.debug(f"{additional_arg = !s}")


if __name__ == '__main__':
    log21.argumentify(main)
