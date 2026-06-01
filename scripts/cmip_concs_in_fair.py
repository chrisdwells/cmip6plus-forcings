import matplotlib.pyplot as plt

from fair import FAIR
from fair.io import read_properties
from fair.interface import fill, initialise
import os
import xarray as xr

import glob
import pickle

# this script plots the concentration and forcings across cmip generations 
# (6. 6plus, 7) for all individual species.
# for cmip6 we plot future scenarios too, for comparison of the historical
# difference with the future scenario range.

datadir = '../data'
timestep='yr'

f_ssps = FAIR()

f_ssps.define_time(1750, 2050, 1)

scenarios = ['ssp119', 'ssp126', 'ssp245', 'ssp370', 'ssp585']
f_ssps.define_scenarios(scenarios)

configs = ['test']
f_ssps.define_configs(configs)

species, properties = read_properties()

f_ssps.define_species(species, properties)

f_ssps.allocate()
f_ssps.fill_species_configs()
f_ssps.fill_from_rcmip()

initialise(f_ssps.concentration, f_ssps.species_configs['baseline_concentration'])
initialise(f_ssps.forcing, 0)
initialise(f_ssps.temperature, 0)
initialise(f_ssps.cumulative_emissions, 0)
initialise(f_ssps.airborne_emissions, 0)

capacities = [4.22335014, 16.5073541, 86.1841127]
kappas = [1.31180598, 2.61194068, 0.92986733]
epsilon = 1.29020599
fill(f_ssps.climate_configs['ocean_heat_capacity'], capacities)
fill(f_ssps.climate_configs['ocean_heat_transfer'], kappas)
fill(f_ssps.climate_configs['deep_ocean_efficacy'], epsilon)

f_ssps.run()

#%%

# dictionaries from cmip gen to FaIR; opposite of in script 02
# we don't use the -eq species as we have them individually
cmip6_to_fair = {
    'mole_fraction_of_carbon_dioxide_in_air':'CO2',
    'mole_fraction_of_methane_in_air':'CH4',
    'mole_fraction_of_nitrous_oxide_in_air':'N2O',
    'mole_fraction_of_c2f6_in_air':'C2F6',
    'mole_fraction_of_c3f8_in_air':'C3F8',
    'mole_fraction_of_c4f10_in_air':'C4F10',
    'mole_fraction_of_c5f12_in_air':'C5F12',
    'mole_fraction_of_c6f14_in_air':'C6F14',
    'mole_fraction_of_c7f16_in_air':'C7F16',
    'mole_fraction_of_c8f18_in_air':'C8F18',
    'mole_fraction_of_c_c4f8_in_air':'c-C4F8',
    'mole_fraction_of_carbon_tetrachloride_in_air':'CCl4',
    'mole_fraction_of_cf4_in_air':'CF4',
    'mole_fraction_of_cfc11_in_air':'CFC-11',
    'mole_fraction_of_cfc113_in_air':'CFC-113',
    'mole_fraction_of_cfc114_in_air':'CFC-114',
    'mole_fraction_of_cfc115_in_air':'CFC-115',
    'mole_fraction_of_cfc12_in_air':'CFC-12',
    'mole_fraction_of_ch2cl2_in_air':'CH2Cl2',
    'mole_fraction_of_methyl_bromide_in_air':'CH3Br',
    'mole_fraction_of_ch3ccl3_in_air':'CH3CCl3',
    'mole_fraction_of_methyl_chloride_in_air':'CH3Cl',
    'mole_fraction_of_chcl3_in_air':'CHCl3',
    'mole_fraction_of_halon1211_in_air':'Halon-1211',
    'mole_fraction_of_halon1301_in_air':'Halon-1301',
    'mole_fraction_of_halon2402_in_air':'Halon-2402',
    'mole_fraction_of_hcfc141b_in_air':'HCFC-141b',
    'mole_fraction_of_hcfc142b_in_air':'HCFC-142b',
    'mole_fraction_of_hcfc22_in_air':'HCFC-22',
    'mole_fraction_of_hfc125_in_air':'HFC-125',
    'mole_fraction_of_hfc134a_in_air':'HFC-134a',
    'mole_fraction_of_hfc143a_in_air':'HFC-143a',
    'mole_fraction_of_hfc152a_in_air':'HFC-152a',
    'mole_fraction_of_hfc227ea_in_air':'HFC-227ea',
    'mole_fraction_of_hfc23_in_air':'HFC-23',
    'mole_fraction_of_hfc236fa_in_air':'HFC-236fa',
    'mole_fraction_of_hfc245fa_in_air':'HFC-245fa',
    'mole_fraction_of_hfc32_in_air':'HFC-32',
    'mole_fraction_of_hfc365mfc_in_air':'HFC-365mfc',
    'mole_fraction_of_hfc4310mee_in_air':'HFC-4310mee',
    'mole_fraction_of_nf3_in_air':'NF3',
    'mole_fraction_of_sf6_in_air':'SF6',
    'mole_fraction_of_so2f2_in_air':'SO2F2',
    # 'mole_fraction_of_cfc11eq_in_air':'CFC11eq',
    # 'mole_fraction_of_cfc12eq_in_air':'CFC12eq',
    # 'mole_fraction_of_hfc134aeq_in_air':'HFC-134aeq',
        }


