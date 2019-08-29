# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'scripts'))
	print(os.getcwd())
except:
	pass
#%%
from IPython import get_ipython

#%% [markdown]
# ## TEMBA results visualisation Jupyter notebook

#%%
import os, sys
import pandas as pd
import numpy as np
from IPython.display import HTML
import ipywidgets as widgets
from IPython.display import display
#import matplotlib as plt
from ipywidgets import interact, interactive, fixed, interact_manual
#importing plotly and cufflinks in offline mode
import plotly as py
import psutil
import pickle
import plotly.graph_objs as go
import plotly.io as pio
import cufflinks
import plotly.offline as pyo
from plotly.offline import plot, iplot, init_notebook_mode
pyo.init_notebook_mode()
cufflinks.go_offline()
cufflinks.set_config_file(world_readable=True, theme='white')
from tkinter import filedialog
from tkinter import *
homedir=os.getcwd()



#%%
# Interactive widget for choosing the results to visualise
from glob import glob

# Extract the result files from those stored in the directory
options = [(x.split(".pickle")[0], x) for x in glob('*.pickle')]

# Build a dropdown widget to select the results you wish to view
result_dropdown = widgets.Dropdown(
    options=options,
    description='Select TEMBA results to view:',
)

def update_results(change):
    """Handles the change in the dropdown menu to select the pickle file and scenario
    """
    global all_params
    # The pickle file for the corressponding powerpool/TEMBA is unbundled in the following steps
    picklefile=change['new']
    pkl_file = open(picklefile, 'rb')
    # The pickle file is loaded onto the all_params dictionary
    all_params = pickle.load(pkl_file)
    
    #Automatic naming of scenarios based on pickle file selection
    #global scenario
    #scen_name=change['new']
    #scenario=scen_name.split('pickle')[0]

result_dropdown.observe(update_results, names='value')

#%% [markdown]
# # Please select the power-pool or TEMBA results that you want to visualize

#%%
display(result_dropdown)


#%%
scenario=input('Enter scenario name:')


#%%
#Fundamental dictionaries that govern naming and colour coding
url1='./agg_col.csv'
url2='./agg_pow_col.csv'
url3='./countrycode.csv'
url4='./power_tech.csv'
url5='./techcodes.csv'
colorcode=pd.read_csv(url5,sep=',',encoding = "ISO-8859-1")
colorcode1=colorcode.drop('colour',axis=1)
colorcode2=colorcode.drop('tech_code',axis=1)
det_col=dict([(a,b) for a,b in zip(colorcode1.tech_code,colorcode1.tech_name)])
color_dict=dict([(a,b) for a,b in zip(colorcode2.tech_name,colorcode2.colour)])
agg1=pd.read_csv(url1,sep=',',encoding = "ISO-8859-1")
agg2=pd.read_csv(url2,sep=',',encoding = "ISO-8859-1")
agg_col=agg1.to_dict('list')
agg_pow_col=agg2.to_dict('list')
power_tech=pd.read_csv(url4,sep=',',encoding = "ISO-8859-1")
t_include = list(power_tech['power_tech'])
#Country code list
country_code=pd.read_csv(url3,sep=',',encoding = "ISO-8859-1")


#%%
# time period definition
years = pd.Series(range(2015,2071))
#home directory for any image/CSV creation
homedir=os.getcwd()


