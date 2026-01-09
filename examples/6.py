# Common Section
import log21


class ReversedText:

    def __init__(self, text: str):
        self._text = text[::-1]

    def __str__(self):
        return self._text

    def __repr__(self):
        return f"<{self.__class__.__name__}(text='{self._text}') at {hex(id(self))}>"


# Old way
def main():
    """Here is my main function."""
    parser = log21.ColorizingArgumentParser()
    parser.add_argument(
        '--positional-arg',
        '-p',
        action='store',
        type=int,
        required=True,
        help="This argument is positional!"
    )
    parser.add_argument(
        '--optional-arg',
        '-o',
        action='store',
        type=ReversedText,
        help="Whatever you pass here will be REVERSED!"
    )
    parser.add_argument(
        '--arg-with-default',
        '-a',
        action='store',
        default=21,
        help="The default value is 21"
    )
    parser.add_argument(
        '--additional-arg', '-A', action='store', help="This one is extra."
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true', help="Increase verbosity"
    )
    args = parser.parse_args()

    if args.verbose:
        log21.basic_config(level='DEBUG')

    log21.info(f"positional_arg = {args.positional_arg}")
    log21.info(f"optional_arg = {args.optional_arg}")
    log21.debug(f"arg_with_default = {args.arg_with_default}")
    log21.debug(f"additional_arg = {args.additional_arg}")


if __name__ == '__main__':
    main()


# New way
def main(
    positional_arg: int,
    /,
    optional_arg: ReversedText,
    arg_with_default: int = 21,
    additional_arg=None,
    verbose: bool = False
):
    """Some description.

    :param positional_arg: This argument is positional!
    :param optional_arg: Whatever you pass here will be REVERSED!
    :param arg_with_default: The default value is 21
    :param additional_arg: This one is extra.
    :param verbose: Increase verbosity
    """
    if verbose:
        log21.basic_config(level='DEBUG')

    log21.info(f"{positional_arg = }")
    log21.info(f"{optional_arg = !s}")
    log21.debug(f"{arg_with_default = }")
    log21.debug(f"{additional_arg = !s}")


if __name__ == '__main__':
    log21.argumentify(main)
