"""Demo some hydrology."""
import logging

import pygeoprocessing.routing

logging.basicConfig(
    level=logging.DEBUG,
    format=(
        '%(asctime)s (%(relativeCreated)d) %(processName)s %(levelname)s '
        '%(name)s [%(funcName)s:%(lineno)d] %(message)s'))
LOGGER = logging.getLogger(__name__)

if __name__ == '__main__':
    raster_path = 'DEM_clip.tif'
    raster_info = pygeoprocessing.get_raster_info(raster_path)
    print(f"{raster_path} is {raster_info['raster_size']} big")

    mfd_flow_raster_path = 'mfd_flow_dir.tif'
    pygeoprocessing.routing.flow_dir_mfd(
        (raster_path, 1), mfd_flow_raster_path)

    flow_accum_mfd_path = 'mfd_flow_accum.tif'
    pygeoprocessing.routing.flow_accumulation_mfd(
        (mfd_flow_raster_path, 1), flow_accum_mfd_path)

    stream_raster_path = 'stream.tif'

    pygeoprocessing.routing.extract_streams_mfd(
        (flow_accum_mfd_path, 1), (mfd_flow_raster_path, 1),
        100, stream_raster_path)
