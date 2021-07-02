# -*- coding: utf-8 -*-

# @File    : logging_config.py
# @Date    : 2021-07-01
# @Author  : 王超逸
# @Brief   : 
detail_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                '[%(levelname)s][%(message)s]'

standard_format = '[%(levelname)s][%(asctime)s][%(name)s][%(filename)s:%(lineno)d]%(message)s'

result_format = '%(message)s  # %(asctime)s'

from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent
LOG_DIR = BASE_PATH / "log"
LOG_PATH = LOG_DIR / "log.log"

LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': standard_format
        },
        'simple': {
            'format': standard_format
        },
        'result': {
            'format': result_format
        },
    },
    'filters': {},
    'handlers': {
        # 打印到终端的日志
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'simple'
        },
        # 打印到文件的日志,收集info及以上的日志
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件,日志轮转
            'formatter': 'standard',
            # 可以定制日志文件路径
            # BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # log文件的目录
            # LOG_PATH = os.path.join(BASE_DIR,'a1.log')
            'filename': str(LOG_PATH),  # 日志文件
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M
            'backupCount': 5,
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
        'result': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',  # 保存到文件
            'formatter': 'result',
            'filename': 'result.txt',
            'encoding': 'utf-8',
        },
        'checked': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',  # 保存到文件
            'formatter': 'result',
            'filename': 'checked.save',
            'encoding': 'utf-8',
        },
    },
    'root': {
        'handlers': ['default', 'console'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
        'level': 'DEBUG',  # loggers(第一层日志级别关限制)--->handlers(第二层日志级别关卡限制)
    },
    'loggers': {
        'result': {
            'handlers': ['result', ],
            'level': 'DEBUG',
            'propagate': True,
        },
        'checked': {
            'handlers': ['checked', ],
            'level': 'DEBUG',
            'propagate': False,
        },
        "asyncssh": {
            'handlers': ['default', 'console'],
            'level': 'WARNING',
            'propagate': False,
        }
    },
}


def config_logging():
    import logging.config
    if not LOG_DIR.exists():
        LOG_DIR.mkdir()
    logging.config.dictConfig(LOGGING_DIC)
