"""Demo of optimization."""
import logging
import os
import sys

import ecoshard
import pygeoprocessing
import taskgraph

logging.basicConfig(
    level=logging.DEBUG,
    format=(
        '%(asctime)s (%(relativeCreated)d) %(levelname)s %(name)s'
        ' [%(funcName)s:%(lineno)d] %(message)s'),
    stream=sys.stdout)

LOGGER = logging.getLogger(__name__)
logging.getLogger('taskgraph').setLevel(logging.WARN)

BACCINI_URL = (
    'https://storage.googleapis.com/ecoshard-root/global_carbon_regression/'
    'baccini_10s_2014_md5_5956a9d06d4dffc89517cefb0f6bb008.tif')

if __name__ == '__main__':
    output_directory = 'raster_optimization_output'
    churn_dir = os.path.join(output_directory, 'churn')
    try:
        os.makedirs(churn_dir)
    except OSError:
        pass

    task_graph = taskgraph.TaskGraph(churn_dir, -1)

    baccini_path = os.path.join(churn_dir, os.path.basename(BACCINI_URL))
    download_task = task_graph.add_task(
        func=ecoshard.download_url,
        args=(BACCINI_URL, baccini_path),
        target_path_list=[baccini_path],
        task_name='download baccini')

    task_graph.add_task(
        func=pygeoprocessing.raster_optimization,
        args=([(baccini_path, 1)], churn_dir, output_directory),
        kwargs={
            'goal_met_cutoffs': [x/100 for x in range(5, 51, 5)],
            'heap_buffer_size': 2**26},
        dependent_task_list=[download_task],
        task_name='optimize raster')

    task_graph.close()
    task_graph.join()
