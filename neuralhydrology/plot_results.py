"""Plot model run results (observed & simulated)

Requires matplotlib and xarray packages
"""

import argparse

import matplotlib.pyplot as plt
import xarray as xr

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Plot NueralHydrology results file. Requires xarray & matplotlib')
    parser.add_argument('results_file', help='test_results.nc file for basin/model')
    args = parser.parse_args()

    ds = xr.open_dataset(args.results_file)
    print(ds)

    qobs = ds['QObs(mm/d)_obs']
    qsim = ds['QObs(mm/d)_sim']

    px = 1/plt.rcParams['figure.dpi'] # inches per pixel
    fig, ax = plt.subplots(figsize=(800*px, 600*px))
    ax.plot(qobs['date'], qobs, label='Observed')
    ax.plot(qsim['date'], qsim, label='Simulated')
    ax.set_ylabel("Discharge (mm/d)")
    ax.set_title(f"Basin {ds.attrs['basin']}/{ds.attrs['run']} - NSE {ds.attrs['NSE']:.3f}")
    ax.legend()
    plt.show()