cmip6plus_to_fair = {
    'co2':'CO2',
    'ch4':'CH4',
    'n2o':'N2O',
    'pfc116':'C2F6',
    'pfc218':'C3F8',
    'pfc3110':'C4F10',
    'pfc4112':'C5F12',
    'pfc5114':'C6F14',
    'pfc6116':'C7F16',
    'pfc7118':'C8F18',
    'pfc318':'c-C4F8',
    'ccl4':'CCl4',
    'cf4':'CF4',
    'cfc11':'CFC-11',
    'cfc113':'CFC-113',
    'cfc114':'CFC-114',
    'cfc115':'CFC-115',
    'cfc12':'CFC-12',
    'ch2cl2':'CH2Cl2',
    'ch3br':'CH3Br',
    'hcc140a':'CH3CCl3',
    'ch3cl':'CH3Cl',
    'chcl3':'CHCl3',
    'halon1211':'Halon-1211',
    'halon1301':'Halon-1301',
    'halon2402':'Halon-2402',
    'hcfc141b':'HCFC-141b',
    'hcfc142b':'HCFC-142b',
    'hcfc22':'HCFC-22',
    'hfc125':'HFC-125',
    'hfc134a':'HFC-134a',
    'hfc143a':'HFC-143a',
    'hfc152a':'HFC-152a',
    'hfc227ea':'HFC-227ea',
    'hfc23':'HFC-23',
    'hfc236fa':'HFC-236fa',
    'hfc245fa':'HFC-245fa',
    'hfc32':'HFC-32',
    'hfc365mfc':'HFC-365mfc',
    'hfc4310mee':'HFC-4310mee',
    'nf3':'NF3',
    'sf6':'SF6',
    'so2f2':'SO2F2',
    # 'cfc11eq':'CFC11eq',
    # 'cfc12eq':'CFC12eq',
    # 'hfc134aeq':'HFC-134aeq',
        }

cmip7_to_fair = {
    'co2':'CO2',
    'ch4':'CH4',
    'n2o':'N2O',
    'c2f6':'C2F6',
    'c3f8':'C3F8',
    'c4f10':'C4F10',
    'c5f12':'C5F12',
    'c6f14':'C6F14',
    'c7f16':'C7F16',
    'c8f18':'C8F18',
    'cc4f8':'c-C4F8',
    'ccl4':'CCl4',
    'cf4':'CF4',
    'cfc11':'CFC-11',
    'cfc113':'CFC-113',
    'cfc114':'CFC-114',
    'cfc115':'CFC-115',
    'cfc12':'CFC-12',
    'ch2cl2':'CH2Cl2',
    'ch3br':'CH3Br',
    'ch3ccl3':'CH3CCl3',
    'ch3cl':'CH3Cl',
    'chcl3':'CHCl3',
    'halon1211':'Halon-1211',
    'halon1301':'Halon-1301',
    'halon2402':'Halon-2402',
    'hcfc141b':'HCFC-141b',
    'hcfc142b':'HCFC-142b',
    'hcfc22':'HCFC-22',
    'hfc125':'HFC-125',
    'hfc134a':'HFC-134a',
    'hfc143a':'HFC-143a',
    'hfc152a':'HFC-152a',
    'hfc227ea':'HFC-227ea',
    'hfc23':'HFC-23',
    'hfc236fa':'HFC-236fa',
    'hfc245fa':'HFC-245fa',
    'hfc32':'HFC-32',
    'hfc365mfc':'HFC-365mfc',
    'hfc4310mee':'HFC-4310mee',
    'nf3':'NF3',
    'sf6':'SF6',
    'so2f2':'SO2F2',
    # 'cfc11eq':'CFC11eq',
    # 'cfc12eq':'CFC12eq',
    # 'hfc134aeq':'HFC-134aeq',
        }

#%%

# run cmip6 w/o changing WMGHGs (CO2, CH4, N2O)
f_cmip6 = FAIR()

f_cmip6.define_time(1750, 2014, 1)

scenarios = ['ssp245']
f_cmip6.define_scenarios(scenarios)

configs = ['test']
f_cmip6.define_configs(configs)

species, properties = read_properties()

for cmip6_spec in cmip6_to_fair.keys():
    if cmip6_to_fair[cmip6_spec] not in ['CO2', 'CH4', 'N2O']:
        properties[cmip6_to_fair[cmip6_spec]]['input_mode'] = 'concentration'
        
f_cmip6.define_species(species, properties)

f_cmip6.allocate()
f_cmip6.fill_species_configs()
f_cmip6.fill_from_rcmip()

initialise(f_cmip6.concentration, f_cmip6.species_configs['baseline_concentration'])
initialise(f_cmip6.forcing, 0)
initialise(f_cmip6.temperature, 0)
initialise(f_cmip6.cumulative_emissions, 0)
initialise(f_cmip6.airborne_emissions, 0)

capacities = [4.22335014, 16.5073541, 86.1841127]
kappas = [1.31180598, 2.61194068, 0.92986733]
epsilon = 1.29020599
fill(f_cmip6.climate_configs['ocean_heat_capacity'], capacities)
fill(f_cmip6.climate_configs['ocean_heat_transfer'], kappas)
fill(f_cmip6.climate_configs['deep_ocean_efficacy'], epsilon)

