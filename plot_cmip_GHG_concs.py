import numpy as np
# import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import os
import glob
import copy
from matplotlib.lines import Line2D
import pickle

from fair import FAIR
from fair.io import read_properties
from fair.interface import fill, initialise


gens = ['CMIP6', 'CMIP6Plus', 'CMIP7']

datadir = 'data'
timestep='yr'

species = ['CO2', 'CH4', 'N2O', 'C2F6', 'C3F8', 'C4F10', 'C5F12', 'C6F14', 'C7F16', 'C8F18', 
 'c-C4F8', 'CCl4', 'CF4', 'CFC-11', 'CFC-113', 'CFC-114', 'CFC-115', 'CFC-12', 
 'CH2Cl2', 'CH3Br', 'CH3CCl3', 'CH3Cl', 'CHCl3', 'Halon-1211', 'Halon-1301', 
 'Halon-2402', 'HCFC-141b', 'HCFC-142b', 'HCFC-22', 'HFC-125', 'HFC-134a', 'HFC-143a', 
 'HFC-152a', 'HFC-227ea', 'HFC-23', 'HFC-236fa', 'HFC-245fa', 'HFC-32', 'HFC-365mfc', 
 'HFC-4310mee', 'NF3', 'SF6', 'SO2F2',
 'CFC11eq', 'CFC12eq', 'HFC-134aeq'
 ]

fair_to_cmip6 = {
    'CO2':'mole_fraction_of_carbon_dioxide_in_air',
    'CH4':'mole_fraction_of_methane_in_air',
    'N2O':'mole_fraction_of_nitrous_oxide_in_air',
    'C2F6':'mole_fraction_of_c2f6_in_air',
    'C3F8':'mole_fraction_of_c3f8_in_air',
    'C4F10':'mole_fraction_of_c4f10_in_air',
    'C5F12':'mole_fraction_of_c5f12_in_air',
    'C6F14':'mole_fraction_of_c6f14_in_air',
    'C7F16':'mole_fraction_of_c7f16_in_air',
    'C8F18':'mole_fraction_of_c8f18_in_air',
    'c-C4F8':'mole_fraction_of_c_c4f8_in_air',
    'CCl4':'mole_fraction_of_carbon_tetrachloride_in_air',
    'CF4':'mole_fraction_of_cf4_in_air',
    'CFC-11':'mole_fraction_of_cfc11_in_air',
    'CFC-113':'mole_fraction_of_cfc113_in_air',
    'CFC-114':'mole_fraction_of_cfc114_in_air',
    'CFC-115':'mole_fraction_of_cfc115_in_air',
    'CFC-12':'mole_fraction_of_cfc12_in_air',
    'CH2Cl2':'mole_fraction_of_ch2cl2_in_air',
    'CH3Br':'mole_fraction_of_methyl_bromide_in_air',
    'CH3CCl3':'mole_fraction_of_ch3ccl3_in_air',
    'CH3Cl':'mole_fraction_of_methyl_chloride_in_air',
    'CHCl3':'mole_fraction_of_chcl3_in_air',
    'Halon-1211':'mole_fraction_of_halon1211_in_air',
    'Halon-1301':'mole_fraction_of_halon1301_in_air',
    'Halon-2402':'mole_fraction_of_halon2402_in_air',
    'HCFC-141b':'mole_fraction_of_hcfc141b_in_air',
    'HCFC-142b':'mole_fraction_of_hcfc142b_in_air',
    'HCFC-22':'mole_fraction_of_hcfc22_in_air',
    'HFC-125':'mole_fraction_of_hfc125_in_air',
    'HFC-134a':'mole_fraction_of_hfc134a_in_air',
    'HFC-143a':'mole_fraction_of_hfc143a_in_air',
    'HFC-152a':'mole_fraction_of_hfc152a_in_air',
    'HFC-227ea':'mole_fraction_of_hfc227ea_in_air',
    'HFC-23':'mole_fraction_of_hfc23_in_air',
    'HFC-236fa':'mole_fraction_of_hfc236fa_in_air',
    'HFC-245fa':'mole_fraction_of_hfc245fa_in_air',
    'HFC-32':'mole_fraction_of_hfc32_in_air',
    'HFC-365mfc':'mole_fraction_of_hfc365mfc_in_air',
    'HFC-4310mee':'mole_fraction_of_hfc4310mee_in_air',
    'NF3':'mole_fraction_of_nf3_in_air',
    'SF6':'mole_fraction_of_sf6_in_air',
    'SO2F2':'mole_fraction_of_so2f2_in_air',
    
    'CFC11eq':'mole_fraction_of_cfc11eq_in_air',
    'CFC12eq':'mole_fraction_of_cfc12eq_in_air',
    'HFC-134aeq':'mole_fraction_of_hfc134aeq_in_air',
    }
    
