"""Report pixel raster stats of unique LULC codes against another raster."""
import logging

import pygeoprocessing

logging.basicConfig(
    level=logging.DEBUG,
    format=(
        '%(asctime)s (%(relativeCreated)d) %(processName)s %(levelname)s '
        '%(name)s [%(funcName)s:%(lineno)d] %(message)s'))
LOGGER = logging.getLogger(__name__)


if __name__ == '__main__':
    lulc_raster_path = 'lulc_clip_md5_47ec7ed92e0fdef77d3c0bf3909c71a8.tif'
    biomass_raster_path = \
        'biomass_clip_md5_f80fd87381a5c279a65d9f5325361139.tif'

    lulc_raster_info = pygeoprocessing.get_raster_info(lulc_raster_path)
    biomass_raster_info = pygeoprocessing.get_raster_info(biomass_raster_path)

    workspace_dir = 'raster_by_raster_workspace'

    # TODO: ensure lulc and biomass are aligned

    # TODO: calcualte stats by lulc vs. biomass

    #   report: 1 line per unique lulc code,
    print('line: lulc code, pixel count, biomass sum, average biomass')
