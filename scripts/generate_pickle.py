"""Generate a pickle file from TEMBA solution

Notes
-----
Could use existing CSVFiles melted into narrow dataframes::

    >>> df = pd.read_csv('CSVFiles/EmissionActivityRatio.csv')
    >>> df.melt(id_vars=['TECHNOLOGY','EMISSION','MODEOFOPERATION'],
                var_name='YEAR',
                value_name="EmissionActivityRatio")
"""
import sys
import pandas as pd


def main(data_file : str, pickle_file : str):
    """

    Arguments
    ---------
    data_file : str
        Path to the solution file
    pickle_file : str
        Path to which to write the pickle file
    """

    df = pd.read_csv(data_file, sep='$', header=None, skiprows=2)
    df.columns = ['temp']
    df[['parameter', 'id', 'value']] = df['temp'].str.split(r'\)|\(', expand=True)
    df = df.drop('temp', axis=1)

    params = df.parameter.unique()
    all_params = {}
    cols = {'NewCapacity': ['r','t','y'],
            'AccumulatedNewCapacity':['r','t','y'], 
            'TotalCapacityAnnual':['r','t','y'],
            'CapitalInvestment':['r','t','y'],
            'AnnualVariableOperatingCost':['r','t','y'],
            'AnnualFixedOperatingCost':['r','t','y'],
            'SalvageValue':['r','t','y'],
            'DiscountedSalvageValue':['r','t','y'],
            'TotalTechnologyAnnualActivity':['r','t','y'],
            'RateOfActivity':['r','l','t','m','y'],
            'RateOfTotalActivity':['r','t','l','y'],
            'Demand':['r','l','f','y'],
            'TotalAnnualTechnologyActivityByMode':['r','t','m','y'],
            'TotalTechnologyModelPeriodActivity':['r','t'],
            'ProductionByTechnologyAnnual':['r','t','f','y'],
            'AnnualTechnologyEmissionByMode':['r','t','e','m','y'],
            'AnnualTechnologyEmission':['r','t','e','y'],
            'AnnualEmissions':['r','e','y'],
            'UseByTechnologyAnnual':['r','t','f','y']
            }

    for each in params:
        df_p = df[df.parameter == each].copy()
        df_p[cols[each]] = df_p['id'].str.split(',', expand=True)
        cols[each].append('value')
        df_p = df_p[cols[each]] # Reorder dataframe to include 'value' as last column
        all_params[each] = pd.DataFrame(df_p) # Create a dataframe for each parameter
        df_p = df_p.rename(columns={'value': each})
        df_p.to_csv(str(each) + '.csv', index=None) # Print data for each paramter to a CSV file
        
    lines = []

    parsing = False

    data_all = []
    data_out = []
    data_inp = []
    data_emission = []

    output_table = []
    input_table= []

    with open(data_file, 'r') as f:
        for line in f:
            if line.startswith('set YEAR'):
                start_year = line.split(' ')[3]
            elif line.startswith('set COMMODITY'): # Extracts list of COMMODITIES from data file. Some models use FUEL instead. 
                fuel_list = line.split(' ')[3:-1]
            elif line.startswith('set FUEL'): # Extracts list of FUELS from data file. Some models use COMMODITIES instead. 
                fuel_list = line.split(' ')[3:-1]
            elif line.startswith('set TECHNOLOGY'):
                tech_list = line.split(' ')[3:-1]
            elif line.startswith('set STORAGE'):
                storage_list = line.split(' ')[3:-1]
            elif line.startswith('set EMISSION'):
                emission_list = line.split(' ')[3:-1]
            elif line.startswith('set MODE_OF_OPERATION'):
                mode_list = line.split(' ')[3:-1]

    emission_table = []
    # Emission activity ratios-reading them from the data file
    with open(data_file, 'r') as f:
        for line in f:
            if line.startswith(";"):
                parsing = False   
            if parsing:
                if line.startswith('['):
                    emission = line.split(', ')[2]
                    tech = line.split(', ')[1]
                elif line.startswith(start_year):
                    years = line.rstrip().split(' ')[0:]
                    years = [i.strip(' :=') for i in years]
                elif not line.startswith(start_year):
                    values = line.rstrip().split(' ')[1:]
                    mode = line.split(' ')[0]
                    data_emission.append(tuple([emission,tech,mode]))
                    data_all.append(tuple([tech,mode]))
                    for i in range(0,len(years)):
                        emission_table.append(tuple([tech,emission,mode,years[i],values[i]]))
            if line.startswith('param EmissionActivityRatio'):
                parsing = True
                
                
    # input activity ratios-reading them from the data file
    with open(data_file, 'r') as f:
        for line in f:
            if line.startswith(";"):
                parsing = False
            if parsing:
                if line.startswith('['):
                    fuel = line.split(', ')[2]
                    tech = line.split(', ')[1]
                elif line.startswith(start_year):
                    years = line.rstrip().split(' ')[0:]
                    years = [i.strip(' :=') for i in years]
                elif not line.startswith(start_year):
                    values = line.rstrip().split(' ')[1:]
                    mode = line.split(' ')[0]
                    data_inp.append(tuple([fuel,tech,mode]))
                    data_all.append(tuple([tech,mode]))
                    for i in range(0,len(years)):
                        input_table.append(tuple([tech,fuel,mode,years[i],values[i]]))
            if line.startswith('param InputActivityRatio'):
                parsing = True            
                
                
    # Output activity ratios-reading them from the data file
    with open(data_file, 'r') as f:
        for line in f:
            if line.startswith(";"):
                parsing = False   
            if parsing:
                if line.startswith('['):
                    fuel = line.split(', ')[2]
                    tech = line.split(', ')[1]
                elif line.startswith(start_year):
                    years = line.rstrip().split(' ')[0:]
                    years = [i.strip(' :=') for i in years]
                elif not line.startswith(start_year):
                    values = line.rstrip().split(' ')[1:]
                    mode = line.split(' ')[0]
                    data_out.append(tuple([fuel,tech,mode]))
                    data_all.append(tuple([tech,mode]))
                    for i in range(0,len(years)):
                        output_table.append(tuple([tech,fuel,mode,years[i],values[i]]))
            if line.startswith('param OutputActivityRatio'):
                parsing = True


    year_split = []
    parsing = False

    with open(data_file, 'r') as f:
        for line in f:
            if line.startswith(";"):
                parsing = False   
            if parsing:
                if line.startswith(start_year):
                    years = line.rstrip().split(' ')[0:]
                    years = [i.strip(':=') for i in years]
                elif not line.startswith(start_year):
                    time_slice = line.rstrip().split(' ')[0]
                    values = line.rstrip().split(' ')[1:]
                    for i in range(0,len(years)):
                        year_split.append(tuple([time_slice,years[i],values[i]]))
            if line.startswith('param YearSplit'):
                parsing = True

    df_output = pd.DataFrame(output_table, columns=['t','f','m','y','OutputActivityRatio'])
    df_input = pd.DataFrame(input_table, columns=['t','f','m','y','InputActivityRatio'])
    df_emission = pd.DataFrame(emission_table, columns=['t','e','m','y','EmissionActivityRatio'])
    df_yearsplit = pd.DataFrame(year_split, columns=['l','y','YearSplit'])
    df_activity = all_params['RateOfActivity'].rename(columns={'value':'RateOfActivity'})

    # To write production by technology annual
    df_out_ys = pd.merge(df_output, df_yearsplit, on='y')
    df_out_ys['t']=df_out_ys['t'].astype(str)
    df_out_ys['m']=df_out_ys['m'].astype(float)
    df_out_ys['y']=df_out_ys['y'].astype(float)
    df_out_ys['l']=df_out_ys['l'].astype(str)
    ###########33
    df_activity['t']=df_activity['t'].astype(str)
    df_activity['m']=df_activity['m'].astype(float)
    df_activity['y']=df_activity['y'].astype(float)
    df_activity['l']=df_activity['l'].astype(str)
    #########
    df_out_ys['OutputActivityRatio'] = df_out_ys['OutputActivityRatio'].astype(float)
    df_out_ys['YearSplit'] = df_out_ys['YearSplit'].astype(float)
    df_activity['RateOfActivity']=df_activity['RateOfActivity'].astype(float)
    df_out_ys.set_index(['t','m','y','l'],inplace=True)
    df_prod=df_activity.join(df_out_ys, on=['t','m','y','l'])


    df_prod['ProductionByTechnologyAnnual'] = df_prod['OutputActivityRatio']*df_prod['YearSplit']*df_prod['RateOfActivity']
    df_prod = df_prod.drop(['OutputActivityRatio','YearSplit','RateOfActivity'], axis=1)

    df_prod = df_prod.groupby(['r','t','f','y'])['ProductionByTechnologyAnnual'].sum().reset_index()
    df_prod['ProductionByTechnologyAnnual'] = df_prod['ProductionByTechnologyAnnual'].astype(float).round(4)

    df_prod.to_csv(r'./ProductionByTechnologyAnnual.csv', index=None)
    all_params['ProductionByTechnologyAnnual'] = df_prod.rename(columns={'ProductionByTechnologyAnnual':'value'})

    # To write Use by technology annual
    df_in_ys = pd.merge(df_input, df_yearsplit, on='y')
    df_in_ys['t']=df_in_ys['t'].astype(str)
    df_in_ys['m']=df_in_ys['m'].astype(float)
    df_in_ys['y']=df_in_ys['y'].astype(float)
    df_in_ys['l']=df_in_ys['l'].astype(str)
    ###########
    #########
    df_in_ys['InputActivityRatio'] = df_in_ys['InputActivityRatio'].astype(float)
    df_in_ys['YearSplit'] = df_in_ys['YearSplit'].astype(float)
    df_activity['RateOfActivity']=df_activity['RateOfActivity'].astype(float)
    df_in_ys.set_index(['t','m','y','l'],inplace=True)
    df_use=df_activity.join(df_in_ys, on=['t','m','y','l'])


    df_use['UseByTechnologyAnnual'] = df_use['InputActivityRatio']*df_use['YearSplit']*df_use['RateOfActivity']
    df_use = df_use.drop(['InputActivityRatio','YearSplit','RateOfActivity'], axis=1)

    df_use = df_use.groupby(['r','t','f','y'])['UseByTechnologyAnnual'].sum().reset_index()
    df_use['UseByTechnologyAnnual'] = df_use['UseByTechnologyAnnual'].astype(float).round(4)

    df_use.to_csv(r'./UseByTechnologyAnnual.csv', index=None)
    all_params['UseByTechnologyAnnual'] = df_use.rename(columns={'UseByTechnologyAnnual':'value'})

    # To write AnnualTechnologyEmissions
    df_ems_ys = pd.merge(df_emission, df_yearsplit, on='y')
    df_ems_ys['t']=df_ems_ys['t'].astype(str)
    df_ems_ys['m']=df_ems_ys['m'].astype(float)
    df_ems_ys['y']=df_ems_ys['y'].astype(float)
    df_ems_ys['l']=df_ems_ys['l'].astype(str)
    ###########33
    #########
    df_ems_ys['EmissionActivityRatio'] = df_ems_ys['EmissionActivityRatio'].astype(float)
    df_ems_ys['YearSplit'] = df_ems_ys['YearSplit'].astype(float)
    df_activity['RateOfActivity'] = df_activity['RateOfActivity'].astype(float)
    df_ems_ys.set_index(['t','m','y','l'],inplace=True)
    df_antechem=df_activity.join(df_ems_ys, on=['t','m','y','l'])
    #df_antechem is for Annual technology emissions
    #df_anemm is for annual emissions by emisiosn type
    df_antechem['AnnualTechnologyEmission'] = df_antechem['EmissionActivityRatio']*df_antechem['YearSplit']*df_antechem['RateOfActivity']
    df_antechem = df_antechem.drop(['EmissionActivityRatio','YearSplit','RateOfActivity'], axis=1)
    df_antechem = df_antechem.groupby(['r','t','e','y'])['AnnualTechnologyEmission'].sum().reset_index()
    ########3
    df_anemm=df_antechem.groupby(['r','e','y'])['AnnualTechnologyEmission'].sum().reset_index()
    df_anemm.rename(columns={'AnnualTechnologyEmission':'AnnualEmissions'}, inplace=True)
    df_anemm

    #Annual technology Emission
    df_antechem['AnnualTechnologyEmission'] = df_antechem['AnnualTechnologyEmission'].astype(float).round(4)
    df_antechem.to_csv(r'./AnnualTechnologyEmission.csv', index=None)
    all_params['AnnualTechnologyEmission'] = df_antechem.rename(columns={'AnnualTechnologyEmission':'value'})
    #Annual emissions
    df_anemm['AnnualEmissions'] = df_anemm['AnnualEmissions'].astype(float).round(4)
    df_anemm.to_csv(r'./AnnualEmissions.csv', index=None)
    all_params['AnnualEmissions'] = df_anemm.rename(columns={'AnnualEmissions':'value'})

    # Removing the rate of activity fromt he results to make the pickle file lighter. 
    del all_params['RateOfActivity']

    with open(pickle_file, 'wb') as handle:
        pickle.dump(all_params, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':

    if len(sys.argv) != 3:
        msg = "Usage: python {} <CBC or Gurobi solution file> <picklefile>"
        print(msg.format(sys.argv[0]))
        sys.exit(1)
    else:
        data_file = sys.argv[1]
        pickle_file = sys.argv[2]
        try:
            main(data_file, pickle_file)
            sys.exit(0)
        except:
            sys.exit(1)

    