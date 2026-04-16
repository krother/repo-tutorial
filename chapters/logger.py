import logging

log = logging.getLogger('example logger')
log.setLevel(logging.INFO)

fmt='%(asctime)s | %(message)s'
formatter = logging.Formatter(fmt, datefmt='%m/%d/%Y %I:%M:%S %p')

handler = logging.FileHandler('logfile.log', mode='w')
handler.setFormatter(formatter)
log.addHandler(handler)

log.info('message from logger ')
log.warning('warning from logger')
log.error('an error has occured')
