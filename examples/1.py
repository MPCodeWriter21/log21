import log21

log21.print(
    log21.get_color('#FF0000') + 'This' + log21.get_color((0, 255, 0)) + ' is' +
    log21.get_color('Blue') + ' Blue' + log21.get_colors('BackgroundWhite', 'Black') +
    ' 8)'
)

logger = log21.get_logger(
    'My Logger',
    level_names={
        21: 'SpecialInfo',
        log21.WARNING: ' ! ',
        log21.ERROR: '!!!'
    }
)
logger.info('You are reading the README.md file...')

logger.log(21, 'Here', '%s', 'GO!', args=('we', ))

logger.setLevel(log21.WARNING)
logger.warning("We can't log messages with a level less than 30 anymore!")

logger.debug("You won't see this!")
logger.info("Am I visible?")

logger.error(log21.get_colors('LightRed') + "I'm still here ;1")
