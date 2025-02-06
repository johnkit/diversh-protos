"""Extract locations of TVA Hydro power stations.

Parses html file saved from public argis page, listing TVA dams
https://www.arcgis.com/home/item.html?id=b7d45f7a0d1243e3ad10fef60f86e927&view=list&sortOrder=desc&sortField=defaultFSOrder&showFilters=true#data

Uses Beautiful Soup library
On turtleland4, use ~/.py3-venv/misc
"""

import csv
from dataclasses import dataclass
import pathlib
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup

CSV_HEADER = ['name', 'url', 'latitude', 'longitude']

@dataclass
class InputData:
    """Contents of one row in html table"""
    name: str
    google_url: str
    apple_url: str
    url: str
    hydro_type: str
    object_id: int

    def to_csv(self):
        """Parse google_url to get lat/lon coordinates"""
        parsed_url = urlparse(self.google_url)
        query_dict = parse_qs(parsed_url.query)
        lat_lon_str = query_dict['q'][0]
        lat_lon_split = lat_lon_str.split(',')
        lat_lon_float = [float(l) for l in lat_lon_split]
        lat, lon = lat_lon_float
        return [self.name, self.url, lat, lon]


if __name__ == '__main__':
    # Load html file
    this_dir = pathlib.Path(__file__).parent
    path = this_dir / 'TVA_Dams_Hosted - Data.html'
    html_content = ''
    with open(path) as fp:
        html_content = fp.read()

    # Use list to store output csv data
    csv_table = list()

    # Use BeautifulSoup to parse html
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = list(soup.find_all('table'))
    # print(f'{len(tables)} tables')
    for table in tables:
        tds = list(table.find_all('td'))
        if len(tds) == 6:
            fields = [td.get_text() for td in tds]
            input_data = InputData(*fields)
            if input_data.hydro_type == 'Power':
                csv_row = input_data.to_csv()
                csv_table.append(csv_row)

    # Sort csv_table by name
    csv_table.sort(key=lambda row: row[0])
    print(csv_table)

    csv_filename = 'tva_hydro.csv'
    with open(csv_filename, 'w') as fp:
        writer = csv.writer(fp)
        writer.writerow(CSV_HEADER)
        writer.writerows(csv_table)
        print(f'Wrote {csv_filename}')