fair_to_cmip6plus = {    
    'CO2':'co2',
    'CH4':'ch4',
    'N2O':'n2o',
    'C2F6':'pfc116',
    'C3F8':'pfc218',
    'C4F10':'pfc3110',
    'C5F12':'pfc4112',
    'C6F14':'pfc5114',
    'C7F16':'pfc6116',
    'C8F18':'pfc7118',
    'c-C4F8':'pfc318',
    'CCl4':'ccl4',
    'CF4':'cf4',
    'CFC-11':'cfc11',
    'CFC-113':'cfc113',
    'CFC-114':'cfc114',
    'CFC-115':'cfc115',
    'CFC-12':'cfc12',
    'CH2Cl2':'ch2cl2',
    'CH3Br':'ch3br',
    'CH3CCl3':'hcc140a',
    'CH3Cl':'ch3cl',
    'CHCl3':'chcl3',
    'Halon-1211':'halon1211',
    'Halon-1301':'halon1301',
    'Halon-2402':'halon2402',
    'HCFC-141b':'hcfc141b',
    'HCFC-142b':'hcfc142b',
    'HCFC-22':'hcfc22',
    'HFC-125':'hfc125',
    'HFC-134a':'hfc134a',
    'HFC-143a':'hfc143a',
    'HFC-152a':'hfc152a',
    'HFC-227ea':'hfc227ea',
    'HFC-23':'hfc23',
    'HFC-236fa':'hfc236fa',
    'HFC-245fa':'hfc245fa',
    'HFC-32':'hfc32',
    'HFC-365mfc':'hfc365mfc',
    'HFC-4310mee':'hfc4310mee',
    'NF3':'nf3',
    'SF6':'sf6',
    'SO2F2':'so2f2',
    
    'CFC11eq':'cfc11eq',
    'CFC12eq':'cfc12eq',
    'HFC-134aeq':'hfc134aeq',
    }

fair_to_cmip7 = {
    'CO2':'co2',
    'CH4':'ch4',
    'N2O':'n2o',
    'C2F6':'c2f6',
    'C3F8':'c3f8',
    'C4F10':'c4f10',
    'C5F12':'c5f12',
    'C6F14':'c6f14',
    'C7F16':'c7f16',
    'C8F18':'c8f18',
    'c-C4F8':'cc4f8',
    'CCl4':'ccl4',
    'CF4':'cf4',
    'CFC-11':'cfc11',
    'CFC-113':'cfc113',
    'CFC-114':'cfc114',
    'CFC-115':'cfc115',
    'CFC-12':'cfc12',
    'CH2Cl2':'ch2cl2',
    'CH3Br':'ch3br',
    'CH3CCl3':'ch3ccl3',
    'CH3Cl':'ch3cl',
    'CHCl3':'chcl3',
    'Halon-1211':'halon1211',
    'Halon-1301':'halon1301',
    'Halon-2402':'halon2402',
    'HCFC-141b':'hcfc141b',
    'HCFC-142b':'hcfc142b',
    'HCFC-22':'hcfc22',
    'HFC-125':'hfc125',
    'HFC-134a':'hfc134a',
    'HFC-143a':'hfc143a',
    'HFC-152a':'hfc152a',
    'HFC-227ea':'hfc227ea',
    'HFC-23':'hfc23',
    'HFC-236fa':'hfc236fa',
    'HFC-245fa':'hfc245fa',
    'HFC-32':'hfc32',
    'HFC-365mfc':'hfc365mfc',
    'HFC-4310mee':'hfc4310mee',
    'NF3':'nf3',
    'SF6':'sf6',
    'SO2F2':'so2f2',
    
    'CFC11eq':'cfc11eq',
    'CFC12eq':'cfc12eq',
    'HFC-134aeq':'hfc134aeq',
    }

