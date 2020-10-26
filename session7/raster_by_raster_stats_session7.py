"""Report pixel raster stats of unique LULC codes against another raster."""
import collections
import logging

from osgeo import gdal
import pygeoprocessing
import numpy

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

    LOGGER.debug(str(lulc_raster_info))
    LOGGER.info(str(biomass_raster_info))

    workspace_dir = 'raster_by_raster_workspace'

    # TODO: ensure lulc and biomass are aligned
    # TODO: calculate stats by lulc vs. biomass

    unique_lulc_codes = set()
    lulc_code_count = collections.defaultdict(int)

    lulc_pixel_total_count = (
        lulc_raster_info['raster_size'][0] *
        lulc_raster_info['raster_size'][1])
    lulc_pixels_processed = 0

    lulc_raster = gdal.OpenEx(lulc_raster_path)
    lulc_band = lulc_raster.GetRasterBand(1)

    biomass_raster = gdal.OpenEx(biomass_raster_path)
    biomass_band = biomass_raster.GetRasterBand(1)

    for offset_dict in pygeoprocessing.iterblocks(
            (lulc_raster_path, 1), offset_only=True):

        # data_block = lulc_band.ReadAsArray(
        #     xoff=offset_dict['xoff'],
        #     yoff=offset_dict['yoff'],
        #     win_xsize=offset_dict['win_xsize'],
        #     win_ysize=offset_dict['win_ysize'])

        lulc_block = lulc_band.ReadAsArray(
            **offset_dict)
        biomass_block = biomass_band.ReadAsArray(
            **offset_dict)

        LOGGER.debug(biomass_block)

        unique_lulc_codes.update(numpy.unique(lulc_block))

        for lulc_code in numpy.unique(lulc_block):
            lulc_code_count[lulc_code] += numpy.count_nonzero(
                lulc_block == lulc_code)

        LOGGER.debug(offset_dict)

        lulc_pixels_processed += (
            offset_dict['win_xsize'] * offset_dict['win_ysize'])

        LOGGER.info(
            f'{lulc_pixels_processed/lulc_pixel_total_count*100:.2f}% complete')

    LOGGER.debug(f'unique_lulc_codes: {list(sorted(unique_lulc_codes))}')
    LOGGER.debug(f'lulc code counts: {lulc_code_count}')

    #   report: 1 line per unique lulc code,
    print('line: lulc code, pixel count, biomass sum, average biomass')
