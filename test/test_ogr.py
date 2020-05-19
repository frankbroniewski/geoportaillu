import unittest
from osgeo import ogr
from osgeo import osr
from osgeo.gdal import VersionInfo
from osgeo.osr import OAMS_TRADITIONAL_GIS_ORDER

class TestServices(unittest.TestCase):
    
        def test_transformation(self):
            """
            Test for CRS and axis order
            
            Before GDAL 3.0, the OGRSpatialReference class did not honour the 
            axis order mandated by the authority defining a CRS and consequently 
            stripped axis order information from the WKT string when the order 
            was latitude first, longitude second. [...]
            Starting with GDAL 3.0, the axis order mandated by the authority 
            defining a CRS is by default honoured by the 
            OGRCoordinateTransformation class, and always exported in WKT1.
            (https://gdal.org/tutorials/osr_api_tut.html)
            
            Input geometry: {'coordinates': [6.1409004235, 49.6127108119], 'type': 'Point'}
            Output geometry: { "type": "Point", "coordinates": [ 78032.625859561609104, 75343.040142811907572 ] }
            
            // 'urn:ogc:def:crs:OGC:1.3:CRS84'
            """
            
            # correctly transformed geometry X/Y (LUREF epsg:2169)
            target_geom = ogr.CreateGeometryFromJson('{ "type": "Point", "coordinates": [ 78032.625859561609104, 75343.040142811907572 ] }')
            
            # source geometry with LON/LAT coordinates
            ogr_geom = ogr.CreateGeometryFromJson('{"coordinates": [6.1409004235, 49.6127108119], "type": "Point"}')
            
            source_srs = osr.SpatialReference()
            source_srs.ImportFromEPSG(4326)

            target_srs = osr.SpatialReference()
            target_srs.ImportFromEPSG(2169)
            
            if VersionInfo().startswith('3'):
                source_srs.SetAxisMappingStrategy(OAMS_TRADITIONAL_GIS_ORDER)            
                target_srs.SetAxisMappingStrategy(OAMS_TRADITIONAL_GIS_ORDER)

            transformation = osr.CoordinateTransformation(source_srs, target_srs)
            ogr_geom.Transform(transformation)
            
            self.assertEqual(target_geom.ExportToWkt(), ogr_geom.ExportToWkt())
