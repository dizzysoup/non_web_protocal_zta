import logging

logging.basicConfig(
    level=logging.DEBUG,
    format= '%(name)s - %(levelname)s - %(message)s',
    filename='app.log',
    filemode='w'
)

logger = logging.getLogger('MyLogger')