for cmip6_spec in cmip6_to_fair.keys():
    
    if cmip6_to_fair[cmip6_spec] in ['CO2', 'CH4', 'N2O']:
        continue
    
    print(cmip6_spec)
    
    file = (
    f'{datadir}/cmip6/{timestep}/{cmip6_spec.replace("_","-")}'
    '_input4MIPs_GHGConcentrations_CMIP_UoM-CMIP-1-2-0_gr1-GMNHSH_0000-2014.nc'
        )
    
    with xr.open_dataset(file, decode_times=False) as ds:
            
            
        if ds.attrs["frequency"] == "yr":
            ds = ds.isel(time=slice(1, None))
        
        else:
            ds = ds.isel(time=slice(12, None))
        
        if ds["time"].attrs["units"] == "days since 0-1-1":
            ds["time"].attrs["units"] =  "days since 0001-1-1"
            old_attrs = ds["time"].attrs
            ds["time"] = ds["time"] - 365
            ds["time"].attrs = old_attrs
    
        ds = xr.decode_cf(ds, decode_times=True, use_cftime=True)
    
        da = ds[cmip6_spec]

        
        f_cmip6.concentration.loc[
            dict(specie=cmip6_to_fair[cmip6_spec])
        ][:,0,0] = da.sel(time=(slice('1750', '2015')), sector=0).rename({'time': 'timepoints'}).data 
        
        f_cmip6.species_configs['baseline_concentration'][
            0,f_cmip6.species.index(cmip6_to_fair[cmip6_spec])
            ] = f_cmip6.concentration[0,0,0,f_cmip6.species.index(cmip6_to_fair[cmip6_spec])]

        f_cmip6.species_configs['forcing_reference_concentration'][
            0,f_cmip6.species.index(cmip6_to_fair[cmip6_spec])
            ] = f_cmip6.concentration[0,0,0,f_cmip6.species.index(cmip6_to_fair[cmip6_spec])]
                

f_cmip6.run()

#%%

# run cmip6plus w/o changing WMGHGs (CO2, CH4, N2O)
f_cmip6plus = FAIR()

f_cmip6plus.define_time(1750, 2022, 1)

scenarios = ['ssp245']
f_cmip6plus.define_scenarios(scenarios)

configs = ['test']
f_cmip6plus.define_configs(configs)

species, properties = read_properties()


for cmip6plus_spec in cmip6plus_to_fair.keys():
    if cmip6plus_to_fair[cmip6plus_spec] not in ['CO2', 'CH4', 'N2O']:
        properties[cmip6plus_to_fair[cmip6plus_spec]]['input_mode'] = 'concentration'

f_cmip6plus.define_species(species, properties)

f_cmip6plus.allocate()
f_cmip6plus.fill_species_configs()
f_cmip6plus.fill_from_rcmip()

initialise(f_cmip6plus.concentration, f_cmip6plus.species_configs['baseline_concentration'])
initialise(f_cmip6plus.forcing, 0)
initialise(f_cmip6plus.temperature, 0)
initialise(f_cmip6plus.cumulative_emissions, 0)
initialise(f_cmip6plus.airborne_emissions, 0)

capacities = [4.22335014, 16.5073541, 86.1841127]
kappas = [1.31180598, 2.61194068, 0.92986733]
epsilon = 1.29020599
fill(f_cmip6plus.climate_configs['ocean_heat_capacity'], capacities)
fill(f_cmip6plus.climate_configs['ocean_heat_transfer'], kappas)
fill(f_cmip6plus.climate_configs['deep_ocean_efficacy'], epsilon)

units = {}

for cmip6plus_spec in cmip6plus_to_fair.keys():
    
    if cmip6plus_to_fair[cmip6plus_spec] in ['CO2', 'CH4', 'N2O']:
        continue

    print(cmip6plus_spec)
    
    data_folders = os.listdir(f"{datadir}/cmip6plus/{timestep}/{cmip6plus_spec}/gm/")
    if len(data_folders) > 1:
        print(f'{len(data_folders)} for {cmip6plus_spec}')
    data_folder = data_folders[0]

    files = os.listdir(f"{datadir}/cmip6plus/{timestep}/{cmip6plus_spec}/gm/{data_folder}/")

    if len(files) > 1:
        print(f'{len(files)} for {cmip6plus_spec}')

    file = f"{datadir}/cmip6plus/{timestep}/{cmip6plus_spec}/gm/{data_folder}/{files[0]}"

    
    with xr.open_dataset(file, use_cftime=True) as ds:
        ds.convert_calendar("proleptic_gregorian")
    
        da = ds[cmip6plus_spec]

        
        f_cmip6plus.concentration.loc[
            dict(specie=cmip6plus_to_fair[cmip6plus_spec])
        ][:,0,0] = da.sel(time=(slice('1750', '2022'))).rename({'time': 'timepoints'}).data 
        
        f_cmip6plus.species_configs['baseline_concentration'][
            0,f_cmip6plus.species.index(cmip6plus_to_fair[cmip6plus_spec])
            ] = f_cmip6plus.concentration[0,0,0,f_cmip6plus.species.index(cmip6plus_to_fair[cmip6plus_spec])]

        f_cmip6plus.species_configs['forcing_reference_concentration'][
            0,f_cmip6plus.species.index(cmip6plus_to_fair[cmip6plus_spec])
            ] = f_cmip6plus.concentration[0,0,0,f_cmip6plus.species.index(cmip6plus_to_fair[cmip6plus_spec])]
                
        
        units[cmip6plus_to_fair[cmip6plus_spec]] = da.attrs["units"]

f_cmip6plus.run()
#%%


# run cmip7 w/o changing WMGHGs (CO2, CH4, N2O)
f_cmip7 = FAIR()

f_cmip7.define_time(1750, 2022, 1)

