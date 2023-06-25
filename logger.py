from loguru import logger as log

log.add(
    "loggs.log",
    format='{time} | {level} | {message}',
    rotation="10 MB",
    compression="zip",
    encoding='utf-8'
)