#%%


spec_data = {}
spec_data['time'] = {}
spec_data['data'] = {}

for gen in gens:
    spec_data['time'][gen] = {}
    spec_data['data'][gen] = {}


units_conv_cmip6_cmipplus = {
    "1.e-6":"ppm",
    "1.e-9":"ppb",
    "1.e-12":"ppt",
}
    

for specie in species:
    print(specie)


    # cmip6
    
    file_cmip6 = (
    f'{datadir}/cmip6/{timestep}/{fair_to_cmip6[specie].replace("_","-")}'
    '_input4MIPs_GHGConcentrations_CMIP_UoM-CMIP-1-2-0_gr1-GMNHSH_0000-2014.nc'
        )
    
    ## cribbed from Zeb
    out = xr.open_dataset(file_cmip6, decode_times=False)
    
    if out.attrs["frequency"] == "yr":
        out = out.isel(time=slice(1, None))
    
    else:
        out = out.isel(time=slice(12, None))
    
    if out["time"].attrs["units"] == "days since 0-1-1":
        out["time"].attrs["units"] =  "days since 0001-1-1"
        old_attrs = out["time"].attrs
        out["time"] = out["time"] - 365
        out["time"].attrs = old_attrs
    
    out = xr.decode_cf(out, decode_times=True, use_cftime=True)

    spec_data['time']['CMIP6'][specie] = out['time']
    spec_data['data']['CMIP6'][specie] = out[fair_to_cmip6[specie]].sel(sector=0)
        
    
    # cmip6plus
    
    data_folders = os.listdir(f"{datadir}/cmip6plus/{timestep}/{fair_to_cmip6plus[specie]}/gm/")
    if len(data_folders) > 1:
        print(f'{len(data_folders)} for {fair_to_cmip6plus[specie]}')
    data_folder = data_folders[0]

    files = os.listdir(f"{datadir}/cmip6plus/{timestep}/{fair_to_cmip6plus[specie]}/gm/{data_folder}/")
    if len(files) > 1:
        print(f'{len(files)} for {fair_to_cmip6plus[specie]}')

    file_cmip6plus = f"{datadir}/cmip6plus/{timestep}/{fair_to_cmip6plus[specie]}/gm/{data_folder}/{files[0]}"

    with xr.open_dataset(file_cmip6plus, use_cftime=True) as ds:
        ds.convert_calendar("proleptic_gregorian")
        spec_data['time']['CMIP6Plus'][specie] = ds['time']
        spec_data['data']['CMIP6Plus'][specie] = ds[fair_to_cmip6plus[specie]]
        
        
    # cmip7
    
    filelist = glob.glob(f"{datadir}/cmip7/{timestep}/{fair_to_cmip7[specie]}_*nc")

    with xr.open_mfdataset(filelist, use_cftime=True) as ds:
        ds.convert_calendar("proleptic_gregorian")
        spec_data['time']['CMIP7'][specie] = ds['time']
        spec_data['data']['CMIP7'][specie] = ds[fair_to_cmip7[specie]]
        
        
#%%

f_gases = ['CF4',
 'C2F6',
 'C3F8',
 'c-C4F8',
 'C7F16',
 'C8F18',
 'NF3',
 'SF6',
 'SO2F2',
 'HFC-125',
 'HFC-134a',
 'HFC-143a',
 'HFC-152a',
 'HFC-227ea',
 'HFC-23',
 'HFC-236fa',
 'HFC-245fa',
 'HFC-32',
 'HFC-365mfc',
 'C4F10',
 'C5F12',
 'C6F14',
 'HFC-4310mee']