scenarios = ['ssp245']
f_cmip7.define_scenarios(scenarios)

configs = ['test']
f_cmip7.define_configs(configs)

species, properties = read_properties()


for cmip7_spec in cmip7_to_fair.keys():
    if cmip7_to_fair[cmip7_spec] not in ['CO2', 'CH4', 'N2O']:
        properties[cmip7_to_fair[cmip7_spec]]['input_mode'] = 'concentration'

f_cmip7.define_species(species, properties)

f_cmip7.allocate()
f_cmip7.fill_species_configs()
f_cmip7.fill_from_rcmip()

initialise(f_cmip7.concentration, f_cmip7.species_configs['baseline_concentration'])
initialise(f_cmip7.forcing, 0)
initialise(f_cmip7.temperature, 0)
initialise(f_cmip7.cumulative_emissions, 0)
initialise(f_cmip7.airborne_emissions, 0)

capacities = [4.22335014, 16.5073541, 86.1841127]
kappas = [1.31180598, 2.61194068, 0.92986733]
epsilon = 1.29020599
fill(f_cmip7.climate_configs['ocean_heat_capacity'], capacities)
fill(f_cmip7.climate_configs['ocean_heat_transfer'], kappas)
fill(f_cmip7.climate_configs['deep_ocean_efficacy'], epsilon)

units = {}

for cmip7_spec in cmip7_to_fair.keys():
    
    if cmip7_to_fair[cmip7_spec] in ['CO2', 'CH4', 'N2O']:
        continue

    print(cmip7_spec)
    
    
    filelist = glob.glob(f"{datadir}/cmip7/{timestep}/{cmip7_spec}_*nc")
    
    with xr.open_mfdataset(filelist, use_cftime=True) as ds:
        ds.convert_calendar("proleptic_gregorian")
    
        da = ds[cmip7_spec]

        
        f_cmip7.concentration.loc[
            dict(specie=cmip7_to_fair[cmip7_spec])
        ][:,0,0] = da.sel(time=(slice('1750', '2022'))).rename({'time': 'timepoints'}).data 
        
        f_cmip7.species_configs['baseline_concentration'][
            0,f_cmip7.species.index(cmip7_to_fair[cmip7_spec])
            ] = f_cmip7.concentration[0,0,0,f_cmip7.species.index(cmip7_to_fair[cmip7_spec])]

        f_cmip7.species_configs['forcing_reference_concentration'][
            0,f_cmip7.species.index(cmip7_to_fair[cmip7_spec])
            ] = f_cmip7.concentration[0,0,0,f_cmip7.species.index(cmip7_to_fair[cmip7_spec])]
                
        
        units[cmip7_to_fair[cmip7_spec]] = da.attrs["units"]

f_cmip7.run()


#%%

# now run cmip6 w/ changing WMGHGs (CO2, CH4, N2O)

f_cmip6_inc_wmghgs = FAIR()

f_cmip6_inc_wmghgs.define_time(1750, 2014, 1)

scenarios = ['ssp245']
f_cmip6_inc_wmghgs.define_scenarios(scenarios)

configs = ['test']
f_cmip6_inc_wmghgs.define_configs(configs)

species, properties = read_properties()

for cmip6_spec in cmip6_to_fair.keys():
        properties[cmip6_to_fair[cmip6_spec]]['input_mode'] = 'concentration'
        

f_cmip6_inc_wmghgs.define_species(species, properties)

f_cmip6_inc_wmghgs.allocate()
f_cmip6_inc_wmghgs.fill_species_configs()
f_cmip6_inc_wmghgs.fill_from_rcmip()

initialise(f_cmip6_inc_wmghgs.concentration, f_cmip6_inc_wmghgs.species_configs['baseline_concentration'])
initialise(f_cmip6_inc_wmghgs.forcing, 0)
initialise(f_cmip6_inc_wmghgs.temperature, 0)
initialise(f_cmip6_inc_wmghgs.cumulative_emissions, 0)
initialise(f_cmip6_inc_wmghgs.airborne_emissions, 0)

capacities = [4.22335014, 16.5073541, 86.1841127]
kappas = [1.31180598, 2.61194068, 0.92986733]
epsilon = 1.29020599
fill(f_cmip6_inc_wmghgs.climate_configs['ocean_heat_capacity'], capacities)
fill(f_cmip6_inc_wmghgs.climate_configs['ocean_heat_transfer'], kappas)
fill(f_cmip6_inc_wmghgs.climate_configs['deep_ocean_efficacy'], epsilon)

