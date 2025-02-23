#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

from keplergl import KeplerGl
from sedona.maps.SedonaKepler import SedonaKepler
from tests.test_base import TestBase
from tests import mixed_wkt_geometry_input_location
from tests import csv_point_input_location
import geopandas as gpd


class TestVisualization(TestBase):
    """ _repr_html() creates a html encoded string of the current map data, can be used to assert data equality """

    def test_basic_map_creation(self):
        sedona_kepler_map = SedonaKepler.create_map()
        kepler_map = KeplerGl()
        assert sedona_kepler_map.config == kepler_map.config

    def test_map_creation_with_df(self):
        polygon_wkt_df = self.spark.read.format("csv"). \
            option("delimiter", "\t"). \
            option("header", "false"). \
            load(mixed_wkt_geometry_input_location)

        polygon_wkt_df.createOrReplaceTempView("polygontable")
        polygon_df = self.spark.sql("select ST_GeomFromWKT(polygontable._c0) as countyshape from polygontable")
        polygon_gdf = gpd.GeoDataFrame(data=polygon_df.toPandas(), geometry="countyshape")
        polygon_gdf_renamed = polygon_gdf.rename(columns={"countyshape": "geometry"})

        sedona_kepler_map = SedonaKepler.create_map(df=polygon_df, name="data_1", geometry_col="countyshape")
        kepler_map = KeplerGl()
        kepler_map.add_data(data=polygon_gdf_renamed, name="data_1")

        assert sedona_kepler_map._repr_html_() == kepler_map._repr_html_()
        assert sedona_kepler_map.config == kepler_map.config

    def test_df_addition(self):
        polygon_wkt_df = self.spark.read.format("csv"). \
            option("delimiter", "\t"). \
            option("header", "false"). \
            load(mixed_wkt_geometry_input_location)

        polygon_wkt_df.createOrReplaceTempView("polygontable")

        polygon_df = self.spark.sql("select ST_GeomFromWKT(polygontable._c0) as countyshape from polygontable")
        polygon_gdf = gpd.GeoDataFrame(data=polygon_df.toPandas(), geometry="countyshape")
        polygon_gdf_renamed = polygon_gdf.rename(columns={"countyshape": "geometry"})

        sedona_kepler_empty_map = SedonaKepler.create_map()
        SedonaKepler.add_df(sedona_kepler_empty_map, polygon_df, name="data_1", geometry_col="countyshape")

        kepler_map = KeplerGl()
        kepler_map.add_data(polygon_gdf_renamed, name="data_1")

        assert sedona_kepler_empty_map._repr_html_() == kepler_map._repr_html_()
        assert sedona_kepler_empty_map.config == kepler_map.config

    def test_adding_multiple_datasets(self):
        config = {'version': 'v1',
                  'config': {'visState': {'filters': [],
                                          'layers': [{'id': 'ikzru0t',
                                                      'type': 'geojson',
                                                      'config': {'dataId': 'AirportCount',
                                                                 'label': 'AirportCount',
                                                                 'color': [218, 112, 191],
                                                                 'highlightColor': [252, 242, 26, 255],
                                                                 'columns': {'geojson': 'geometry'},
                                                                 'isVisible': True,
                                                                 'visConfig': {'opacity': 0.8,
                                                                               'strokeOpacity': 0.8,
                                                                               'thickness': 0.5,
                                                                               'strokeColor': [18, 92, 119],
                                                                               'colorRange': {
                                                                                   'name': 'Uber Viz Sequential 6',
                                                                                   'type': 'sequential',
                                                                                   'category': 'Uber',
                                                                                   'colors': ['#E6FAFA',
                                                                                              '#C1E5E6',
                                                                                              '#9DD0D4',
                                                                                              '#75BBC1',
                                                                                              '#4BA7AF',
                                                                                              '#00939C',
                                                                                              '#108188',
                                                                                              '#0E7077']},
                                                                               'strokeColorRange': {
                                                                                   'name': 'Global Warming',
                                                                                   'type': 'sequential',
                                                                                   'category': 'Uber',
                                                                                   'colors': ['#5A1846',
                                                                                              '#900C3F',
                                                                                              '#C70039',
                                                                                              '#E3611C',
                                                                                              '#F1920E',
                                                                                              '#FFC300']},
                                                                               'radius': 10,
                                                                               'sizeRange': [0, 10],
                                                                               'radiusRange': [0, 50],
                                                                               'heightRange': [0, 500],
                                                                               'elevationScale': 5,
                                                                               'enableElevationZoomFactor': True,
                                                                               'stroked': False,
                                                                               'filled': True,
                                                                               'enable3d': False,
                                                                               'wireframe': False},
                                                                 'hidden': False,
                                                                 'textLabel': [{'field': None,
                                                                                'color': [255, 255, 255],
                                                                                'size': 18,
                                                                                'offset': [0, 0],
                                                                                'anchor': 'start',
                                                                                'alignment': 'center'}]},
                                                      'visualChannels': {'colorField': {'name': 'AirportCount',
                                                                                        'type': 'integer'},
                                                                         'colorScale': 'quantize',
                                                                         'strokeColorField': None,
                                                                         'strokeColorScale': 'quantile',
                                                                         'sizeField': None,
                                                                         'sizeScale': 'linear',
                                                                         'heightField': None,
                                                                         'heightScale': 'linear',
                                                                         'radiusField': None,
                                                                         'radiusScale': 'linear'}}],
                                          'interactionConfig': {
                                              'tooltip': {'fieldsToShow': {'AirportCount': [{'name': 'NAME_EN',
                                                                                             'format': None},
                                                                                            {'name': 'AirportCount',
                                                                                             'format': None}]},
                                                          'compareMode': False,
                                                          'compareType': 'absolute',
                                                          'enabled': True},
                                              'brush': {'size': 0.5, 'enabled': False},
                                              'geocoder': {'enabled': False},
                                              'coordinate': {'enabled': False}},
                                          'layerBlending': 'normal',
                                          'splitMaps': [],
                                          'animationConfig': {'currentTime': None, 'speed': 1}},
                             'mapState': {'bearing': 0,
                                          'dragRotate': False,
                                          'latitude': 56.422456606624316,
                                          'longitude': 9.778836615231771,
                                          'pitch': 0,
                                          'zoom': 0.4214991225736964,
                                          'isSplit': False},
                             'mapStyle': {'styleType': 'dark',
                                          'topLayerGroups': {},
                                          'visibleLayerGroups': {'label': True,
                                                                 'road': True,
                                                                 'border': False,
                                                                 'building': True,
                                                                 'water': True,
                                                                 'land': True,
                                                                 '3d building': False},
                                          'threeDBuildingColor': [9.665468314072013,
                                                                  17.18305478057247,
                                                                  31.1442867897876],
                                          'mapStyles': {}}}}
        polygon_wkt_df = self.spark.read.format("csv"). \
            option("delimiter", "\t"). \
            option("header", "false"). \
            load(mixed_wkt_geometry_input_location)

        point_csv_df = self.spark.read.format("csv"). \
            option("delimiter", ","). \
            option("header", "false"). \
            load(csv_point_input_location)

        point_csv_df.createOrReplaceTempView("pointtable")
        point_df = self.spark.sql("select ST_Point(cast(pointtable._c0 as Decimal(24,20)), cast(pointtable._c1 as Decimal(24,20))) as arealandmark from pointtable")
        polygon_wkt_df.createOrReplaceTempView("polygontable")
        polygon_df = self.spark.sql("select ST_GeomFromWKT(polygontable._c0) as countyshape from polygontable")

        sedona_kepler_map = SedonaKepler.create_map(df=polygon_df, name="data_1", geometry_col="countyshape", config=config)
        # SedonaKepler.add_df(sedona_kepler_map, polygon_df, "data_1", "countyshape")
        SedonaKepler.add_df(sedona_kepler_map, point_df, name="data_2", geometry_col="arealandmark")

        polygon_gdf = gpd.GeoDataFrame(data=polygon_df.toPandas(), geometry="countyshape")
        polygon_gdf_renamed = polygon_gdf.rename(columns={"countyshape": "geometry"})
        point_gdf = gpd.GeoDataFrame(data=point_df.toPandas(), geometry="arealandmark")
        point_gdf_renamed = point_gdf.rename(columns={"arealandmark": "geometry"})

        kepler_map = KeplerGl(config=config)
        kepler_map.add_data(polygon_gdf_renamed, "data_1")
        kepler_map.add_data(point_gdf_renamed, name="data_2")

        assert sedona_kepler_map._repr_html_() == kepler_map._repr_html_()
        assert sedona_kepler_map.config == kepler_map.config