montreals = ['CFC-11',
 'CFC-113',
 'CFC-114',
 'CFC-115',
 'CFC11eq',
 'CFC-12',
 'CFC12eq',
 'HCFC-141b',
 'HCFC-142b',
 'HCFC-22',
 'CCl4',
 'Halon-1211',
 'Halon-1301',
 'Halon-2402']

cfcs = ['CFC-11', 'CFC-113', 'CFC-114', 'CFC-115', 'CFC11eq', 'CFC-12', 'CFC12eq']

hcfcs = ['HCFC-141b', 'HCFC-142b', 'HCFC-22']

halons = ['Halon-1211', 'Halon-1301', 'Halon-2402']

var_groups = {
    'All':[],
    'Going negative':['C3F8', 'HCFC-142b', 'HFC-143a', 'HFC-152a', 'HFC-227ea', 'HFC-236fa', 'NF3'],
    'CO2, CH4, N2O':['CO2', 'CH4', 'N2O'],
    'CFC114':['CFC-114'],
    'Accelerating HFCs':['HFC-32', 'HFC-125', 'HFC-134a', 'HFC-134aeq', 'HFC-143a', 'HFC-227ea'],
    'F-gases':f_gases,
    'Montreal gases':montreals,
    'CFCs':cfcs,
    'HCFCs':hcfcs,
    'Halons':halons,
    # 'Ozone':['Ozone'],
    # 'Equivalent effective stratospheric chlorine':['Equivalent effective stratospheric chlorine'],
    'CO2':['CO2'],
    'CH4':['CH4'],
    'N2O':['N2O'],
    }

#%%

f = FAIR()
f.define_time(1750, 2035, 1)
scenarios = ['ssp119']
f.define_scenarios(scenarios)
configs = ['test']
f.define_configs(configs)
species, properties = read_properties()
f.define_species(species, properties)

with open('save_forcings.pkl', 'rb') as handle:
    fair_forcings = pickle.load(handle)
    
gen_comps = [
    ['CMIP7', 'CMIP6'], # i.e. plot CMIP7 - CMIP6 etc
    ['CMIP7', 'CMIP6Plus'],
    ['CMIP6Plus', 'CMIP6'],
    ]

SIZE_DEFAULT = 14
SIZE_LARGE = 16

time_ax2 = 2014 + np.arange(9)