for cmip6_spec in cmip6_to_fair.keys():
    
    print(cmip6_spec)
    
    file = (
    f'{datadir}/cmip6/{timestep}/{cmip6_spec.replace("_","-")}'
    '_input4MIPs_GHGConcentrations_CMIP_UoM-CMIP-1-2-0_gr1-GMNHSH_0000-2014.nc'
        )
    
    with xr.open_dataset(file, decode_times=False) as ds:
            
            
        if ds.attrs["frequency"] == "yr":
            ds = ds.isel(time=slice(1, None))
        
        else:
            ds = ds.isel(time=slice(12, None))
        
        if ds["time"].attrs["units"] == "days since 0-1-1":
            ds["time"].attrs["units"] =  "days since 0001-1-1"
            old_attrs = ds["time"].attrs
            ds["time"] = ds["time"] - 365
            ds["time"].attrs = old_attrs
    
        ds = xr.decode_cf(ds, decode_times=True, use_cftime=True)
    
        da = ds[cmip6_spec]

        
        f_cmip6_inc_wmghgs.concentration.loc[
            dict(specie=cmip6_to_fair[cmip6_spec])
        ][:,0,0] = da.sel(time=(slice('1750', '2015')), sector=0).rename({'time': 'timepoints'}).data 
        
        f_cmip6_inc_wmghgs.species_configs['baseline_concentration'][
            0,f_cmip6_inc_wmghgs.species.index(cmip6_to_fair[cmip6_spec])
            ] = f_cmip6_inc_wmghgs.concentration[0,0,0,f_cmip6_inc_wmghgs.species.index(cmip6_to_fair[cmip6_spec])]

        f_cmip6_inc_wmghgs.species_configs['forcing_reference_concentration'][
            0,f_cmip6_inc_wmghgs.species.index(cmip6_to_fair[cmip6_spec])
            ] = f_cmip6_inc_wmghgs.concentration[0,0,0,f_cmip6_inc_wmghgs.species.index(cmip6_to_fair[cmip6_spec])]
                    

f_cmip6_inc_wmghgs.run()

#%%

# and cmip6plus w/ changing WMGHGs (CO2, CH4, N2O)
f_cmip6plus_inc_wmghgs = FAIR()

f_cmip6plus_inc_wmghgs.define_time(1750, 2022, 1)

scenarios = ['ssp245']
f_cmip6plus_inc_wmghgs.define_scenarios(scenarios)

configs = ['test']
f_cmip6plus_inc_wmghgs.define_configs(configs)

species, properties = read_properties()


for cmip6_spec in cmip6plus_to_fair.keys():
        properties[cmip6plus_to_fair[cmip6_spec]]['input_mode'] = 'concentration'
        

f_cmip6plus_inc_wmghgs.define_species(species, properties)

f_cmip6plus_inc_wmghgs.allocate()
f_cmip6plus_inc_wmghgs.fill_species_configs()
f_cmip6plus_inc_wmghgs.fill_from_rcmip()

initialise(f_cmip6plus_inc_wmghgs.concentration, f_cmip6plus_inc_wmghgs.species_configs['baseline_concentration'])
initialise(f_cmip6plus_inc_wmghgs.forcing, 0)
initialise(f_cmip6plus_inc_wmghgs.temperature, 0)
initialise(f_cmip6plus_inc_wmghgs.cumulative_emissions, 0)
initialise(f_cmip6plus_inc_wmghgs.airborne_emissions, 0)

capacities = [4.22335014, 16.5073541, 86.1841127]
kappas = [1.31180598, 2.61194068, 0.92986733]
epsilon = 1.29020599
fill(f_cmip6plus_inc_wmghgs.climate_configs['ocean_heat_capacity'], capacities)
fill(f_cmip6plus_inc_wmghgs.climate_configs['ocean_heat_transfer'], kappas)
fill(f_cmip6plus_inc_wmghgs.climate_configs['deep_ocean_efficacy'], epsilon)

units = {}

for cmip6plus_spec in cmip6plus_to_fair.keys():
    
    print(cmip6plus_spec)
    
    data_folders = os.listdir(f"{datadir}/cmip6plus/{timestep}/{cmip6plus_spec}/gm/")
    if len(data_folders) > 1:
        print(f'{len(data_folders)} for {cmip6plus_spec}')
    data_folder = data_folders[0]

    files = os.listdir(f"{datadir}/cmip6plus/{timestep}/{cmip6plus_spec}/gm/{data_folder}/")

    if len(files) > 1:
        print(f'{len(files)} for {cmip6plus_spec}')

    file = f"{datadir}/cmip6plus/{timestep}/{cmip6plus_spec}/gm/{data_folder}/{files[0]}"

    
    with xr.open_dataset(file, use_cftime=True) as ds:
        ds.convert_calendar("proleptic_gregorian")
    
        da = ds[cmip6plus_spec]

        
        f_cmip6plus_inc_wmghgs.concentration.loc[
            dict(specie=cmip6plus_to_fair[cmip6plus_spec])
        ][:,0,0] = da.sel(time=(slice('1750', '2022'))).rename({'time': 'timepoints'}).data 
        

        f_cmip6plus_inc_wmghgs.species_configs['baseline_concentration'][
            0,f_cmip6plus_inc_wmghgs.species.index(cmip6plus_to_fair[cmip6plus_spec])
            ] = f_cmip6plus_inc_wmghgs.concentration[0,0,0,f_cmip6plus_inc_wmghgs.species.index(cmip6plus_to_fair[cmip6plus_spec])]

        f_cmip6plus_inc_wmghgs.species_configs['forcing_reference_concentration'][
            0,f_cmip6plus_inc_wmghgs.species.index(cmip6plus_to_fair[cmip6plus_spec])
            ] = f_cmip6plus_inc_wmghgs.concentration[0,0,0,f_cmip6plus_inc_wmghgs.species.index(cmip6plus_to_fair[cmip6plus_spec])]
                    
        
        units[cmip6plus_to_fair[cmip6plus_spec]] = da.attrs["units"]

f_cmip6plus_inc_wmghgs.run()

#%%

# and cmip7
f_cmip7_inc_wmghgs = FAIR()

f_cmip7_inc_wmghgs.define_time(1750, 2022, 1)

scenarios = ['ssp245']
f_cmip7_inc_wmghgs.define_scenarios(scenarios)

