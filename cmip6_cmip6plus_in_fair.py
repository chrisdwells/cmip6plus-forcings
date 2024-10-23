# import pandas as pd
import matplotlib.pyplot as plt
# from scipy.interpolate import CubicSpline
# import numpy as np

from fair import FAIR
from fair.io import read_properties
from fair.interface import fill, initialise
import os
import xarray as xr
# import cftime

datadir = 'data'
timestep='yr'

#%%
f_ssps = FAIR()

f_ssps.define_time(1750, 2035, 1)

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


cmip6_to_fair = {
    # 'mole_fraction_of_carbon_dioxide_in_air': 'co2',
 # 'mole_fraction_of_methane_in_air': 'ch4',
 # 'mole_fraction_of_nitrous_oxide_in_air': 'n2o',
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

f_cmip6 = FAIR()

f_cmip6.define_time(1750, 2014, 1)

scenarios = ['ssp245']
f_cmip6.define_scenarios(scenarios)

configs = ['test']
f_cmip6.define_configs(configs)

species, properties = read_properties()

for cmip6_spec in cmip6_to_fair.keys():
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



cmip6plus_to_fair = {
 # 'co2':'co2',
 # 'ch4':'ch4',
 # 'n2o':'n2o',
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

f_cmip6plus = FAIR()

f_cmip6plus.define_time(1750, 2022, 1)

scenarios = ['ssp245']
f_cmip6plus.define_scenarios(scenarios)

configs = ['test']
f_cmip6plus.define_configs(configs)

species, properties = read_properties()


for cmip6_spec in cmip6plus_to_fair.keys():
        properties[cmip6plus_to_fair[cmip6_spec]]['input_mode'] = 'concentration'
        

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




cmip6_to_fair = {
    'mole_fraction_of_carbon_dioxide_in_air': 'CO2',
  'mole_fraction_of_methane_in_air': 'CH4',
  'mole_fraction_of_nitrous_oxide_in_air': 'N2O',
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
        
        if cmip6_to_fair[cmip6_spec] not in ['CO2', 'CH4', 'N2O']:
            
                
            f_cmip6_inc_wmghgs.species_configs['baseline_concentration'][
                0,f_cmip6_inc_wmghgs.species.index(cmip6_to_fair[cmip6_spec])
                ] = f_cmip6_inc_wmghgs.concentration[0,0,0,f_cmip6_inc_wmghgs.species.index(cmip6_to_fair[cmip6_spec])]
    
            f_cmip6_inc_wmghgs.species_configs['forcing_reference_concentration'][
                0,f_cmip6_inc_wmghgs.species.index(cmip6_to_fair[cmip6_spec])
                ] = f_cmip6_inc_wmghgs.concentration[0,0,0,f_cmip6_inc_wmghgs.species.index(cmip6_to_fair[cmip6_spec])]
                    

f_cmip6_inc_wmghgs.run()



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
        
        if cmip6plus_to_fair[cmip6plus_spec] not in ['CO2', 'CH4', 'N2O']:
    
            f_cmip6plus_inc_wmghgs.species_configs['baseline_concentration'][
                0,f_cmip6plus_inc_wmghgs.species.index(cmip6plus_to_fair[cmip6plus_spec])
                ] = f_cmip6plus_inc_wmghgs.concentration[0,0,0,f_cmip6plus_inc_wmghgs.species.index(cmip6plus_to_fair[cmip6plus_spec])]
    
            f_cmip6plus_inc_wmghgs.species_configs['forcing_reference_concentration'][
                0,f_cmip6plus_inc_wmghgs.species.index(cmip6plus_to_fair[cmip6plus_spec])
                ] = f_cmip6plus_inc_wmghgs.concentration[0,0,0,f_cmip6plus_inc_wmghgs.species.index(cmip6plus_to_fair[cmip6plus_spec])]
                    
        
        units[cmip6plus_to_fair[cmip6plus_spec]] = da.attrs["units"]

f_cmip6plus_inc_wmghgs.run()

#%%
plot_list = []
for cmip6plus_spec in cmip6plus_to_fair.keys():
    plot_list.append(cmip6plus_to_fair[cmip6plus_spec])
    
plot_list.append('Ozone')
plot_list.append('Equivalent effective stratospheric chlorine')

units['Ozone'] = ''
units['Equivalent effective stratospheric chlorine'] = ''

colors = {
    'ssp119':'darkblue', 
    'ssp126':'blue', 
    'ssp245':'purple', 
    'ssp370':'red', 
    'ssp585':'darkred',    
    'CMIP6':'#1f77b4',
    'CMIP6Plus':'#ff7f0e',
    }


#%%
for spec in plot_list:
    
    fig = plt.figure()
    
    for scen in f_ssps.scenarios:
        plt.plot(f_ssps.timebounds, f_ssps.concentration[:,f_ssps.scenarios.index(scen),
                 0,f_ssps.species.index(spec)], label=f'Hist+{scen.upper()}', color=colors[scen])
    plt.plot(f_cmip6.timebounds, f_cmip6.concentration[:,0,0,f_ssps.species.index(spec)], label='CMIP6', color=colors['CMIP6'])
    plt.plot(f_cmip6plus.timebounds, f_cmip6plus.concentration[:,0,0,f_ssps.species.index(spec)], label='CMIP6Plus', color=colors['CMIP6Plus'])
    
    if spec in ['CO2', 'CH4', 'N2O']:
        
        plt.plot(f_cmip6_inc_wmghgs.timebounds, f_cmip6_inc_wmghgs.concentration[
            :,0,0,f_ssps.species.index(spec)], label='CMIP6 inc. WMGHGs', color=colors['CMIP6'], linestyle='--')
        plt.plot(f_cmip6plus_inc_wmghgs.timebounds, f_cmip6plus_inc_wmghgs.concentration[
            :,0,0,f_ssps.species.index(spec)], label='CMIP6Plus inc. WMGHGs', color=colors['CMIP6Plus'], linestyle='--')
            
        
    
    plt.legend()
    plt.title(f'{spec} concentration')
    plt.tight_layout()
    plt.ylabel(f'{units[spec]}')
    
    
    plt.savefig(
        f"plots_fair/{spec}_concentration.png", dpi=100
    )
    
    
    fig = plt.figure()
        
    for scen in f_ssps.scenarios:
        plt.plot(f_ssps.timebounds, f_ssps.forcing[:,f_ssps.scenarios.index(scen),
                 0,f_ssps.species.index(spec)], label=f'Hist+{scen.upper()}', color=colors[scen])
    plt.plot(f_cmip6.timebounds, f_cmip6.forcing[:,0,0,f_ssps.species.index(spec)], label='CMIP6', color=colors['CMIP6'])
    plt.plot(f_cmip6plus.timebounds, f_cmip6plus.forcing[:,0,0,f_ssps.species.index(spec)], label='CMIP6Plus', color=colors['CMIP6Plus'])
    

    if spec in ['CO2', 'CH4', 'N2O']:
    
        plt.plot(f_cmip6_inc_wmghgs.timebounds, f_cmip6_inc_wmghgs.forcing[
            :,0,0,f_ssps.species.index(spec)], label='CMIP6 inc. WMGHGs', color=colors['CMIP6'], linestyle='--')
        plt.plot(f_cmip6plus_inc_wmghgs.timebounds, f_cmip6plus_inc_wmghgs.forcing[
            :,0,0,f_ssps.species.index(spec)], label='CMIP6Plus inc. WMGHGs', color=colors['CMIP6Plus'], linestyle='--')
        
                    
    
    plt.legend()
    plt.title(f'{spec} forcing')
    plt.tight_layout()
    plt.ylabel('W/m2')
        
    plt.savefig(
        f"plots_fair/{spec}_forcing.png", dpi=100
    )
#%%

fig, axs = plt.subplots(1, 2, figsize=(12, 8))

for scen in f_ssps.scenarios:
    axs[0].plot(f_ssps.timebounds, f_ssps.temperature[:,f_ssps.scenarios.index(scen),
             0,0], label=f'Hist+{scen.upper()}', color=colors[scen])
axs[0].plot(f_cmip6.timebounds, f_cmip6.temperature[:,0,0,0], label='CMIP6', color=colors['CMIP6'])
axs[0].plot(f_cmip6plus.timebounds, f_cmip6plus.temperature[:,0,0,0], label='CMIP6Plus', color=colors['CMIP6Plus'])

axs[0].plot(f_cmip6_inc_wmghgs.timebounds, f_cmip6_inc_wmghgs.temperature[:,0,0,0]
            , label='CMIP6 inc. WMGHGs', color=colors['CMIP6'], linestyle='--')
axs[0].plot(f_cmip6plus_inc_wmghgs.timebounds, f_cmip6plus_inc_wmghgs.temperature[:,0,0,0]
            , label='CMIP6Plus inc. WMGHGs', color=colors['CMIP6Plus'], linestyle='--')


axs[0].legend()
axs[0].set_title('GMST')
axs[0].set_ylabel('deg C')
axs[0].set_xlim([2000, 2040])
axs[0].set_ylim([0.5, 1.8])

cmip6plus_minus_cmip6 = f_cmip6plus.temperature[:,0,0,0
            ] - f_cmip6.temperature[:f_cmip6._n_timebounds,0,0,0]

cmip6plus_minus_cmip6_inc_wmghgs = f_cmip6plus_inc_wmghgs.temperature[:,0,0,0
            ] - f_cmip6_inc_wmghgs.temperature[:f_cmip6_inc_wmghgs._n_timebounds,0,0,0]


axs[1].plot(f_cmip6.timebounds, cmip6plus_minus_cmip6, label='CMIP6Plus - CMIP6', color='#2ca02c')
axs[1].plot(f_cmip6.timebounds, cmip6plus_minus_cmip6_inc_wmghgs, label='CMIP6Plus - CMIP6 inc. WMGHGs', color='#2ca02c', linestyle='--')


axs[1].legend()
axs[1].set_title('GMST difference')
axs[1].set_ylabel('deg C')
# axs[1].set_xlim([2000, 2040])
# axs[1].set_ylim([0.5, 1.8])

axs[1].axhline(y=0, color='grey', linestyle='--')


plt.tight_layout()
  
plt.savefig(
    "plots_fair/GMST.png", dpi=100
)
   

fig, axs = plt.subplots(1, 2, figsize=(12, 8))

for scen in f_ssps.scenarios:
    axs[0].plot(f_ssps.timebounds, f_ssps.forcing_sum[:,f_ssps.scenarios.index(scen),
             0], label=f'Hist+{scen.upper()}', color=colors[scen])
axs[0].plot(f_cmip6.timebounds, f_cmip6.forcing_sum[:,0,0], label='CMIP6')
axs[0].plot(f_cmip6plus.timebounds, f_cmip6plus.forcing_sum[:,0,0], label='CMIP6Plus')

axs[0].plot(f_cmip6_inc_wmghgs.timebounds, f_cmip6_inc_wmghgs.forcing_sum[:,0,0]
            , label='CMIP6 inc. WMGHGs', color=colors['CMIP6'], linestyle='--')
axs[0].plot(f_cmip6plus_inc_wmghgs.timebounds, f_cmip6plus_inc_wmghgs.forcing_sum[:,0,0]
            , label='CMIP6Plus inc. WMGHGs', color=colors['CMIP6Plus'], linestyle='--')



axs[0].legend()
axs[0].set_title('Forcing')
axs[0].set_ylabel('W/m2')
axs[0].set_xlim([2000, 2040])
axs[0].set_ylim([1.8, 4])

cmip6plus_minus_cmip6 = f_cmip6plus.forcing_sum[:,0,0
            ] - f_cmip6.forcing_sum[:f_cmip6._n_timebounds,0,0]

cmip6plus_minus_cmip6_inc_wmghgs = f_cmip6plus_inc_wmghgs.forcing_sum[:,0,0
            ] - f_cmip6_inc_wmghgs.forcing_sum[:f_cmip6_inc_wmghgs._n_timebounds,0,0]


axs[1].plot(f_cmip6.timebounds, cmip6plus_minus_cmip6, label='CMIP6Plus - CMIP6', color='#2ca02c')
axs[1].plot(f_cmip6.timebounds, cmip6plus_minus_cmip6_inc_wmghgs, label='CMIP6Plus - CMIP6 inc. WMGHGs', color='#2ca02c', linestyle='--')


axs[1].legend()
axs[1].set_title('Forcing difference')
axs[1].set_ylabel('W/m2')
# axs[1].set_xlim([2000, 2040])
# axs[1].set_ylim([0.5, 1.8])

axs[1].axhline(y=0, color='grey', linestyle='--')


plt.tight_layout()
  
plt.savefig(
    "plots_fair/Forcing.png", dpi=100
)
     
#%%

import numpy as np
import copy
from matplotlib.lines import Line2D
import pickle

fair_to_cmip6plus = {    
    "CO2":"co2",
    "CH4":"ch4",
    "N2O":"n2o",
    "C2F6":"pfc116",
    "C3F8":"pfc218",
    "C4F10":"pfc3110",
    "C5F12":"pfc4112",
    "C6F14":"pfc5114",
    "C7F16":"pfc6116",
    "C8F18":"pfc7118",
    "c-C4F8":"pfc318",
    "CCl4":"ccl4",
    "CF4":"cf4",
    "CFC-11":"cfc11",
    "CFC-113":"cfc113",
    "CFC-114":"cfc114",
    "CFC-115":"cfc115",
    "CFC-12":"cfc12",
    "CH2Cl2":"ch2cl2",
    "CH3Br":"ch3br",
    "CH3CCl3":"hcc140a",
    "CH3Cl":"ch3cl",
    "CHCl3":"chcl3",
    "Halon-1211":"halon1211",
    "Halon-1301":"halon1301",
    "Halon-2402":"halon2402",
    "HCFC-141b":"hcfc141b",
    "HCFC-142b":"hcfc142b",
    "HCFC-22":"hcfc22",
    "HFC-125":"hfc125",
    "HFC-134a":"hfc134a",
    "HFC-143a":"hfc143a",
    "HFC-152a":"hfc152a",
    "HFC-227ea":"hfc227ea",
    "HFC-23":"hfc23",
    "HFC-236fa":"hfc236fa",
    "HFC-245fa":"hfc245fa",
    "HFC-32":"hfc32",
    "HFC-365mfc":"hfc365mfc",
    "HFC-4310mee":"hfc4310mee",
    "NF3":"nf3",
    "SF6":"sf6",
    "SO2F2":"so2f2",
    "Ozone":"Ozone",
    "Equivalent effective stratospheric chlorine":"Equivalent effective stratospheric chlorine",
    }


with open('data/save_dict.pkl', 'rb') as handle:
    save_dict = pickle.load(handle)

cmip6plus_to_fair['Ozone'] = 'Ozone'
cmip6plus_to_fair['Equivalent effective stratospheric chlorine'] = 'Equivalent effective stratospheric chlorine'


time_conc = 1 + np.arange(2014)
time2_conc = 2014 + np.arange(9)


time = 1750 + np.arange(265)
time2 = 2014 + np.arange(9)

f_gases = ['cf4', 'pfc116', 'pfc218', 'pfc318', 'pfc6116', 'pfc7118', 'nf3', 'sf6', 'so2f2', 'hfc125', 'hfc134a', 'hfc143a', 'hfc152a', 'hfc227ea',
 'hfc23', 'hfc236fa', 'hfc245fa', 'hfc32', 'hfc365mfc', 'pfc3110', 'pfc4112', 'pfc5114', 'hfc4310mee']

montreals = ['cfc11', 'cfc113', 'cfc114', 'cfc115', 'cfc12', 
             'hcfc141b', 'hcfc142b', 'hcfc22', 'ccl4', 'halon1211',
             'halon1301', 'halon2402']

cfcs = ['cfc11', 'cfc113', 'cfc114', 'cfc115', 'cfc12']

hcfcs = ['hcfc141b', 'hcfc142b', 'hcfc22']

halons = ['halon1211', 'halon1301', 'halon2402']

var_groups = {
    # 'All':[],
    # 'Going negative':['pfc218', 'hcfc142b', 'hfc143a', 'hfc152a', 'hfc227ea', 'hfc236fa', 'nf3'],
    # 'CO2, CH4, N2O':['co2', 'ch4', 'n2o'],
    # 'CFC114':['cfc114'],
    # 'Accelerating HFCs':['hfc32', 'hfc125', 'hfc134a', 'hfc143a', 'hfc227ea'],
    # 'F-gases':f_gases,
    # 'Montreal gases':montreals,
    # 'CFCs':cfcs,
    # 'HCFCs':hcfcs,
    # 'Halons':halons,
    'Ozone':['Ozone'],
    # 'Equivalent effective stratospheric chlorine':['Equivalent effective stratospheric chlorine'],
    # 'CO2':['co2'],
    # 'CH4':['ch4'],
    # 'N2O':['n2o'],
    }

for var_group in var_groups.keys():

    speclist = [cmip6plus_to_fair[s] for s in var_groups[var_group]]

    fig = plt.figure(figsize=(16, 8))
        
    SIZE_DEFAULT = 14
    SIZE_LARGE = 16
    plt.rc("font", weight="normal")  # controls default font
    plt.rc("font", size=SIZE_DEFAULT)  # controls default text sizes
    plt.rc("axes", titlesize=SIZE_LARGE)  # fontsize of the axes title
    plt.rc("axes", labelsize=SIZE_LARGE)  # fontsize of the x and y labels
    plt.rc("xtick", labelsize=SIZE_DEFAULT)  # fontsize of the tick labels
    plt.rc("ytick", labelsize=SIZE_DEFAULT)  # fontsize of the tick labels
    
      
    

    ax = fig.add_subplot(121)
    ax2 = ax.twinx()

    
    specs_ordered = copy.deepcopy(plot_list)    
    specs_ordered = [e for e in specs_ordered if e not in speclist]
    
    specs_ordered.extend(speclist)

    for specie in specs_ordered:
        
        specie_fair = fair_to_cmip6plus[specie]
        
        if specie_fair in ['Ozone', 'Equivalent effective stratospheric chlorine']:
            continue

        color='grey'
        linewidth = 1
        if specie in speclist:
            color='red'
            linewidth = 2

    
        diff = save_dict[specie_fair]['diff']
    
        diff[diff >= 250] = np.nan
        diff[diff <= -250] = np.nan 
        
        ax.plot(time_conc, diff, color=color, linewidth=linewidth)
       
    
        change_cf_2005_14 = save_dict[specie_fair]['change_cf_2005_14']
    
        ax2.plot(time2_conc, change_cf_2005_14, color=color, linewidth=linewidth)
        
    

    ax.set_ylim([-200, 200])
    ax.set_ylabel('% change CMIP6Plus cf CMIP6')
    ax.set_xlim([1900, 2025])
    
    ax.axvline(x=2014, color='black', linestyle='--')

    ax2.set_ylim([-50, 50])
    ax2.set_ylabel('% change in CMIP6Plus cf 2005-14')
    ax.set_title('Concentration')
    
    
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)

    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_visible(False)
    ax2.spines["top"].set_visible(False)


    if len(speclist) > 0:
        handles = []
        handles.append(Line2D([0], [0], label=var_group, color='red', linewidth=linewidth))
        ax.legend(handles=handles, loc='lower left')

        

    ax = fig.add_subplot(122)
    ax2 = ax.twinx()

    for specie in specs_ordered:
        
        # specie = cmip6plus_to_fair[specie_in]

        color='grey'
        linewidth = 1
        if specie in speclist:
            color='red'
            linewidth = 2

    
        cmip6plus_in = f_cmip6plus_inc_wmghgs.forcing[
            :,0,0,f_ssps.species.index(specie)]
            
        
        cmip6_in = f_cmip6_inc_wmghgs.forcing[
            :,0,0,f_ssps.species.index(specie)]
        
        #cmip6plus_in[cmip6plus_in == 0] = np.nan
        #cmip6_in[cmip6_in == 0] = np.nan
    
    
        diff = cmip6plus_in[:265] - cmip6_in
    
        # diff[diff >= 250] = np.nan
        # diff[diff <= -250] = np.nan 
        
        ax.plot(time, 1000*diff, color=color, linewidth=linewidth)
       
    
        change_cf_2005_14 = cmip6plus_in[-9:] - np.mean(cmip6plus_in[-19:-9])
    
        ax2.plot(time2, 1000*change_cf_2005_14, color=color, linewidth=linewidth)
        
    

    ax.set_ylim([-40, 40])
    ax.set_ylabel(r'CMIP6Plus - CMIP6 (mWm$^{-2}$)')
    ax.set_xlim([1900, 2025])
    
    ax.axvline(x=2014, color='black', linestyle='--')

    ax2.set_ylim([-10, 10])
    ax2.set_yticks(np.linspace(-8, 8, 5))

    
    ax2.set_ylabel(r'Change in CMIP6Plus cf 2005-14 (mWm$^{-2}$)')
    ax.set_title(r'Forcing (mWm$^{-2}$)')

    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)

    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_visible(False)
    ax2.spines["top"].set_visible(False)


    if len(speclist) > 0:
        handles = []
        handles.append(Line2D([0], [0], label=var_group, color='red', linewidth=linewidth))
        ax.legend(handles=handles, loc='lower left')


    plt.tight_layout()
    
    
    # plt.savefig(f'plots_for_reading/{var_group}_combined.png', dpi=100, transparent=True)
    
#%%

colors_list = [ 'grey', '#17becf', '#bcbd22', '#e377c2', '#8c564b',
 '#9467bd', '#d62728', '#2ca02c', '#ff7f0e', '#1f77b4']

var_groups = {
    'All':[],
    'F-gases':f_gases,
    'Halons':halons,
    'HCFCs':hcfcs,
    'CFCs':cfcs,
    'Going negative':['pfc218', 'hcfc142b', 'hfc143a', 'hfc152a', 'hfc227ea', 'hfc236fa', 'nf3'],
    'HFCs':['hfc32', 'hfc125', 'hfc134a', 'hfc143a', 'hfc227ea'],
    'CFC114':['cfc114'],
    'CO2, CH4, N2O':['co2', 'ch4', 'n2o'],
    }


legend_order = ['CO2, CH4, N2O',  'Going negative', 'CFC114', 
                'HFCs', 'CFCs', 'HCFCs', 'Halons', 'F-gases']

fig = plt.figure(figsize=(16, 8))

ax = fig.add_subplot(121)
ax2 = ax.twinx()

ax.set_ylim([-200, 200])
ax.set_ylabel('% change CMIP6Plus cf CMIP6')
ax.set_xlim([1900, 2025])

ax.axvline(x=2014, color='black', linestyle='--')

ax2.set_ylim([-50, 50])
ax2.set_ylabel('% change in CMIP6Plus cf 2005-14')
ax.set_title('Concentration')


ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["top"].set_visible(False)

ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_visible(False)
ax2.spines["top"].set_visible(False)


for var_group_i, var_group in enumerate(var_groups.keys()):

    speclist = [cmip6plus_to_fair[s] for s in var_groups[var_group]]

    specs_ordered = copy.deepcopy(plot_list)    
    specs_ordered = [e for e in specs_ordered if e not in speclist]
    
    specs_ordered.extend(speclist)

    for specie in specs_ordered:
        
        specie_fair = fair_to_cmip6plus[specie]
        
        if specie_fair in ['Ozone', 'Equivalent effective stratospheric chlorine']:
            continue

        if specie not in speclist:
            if var_group == 'All':
                color='grey'
                linewidth=2
            else:
                continue
        else:
            color=colors_list[var_group_i]
            linewidth = 2

    
        diff = save_dict[specie_fair]['diff']
    
        diff[diff >= 250] = np.nan
        diff[diff <= -250] = np.nan 
        
        ax.plot(time_conc, diff, color=color, linewidth=linewidth)
       
        change_cf_2005_14 = save_dict[specie_fair]['change_cf_2005_14']
    
        ax2.plot(time2_conc, change_cf_2005_14, color=color, linewidth=linewidth)
        

handles = []
for var_group_i, var_group in enumerate(legend_order):
    handles.append(Line2D([0], [0], label=var_group, 
      color=colors_list[list(var_groups.keys()).index(var_group)], linewidth=linewidth))
    
ax.legend(handles=handles, loc='lower left', framealpha=1)
        

ax = fig.add_subplot(122)
ax2 = ax.twinx()

ax.set_ylim([-40, 40])
ax.set_ylabel(r'CMIP6Plus - CMIP6 (mWm$^{-2}$)')
ax.set_xlim([1900, 2025])

ax.axvline(x=2014, color='black', linestyle='--')

ax2.set_ylim([-10, 10])
ax2.set_yticks(np.linspace(-8, 8, 5))


ax2.set_ylabel(r'Change in CMIP6Plus cf 2005-14 (mWm$^{-2}$)')
ax.set_title(r'Forcing (mWm$^{-2}$)')

ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["top"].set_visible(False)

ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_visible(False)
ax2.spines["top"].set_visible(False)


for var_group_i, var_group in enumerate(var_groups.keys()):

    speclist = [cmip6plus_to_fair[s] for s in var_groups[var_group]]

    specs_ordered = copy.deepcopy(plot_list)    
    specs_ordered = [e for e in specs_ordered if e not in speclist]
    
    specs_ordered.extend(speclist)        


    for specie in specs_ordered:
        
        # specie = cmip6plus_to_fair[specie_in]

        if specie not in speclist:
            if var_group == 'All':
                color='grey'
                linewidth=2
            else:
                continue
        
        else:
            color=colors_list[var_group_i]
            linewidth = 2
            
        cmip6plus_in = f_cmip6plus_inc_wmghgs.forcing[
            :,0,0,f_ssps.species.index(specie)]
            
        
        cmip6_in = f_cmip6_inc_wmghgs.forcing[
            :,0,0,f_ssps.species.index(specie)]
        
        #cmip6plus_in[cmip6plus_in == 0] = np.nan
        #cmip6_in[cmip6_in == 0] = np.nan
    
    
        diff = cmip6plus_in[:265] - cmip6_in
    
        # diff[diff >= 250] = np.nan
        # diff[diff <= -250] = np.nan 
        
        ax.plot(time, 1000*diff, color=color, linewidth=linewidth)
       
    
        change_cf_2005_14 = cmip6plus_in[-9:] - np.mean(cmip6plus_in[-19:-9])
    
        ax2.plot(time2, 1000*change_cf_2005_14, color=color, linewidth=linewidth)
        
    

ax.legend(handles=handles, loc='upper left', ncol=2)

plt.tight_layout()


plt.savefig('plots_for_reading/conclusions_combined.png', dpi=100, transparent=True)
    