for gen_comp in gen_comps:
    end_yr = 2022
    if 'CMIP6' in gen_comp:
        end_yr = 2014
    
    forc_len = end_yr - 1750 + 1
    time_conc = 1 + np.arange(end_yr)
    time_forc = 1750 + np.arange(forc_len)


    
    for var_group in var_groups.keys():
        fig = plt.figure(figsize=(16, 8))
            
        plt.rc("font", weight="normal")  # controls default font
        plt.rc("font", size=SIZE_DEFAULT)  # controls default text sizes
        plt.rc("axes", titlesize=SIZE_LARGE)  # fontsize of the axes title
        plt.rc("axes", labelsize=SIZE_LARGE)  # fontsize of the x and y labels
        plt.rc("xtick", labelsize=SIZE_DEFAULT)  # fontsize of the tick labels
        plt.rc("ytick", labelsize=SIZE_DEFAULT)  # fontsize of the tick labels
    
        ax = fig.add_subplot(121)
        if 'CMIP6' in gen_comp:
            ax2 = ax.twinx()
    
        
        specs_ordered = copy.deepcopy(list(fair_to_cmip6plus.keys()))   
        specs_ordered = [e for e in specs_ordered if e not in var_groups[var_group]]
        
        specs_ordered.extend(var_groups[var_group])
    
        for specie in specs_ordered:
            
    
            color='grey'
            linewidth = 1
            if specie in var_groups[var_group]:
                color='red'
                linewidth = 2
    
            gen2_in = spec_data['data'][gen_comp[0]][specie].values
            gen1_in = spec_data['data'][gen_comp[1]][specie].values
            
            diff = 100*(gen2_in[:end_yr] - gen1_in[:end_yr])/gen1_in[:end_yr]
        
            diff[diff >= 250] = np.nan
            diff[diff <= -250] = np.nan 
            
            ax.plot(time_conc, diff, color=color, linewidth=linewidth)
           
            if 'CMIP6' in gen_comp:
                change_cf_2005_14 = 100*(gen2_in[2013:] - np.mean(gen2_in[2004:2014]))/np.mean(gen2_in[2004:2014])
                ax2.plot(time_ax2, change_cf_2005_14, color=color, linewidth=linewidth)
                
    
    
        ax.set_ylim([-200, 200])
        ax.set_ylabel(f'% change {gen_comp[0]} cf {gen_comp[1]}')
        ax.set_xlim([1900, 2025])
        
    
        ax.set_title('Concentration')
        
        
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["top"].set_visible(False)
        
        if 'CMIP6' in gen_comp:
            ax.axvline(x=2014, color='black', linestyle='--')

            ax2.set_ylim([-50, 50])
            ax2.set_ylabel(f'% change in {gen_comp[0]} cf 2005-14')
        
            ax2.spines["right"].set_visible(False)
            ax2.spines["left"].set_visible(False)
            ax2.spines["top"].set_visible(False)
        
    
        if len(var_groups[var_group]) > 0:
            handles = []
            handles.append(Line2D([0], [0], label=var_group, color='red', linewidth=linewidth))
            ax.legend(handles=handles, loc='lower left')
    
        
    
        ax = fig.add_subplot(122)
        
        if 'CMIP6' in gen_comp:
            ax2 = ax.twinx()
            ax2.set_ylim([-10, 10])
            ax2.set_yticks(np.linspace(-8, 8, 5))
    
    
        for specie in specs_ordered:
            if specie not in f.species:
                continue
            
            color='grey'
            linewidth = 1
            if specie in var_groups[var_group]:
                color='red'
                linewidth = 2
    
        
            gen2_in = fair_forcings[gen_comp[0]][
                :,0,0,f.species.index(specie)]
            
            gen1_in = fair_forcings[gen_comp[1]][
                :,0,0,f.species.index(specie)]
                
        
            diff = gen2_in[:forc_len] - gen1_in[:forc_len]
            
            
            ax.plot(time_forc, 1000*diff, color=color, linewidth=linewidth)
        
            change_cf_2005_14 = gen2_in[-9:] - np.mean(gen2_in[-19:-9])
        
            if 'CMIP6' in gen_comp:
                ax2.plot(time_ax2, 1000*change_cf_2005_14, color=color, linewidth=linewidth)
        
    
        ax.set_ylim([-40, 40])
        ax.set_ylabel(f'{gen_comp[0]} - {gen_comp[1]} ' + r'(mWm$^{-2}$)')
        ax.set_xlim([1900, 2025])
        
        ax.set_title(r'Forcing (mWm$^{-2}$)')
    
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["top"].set_visible(False)
        
    
        if 'CMIP6' in gen_comp:
            ax.axvline(x=2014, color='black', linestyle='--')

            ax2.set_ylabel(f'Change in {gen_comp[0]} cf 2005-14 ' + r'(mWm$^{-2}$)')
            ax2.spines["right"].set_visible(False)
            ax2.spines["left"].set_visible(False)
            ax2.spines["top"].set_visible(False)
        
    
        if len(var_groups[var_group]) > 0:
            handles = []
            handles.append(Line2D([0], [0], label=var_group, color='red', linewidth=linewidth))
            ax.legend(handles=handles, loc='lower left')
    
    
        plt.tight_layout()
        
        
        plt.savefig(f'plots/plots_comparison/{var_group}_{gen_comp[0]}_cf_{gen_comp[1]}.png', dpi=100, transparent=True)
    
        plt.clf()
    
    
#%%

fair_to_cmip6plus["Ozone"] = "Ozone"
fair_to_cmip6plus["Equivalent effective stratospheric chlorine"] = "Equivalent effective stratospheric chlorine"

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
    'CO2, CH4, N2O':['CO2', 'CH4', 'N2O'],
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


plt.savefig('plots/plots_for_reading/conclusions_combined.png', dpi=100, transparent=True)
  

#%%
import numpy as np

