"""Import key libraries and print their versions."""
import importlib
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format=(
        '%(asctime)s (%(relativeCreated)d) %(levelname)s %(name)s'
        ' [%(funcName)s:%(lineno)d] %(message)s'),
    stream=sys.stdout)

LOGGER = logging.getLogger(__name__)

if __name__ == '__main__':

    for package_name in [
            'pygeoprocessing',
            'taskgraph',
            'ecoshard',
            'natcap.invest',
            'inspring']:
        try:
            package = importlib.import_module(package_name)
            LOGGER.info(f'{package_name} version: {package.__version__}')
        except ImportError:
            LOGGER.error(f'could not import {package_name}')
        except AttributeError:
            LOGGER.info(f'imported {package_name}')
