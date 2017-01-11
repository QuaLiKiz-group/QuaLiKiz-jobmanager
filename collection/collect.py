"""
Copyright Dutch Institute for Fundamental Energy Research (2016)
Contributors: Karel van de Plassche (karelvandeplassche@gmail.com)
License: CeCILL v2.1

Merge together multiple netCDF files. It assumes a folder structure
as generated by copy_hsi.sh
"""

import xarray as xr; import glob; import os;
import numpy as np
from IPython import embed
from qualikiz_tools.qualikiz_io.outputfiles import sort_dims

mergelist=['dfe_GB', 'dfi_GB', 'pfe_GB', 'pfi_GB', 'efe_GB', 'efi_GB',
           'ome_GB', 'gam_GB', 'vte_GB', 'vti_GB', 'vce_GB', 'vci_GB',
           'cke', 'cki']

for Zeff_folder in ['Zeff1.0', 'Zeff1.3', 'Zeff1.7', 'Zeff2.2', 'Zeff3.0']:
    if not os.path.isdir(Zeff_folder):
        continue
    dsNs = []
    for Nustar_folder in os.listdir(Zeff_folder):
        dsTs = []
        for TiTe_folder in os.listdir(os.path.join(Zeff_folder, Nustar_folder)):
            dsxs = []
            for file in glob.iglob(os.path.join(Zeff_folder, Nustar_folder, TiTe_folder) + '/*.nc'):
                print(file)
                ds = xr.open_dataset(file)
                dellist = []
                for var in ds.data_vars:
                    if var not in mergelist:
                        dellist.append(var)
                for var in dellist:
                    del ds[var]
                encoding = {}

                dsxs.append(ds.copy(deep=True))
                del ds
            if len(dsxs) > 0:
                dsTs.append(xr.concat(dsxs, dim='x'))
                del dsxs
        if len(dsTs) > 0:
            dsNs.append(xr.concat(dsTs, dim='Ti_Te'))
            del dsTs
    if len(dsNs) > 0:
        dsZs = xr.concat(dsNs, dim='Nustar')
        print('Collected data, sending to file')
        for var in dsZs:
            encoding[var] = {'dtype': 'float32'}
        #for var in ['Nustar', 'Ti_Te', 'x']:
            #dsZs[var] = np.sort(dsZs[var])
        dsZs = sort_dims(dsZs)
        dsZs = dsZs.transpose('Ati', 'Ate', 'An', 'qx', 'smag', 'x', 'Ti_Te', 'Nustar', 'kthetarhos', 'nions', 'numsols')
        dsZs.to_netcdf(Zeff_folder + '.nc', encoding=encoding)
        del dsNs
        del dsZs