o3_specs = []
# for cmip6plus_spec in cmip6plus_to_fair.keys():
    
#     if f_cmip6_inc_wmghgs.species_configs['ozone_radiative_efficiency'
#           ][0,f_cmip6_inc_wmghgs.species.index(cmip6plus_to_fair[cmip6plus_spec])] == 0:
#         o3_specs.append(cmip6plus_to_fair[cmip6plus_spec])
#         continue
#     elif f_cmip6_inc_wmghgs.species_configs['cl_atoms'
#           ][f_cmip6_inc_wmghgs.species.index(cmip6plus_to_fair[cmip6plus_spec])] not in [0.0, np.nan]:
#         o3_specs.append(cmip6plus_to_fair[cmip6plus_spec])
#         continue
#     elif f_cmip6_inc_wmghgs.species_configs['br_atoms'
#           ][f_cmip6_inc_wmghgs.species.index(cmip6plus_to_fair[cmip6plus_spec])] not in [0.0, np.nan]:
#         o3_specs.append(cmip6plus_to_fair[cmip6plus_spec])
#         continue    
#     else:
#         continue
 
for cmip6plus_spec in cmip6plus_to_fair.keys():
    o3_specs.append(cmip6plus_to_fair[cmip6plus_spec])

o3_specs = [e for e in o3_specs if e not in ('Ozone', 'Equivalent effective stratospheric chlorine')]


#%%
o3_dict = {}
o3_dict['Temperature'] = {}
o3_dict['O3 Forcing'] = {}


for o3_spec in o3_specs:
    
    
        
    f_cmip6plus_inc_wmghgs_o3 = FAIR()
    
    f_cmip6plus_inc_wmghgs_o3.define_time(1750, 2022, 1)
    
    scenarios = ['ssp245']
    f_cmip6plus_inc_wmghgs_o3.define_scenarios(scenarios)
    
    configs = ['test']
    f_cmip6plus_inc_wmghgs_o3.define_configs(configs)
    
    species, properties = read_properties()
    
    
    for cmip6_spec in cmip6plus_to_fair.keys():
        if cmip6_spec not in ['Ozone', 'Equivalent effective stratospheric chlorine']:
            properties[cmip6plus_to_fair[cmip6_spec]]['input_mode'] = 'concentration'
            
    
    f_cmip6plus_inc_wmghgs_o3.define_species(species, properties)
    
    f_cmip6plus_inc_wmghgs_o3.allocate()
    f_cmip6plus_inc_wmghgs_o3.fill_species_configs()
    f_cmip6plus_inc_wmghgs_o3.fill_from_rcmip()
    
    initialise(f_cmip6plus_inc_wmghgs_o3.concentration, f_cmip6plus_inc_wmghgs_o3.species_configs['baseline_concentration'])
    initialise(f_cmip6plus_inc_wmghgs_o3.forcing, 0)
    initialise(f_cmip6plus_inc_wmghgs_o3.temperature, 0)
    initialise(f_cmip6plus_inc_wmghgs_o3.cumulative_emissions, 0)
    initialise(f_cmip6plus_inc_wmghgs_o3.airborne_emissions, 0)
    
    capacities = [4.22335014, 16.5073541, 86.1841127]
    kappas = [1.31180598, 2.61194068, 0.92986733]
    epsilon = 1.29020599
    fill(f_cmip6plus_inc_wmghgs_o3.climate_configs['ocean_heat_capacity'], capacities)
    fill(f_cmip6plus_inc_wmghgs_o3.climate_configs['ocean_heat_transfer'], kappas)
    fill(f_cmip6plus_inc_wmghgs_o3.climate_configs['deep_ocean_efficacy'], epsilon)
    
    units = {}
    
    for cmip6plus_spec in cmip6plus_to_fair.keys():
        
        if cmip6plus_to_fair[cmip6plus_spec] != o3_spec:
            continue
        else:
            print(o3_spec)
        
        #print(cmip6plus_spec)
        
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
    
            
            f_cmip6plus_inc_wmghgs_o3.concentration.loc[
                dict(specie=cmip6plus_to_fair[cmip6plus_spec])
            ][:,0,0] = da.sel(time=(slice('1750', '2022'))).rename({'time': 'timepoints'}).data 
            
            if cmip6plus_to_fair[cmip6plus_spec] not in ['CO2', 'CH4', 'N2O']:
        
                f_cmip6plus_inc_wmghgs_o3.species_configs['baseline_concentration'][
                    0,f_cmip6plus_inc_wmghgs_o3.species.index(cmip6plus_to_fair[cmip6plus_spec])
                    ] = f_cmip6plus_inc_wmghgs_o3.concentration[0,0,0,f_cmip6plus_inc_wmghgs_o3.species.index(cmip6plus_to_fair[cmip6plus_spec])]
        
                f_cmip6plus_inc_wmghgs_o3.species_configs['forcing_reference_concentration'][
                    0,f_cmip6plus_inc_wmghgs_o3.species.index(cmip6plus_to_fair[cmip6plus_spec])
                    ] = f_cmip6plus_inc_wmghgs_o3.concentration[0,0,0,f_cmip6plus_inc_wmghgs_o3.species.index(cmip6plus_to_fair[cmip6plus_spec])]
                        
            
            units[cmip6plus_to_fair[cmip6plus_spec]] = da.attrs["units"]
    
    f_cmip6plus_inc_wmghgs_o3.run()
    
    o3_dict['Temperature'][o3_spec] = f_cmip6plus_inc_wmghgs_o3.temperature[:,0,
             0,0]
    
    o3_dict['O3 Forcing'][o3_spec] = f_cmip6plus_inc_wmghgs_o3.forcing[
        :,0,0,f_ssps.species.index('Ozone')]
    
