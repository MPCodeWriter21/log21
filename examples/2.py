import log21
from log21 import ColorizingArgumentParser, get_colors as gc, get_logger

parser = ColorizingArgumentParser(
    description="This is a simple example of a ColorizingArgumentParser.",
    colors={'help': 'LightCyan'}
)
parser.add_argument('test1', action='store', help='Test 1')
parser.add_argument('test2', action='store', help='Test 2')
parser.add_argument(
    '--optional-arg', '-o', action='store', type=int, help='An optional integer'
)
parser.add_argument('--verbose', '-v', action='store_true', help='Increase verbosity.')

args = parser.parse_args()

logger = get_logger(
    'My Logger',
    level_names={
        log21.DEBUG: ' ? ',
        log21.INFO: ' + ',
        log21.WARNING: ' ! ',
        log21.ERROR: '!!!'
    }
)

if args.verbose:
    logger.setLevel(log21.DEBUG)
else:
    logger.setLevel(log21.INFO)

logger.debug(gc('LightBlue') + 'Verbose mode on!')

logger.debug(
    'Arguments:\n'
    '\tTest 1: %s\n'
    '\tTest 2: %s\n'
    '\tOptional: %s',
    args=(args.test1, args.test2, args.optional_arg)
)

logger.info(gc('LightGreen') + args.test1)

logger.info(gc('LightWhite') + 'Done!')