configs = ['test']
f_cmip7_inc_wmghgs.define_configs(configs)

species, properties = read_properties()

for cmip7_spec in cmip7_to_fair.keys():
        properties[cmip7_to_fair[cmip7_spec]]['input_mode'] = 'concentration'
        

f_cmip7_inc_wmghgs.define_species(species, properties)

f_cmip7_inc_wmghgs.allocate()
f_cmip7_inc_wmghgs.fill_species_configs()
f_cmip7_inc_wmghgs.fill_from_rcmip()

initialise(f_cmip7_inc_wmghgs.concentration, f_cmip7_inc_wmghgs.species_configs['baseline_concentration'])
initialise(f_cmip7_inc_wmghgs.forcing, 0)
initialise(f_cmip7_inc_wmghgs.temperature, 0)
initialise(f_cmip7_inc_wmghgs.cumulative_emissions, 0)
initialise(f_cmip7_inc_wmghgs.airborne_emissions, 0)

capacities = [4.22335014, 16.5073541, 86.1841127]
kappas = [1.31180598, 2.61194068, 0.92986733]
epsilon = 1.29020599
fill(f_cmip7_inc_wmghgs.climate_configs['ocean_heat_capacity'], capacities)
fill(f_cmip7_inc_wmghgs.climate_configs['ocean_heat_transfer'], kappas)
fill(f_cmip7_inc_wmghgs.climate_configs['deep_ocean_efficacy'], epsilon)

units = {}

for cmip7_spec in cmip7_to_fair.keys():
    
    print(cmip7_spec)
    
    filelist = glob.glob(f"{datadir}/cmip7/{timestep}/{cmip7_spec}_*nc")
    
    with xr.open_mfdataset(filelist, use_cftime=True) as ds:
        ds.convert_calendar("proleptic_gregorian")
    
        da = ds[cmip7_spec]
        
        f_cmip7_inc_wmghgs.concentration.loc[
            dict(specie=cmip7_to_fair[cmip7_spec])
        ][:,0,0] = da.sel(time=(slice('1750', '2022'))).rename({'time': 'timepoints'}).data 
        

        f_cmip7_inc_wmghgs.species_configs['baseline_concentration'][
            0,f_cmip7_inc_wmghgs.species.index(cmip7_to_fair[cmip7_spec])
            ] = f_cmip7_inc_wmghgs.concentration[0,0,0,f_cmip7_inc_wmghgs.species.index(cmip7_to_fair[cmip7_spec])]

        f_cmip7_inc_wmghgs.species_configs['forcing_reference_concentration'][
            0,f_cmip7_inc_wmghgs.species.index(cmip7_to_fair[cmip7_spec])
            ] = f_cmip7_inc_wmghgs.concentration[0,0,0,f_cmip7_inc_wmghgs.species.index(cmip7_to_fair[cmip7_spec])]
                
        
        units[cmip7_to_fair[cmip7_spec]] = da.attrs["units"]

f_cmip7_inc_wmghgs.run()

#%%
plot_list = []
for cmip6plus_spec in cmip6plus_to_fair.keys():
    plot_list.append(cmip6plus_to_fair[cmip6plus_spec])
    
plot_list.append('Ozone')
plot_list.append('Equivalent effective stratospheric chlorine')

units['Ozone'] = ''
units['Equivalent effective stratospheric chlorine'] = ''


with open('../data/misc/colors_pd.pkl', 'rb') as handle:
    colors_pd = pickle.load(handle)

colors = {
    'CMIP6':'#1f77b4',
    'CMIP6Plus':'#ff7f0e',
    'CMIP7':'green',
    }

scen_names = {
"ssp119":"AR6-SSP1-1.9",
"ssp126":"AR6-SSP1-2.6",
"ssp245":"AR6-SSP2-4.5",
"ssp370":"AR6-SSP3-7.0",
"ssp434":"AR6-SSP4-3.4",
"ssp460":"AR6-SSP4-6.0",
"ssp534-over":"AR6-SSP5-3.4-OS",
"ssp585":"AR6-SSP5-8.5",
    }

for scen in scen_names.keys():
    
    colors[scen]=colors_pd.loc[
            colors_pd['name'] == scen_names[scen]]['color'].values[0]