#%%  
  

colors_list = ['#17becf', '#bcbd22', '#e377c2', '#8c564b',
 '#9467bd', '#d62728', '#2ca02c', '#ff7f0e', '#1f77b4']

colors_list = colors_list * 5


cmip6_in = f_cmip6_inc_wmghgs.forcing[
    :,0,0,f_ssps.species.index('Ozone')]

cmip6_in_temp = f_cmip6_inc_wmghgs.temperature[
    :,0,0,0]

threshold = 0.0033

to_highlight = []
for o3_spec in o3_specs:
    abs_diff = np.abs(o3_dict['O3 Forcing'][o3_spec][:265] - cmip6_in)
    
    if np.amax(abs_diff) > threshold:
        to_highlight.append(o3_spec)


#%%
fig = plt.figure(figsize=(24, 8))

ax = fig.add_subplot(131)
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


for o3_spec in o3_specs:

    
    specie_fair = fair_to_cmip6plus[o3_spec]
    

    if o3_spec not in to_highlight:
        color='grey'
        linewidth=1
    else:
        color=colors_list[to_highlight.index(o3_spec)]
        linewidth = 2


    diff = save_dict[specie_fair]['diff']

    diff[diff >= 250] = np.nan
    diff[diff <= -250] = np.nan 
    
    ax.plot(time_conc, diff, color=color, linewidth=linewidth)
   
    change_cf_2005_14 = save_dict[specie_fair]['change_cf_2005_14']

    ax2.plot(time2_conc, change_cf_2005_14, color=color, linewidth=linewidth)
        

handles = []
for o3_i, o3_spec in enumerate(to_highlight):
    handles.append(Line2D([0], [0], label=o3_spec, 
      color=colors_list[o3_i], linewidth=2))
    
ax.legend(handles=handles, loc='lower left', framealpha=1)
        

ax = fig.add_subplot(132)
ax2 = ax.twinx()

ax.set_ylim([-40, 40])
ax.set_ylabel(r'CMIP6Plus - CMIP6 (mWm$^{-2}$)')
ax.set_xlim([1900, 2025])

ax.axvline(x=2014, color='black', linestyle='--')

ax2.set_ylim([-40, 40])
# ax2.set_yticks(np.linspace(-8, 8, 5))


ax2.set_ylabel(r'Change in CMIP6Plus cf 2005-14 (mWm$^{-2}$)')
ax.set_title(rf'O3 ERF change, species with max > {1000*threshold} (mWm$^{-2}$)')

ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["top"].set_visible(False)

ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_visible(False)
ax2.spines["top"].set_visible(False)