#%%
#base function used for many different variables (mainly cost)
def df_filter(df,lb,ub,t_exclude):
    df['t'] = df['t'].str[lb:ub]
    df['value'] = df['value'].astype('float64')
    df = df[~df['t'].isin(t_exclude)].pivot_table(index='y', 
                                          columns='t',
                                          values='value', 
                                          aggfunc='sum').reset_index().fillna(0)
    df = df.reindex(sorted(df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    df['y'] = years
    #df=df[df['y']>2018]
    return df
#### PLotting function for all graphs except Gas (as it needs relative charts)
def df_plot(df,y_title,p_title):
    if len(df.columns)==1:
        print('There are no values for the result variable that you want to plot')
    else:
        fig = df.iplot(x='y',
             kind='bar', 
             barmode='stack',
             xTitle='Year',
             yTitle=y_title,
             color=[color_dict[x] for x in df.columns if x != 'y'],
             title=(p_title+"-"+scenario),
             showlegend=True,
             asFigure=True)
        fig.update_xaxes(range=[2015,2065]) 
        pio.write_image(fig, '{}.png'.format(p_title))
        df.to_csv(os.path.join(homedir,p_title+"-"+scenario+".csv"))
        return iplot(fig)
#### Emissions#####
def df_filter_emission_tech(df,lb,ub):
    df['t'] = df['t'].str[lb:ub]
    df['e'] = df['e'].str[2:5]
    df['value'] = df['value'].astype('float64')
    df = df.pivot_table(index='y',columns='t',
                        values='value',
                        aggfunc='sum').reset_index().fillna(0)
    df = df.reindex(sorted(df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    df['y'] = years
    #df=df[df['y']>2018]
    return df
### Annual Emissions
def df_filter_emission_tot(df):
    df['e'] = df['e'].str[2:5]
    df['value'] = df['value'].astype('float64')
    df = df.pivot_table(index='y',columns='e',
                        values='value',
                        aggfunc='sum').reset_index().fillna(0)
    df = df.reindex(sorted(df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    df['y'] = years
    #df=df[df['y']>2018]
    return df


#%%
def power_chart(Country):
    cc=country_code[country_code['Country Name']==Country]['Country code'].tolist()[0]
    #print('The country code is:'+cc)
    # Power capacity (detailed)
    #cap_df = all_params['TotalCapacityAnnual'][all_params['TotalCapacityAnnual'].t.str.startswith('PWR')].drop('r', axis=1)
    cap_df = all_params['TotalCapacityAnnual']
    cap_df=cap_df[cap_df['t'].str[:2]==cc].copy()
    cap_df['t'] = cap_df['t'].str[2:10]
    cap_df['value'] = cap_df['value'].astype('float64')
    cap_df = cap_df[cap_df['t'].isin(t_include)].pivot_table(index='y', 
                                               columns='t',
                                               values='value', 
                                               aggfunc='sum').reset_index().fillna(0)
    cap_df = cap_df.reindex(sorted(cap_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    #cap_df['y'] = years
    #cap_df=cap_df[cap_df['y']>2018]
    # The following code can be unhashed to get a detailed power capcity graph.
    #df_plot(cap_df,'Gigawatts (GW)',cc+"-"+'Power Generation Capacity (Detail)')
    #***********************************************
    # Power capacity (Aggregated)
    cap_agg_df = pd.DataFrame(columns=agg_pow_col)
    cap_agg_df.insert(0,'y',cap_df['y'])
    cap_agg_df  = cap_agg_df.fillna(0.00)
    #
    for each in agg_pow_col:
        for tech_exists in agg_pow_col[each]:
            if tech_exists in cap_df.columns:
                try:
                    cap_agg_df[each] = cap_agg_df[each] + cap_df[tech_exists]
                except TypeError as ex:
                    print(cap_agg_df[each].dtypes,cap_df[tech_exists].dtypes)
                    raise TypeError(ex)
                cap_agg_df[each] = cap_agg_df[each].round(3)
    #
    df_plot(cap_agg_df,'Gigawatts (GW)',cc+"-"+'Power Generation Capacity (Aggregate)')
    #df_plot(gen_agg_df,'Petajoules (PJ)',cc+"-"+'Power Generation (Aggregate)')
    # New capacity (detailed)
    cap_new_df = all_params['NewCapacity']
    cap_new_df=cap_new_df[cap_new_df['t'].str[:2]==cc].copy()
    cap_new_df['t'] = cap_new_df['t'].str[2:10]
    cap_new_df['value'] = cap_new_df['value'].astype('float64')
    cap_new_df = cap_new_df[cap_new_df['t'].isin(t_include)].pivot_table(index='y', 
                                               columns='t',
                                               values='value', 
                                               aggfunc='sum').reset_index().fillna(0)
    cap_new_df = cap_new_df.reindex(sorted(cap_new_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    #cap_new_df['y'] = years
    #cap_new_df=cap_new_df[cap_new_df['y']>2018]
    # The following code can be unhashed to get a detailed power capacity graph.
    #df_plot(cap_new_df,'Gigawatts (GW)','New Power Generation Capacity (Detail)')
    #***********************************************
    # Power capacity (Aggregated)
    cap_new_agg_df = pd.DataFrame(columns=agg_pow_col)
    cap_new_agg_df.insert(0,'y',cap_new_df['y'])
    cap_new_agg_df  = cap_new_agg_df.fillna(0.00)
    #
    for each in agg_pow_col:
        for tech_exists in agg_pow_col[each]:
            if tech_exists in cap_new_df.columns:
                cap_new_agg_df[each] = cap_new_agg_df[each] + cap_new_df[tech_exists]
                cap_new_agg_df[each] = cap_new_agg_df[each].round(3)
                ##
    df_plot(cap_new_agg_df,'Gigawatts (GW)',cc+"-"+ 'New power generation capacity (Aggregate)')

    ## Power generation (Detailed)
    gen_df = all_params['ProductionByTechnologyAnnual'].copy()
    #gen_df=gen_df[gen_df['t'].str[:2]==cc].copy()
    #gen_df['t'] = gen_df['t'].str[2:10]
    gen_df_export=gen_df[(gen_df['f'].str[2:6]=='EL01')&(gen_df['f'].str[0:2]!=cc)].copy()
    gen_df_export=gen_df_export[gen_df_export['t'].str[6:10]=='BP00'].copy()
    gen_df_export=gen_df_export[(gen_df_export['t'].str[0:2]==cc)|(gen_df_export['t'].str[4:6]==cc)]
    gen_df_export['value'] = gen_df_export['value'].astype(float)*-1
    gen_df=gen_df[(gen_df['f'].str[:2]==cc)].copy()
    gen_df=gen_df[(gen_df['f'].str[2:6]=='EL01')|(gen_df['f'].str[2:6]=='EL03')].copy()
    gen_df=gen_df[(gen_df['t'].str[2:10]!='EL00T00X')&(gen_df['t'].str[2:10]!='EL00TDTX')].copy()
    gen_df=pd.concat([gen_df,gen_df_export])
    gen_df['value'] = gen_df['value'].astype('float64')
    gen_df = gen_df.pivot_table(index='y', 
                                           columns='t',
                                           values='value', 
                                           aggfunc='sum').reset_index().fillna(0)
    for each in gen_df.columns:
        if len(each)!=1:
            if (each[2:4]=='EL') & (each[6:10]=='BP00'):
                pass
            else:
                gen_df.rename(columns={each:each[2:10]},inplace=True)
        else:
            pass
    gen_df = gen_df.reindex(sorted(gen_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    #gen_df['y'] = years
    #gen_df=gen_df[gen_df['y']>2018]
    #df_plot(gen_df,'Petajoules (PJ)',cc+"-"+'Power Generation (Detail)')
    #####
    # Power generation (Aggregated)
    gen_agg_df = pd.DataFrame(columns=agg_pow_col)
    gen_agg_df.insert(0,'y',gen_df['y'])
    gen_agg_df  = gen_agg_df.fillna(0.00)
    for each in agg_pow_col:
        for tech_exists in agg_pow_col[each]:
            if tech_exists in gen_df.columns:
                gen_agg_df[each] = gen_agg_df[each] + gen_df[tech_exists]
                gen_agg_df[each] = gen_agg_df[each].round(2)
    fig = gen_agg_df.iplot(x='y',
                 kind='bar', 
                 barmode='relative',
                 xTitle='Year',
                 yTitle="Petajoules (PJ)",
                 color=[color_dict[x] for x in gen_agg_df.columns if x != 'y'],
                 title=cc+"-"+"Power Generation (Aggregate)"+scenario,
                 showlegend=True,
                 asFigure=True)
    fig.update_xaxes(range=[2015,2065]) 
    title=(cc+"-"+"Power Generation (Aggregate)")
    pio.write_image(fig, '{}.png'.format(title+"-"+scenario))
    gen_agg_df.to_csv(os.path.join(homedir,cc+"-"+"Power Generation (Aggregate)"+"-"+scenario+".csv"))
    return iplot(fig)
    


#%%
def water_chart (Country):
    cc=country_code[country_code['Country Name']==Country]['Country code'].tolist()[0]
    #print('The country code is:'+cc)
    #water withdrawal detailed
    wat_w_df = all_params['UseByTechnologyAnnual']
    wat_w_df=wat_w_df[wat_w_df['f'].str[:6]==cc+'WAT1'].copy()

    wat_w_df['t'] = wat_w_df['t'].str[2:10]
    wat_w_df['value'] = wat_w_df['value'].astype('float64')
    wat_w_df = wat_w_df.pivot_table(index='y', 
                                  columns='t',
                                  values='value', 
                                  aggfunc='sum').reset_index().fillna(0)
    wat_w_df = wat_w_df.reindex(sorted(wat_w_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    #wat_w_df['y'] = years
    #wat_w_df=wat_w_df[wat_w_df['y']>2018]
    #df_plot(wat_w_df,'Million cubic metres (Mm^3)',cc+"-"+'Water Withdrawal')
    ###
    #Water Withdrawal (Aggregated)
    watw_agg_df = pd.DataFrame(columns=agg_col)
    watw_agg_df.insert(0,'y',wat_w_df['y'])
    watw_agg_df  = watw_agg_df.fillna(0.00)
    for each in agg_col:
        for tech_exists in agg_col[each]:
            if tech_exists in wat_w_df.columns:
                watw_agg_df[each] = watw_agg_df[each] + wat_w_df[tech_exists]
                watw_agg_df[each] = watw_agg_df[each].round(2)

    df_plot(watw_agg_df,'Million cubic metres (Mm^3)',cc+"-"+'Water Withdrawal')
    ##
    #water output detailed
    wat_o_df = all_params['ProductionByTechnologyAnnual']
    wat_o_df=wat_o_df[wat_o_df['f'].str[:6]==cc+'WAT2'].copy()
    wat_o_df['t'] = wat_o_df['t'].str[2:10].copy()
    wat_o_df['value'] = wat_o_df['value'].astype('float64')
    wat_o_df = wat_o_df.pivot_table(index='y', 
                                 columns='t',
                                 values='value', 
                                 aggfunc='sum').reset_index().fillna(0)
    wat_o_df = wat_o_df.reindex(sorted(wat_o_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    #wat_o_df['y'] = years
    #wat_o_df=wat_o_df[wat_o_df['y']>2018]
    #df_plot(wat_o_df,'Million cubic metres (Mm^3)',cc+"-"+'Water output')
    ###
    #Water consumption missing row additions
    for wd in wat_w_df.columns:
        for wc in wat_o_df.columns:
            if wd in wat_o_df.columns:
                pass
            else:
                wat_o_df[wd]=0
    #####
    ####Water consumption (Detailed)
    wat_c_df=wat_w_df.set_index('y')-wat_o_df.set_index('y')
    wat_c_df=wat_c_df.fillna(0.00)
    wat_c_df.reset_index(inplace=True)
    #wat_c_df['y']=years
    #df_plot(wat_c_df,'Million cubic metres (Mm^3)',cc+"-"+'Water consumption')
    #Water consumption (Aggregate)
    watc_agg_df = pd.DataFrame(columns=agg_col)
    watc_agg_df.insert(0,'y',wat_c_df['y'])
    watc_agg_df  = watc_agg_df.fillna(0.00)
    for each in agg_col:
        for tech_exists in agg_col[each]:
            if tech_exists in wat_c_df.columns:
                watc_agg_df[each] = watc_agg_df[each] + wat_c_df[tech_exists]
                watc_agg_df[each] = watc_agg_df[each].round(2)
    df_plot(watc_agg_df,'Million cubic metres (Mm^3)',cc+'-'+'Water consumption aggregated')


#%%
def emissions_chart(Country):
    cc=country_code[country_code['Country Name']==Country]['Country code'].tolist()[0]
#     #CO2-Emission detailed
#     co2_df = all_params['AnnualTechnologyEmission']
#     co2_df=co2_df[co2_df['e'].str[:5]==cc+'CO2'].copy()

#     co2_df['value'] = co2_df['value'].astype('float64')
#     co2_df = co2_df.pivot_table(index='y',columns='t',
#                             values='value',
#                             aggfunc='sum').reset_index().fillna(0)
#     for each in co2_df.columns:
#         if len(each)!=1:
#             if (each[2:4]=='NG') & (each[6:10]=='BP00'):
#                 pass
#             else:
#                 co2_df.rename(columns={each:each[2:10]},inplace=True)
#         else:
#             pass
#     co2_df = co2_df.reindex(sorted(co2_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
#     #co2_df['y'] = years
#     #co2_df=co2_df[co2_df['y']>2018]
#     df_plot(co2_df,'Million Tonnes (Mt)',cc+'-'+'Emissions (CO2)-by technology')
#     co2_df.iplot(x='y',
#                   kind='bar', 
#                   barmode='relative',
#                   xTitle='Year',
#                   yTitle="Million Tonnes (Mt)",
#                   color=[color_dict[x] for x in co2_df.columns if x != 'y'],
#                   title=cc+'-'+'Emissions (CO2)-by technology',showlegend=True)
    #Total emissions by type- This graph shows the total emissions in the country by emissiontype
    emis_df = all_params['AnnualEmissions']
    emis_df=emis_df[emis_df['e'].str[:5]==cc+'CO2'].copy()
    emis_df = df_filter_emission_tot(emis_df)
    df_plot(emis_df,'Million Tonnes of CO2  (Mt)',cc+'-'+'Annual Emissions')


#%%
def gas_chart(Country):
    cc=country_code[country_code['Country Name']==Country]['Country code'].tolist()[0]
    #GAS Production (Detailed)
    gas_df = all_params['ProductionByTechnologyAnnual']
    gas_df_export1=gas_df[(gas_df['t'].str[0:4]==cc+'NG')&(gas_df['t'].str[6:10]=='BP00')].copy()
    gas_df_export1['value'] = gas_df_export1['value'].astype(float)*-1
    gas_df_import1=gas_df[(gas_df['t'].str[2:10]=='NG'+cc+'BP00')].copy()
    gas_df=gas_df[(gas_df['t'].str[:2]==cc)&(gas_df['t'].str[2:4]=='NG')&(gas_df['t'].str[6:7]!='P')].copy()
    gas_df= gas_df[(gas_df['t'].str[6:10]=='ELGX')|(gas_df['t'].str[6:10]=='ILGX')|(gas_df['t'].str[6:10]=='X00X')].copy()
    #gas_df = df_filter_gas(gas_df,2,10,gas_df_export1,gas_df_import1)
    gas_df['t'] = gas_df['t'].str[2:10]
    gas_df['value'] = gas_df['value'].astype('float64')
    gas_df['t'] = gas_df['t'].astype(str)
    gas_df=pd.concat([gas_df,gas_df_export1,gas_df_import1])
    gas_df = gas_df.pivot_table(index='y',columns='t',
                                      values='value', 
                                      aggfunc='sum').reset_index().fillna(0)
    gas_df = gas_df.reindex(sorted(gas_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    #gas_df['y'] = years
    #gas_df=gas_df[gas_df['y']>2018]
    for each in gas_df.columns:
        if each=='Natural gas exports (Liquification terminal)':
            gas_df[each] =gas_df[each].astype(float)*-1
        else:
            pass
    if len(gas_df.columns)==1:
            print('There are no values for the result variable that you want to plot')
    else:
        fig=gas_df.iplot(x='y',
                 kind='bar', 
                 barmode='relative',
                 xTitle='Year',
                 yTitle="Petajoules (PJ)",
                 color=[color_dict[x] for x in gas_df.columns if x != 'y'],
                 title=cc+"-"+"Gas extraction, imports and exports"+"-"+scenario,
                 showlegend=True,
                 asFigure=True)
        fig.update_xaxes(range=[2015,2065]) 
        title=(cc+"-"+"Gas extraction, imports and exports")
        pio.write_image(fig, '{}.png'.format(title+"-"+scenario),width=1300,height=800)
        gas_df.to_csv(os.path.join(homedir,cc+"-"+"Gas extraction, imports and exports"+"-"+scenario+".csv"))
        return iplot(fig)


#%%
def crude_chart(Country):
    cc=country_code[country_code['Country Name']==Country]['Country code'].tolist()[0]
    #Crude oil refined in the country
    cru_r_df = all_params['ProductionByTechnologyAnnual']
    cru_r_df=cru_r_df[cru_r_df['f'].str[:6]==cc+'CRU2'].copy()
    cru_r_df['t'] = cru_r_df['t'].str[2:10]
    cru_r_df['value'] = cru_r_df['value'].astype('float64')
    cru_r_df = cru_r_df.pivot_table(index='y',columns='t',
                                      values='value', 
                                      aggfunc='sum').reset_index().fillna(0)
    cru_r_df = cru_r_df.reindex(sorted(cru_r_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    #cru_r_df['y'] = years
    #cru_r_df=cru_r_df[cru_r_df['y']>2018]
    df_plot(cru_r_df,'Petajoules (PJ)',cc+'-'+'Crude oil refined in the country')
    #Crude oil production/imports/exports (Detailed)
    cru_df = all_params['ProductionByTechnologyAnnual']
    cru_df=cru_df[(cru_df['f'].str[:6]==cc+'CRU1')].copy()
    cru_df['t'] = cru_df['t'].str[2:10]
    cru_df['value'] = cru_df['value'].astype('float64')
    cru_df['t'] = cru_df['t'].astype(str)
    cru_df = cru_df.pivot_table(index='y',columns='t',
                                      values='value', 
                                      aggfunc='sum').reset_index().fillna(0)
    cru_df = cru_df.reindex(sorted(cru_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    #cru_df['y'] = years
    #cru_df=cru_df[cru_df['y']>2018]
    fig=cru_df.iplot(x='y',
                  kind='bar', 
                  barmode='relative',
                  xTitle='Year',
                  yTitle="Petajoules (PJ)",
                  color=[color_dict[x] for x in cru_df.columns if x != 'y'],
                  title=cc+"-"+"Crude oil extraction, imports and exports"+"-"+scenario,
                  showlegend=True,
                  asFigure=True)
    fig.update_xaxes(range=[2015,2065]) 
    title=(cc+"-"+"Crude oil extraction, imports and exports")
    pio.write_image(fig, '{}.png'.format(title+"-"+scenario))
    cru_df.to_csv(os.path.join(homedir,cc+"-"+"Crude oil extraction, imports and exports"+"-"+scenario+".csv"))
    return iplot(fig)
    


#%%
def coal_biomass_chart(Country):
    cc=country_code[country_code['Country Name']==Country]['Country code'].tolist()[0]
    #Coal overview
    coal_df = all_params['ProductionByTechnologyAnnual']
    coal_df=coal_df[coal_df['f'].str[:6]==cc+'COAL'].copy()
    coal_df['t'] = coal_df['t'].str[2:10]
    coal_df['value'] = coal_df['value'].astype('float64')
    coal_df = coal_df.pivot_table(index='y',columns='t',
                                      values='value', 
                                      aggfunc='sum').reset_index().fillna(0)
    coal_df = coal_df.reindex(sorted(coal_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    #coal_df['y'] = years
    #coal_df=coal_df[coal_df['y']>2018]
    df_plot(coal_df,'Petajoules (PJ)',cc+'-'+'Coal production by technology')
    #Biomass overview
    biom_df = all_params['ProductionByTechnologyAnnual']
    biom_df=biom_df[biom_df['f'].str[:6]==cc+'BIOM'].copy()
    biom_df['t'] = biom_df['t'].str[2:10]
    biom_df['value'] = biom_df['value'].astype('float64')
    biom_df = biom_df.pivot_table(index='y',columns='t',
                                      values='value', 
                                      aggfunc='sum').reset_index().fillna(0)
    biom_df = biom_df.reindex(sorted(biom_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    #biom_df['y'] = years
    #biom_df=biom_df[biom_df['y']>2018]
    df_plot(biom_df,'Petajoules (PJ)',cc+'-'+'Biomass production by technology')


#%%
def hfo_lfo_chart(Country):
    cc=country_code[country_code['Country Name']==Country]['Country code'].tolist()[0]
    #Heavy Fuel Oil overview
    hfo_df = all_params['ProductionByTechnologyAnnual']
    hfo_df=hfo_df[hfo_df['f'].str[:6]==cc+'HFOI'].copy()
    hfo_df['t'] = hfo_df['t'].str[2:10]
    hfo_df['value'] = hfo_df['value'].astype('float64')
    hfo_df = hfo_df.pivot_table(index='y',columns='t',
                                      values='value', 
                                      aggfunc='sum').reset_index().fillna(0)
    hfo_df = hfo_df.reindex(sorted(hfo_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    #hfo_df['y'] = years
    #hfo_df=hfo_df[hfo_df['y']>2018]
    df_plot(hfo_df,'Petajoules (PJ)',cc+'-'+'HFO production by technology')
    #Light Fuel Oil overview
    lfo_df = all_params['ProductionByTechnologyAnnual']
    lfo_df=lfo_df[lfo_df['f'].str[:6]==cc+'LFOI'].copy()
    lfo_df['t'] = lfo_df['t'].str[2:10]
    lfo_df['value'] = lfo_df['value'].astype('float64')
    lfo_df = lfo_df.pivot_table(index='y',columns='t',
                                      values='value', 
                                      aggfunc='sum').reset_index().fillna(0)
    lfo_df = lfo_df.reindex(sorted(lfo_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    #lfo_df['y'] = years
    #lfo_df=lfo_df[lfo_df['y']>2018]
    df_plot(lfo_df,'Petajoules (PJ)',cc+'-'+'LFO production by technology')

#%% [markdown]
# # CHOOSE THE COUNTRY TO VISUALIZE

#%%
country = widgets.Dropdown(options=country_code['Country Name'])
display(country)


#%%
power_chart(country.value)
water_chart(country.value)
emissions_chart(country.value)
gas_chart(country.value)
crude_chart(country.value)
coal_biomass_chart(country.value)
hfo_lfo_chart(country.value)

#%% [markdown]
# # The following code will produce the data necessary for electricity generation charts (bar graphs) for all countries in a specific year 
#%% [markdown]
# ## Please provide the year of your choice

#%%
ref_y=input("Please specify the year: ")
ref_y=int(ref_y)


#%%
get_ipython().run_line_magic('config', "InlineBackend.figure_format ='retina'")
# Input the year to be visualised

# taking the country codes from temba_dict
ccs=country_code['Country code'].values
total_df=[]
for cc in ccs:
    gen_df = all_params['ProductionByTechnologyAnnual'].copy()
    gen_df_export=gen_df[(gen_df['f'].str[2:6]=='EL01')&(gen_df['f'].str[0:2]!=cc)].copy()
    gen_df_export=gen_df_export[gen_df_export['t'].str[6:10]=='BP00'].copy()
    gen_df_export=gen_df_export[(gen_df_export['t'].str[0:2]==cc)|(gen_df_export['t'].str[4:6]==cc)]
    gen_df_export['value'] = gen_df_export['value'].astype(float)*-1
    gen_df=gen_df[(gen_df['f'].str[:2]==cc)].copy()
    gen_df=gen_df[(gen_df['f'].str[2:6]=='EL01')|(gen_df['f'].str[2:6]=='EL03')].copy()
    gen_df=gen_df[(gen_df['t'].str[2:10]!='EL00T00X')&(gen_df['t'].str[2:10]!='EL00TDTX')].copy()
    gen_df=pd.concat([gen_df,gen_df_export])
    gen_df['value'] = gen_df['value'].astype('float64')
    gen_df = gen_df.pivot_table(index='y', 
                                           columns='t',
                                           values='value', 
                                           aggfunc='sum').reset_index().fillna(0)
    for each in gen_df.columns:
        if len(each)!=1:
            if (each[2:4]=='EL') & (each[6:10]=='BP00'):
                pass
            else:
                gen_df.rename(columns={each:each[2:10]},inplace=True)
        else:
            pass
    gen_df = gen_df.reindex(sorted(gen_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    #gen_df['y'] = years
    #gen_df=gen_df[gen_df['y']>2018]
    #df_plot(gen_df,'Petajoules (PJ)',cc+"-"+'Power Generation (Detail)')
    #####
    # Power generation (Aggregated)
    gen_agg_df = pd.DataFrame(columns=agg_pow_col)
    gen_agg_df.insert(0,'y',gen_df['y'])
    gen_agg_df  = gen_agg_df.fillna(0.00)
    for each in agg_pow_col:
        for tech_exists in agg_pow_col[each]:
            if tech_exists in gen_df.columns:
                gen_agg_df[each] = gen_agg_df[each] + gen_df[tech_exists]
                gen_agg_df[each] = gen_agg_df[each].round(2)
#     gen_agg_df.iplot(x='y',
#                      kind='bar', 
#                      barmode='relative',
#                      xTitle='Year',
#                      yTitle="Petajoules (PJ)",
#                      color=[color_dict[x] for x in gen_agg_df.columns if x != 'y'],
#                      title=cc+"-"+"Power Generation (Aggregate)")
    gen_agg_df['Total']= gen_agg_df['Coal']+gen_agg_df['Oil']+gen_agg_df['Gas']+gen_agg_df['Hydro']+gen_agg_df['Nuclear']+gen_agg_df['Solar CSP']+gen_agg_df['Solar PV']+gen_agg_df['Wind']+gen_agg_df['Biomass']+gen_agg_df['Geothermal']+gen_agg_df['Backstop']+gen_agg_df['power_trade']
    gen_agg_df['CCC']=cc
    gen_agg_df=gen_agg_df[gen_agg_df['y']==ref_y].copy()
    total_df.append(gen_agg_df)
    #df_plot(gen_agg_df,'Petajoules (PJ)',cc+"-"+'Power Generation (Aggregate)')
total_df= pd.concat(total_df,ignore_index=True)
total_df=total_df.drop('y',axis=1)
total_df=total_df.drop('Total',axis=1)
total_df=total_df.drop('gas_trade',axis=1,)
# The csv file will be created in the home folder.
ref_y=str(ref_y)
total_df.to_csv(os.path.join(homedir,ref_y+"-generation"+"-"+scenario+".csv"),index=None)


#%%
# Dictionary for the powerpool classifications and countries
pp_def={'CAPP':['CM','CF','TD','CG','CD','GQ','GA'],
'EAPP':['BI','DJ','ER','ET','KE','RW','SO','SD','TZ','UG','EG','SS'],
'NAPP':['DZ','LY','MR','MA','TN'],
'SAPP':['AO','BW','LS','MW','MZ','NM','ZA','SZ','ZM','ZW'],
'WAPP':['BJ','BF','CI','GM','GH','GN','GW','LR','ML','NE','NG','SN','SL','TG'],     
'TEMBA':['DZ','EG','LY','MR','MA','TN','BI','DJ','ER','ET','KE','RW','SO','SD','TZ','UG',
                    'AO','BW','LS','MW','MZ','NM','ZA','SZ','ZM','ZW',
                    'BJ','BF','CI','GM','GH','GN','GW','LR','ML','NE','NG','SN','SL','TG','CM','CF','TD','CG','CD','GQ','GA','SS']}

#%% [markdown]
# # In the follwoing block, the capacity and generation graphs for all the powerpools and TEMBA will be plotted and CSV files generated

#%%
# first for loop to loop over the major dictionary keys 
for tk in pp_def.keys():
    # The following lines are used for creating dummy 
    #(empty) dataframes to print aggregated (powerpool/TEMBA) results as csv files
    total_gen_df=pd.DataFrame(np.zeros(shape=(56,14)),columns=['y','Coal','Oil','Gas','Hydro','Nuclear','Solar CSP','Solar PV',
                'Wind','Biomass','Geothermal','Backstop','power_trade','gas_trade'],dtype='float64')
    total_gen_df['y']=years
    total_cap_df=pd.DataFrame(np.zeros(shape=(56,14)),columns=['y','Coal','Oil','Gas','Hydro','Nuclear','Solar CSP','Solar PV',
                'Wind','Biomass','Geothermal','Backstop','power_trade','gas_trade'],dtype='float64')
    #total_cap_df['y'] = total_cap_df['y'].astype('float64')

    total_cap_df['y']=years
    #for loop for each country inside a powerpool/TEMBA starts here
    for cc in pp_def[tk]:
        cap_df = all_params['TotalCapacityAnnual']
        cap_df=cap_df[cap_df['t'].str[:2]==cc].copy()
        cap_df['t'] = cap_df['t'].str[2:10]
        cap_df['value'] = cap_df['value'].astype('float64')
        cap_df = cap_df[cap_df['t'].isin(t_include)].pivot_table(index='y', 
                                                   columns='t',
                                                   values='value', 
                                                   aggfunc='sum').reset_index().fillna(0)
        cap_df = cap_df.reindex(sorted(cap_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
        #***********************************************
        # Power capacity (Aggregated)
        cap_agg_df = pd.DataFrame(columns=agg_pow_col)
        cap_agg_df.insert(0,'y',cap_df['y'])
        cap_agg_df  = cap_agg_df.fillna(0.00)
        #
        for each in agg_pow_col:
            for tech_exists in agg_pow_col[each]:
                if tech_exists in cap_df.columns:
                    cap_agg_df[each] = cap_agg_df[each] + cap_df[tech_exists]
                    cap_agg_df[each] = cap_agg_df[each].round(3)
        #df_plot(cap_agg_df,'Gigawatts (GW)',cc+"-"+'Power Generation Capacity (Aggregate)')
        #total_cap_df=cap_agg_df+total_cap_df
        total_cap_df= cap_agg_df.set_index('y').add(total_cap_df.set_index('y'), fill_value=0).reset_index()
        #Power generation
        gen_df = all_params['ProductionByTechnologyAnnual'].copy()
        gen_df_export=gen_df[(gen_df['f'].str[2:6]=='EL01')&(gen_df['f'].str[0:2]!=cc)].copy()
        gen_df_export=gen_df_export[gen_df_export['t'].str[6:10]=='BP00'].copy()
        gen_df_export=gen_df_export[(gen_df_export['t'].str[0:2]==cc)|(gen_df_export['t'].str[4:6]==cc)]
        gen_df_export['value'] = gen_df_export['value'].astype(float)*-1
        gen_df=gen_df[(gen_df['f'].str[:2]==cc)].copy()
        gen_df=gen_df[(gen_df['f'].str[2:6]=='EL01')|(gen_df['f'].str[2:6]=='EL03')].copy()
        gen_df=gen_df[(gen_df['t'].str[2:10]!='EL00T00X')&(gen_df['t'].str[2:10]!='EL00TDTX')].copy()
        gen_df=pd.concat([gen_df,gen_df_export])
        gen_df['value'] = gen_df['value'].astype('float64')
        gen_df = gen_df.pivot_table(index='y', 
                                               columns='t',
                                               values='value', 
                                               aggfunc='sum').reset_index().fillna(0)
        for each in gen_df.columns:
            if len(each)!=1:
                if (each[2:4]=='EL') & (each[6:10]=='BP00'):
                    pass
                else:
                    gen_df.rename(columns={each:each[2:10]},inplace=True)
            else:
                pass
        gen_df = gen_df.reindex(sorted(gen_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
        #df_plot(gen_df,'Petajoules (PJ)',cc+"-"+'Power Generation (Detail)')
        #####
        # Power generation (Aggregated)
        gen_agg_df = pd.DataFrame(columns=agg_pow_col)
        gen_agg_df.insert(0,'y',gen_df['y'])
        gen_agg_df  = gen_agg_df.fillna(0.00)
        for each in agg_pow_col:
            for tech_exists in agg_pow_col[each]:
                if tech_exists in gen_df.columns:
                    gen_agg_df[each] = gen_agg_df[each] + gen_df[tech_exists]
                    gen_agg_df[each] = gen_agg_df[each].round(2)
        total_gen_df=gen_agg_df+total_gen_df
    total_gen_df['y']=years
    total_gen_df['y']=total_gen_df['y'].astype('float64')
    total_cap_df['y']=total_cap_df['y'].astype('float64')
    total_gen_df=total_gen_df.drop('gas_trade',axis=1)
    total_gen_df=total_gen_df[total_gen_df['y']<=2065]
    total_cap_df=total_cap_df[total_cap_df['y']<=2065]
    fig=total_gen_df.iplot(x='y',
                          kind='bar', 
                          barmode='relative',
                          xTitle='Year',
                          yTitle="Petajoules (PJ)",
                          color=[color_dict[x] for x in total_gen_df.columns if x != 'y'],
                          title=tk+"-"+"Power Generation (Aggregate)"+"-"+ scenario,
                          showlegend=True,
                          asFigure=True)
    fig.update_xaxes(range=[2015,2065]) 
    title=(tk+"-"+"Power Generation (Aggregate)"+"-"+ scenario)
    pio.write_image(fig, '{}.png'.format(title))
    fig.show()
    #total_cap_df['y']=years
    #total_cap_df=total_cap_df.drop('gas_trade',axis=1)
    df_plot(total_cap_df,'Gigawatts (GW)',tk +"-"+'Power Generation Capacity (Aggregate)')
    total_gen_df.to_csv(os.path.join(homedir,tk +"- Power Generation (Aggregate)"+"-"+scenario+".csv"))
    total_cap_df.to_csv(os.path.join(homedir,tk +"-capacity"+"-"+scenario+".csv"))

#%% [markdown]
# # In the follwoing block, the water consumption and withdrawal graphs for all the powerpools and TEMBA will be plotted and CSV files generated for each

#%%
for tk in pp_def.keys():
    # The following lines are used for creating dummy 
    #(empty) dataframes to print aggregated (powerpool/TEMBA) results as csv files
    total_watc_df=pd.DataFrame(np.zeros(shape=(56,19)),columns=['y','Coal','Oil','Gas','Hydro','Nuclear','Solar CSP','Solar PV',
            'Wind','Geothermal','Biomass','Coal Production','Crude Oil production','Crude oil Refinery',
            'Natural gas extraction','Uranium extraction','Transmission & Distribution','Backstop',
                                                            'Biofuel and Biomass production'],dtype='float64')
    total_watc_df['y']=years
    total_watw_df=pd.DataFrame(np.zeros(shape=(56,19)),columns=['y','Coal','Oil','Gas','Hydro','Nuclear','Solar CSP','Solar PV',
            'Wind','Geothermal','Biomass','Coal Production','Crude Oil production','Crude oil Refinery',
            'Natural gas extraction','Uranium extraction','Transmission & Distribution','Backstop',
                                                            'Biofuel and Biomass production'],dtype='float64')
    total_watw_df['y']=years
    ######
    for cc in pp_def[tk]:
        wat_w_df = all_params['UseByTechnologyAnnual']
        wat_w_df=wat_w_df[wat_w_df['f'].str[:6]==cc+'WAT1'].copy()

        wat_w_df['t'] = wat_w_df['t'].str[2:10]
        wat_w_df['value'] = wat_w_df['value'].astype('float64')
        wat_w_df = wat_w_df.pivot_table(index='y', 
                                      columns='t',
                                      values='value', 
                                      aggfunc='sum').reset_index().fillna(0)
        wat_w_df = wat_w_df.reindex(sorted(wat_w_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
        #wat_w_df['y'] = years
        #wat_w_df=wat_w_df[wat_w_df['y']>2018]
        #df_plot(wat_w_df,'Million cubic metres (Mm^3)',cc+"-"+'Water Withdrawal')
        ###
        #Water Withdrawal (Aggregated)
        watw_agg_df = pd.DataFrame(columns=agg_col)
        watw_agg_df.insert(0,'y',wat_w_df['y'])
        watw_agg_df  = watw_agg_df.fillna(0.00)
        for each in agg_col:
            for tech_exists in agg_col[each]:
                if tech_exists in wat_w_df.columns:
                    watw_agg_df[each] = watw_agg_df[each] + wat_w_df[tech_exists]
                    watw_agg_df[each] = watw_agg_df[each].round(2)
        total_watw_df= total_watw_df.set_index('y').add(watw_agg_df.set_index('y'), fill_value=0).reset_index()
        ##
        #water output detailed
        wat_o_df = all_params['ProductionByTechnologyAnnual']
        wat_o_df=wat_o_df[wat_o_df['f'].str[:6]==cc+'WAT2'].copy()
        wat_o_df['t'] = wat_o_df['t'].str[2:10].copy()
        wat_o_df['value'] = wat_o_df['value'].astype('float64')
        wat_o_df = wat_o_df.pivot_table(index='y', 
                                     columns='t',
                                     values='value', 
                                     aggfunc='sum').reset_index().fillna(0)
        wat_o_df = wat_o_df.reindex(sorted(wat_o_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
        #wat_o_df['y'] = years
        #wat_o_df=wat_o_df[wat_o_df['y']>2018]
        #df_plot(wat_o_df,'Million cubic metres (Mm^3)',cc+"-"+'Water output')
        ###
        #Water consumption missing row additions
        for wd in wat_w_df.columns:
            for wc in wat_o_df.columns:
                if wd in wat_o_df.columns:
                    pass
                else:
                    wat_o_df[wd]=0
        #####
        ####Water consumption (Detailed)
        wat_c_df=wat_w_df.set_index('y')-wat_o_df.set_index('y')
        wat_c_df=wat_c_df.fillna(0.00)
        wat_c_df.reset_index(inplace=True)
        #wat_c_df['y']=years
        #df_plot(wat_c_df,'Million cubic metres (Mm^3)',cc+"-"+'Water consumption')
        #Water consumption (Aggregate)
        watc_agg_df = pd.DataFrame(columns=agg_col)
        watc_agg_df.insert(0,'y',wat_c_df['y'])
        watc_agg_df  = watc_agg_df.fillna(0.00)
        for each in agg_col:
            for tech_exists in agg_col[each]:
                if tech_exists in wat_c_df.columns:
                    watc_agg_df[each] = watc_agg_df[each] + wat_c_df[tech_exists]
                    watc_agg_df[each] = watc_agg_df[each].round(2)
        total_watc_df= total_watc_df.set_index('y').add(watc_agg_df.set_index('y'), fill_value=0).reset_index()
    total_watw_df['y']=years
    total_watc_df['y']=years
    total_watc_df['y']=total_watc_df['y'].astype('float64')
    total_watw_df['y']=total_watw_df['y'].astype('float64')
    total_watw_df=total_watw_df[total_watw_df['y']<=2065]
    total_watc_df=total_watc_df[total_watc_df['y']<=2065]
    df_plot(total_watw_df,'Million cubic metres (Mm^3)',tk+"-"+'Water Withdrawal')
    df_plot(total_watc_df,'Million cubic metres (Mm^3)',tk+"-"+'Water Consumption')
    #df_plot(watw_agg_df,'Million cubic metres (Mm^3)',cc+'Water Withdrawal')
    #df_plot(watc_agg_df,'Million cubic metres (Mm^3)',cc+'Water consumption aggregated')
    total_watc_df.to_csv(os.path.join(homedir,tk +"-"+ scenario + "-wat consumption.csv"))
    total_watw_df.to_csv(os.path.join(homedir,tk +"-"+ scenario + "-wat withdrawal.csv"))


#%%
#This is for taking the pickle file and producing the csvs
# x=[]
# pkl_file = open("./TEMBA_Ref_12_08_modex.pickle", 'rb')
# x = pickle.load(pkl_file)
# df=pd.DataFrame()
# for each in x:
#     df=x[each]
#     df.to_csv(each +".csv")



#%%
#Consolidated Emissions
for tk in pp_def.keys():
    total_emis_df=pd.DataFrame(np.zeros(shape=(56,2)),columns=['y','CO2'],dtype='float64')
    total_emis_df['y'] = total_emis_df['y'].astype('float64')
    total_emis_df['y']=years
    for cc in pp_def[tk]:
        emis_df = all_params['AnnualEmissions']
        emis_df=emis_df[emis_df['e'].str[:5]==cc+'CO2'].copy()
        emis_df = df_filter_emission_tot(emis_df)
        total_emis_df= total_emis_df.set_index('y').add(emis_df.set_index('y'), fill_value=0).reset_index()
    total_emis_df['y']=years
    total_emis_df=total_emis_df[total_emis_df['y']<=2065]
    df_plot(total_emis_df,'Million Tonnes of CO2 (Mt)',tk+"-"+'Annual Emissions')
    #total_emis_df.to_csv(os.path.join(homedir,tk +"-"+ scenario +"-"+'Annual Emissions.csv'))


#%%
#Consolidated HFO and LFO use
for tk in pp_def.keys():
    total_lfo_df=pd.DataFrame(np.zeros(shape=(56,4)),columns=['y','Crude oil refinery 1','Crude oil refinery 2','Light Fuel Oil imports'],dtype='float64')
    total_lfo_df['y'] = total_lfo_df['y'].astype('float64')
    total_lfo_df['y']=years
    total_hfo_df=pd.DataFrame(np.zeros(shape=(56,4)),columns=['y','Crude oil refinery 1','Crude oil refinery 2','Heavy Fuel Oil imports'],dtype='float64')
    total_hfo_df['y'] = total_hfo_df['y'].astype('float64')
    total_hfo_df['y']=years
    for cc in pp_def[tk]:
        #Heavy Fuel Oil overview
        hfo_df = all_params['ProductionByTechnologyAnnual']
        hfo_df=hfo_df[hfo_df['f'].str[:6]==cc+'HFOI'].copy()
        hfo_df['t'] = hfo_df['t'].str[2:10]
        hfo_df['value'] = hfo_df['value'].astype('float64')
        hfo_df = hfo_df.pivot_table(index='y',columns='t',
                                  values='value', 
                                  aggfunc='sum').reset_index().fillna(0)
        hfo_df = hfo_df.reindex(sorted(hfo_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
        total_hfo_df= total_hfo_df.set_index('y').add(hfo_df.set_index('y'), fill_value=0).reset_index()
        #hfo_df['y'] = years
        #hfo_df=hfo_df[hfo_df['y']>2018]
        #Light Fuel Oil overview
        lfo_df = all_params['ProductionByTechnologyAnnual']
        lfo_df=lfo_df[lfo_df['f'].str[:6]==cc+'LFOI'].copy()
        lfo_df['t'] = lfo_df['t'].str[2:10]
        lfo_df['value'] = lfo_df['value'].astype('float64')
        lfo_df = lfo_df.pivot_table(index='y',columns='t',
                                  values='value', 
                                  aggfunc='sum').reset_index().fillna(0)
        lfo_df = lfo_df.reindex(sorted(lfo_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
        #df_plot(lfo_df,'Petajoules (PJ)',cc+"-"+'LFO production by technology')
        total_lfo_df= total_lfo_df.set_index('y').add(lfo_df.set_index('y'), fill_value=0).reset_index()
        #lfo_df['y'] = years
        #lfo_df=lfo_df[lfo_df['y']>2018]
    total_hfo_df['y']=years
    total_lfo_df['y']=years
    total_hfo_df=total_hfo_df[total_hfo_df['y']<=2065]
    total_lfo_df=total_lfo_df[total_lfo_df['y']<=2065]
    df_plot(total_hfo_df,'Petajoules (PJ)',tk+"-"+'HFO production by technology')
    df_plot(total_lfo_df,'Petajoules (PJ)',tk+"-"+'LFO production by technology')
    #total_hfo_df.to_csv(os.path.join(homedir,tk +"-"+ scenario +"-"+'HFO production by technology.csv'))
    #total_lfo_df.to_csv(os.path.join(homedir,tk +"-"+ scenario +"-"+'LFO production by technology.csv'))


#%%
#Cosnsolidated coal and bioamss usage
for tk in pp_def.keys():
    total_coal_df=pd.DataFrame(np.zeros(shape=(56,3)),columns=['y','Coal imports (inland transport, maritime freight)','Coal extraction (mining)'],dtype='float64')
    total_coal_df['y'] = total_coal_df['y'].astype('float64')
    total_coal_df['y']=years
    total_biom_df=pd.DataFrame(np.zeros(shape=(56,2)),columns=['y','Biomass extraction/production/refining'],dtype='float64')
    total_biom_df['y'] = total_biom_df['y'].astype('float64')
    total_biom_df['y']=years
    for cc in pp_def[tk]:
        #Coal overview
        coal_df = all_params['ProductionByTechnologyAnnual']
        coal_df=coal_df[coal_df['f'].str[:6]==cc+'COAL'].copy()
        coal_df['t'] = coal_df['t'].str[2:10]
        coal_df['value'] = coal_df['value'].astype('float64')
        coal_df = coal_df.pivot_table(index='y',columns='t',
                                  values='value', 
                                  aggfunc='sum').reset_index().fillna(0)
        coal_df = coal_df.reindex(sorted(coal_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
        if len(coal_df.columns)==1:
            coal_df=pd.DataFrame(np.zeros(shape=(56,3)),columns=['y','Coal imports (inland transport, maritime freight)','Coal extraction (mining)'],dtype='float64')
            coal_df['y']=years
        total_coal_df= total_coal_df.set_index('y').add(coal_df.set_index('y'), fill_value=0).reset_index()
        #total_coal_df=coal_df+total_coal_df
        #coal_df['y'] = years
        #coal_df=coal_df[coal_df['y']>2018]
        
        #Biomass overview
        biom_df = all_params['ProductionByTechnologyAnnual']
        biom_df=biom_df[biom_df['f'].str[:6]==cc+'BIOM'].copy()
        biom_df['t'] = biom_df['t'].str[2:10]
        biom_df['value'] = biom_df['value'].astype('float64')
        biom_df = biom_df.pivot_table(index='y',columns='t',
                                          values='value', 
                                          aggfunc='sum').reset_index().fillna(0)
        biom_df = biom_df.reindex(sorted(biom_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
        total_biom_df= total_biom_df.set_index('y').add(biom_df.set_index('y'), fill_value=0).reset_index()
        #biom_df['y'] = years
        #biom_df=biom_df[biom_df['y']>2018]
    total_coal_df['y']=years
    total_biom_df['y']=years
    total_coal_df=total_coal_df[total_coal_df['y']<=2065]
    total_biom_df=total_biom_df[total_biom_df['y']<=2065]
    df_plot(total_biom_df,'Petajoules (PJ)',tk+'-'+'Biomass production by technology')
    df_plot(total_coal_df,'Petajoules (PJ)',tk+'-'+'Coal production by technology')


for each in country_code['Country Name']:
    power_chart(each)
    water_chart(each)
    emissions_chart(each)
    gas_chart(each)
    crude_chart(each)
    coal_biomass_chart(each)
    hfo_lfo_chart(each)

# this block will create individual country folders and paste (all country specific csv and png files) 
#files from the home directory to the path mentioned below
import shutil
import os
resultpath=r'C:\Users\vsri\Box Sync\dESA\06 Projects\2018-12_JRC_TEMBA\03. Work\02. Modelling\Python script_Ioannis\Final_results_dissemination_Aug2019\2308_runs\reference\country'
source = homedir
files = os.listdir(source)
for each in country_code['Country code']:
    os.mkdir(resultpath+ '/'+ each)
    dest1 = r'C:\Users\vsri\Box Sync\dESA\06 Projects\2018-12_JRC_TEMBA\03. Work\02. Modelling\Python script_Ioannis\Final_results_dissemination_Aug2019\2308_runs\reference\country' + "/" + each
    for f in files:
        if (f.startswith(each)):
            shutil.move(f, dest1)
     

# this block will create individual Power pool folders and paste (all country specific csv and png files) 
#files from the home directory to the path mentioned below
power_p=['WAPP','EAPP','CAPP','NAPP','SAPP']
resultpath=r'C:\Users\vsri\Box Sync\dESA\06 Projects\2018-12_JRC_TEMBA\03. Work\02. Modelling\Python script_Ioannis\Final_results_dissemination_Aug2019\2308_runs\reference\power_pool'
source = homedir
files = os.listdir(source)
for en in power_p:
    os.mkdir(resultpath+ '/'+ en)
    dest2 = r'C:\Users\vsri\Box Sync\dESA\06 Projects\2018-12_JRC_TEMBA\03. Work\02. Modelling\Python script_Ioannis\Final_results_dissemination_Aug2019\2308_runs\reference\power_pool' + "/" + en
    for f in files:
        if (f.startswith(en)):
            shutil.move(f, dest2)
