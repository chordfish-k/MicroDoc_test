import logging
import colorlog

# 创建日志器对象
logger = logging.getLogger("logger")

# 添加控制台handler，用于输出日志到控制台
console_handler = logging.StreamHandler()
# 添加日志文件handler，用于输出日志到文件中
file_handler = logging.FileHandler(filename='log.log', encoding='UTF-8')

# 将handler添加到日志器中
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# 设置格式并赋予handler
formatter = colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - [%(name)s] - [%(levelname)s] - %(message)s',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