diff_sum = np.zeros(265)

for o3_spec in o3_specs:
    print(o3_spec)
    
    specie_fair = fair_to_cmip6plus[o3_spec]
    
    if o3_spec not in to_highlight:
        color='grey'
        linewidth=1
    else:
        color=colors_list[to_highlight.index(o3_spec)]
        linewidth = 2
        
    cmip6plus_o3_in = o3_dict['O3 Forcing'][o3_spec]
        
    
    diff = cmip6plus_o3_in[:265] - cmip6_in
    
    if o3_spec in to_highlight:
        diff_sum += diff
        print(1000*np.amax(diff_sum.values))
    
    ax.plot(time, 1000*diff, color=color, linewidth=linewidth)
   

    change_cf_2005_14 = cmip6plus_o3_in[-9:] - np.mean(cmip6plus_o3_in[-19:-9])

    ax2.plot(time2, 1000*change_cf_2005_14, color=color, linewidth=linewidth)
    

cmip6plus_in = f_cmip6plus_inc_wmghgs.forcing[
    :,0,0,f_ssps.species.index('Ozone')]
    
diff_full = cmip6plus_in[:265] - cmip6_in

ax.plot(time, 1000*diff_full, color='black', linewidth=3)
   
ax.plot(time, 1000*diff_sum, color='black', linewidth=2, linestyle='--')

change_cf_2005_14 = cmip6plus_in[-9:] - np.mean(cmip6plus_in[-19:-9])

ax2.plot(time2, 1000*change_cf_2005_14, color='black', linewidth=3) 
   



handles.append(Line2D([0], [0], label='All species', 
  color='black', linewidth=3))
handles.append(Line2D([0], [0], label='Sum of coloured', color='black', linewidth=2, linestyle='--'))

ax.legend(handles=handles, loc='upper left', ncol=2)



ax = fig.add_subplot(133)
ax2 = ax.twinx()

ax.set_ylim([-0.01, 0.01])
ax.set_ylabel(r'CMIP6Plus - CMIP6 K')
ax.set_xlim([1900, 2025])

ax.axvline(x=2014, color='black', linestyle='--')

ax2.set_ylim([-0.01, 0.01])
# ax2.set_yticks(np.linspace(-8, 8, 5))


ax2.set_ylabel(r'Change in CMIP6Plus cf 2005-14 K')
ax.set_title(rf'Temp change, species with max > {1000*threshold} (mWm$^{-2}$)')

ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["top"].set_visible(False)

ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_visible(False)
ax2.spines["top"].set_visible(False)



for o3_spec in o3_specs:
    
    specie_fair = fair_to_cmip6plus[o3_spec]
    
    if o3_spec not in to_highlight:
        color='grey'
        linewidth=1
    else:
        color=colors_list[to_highlight.index(o3_spec)]
        linewidth = 2
        
    cmip6plus_o3_in = o3_dict['Temperature'][o3_spec]
        
    
    diff = cmip6plus_o3_in[:265] - cmip6_in_temp
    
    ax.plot(time, diff, color=color, linewidth=linewidth)
   

    change_cf_2005_14 = cmip6plus_o3_in[-9:] - np.mean(cmip6plus_o3_in[-19:-9])

    ax2.plot(time2, change_cf_2005_14, color=color, linewidth=linewidth)
    


cmip6plus_in = f_cmip6plus_inc_wmghgs.temperature[
    :,0,0,0]
    
diff_full = cmip6plus_in[:265] - cmip6_in_temp

ax.plot(time, diff_full, color='black', linewidth=3)
   

change_cf_2005_14 = cmip6plus_in[-9:] - np.mean(cmip6plus_in[-19:-9])

ax2.plot(time2, change_cf_2005_14, color='black', linewidth=3) 
   


ax.legend(handles=handles, loc='upper left', ncol=2)


plt.tight_layout()


plt.savefig('plots/plots_for_reading/Ozone_by_contributors.png', dpi=100, transparent=True)
  