#%%
for spec in plot_list:
    
    fig, axes = plt.subplots(ncols=2, figsize=(12, 5))
    
    ax = axes[0]
    
    for scen in f_ssps.scenarios:
        ax.plot(f_ssps.timebounds, f_ssps.concentration[:,f_ssps.scenarios.index(scen),
                 0,f_ssps.species.index(spec)], label=f'Hist+{scen.upper()}', color=colors[scen])
    ax.plot(f_cmip6.timebounds, f_cmip6.concentration[:,0,0,f_ssps.species.index(spec)], label='CMIP6', color=colors['CMIP6'])
    ax.plot(f_cmip6plus.timebounds, f_cmip6plus.concentration[:,0,0,f_ssps.species.index(spec)], label='CMIP6Plus', color=colors['CMIP6Plus'])
    ax.plot(f_cmip7.timebounds, f_cmip7.concentration[:,0,0,f_ssps.species.index(spec)], label='CMIP7', color=colors['CMIP7'])

    if spec in ['CO2', 'CH4', 'N2O']:
        ax.plot(f_cmip6_inc_wmghgs.timebounds, f_cmip6_inc_wmghgs.concentration[
            :,0,0,f_ssps.species.index(spec)], label='CMIP6 inc. WMGHGs', color=colors['CMIP6'], linestyle='--')
        ax.plot(f_cmip6plus_inc_wmghgs.timebounds, f_cmip6plus_inc_wmghgs.concentration[
            :,0,0,f_ssps.species.index(spec)], label='CMIP6Plus inc. WMGHGs', color=colors['CMIP6Plus'], linestyle='--')
        ax.plot(f_cmip7_inc_wmghgs.timebounds, f_cmip7_inc_wmghgs.concentration[
            :,0,0,f_ssps.species.index(spec)], label='CMIP7 inc. WMGHGs', color=colors['CMIP7'], linestyle='--')
    
    ax.legend()
    ax.set_title(f'{spec} concentration')
    ax.set_ylabel(f'{units[spec]}')
    
    
    ax = axes[1]
        
    for scen in f_ssps.scenarios:
        ax.plot(f_ssps.timebounds, f_ssps.forcing[:,f_ssps.scenarios.index(scen),
                 0,f_ssps.species.index(spec)], label=f'Hist+{scen.upper()}', color=colors[scen])
    ax.plot(f_cmip6.timebounds, f_cmip6.forcing[:,0,0,f_ssps.species.index(spec)], label='CMIP6', color=colors['CMIP6'])
    ax.plot(f_cmip6plus.timebounds, f_cmip6plus.forcing[:,0,0,f_ssps.species.index(spec)], label='CMIP6Plus', color=colors['CMIP6Plus'])
    ax.plot(f_cmip7.timebounds, f_cmip7.forcing[:,0,0,f_ssps.species.index(spec)], label='CMIP7', color=colors['CMIP7'])

    if spec in ['CO2', 'CH4', 'N2O']:
        ax.plot(f_cmip6_inc_wmghgs.timebounds, f_cmip6_inc_wmghgs.forcing[
            :,0,0,f_ssps.species.index(spec)], label='CMIP6 inc. WMGHGs', color=colors['CMIP6'], linestyle='--')
        ax.plot(f_cmip6plus_inc_wmghgs.timebounds, f_cmip6plus_inc_wmghgs.forcing[
            :,0,0,f_ssps.species.index(spec)], label='CMIP6Plus inc. WMGHGs', color=colors['CMIP6Plus'], linestyle='--')
        ax.plot(f_cmip6plus_inc_wmghgs.timebounds, f_cmip7_inc_wmghgs.forcing[
            :,0,0,f_ssps.species.index(spec)], label='CMIP7 inc. WMGHGs', color=colors['CMIP7'], linestyle='--')
    
    ax.legend()
    ax.set_title(f'{spec} forcing')
    ax.set_ylabel('W/m2')
    
    plt.tight_layout()
    plt.savefig(
        f"../plots/single_species/{spec}_conc_erf.png", dpi=100
    )
#%%

fig, axs = plt.subplots(1, 2, figsize=(12, 8))

for scen in f_ssps.scenarios:
    axs[0].plot(f_ssps.timebounds, f_ssps.temperature[:,f_ssps.scenarios.index(scen),
             0,0], label=f'Hist+{scen.upper()}', color=colors[scen])
axs[0].plot(f_cmip6.timebounds, f_cmip6.temperature[:,0,0,0], label='CMIP6', color=colors['CMIP6'])
axs[0].plot(f_cmip6plus.timebounds, f_cmip6plus.temperature[:,0,0,0], label='CMIP6Plus', color=colors['CMIP6Plus'])
axs[0].plot(f_cmip7.timebounds, f_cmip7.temperature[:,0,0,0], label='CMIP7', color=colors['CMIP7'])

axs[0].plot(f_cmip6_inc_wmghgs.timebounds, f_cmip6_inc_wmghgs.temperature[:,0,0,0]
            , label='CMIP6 inc. WMGHGs', color=colors['CMIP6'], linestyle='--')
axs[0].plot(f_cmip6plus_inc_wmghgs.timebounds, f_cmip6plus_inc_wmghgs.temperature[:,0,0,0]
            , label='CMIP6Plus inc. WMGHGs', color=colors['CMIP6Plus'], linestyle='--')
axs[0].plot(f_cmip7_inc_wmghgs.timebounds, f_cmip7_inc_wmghgs.temperature[:,0,0,0]
            , label='CMIP7 inc. WMGHGs', color=colors['CMIP7'], linestyle='--')


axs[0].legend()
axs[0].set_title('GMST')
axs[0].set_ylabel('deg C')
axs[0].set_xlim([2000, 2040])
axs[0].set_ylim([0.5, 1.8])

cmip6plus_minus_cmip6 = f_cmip6plus.temperature[:,0,0,0
            ] - f_cmip6.temperature[:f_cmip6._n_timebounds,0,0,0]

cmip6plus_minus_cmip6_inc_wmghgs = f_cmip6plus_inc_wmghgs.temperature[:,0,0,0
            ] - f_cmip6_inc_wmghgs.temperature[:f_cmip6_inc_wmghgs._n_timebounds,0,0,0]

cmip7_minus_cmip6 = f_cmip7.temperature[:,0,0,0
            ] - f_cmip6.temperature[:f_cmip6._n_timebounds,0,0,0]

cmip7_minus_cmip6_inc_wmghgs = f_cmip7_inc_wmghgs.temperature[:,0,0,0
            ] - f_cmip6_inc_wmghgs.temperature[:f_cmip6_inc_wmghgs._n_timebounds,0,0,0]


