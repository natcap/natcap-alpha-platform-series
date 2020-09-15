"""Demo some clipping."""
import logging

import pygeoprocessing

logging.basicConfig(
    level=logging.DEBUG,
    format=(
        '%(asctime)s (%(relativeCreated)d) %(processName)s %(levelname)s '
        '%(name)s [%(funcName)s:%(lineno)d] %(message)s'))
LOGGER = logging.getLogger(__name__)

if __name__ == '__main__':
    raster_path = 'DEM_md5_53d4998eec75d803a318fafd28c40a3e.tif'
    aoi_vector_path = 'aoi.gpkg'
    raster_info = pygeoprocessing.get_raster_info(raster_path)
    vector_info = pygeoprocessing.get_vector_info(aoi_vector_path)

    raster_projected_bounding_box = pygeoprocessing.transform_bounding_box(
        vector_info['bounding_box'], vector_info['projection_wkt'],
        raster_info['projection_wkt'])

    target_clipped_raster_path = 'DEM_clip.tif'
    pygeoprocessing.warp_raster(
        raster_path, raster_info['pixel_size'], target_clipped_raster_path,
        'near', target_bb=raster_projected_bounding_box)
