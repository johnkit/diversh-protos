"""Inputs csv file and generates geojson file."""

import argparse

import pandas as pd
import geopandas as gpd

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load csv and generate geopandas dataframe')
    parser.add_argument('input_file', help='csv file with lat/lon coordinates')
    parser.add_argument('-l', '--lat_column', help='latitude column name', default='latitude')
    parser.add_argument('-m', '--lon_column', help='longitude column name', default='longitude')
    parser.add_argument('-o', '--output_file', help='output filename (.geojson)')
    args = parser.parse_args()

    df = pd.read_csv(args.input_file)
    df['geometry'] = gpd.points_from_xy(df[args.lon_column], df[args.lat_column])
    gdf = gpd.GeoDataFrame(df, crs="EPSG:4326")

    print(gdf)
    if args.output_file:
        gdf.to_file(args.output_file, driver='GeoJSON')
        print(f'Wrote {args.output_file}')