axs[1].plot(f_cmip6.timebounds, cmip6plus_minus_cmip6, label='CMIP6Plus - CMIP6', color=colors['CMIP6Plus'])
axs[1].plot(f_cmip6.timebounds, cmip6plus_minus_cmip6_inc_wmghgs, label='CMIP6Plus - CMIP6 inc. WMGHGs', color=colors['CMIP6Plus'], linestyle='--')

axs[1].plot(f_cmip6.timebounds, cmip7_minus_cmip6, label='CMIP7 - CMIP6', color=colors['CMIP7'])
axs[1].plot(f_cmip6.timebounds, cmip7_minus_cmip6_inc_wmghgs, label='CMIP7 - CMIP6 inc. WMGHGs', color=colors['CMIP7'], linestyle='--')



axs[1].legend()
axs[1].set_title('GMST difference')
axs[1].set_ylabel('deg C')
# axs[1].set_xlim([2000, 2040])
# axs[1].set_ylim([0.5, 1.8])

axs[1].axhline(y=0, color='grey', linestyle='--')


plt.tight_layout()
  
plt.savefig(
    "../plots/single_species/aggregated/GMST.png", dpi=100
)
   
#%%

fig, axs = plt.subplots(1, 2, figsize=(12, 8))

for scen in f_ssps.scenarios:
    axs[0].plot(f_ssps.timebounds, f_ssps.forcing_sum[:,f_ssps.scenarios.index(scen),
             0], label=f'Hist+{scen.upper()}', color=colors[scen])
axs[0].plot(f_cmip6.timebounds, f_cmip6.forcing_sum[:,0,0], label='CMIP6')
axs[0].plot(f_cmip6plus.timebounds, f_cmip6plus.forcing_sum[:,0,0], label='CMIP6Plus')
axs[0].plot(f_cmip7.timebounds, f_cmip7.forcing_sum[:,0,0], label='CMIP7')

axs[0].plot(f_cmip6_inc_wmghgs.timebounds, f_cmip6_inc_wmghgs.forcing_sum[:,0,0]
            , label='CMIP6 inc. WMGHGs', color=colors['CMIP6'], linestyle='--')
axs[0].plot(f_cmip6plus_inc_wmghgs.timebounds, f_cmip6plus_inc_wmghgs.forcing_sum[:,0,0]
            , label='CMIP6Plus inc. WMGHGs', color=colors['CMIP6Plus'], linestyle='--')
axs[0].plot(f_cmip7_inc_wmghgs.timebounds, f_cmip7_inc_wmghgs.forcing_sum[:,0,0]
            , label='CMIP7 inc. WMGHGs', color=colors['CMIP7'], linestyle='--')


axs[0].legend()
axs[0].set_title('Forcing')
axs[0].set_ylabel('W/m2')
axs[0].set_xlim([2000, 2040])
axs[0].set_ylim([1.8, 4])

cmip6plus_minus_cmip6 = f_cmip6plus.forcing_sum[:,0,0
            ] - f_cmip6.forcing_sum[:f_cmip6._n_timebounds,0,0]

cmip6plus_minus_cmip6_inc_wmghgs = f_cmip6plus_inc_wmghgs.forcing_sum[:,0,0
            ] - f_cmip6_inc_wmghgs.forcing_sum[:f_cmip6_inc_wmghgs._n_timebounds,0,0]

cmip7_minus_cmip6 = f_cmip7.forcing_sum[:,0,0
            ] - f_cmip6.forcing_sum[:f_cmip6._n_timebounds,0,0]

cmip7_minus_cmip6_inc_wmghgs = f_cmip7_inc_wmghgs.forcing_sum[:,0,0
            ] - f_cmip6_inc_wmghgs.forcing_sum[:f_cmip6_inc_wmghgs._n_timebounds,0,0]



axs[1].plot(f_cmip6.timebounds, cmip6plus_minus_cmip6, label='CMIP6Plus - CMIP6', color=colors['CMIP6Plus'])
axs[1].plot(f_cmip6.timebounds, cmip6plus_minus_cmip6_inc_wmghgs, label='CMIP6Plus - CMIP6 inc. WMGHGs', color=colors['CMIP6Plus'], linestyle='--')

axs[1].plot(f_cmip6.timebounds, cmip7_minus_cmip6, label='CMIP7 - CMIP6', color=colors['CMIP7'])
axs[1].plot(f_cmip6.timebounds, cmip7_minus_cmip6_inc_wmghgs, label='CMIP7 - CMIP6 inc. WMGHGs', color=colors['CMIP7'], linestyle='--')


axs[1].legend()
axs[1].set_title('Forcing difference')
axs[1].set_ylabel('W/m2')
# axs[1].set_xlim([2000, 2040])
# axs[1].set_ylim([0.5, 1.8])

axs[1].axhline(y=0, color='grey', linestyle='--')


plt.tight_layout()
  
plt.savefig(
    "../plots/single_species/aggregated/ERF.png", dpi=100
)

#%%
save_forcings = {}
save_forcings['CMIP6'] = f_cmip6_inc_wmghgs.forcing
save_forcings['CMIP6Plus'] = f_cmip6plus_inc_wmghgs.forcing
save_forcings['CMIP7'] = f_cmip7_inc_wmghgs.forcing

with open('../data/misc/save_forcings.pkl', 'wb') as handle:
    pickle.dump(save_forcings, handle, protocol=pickle.HIGHEST_PROTOCOL)


