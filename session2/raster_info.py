"""Demo some raster info."""
import pygeoprocessing

if __name__ == '__main__':
    raster_path = 'LULC_2000_md5_e0523f6f5c4bc8e9ee4865958fe876e0.tif'
    raster_info = pygeoprocessing.get_raster_info(raster_path)
    print(raster_info)
