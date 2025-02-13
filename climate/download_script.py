import os
import requests
import click

# Configuration
default_output_dir = "./outputs"

# Base URL patterns and filenames
base_urls = [
    {
        "url": "https://esgf-data1.llnl.gov/thredds/fileServer/css03_data/CMIP6/ScenarioMIP/NCAR/CESM2/ssp{scenario}/r11i1p1f1/Amon/{variable}/gn/v20200528/{variable}_Amon_CESM2_ssp{scenario}_r11i1p1f1_gn_201501-206412.nc",
        "filename": "{variable}_Amon_CESM2_ssp{scenario}_r11i1p1f1_gn_201501-206412.nc",
    },
    {
        "url": "https://esgf-data1.llnl.gov/thredds/fileServer/css03_data/CMIP6/ScenarioMIP/NCAR/CESM2/ssp{scenario}/r10i1p1f1/Amon/{variable}/gn/v20200528/{variable}_Amon_CESM2_ssp{scenario}_r10i1p1f1_gn_201501-206412.nc",
        "filename": "{variable}_Amon_CESM2_ssp{scenario}_r10i1p1f1_gn_201501-206412.nc",
    },
    {
        "url": "https://esgf-data1.llnl.gov/thredds/fileServer/css03_data/CMIP6/ScenarioMIP/NCAR/CESM2/ssp{scenario}/r4i1p1f1/Amon/{variable}/gn/v20200528/{variable}_Amon_CESM2_ssp{scenario}_r4i1p1f1_gn_201501-206412.nc",
        "filename": "{variable}_Amon_CESM2_ssp{scenario}_r4i1p1f1_gn_201501-206412.nc",
    },
    {
        "url": "https://aims3.llnl.gov/thredds/fileServer/css03_data/CMIP6/ScenarioMIP/CNRM-CERFACS/CNRM-CM6-1/ssp{scenario}/r4i1p1f2/Amon/{variable}/gr/v20190410/{variable}_Amon_CNRM-CM6-1_ssp{scenario}_r4i1p1f2_gr_201501-210012.nc",
        "filename": "{variable}_Amon_CNRM-CM6-1_ssp{scenario}_r4i1p1f2_gr_201501-210012.nc",
    },
    {
        "url": "https://aims3.llnl.gov/thredds/fileServer/css03_data/CMIP6/ScenarioMIP/CNRM-CERFACS/CNRM-CM6-1/ssp{scenario}/r6i1p1f2/Amon/{variable}/gr/v20190410/{variable}_Amon_CNRM-CM6-1_ssp{scenario}_r6i1p1f2_gr_201501-210012.nc",
        "filename": "{variable}_Amon_CNRM-CM6-1_ssp{scenario}_r6i1p1f2_gr_201501-210012.nc",
    },
]

variables = ["tas", "pr", "evspsbl"]
scenarios = ["585", "245", "126"]

def download_file(url, output_path, file_index, total_files):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    progress = (downloaded / total_size) * 100 if total_size > 0 else 0
                    print(f"File {file_index}/{total_files}: {output_path} - {progress:.2f}% completed", end='\r')

        print(f"\nDownloaded: {output_path} ({file_index}/{total_files})")
    except Exception as e:
        print(f"\nFailed to download {url}: {e}")

@click.command()
@click.option('--output_dir', default=default_output_dir, help='Directory to save downloaded files')
def download_data(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    file_list = [(entry, variable, scenario) for entry in base_urls for variable in variables for scenario in scenarios]
    total_files = len(file_list)

    for index, (entry, variable, scenario) in enumerate(file_list, start=1):
        file_url = entry["url"].format(scenario=scenario, variable=variable)
        file_name = entry["filename"].format(scenario=scenario, variable=variable)
        output_path = os.path.join(output_dir, file_name)
        download_file(file_url, output_path, index, total_files)

if __name__ == '__main__':
    download_data()
