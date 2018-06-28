import os
import logging
import logging.config as log_conf

log_dir = os.path.dirname(os.path.dirname(__file__))+'/logs'
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

log_path = os.path.join(log_dir, 'weibo.log')

log_config = {
    'version': 1.0,
    'formatters': {
        'detail': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'detail'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 10,
            'filename': log_path,
            'level': 'INFO',
            'formatter': 'detail',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'crawler': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'parser': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'other': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'storage': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'thread' : {
            'handlers':['console'],
            'level':'INFO',
        }
    }
}

log_conf.dictConfig(log_config)
crawler = logging.getLogger('crawler')
parser = logging.getLogger('parser')
other = logging.getLogger('other')
storage = logging.getLogger('storage')
thread = logging.getLogger('thread')