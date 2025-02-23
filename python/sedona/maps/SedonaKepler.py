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
import geopandas as gpd


class SedonaKepler:

    @classmethod
    def create_map(cls, df=None, name="unnamed", geometry_col="geometry", config=None):
        """
        Creates a map visualization using kepler, optionally taking a sedona dataFrame as data input
        :param df: [Optional] SedonaDataFrame to plot on the map
        :param name: [Optional] Name to be associated with the given dataframe, if a df is passed with no name, a default name of 'unnamed' is set for it.
        :param geometry_col: [Optional] Custom name of geometry column in the sedona data frame,
                            if no name is provided, it is assumed that the column has the default name 'geometry'.
        :param config: [Optional] A map config to be applied to the rendered map
        :return: A map object
        """
        kepler_map = KeplerGl()
        if df is not None:
            SedonaKepler.add_df(kepler_map, df, name, geometry_col)

        if config is not None:
            kepler_map.config = config

        return kepler_map

    @classmethod
    def add_df(cls, kepler_map, df, name="unnamed", geometry_col="geometry"):
        """
        Adds a SedonaDataFrame to a given map object.
        :param kepler_map: Map object to add SedonaDataFrame to
        :param df: SedonaDataFrame to add
        :param name: [Optional] Name to assign to the dataframe, default name assigned is 'unnamed'
        :param geometry_col: [Optional] Custom name of geometry_column if any, if no name is provided, a default name of 'geometry' is assumed.
        :return: Does not return anything, adds df directly to the given map object
        """
        geo_df = SedonaKepler._convert_to_gdf(df, geometry_col)
        kepler_map.add_data(geo_df, name=name)

    @classmethod
    def _convert_to_gdf(cls, df, geometry_col="geometry"):
        """
        Converts a SedonaDataFrame to a GeoPandasDataFrame and also renames geometry column to a standard name of 'geometry'
        :param df: SedonaDataFrame to convert
        :param geometry_col: [Optional]
        :return:
        """
        pandas_df = df.toPandas()
        geo_df = gpd.GeoDataFrame(pandas_df, geometry=geometry_col)
        if geometry_col != "geometry":
            geo_df = geo_df.rename(columns={geometry_col: "geometry"})
        return geo_df
