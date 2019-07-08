#!/usr/bin/env python
# coding: utf-8

# In[1]:


import xlrd #Extract data from Excel spreadsheets (.xls and .xlsx)
import csv #Import the csv file that I want as an output, need to convert the xls format to csv format
import os #To create the csv outputs (per sheet) in a folder called CSV files


# In[4]:


def main():
  filePath = input("Please enter the full path of the excel file: \n");   #I read the xlsx file
  csv_from_excel(filePath);

def csv_from_excel(filePath): 
  workBook = xlrd.open_workbook(filePath + '\\TEMBA_06_07_2oC.xlsx'); #I read the specific xlsx file
  sheetNames = workBook.sheet_names(); #I read all the sheets in the xlsx file
  modifiedSheetNames = modifyNames(sheetNames); #I modify the names of the sheets since some do not match with the actual ones
  
  for i in range(len(sheetNames)): #14-27 line: I create all the csv files in a new folder called CSVFiles
    sh = workBook.sheet_by_name(sheetNames[i]) #all the sheet names
    if not os.path.exists("CSVFiles"): 
      os.makedirs("CSVFiles"); ##creates the csv folder
    your_csv_file = open('CSVfiles/' + modifiedSheetNames[i] + '.csv', 'w', newline='') #I open the sheet name in the xlsx file and I write it in csv format
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)
    
    for rownum in range(sh.nrows): #reads each row in the csv file
      if (all(isinstance(n, float) for n in sh.row_values(rownum))): 
        wr.writerow(list(map(int, sh.row_values(rownum)))); #function  to convert all float numbers to integers....need to check it!!
      else:
        wr.writerow(sh.row_values(rownum));

    your_csv_file.close()  #The csv files created

  fileOutput = parseCSVFilesAndConvert(modifiedSheetNames); #I create a txt file - string that contains the csv files
  if not os.path.exists("output"): #I create the output folder
      os.makedirs("output"); 
  text_file = open("output/Output.txt", "w");
  text_file.write(fileOutput); 
  text_file.close();
  print("The file successfully created!");
  workBook.release_resources(); #release the workbook-resources
  del workBook;
  

def parseCSVFilesAndConvert(sheetNames): #for loop pou trexei ola ta sheet name kai paragei to format se csv
  result = '';
  for i in range(len(sheetNames)):
    if (sheetNames[i] in ['STORAGE', 'EMISSION', 'MODE_OF_OPERATION', 'REGION', 'FUEL', 'TIMESLICE', 'TECHNOLOGY', 'YEAR']): #8 #all the parameters thad do not have variables
      result += 'set ' + sheetNames[i] + ' := ';
      with open('CSVFiles/' + sheetNames[i] + '.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
          result += " ".join(row) + " ";
    elif (sheetNames[i] in ['AccumulatedAnnualDemand', 'CapitalCost', 'FixedCost', 'ResidualCapacity', 'SpecifiedAnnualDemand', 'TotalAnnualMinCapacity', 'TotalAnnualMinCapacityInvestment', 'TotalTechnologyAnnualActivityLowerLimit']): #24 #all the parameters that have one variable
      result += 'param ' + sheetNames[i] + ' default 0 := ';
      result += '\n[REGION, *, *]:\n';
      with open('CSVFiles/' + sheetNames[i] + '.csv', newline='') as csvfile:
        reader = csv.reader(csvfile);
        newRow = next(reader);
        newRow.pop(0); #removes the first element of the row
        result += " ".join(newRow) + " ";
        result += ':=\n';
        for row in reader:
          result += " ".join(row) + " ";
          result += '\n';
    elif (sheetNames[i] in ['TotalAnnualMaxCapacityInvestment']): #24 #all the parameters that have one variable
      result += 'param ' + sheetNames[i] + ' default 99999 := ';
      result += '\n[REGION, *, *]:\n';
      with open('CSVFiles/' + sheetNames[i] + '.csv', newline='') as csvfile:
        reader = csv.reader(csvfile);
        newRow = next(reader);
        newRow.pop(0); #removes the first element of the row
        result += " ".join(newRow) + " ";
        result += ':=\n';
        for row in reader:
          result += " ".join(row) + " ";
          result += '\n';    
    elif (sheetNames[i] in ['AvailabilityFactor']):
      result += 'param ' + sheetNames[i] + ' default 1 := ';
      result += '\n[REGION, *, *]:\n';
      with open('CSVFiles/' + sheetNames[i] + '.csv', newline='') as csvfile:
        reader = csv.reader(csvfile);
        newRow = next(reader);
        newRow.pop(0); #removes the first element of the row
        result += " ".join(newRow) + " ";
        result += ':=\n';
        for row in reader:
          result += " ".join(row) + " ";
          result += '\n';   
    elif (sheetNames[i] in ['TotalAnnualMaxCapacity', 'TotalTechnologyAnnualActivityUpperLimit']):
      result += 'param ' + sheetNames[i] + ' default 9999999 := ';
      result += '\n[REGION, *, *]:\n';
      with open('CSVFiles/' + sheetNames[i] + '.csv', newline='') as csvfile:
        reader = csv.reader(csvfile);
        newRow = next(reader);
        newRow.pop(0); #removes the first element of the row
        result += " ".join(newRow) + " ";
        result += ':=\n';
        for row in reader:
          result += " ".join(row) + " ";
          result += '\n';   
    elif (sheetNames[i] in ['AnnualEmissionLimit']):
      result += 'param ' + sheetNames[i] + ' default 99999 := ';
      result += '\n[REGION, *, *]:\n';
      with open('CSVFiles/' + sheetNames[i] + '.csv', newline='') as csvfile:
        reader = csv.reader(csvfile);
        newRow = next(reader);
        newRow.pop(0); #removes the first element of the row
        result += " ".join(newRow) + " ";
        result += ':=\n';
        for row in reader:
          result += " ".join(row) + " ";
          result += '\n';      
    elif (sheetNames[i] in ['YearSplit']):
      result += 'param ' + sheetNames[i] + ' default 0 :\n';
      with open('CSVFiles/' + sheetNames[i] + '.csv', newline='') as csvfile:
        reader = csv.reader(csvfile);
        newRow = next(reader);
        newRow.pop(0); #removes the first element of the row
        result += " ".join(newRow) + " ";
        result += ':=\n';
        for row in reader:
          result += " ".join(row) + " ";
          result += '\n';      
    elif (sheetNames[i] in ['CapacityOfOneTechnologyUnit', 'EmissionsPenalty', 'REMinProductionTarget', 'RETagFuel', 'RETagTechnology', 'ReserveMargin', 'ReserveMarginTagFuel', 'ReserveMarginTagTechnology', 'TradeRoute']):         
      result += 'param ' + sheetNames[i] + ' default 0 := \n';
    elif (sheetNames[i] in ['SpecifiedDemandProfile']): #3 #all the parameters that have 2 variables
      result += 'param ' + sheetNames[i] + ' default 0 := \n';
      with open('CSVFiles/' + sheetNames[i] + '.csv', newline='') as csvfile:
        reader = csv.reader(csvfile);
        newRow = next(reader);
        newRow.pop(0); 
        newRow.pop(0);
        year = newRow.copy();
        for row in reader:
          result += '[REGION, ' + row.pop(0) + ', *, *]:';
          result += '\n';
          result += " ".join(year) + " ";
          result += ':=\n';
          result += " ".join(row) + " ";
          result += '\n';
    elif (sheetNames[i] in ['VariableCost']): #3 #all the parameters that have 2 variables
      result += 'param ' + sheetNames[i] + ' default 9999999 := \n';
      with open('CSVFiles/' + sheetNames[i] + '.csv', newline='') as csvfile:
        reader = csv.reader(csvfile);
        newRow = next(reader);
        newRow.pop(0); 
        newRow.pop(0);
        year = newRow.copy();
        for row in reader:
          result += '[REGION, ' + row.pop(0) + ', *, *]:';
          result += '\n';
          result += " ".join(year) + " ";
          result += ':=\n';
          result += " ".join(row) + " ";
          result += '\n';    
    elif (sheetNames[i] in ['CapacityFactor']): #3 #all the parameters that have 2 variables
      result += 'param ' + sheetNames[i] + ' default 1 := \n';
      with open('CSVFiles/' + sheetNames[i] + '.csv', newline='') as csvfile:
        reader = csv.reader(csvfile);
        newRow = next(reader);
        newRow.pop(0); 
        newRow.pop(0);
        year = newRow.copy();
        for row in reader:
          result += '[REGION, ' + row.pop(0) + ', *, *]:';
          result += '\n';
          result += " ".join(year) + " ";
          result += ':=\n';
          result += " ".join(row) + " ";
          result += '\n';
    elif (sheetNames[i] in ['EmissionActivityRatio', 'InputActivityRatio', 'OutputActivityRatio']): #3 #all the parameters that have 3 variables
      result += 'param ' + sheetNames[i] + ' default 0 := \n';
      with open('CSVFiles/' + sheetNames[i] + '.csv', newline='') as csvfile:
        reader = csv.reader(csvfile);
        newRow = next(reader);
        newRow.pop(0);
        newRow.pop(0);
        newRow.pop(0);
        year = newRow.copy();
        for row in reader:
          result += '[REGION, ' + row.pop(0) + ', ' + row.pop(0) + ', *, *]:';
          result += '\n';
          result += " ".join(year) + " ";
          result += ':=\n';
          result += " ".join(row) + " ";
          result += '\n';
    elif (sheetNames[i] in ['TotalTechnologyModelPeriodActivityUpperLimit']): #8 #all the parameters that do not have variables
      result += 'param ' + sheetNames[i] + ' default 9999999 : \n';
      with open('CSVFiles/' + sheetNames[i] + '.csv', newline='') as csvfile:
        reader = csv.reader(csvfile);
        newRow = next(reader);
        firstColumn = [];
        secondColumn = [];
        secondColumn.append('REGION');
        for row in reader:
          firstColumn.append(row[0]);
          secondColumn.append(row[1]);
        result += " ".join(firstColumn) + ' ';
        result += ':=\n';
        result += " ".join(secondColumn) + ' ';
        result += '\n';
    elif (sheetNames[i] in ['CapacityToActivityUnit']):
      result += 'param ' + sheetNames[i] + ' default 1 : \n';
      with open('CSVFiles/' + sheetNames[i] + '.csv', newline='') as csvfile:
        reader = csv.reader(csvfile);
        newRow = next(reader);
        firstColumn = [];
        secondColumn = [];
        secondColumn.append('REGION');
        for row in reader:
          firstColumn.append(row[0]);
          secondColumn.append(row[1]);
        result += " ".join(firstColumn) + ' ';
        result += ':=\n';
        result += " ".join(secondColumn) + ' ';
        result += '\n';    
    elif (sheetNames[i] in ['TotalTechnologyAnnualActivityLowerLimit']): #8 #all the parameters that do not have variables
      result += 'param ' + sheetNames[i] + ' default 0 := \n';
      with open('CSVFiles/' + sheetNames[i] + '.csv', newline='') as csvfile:
        reader = csv.reader(csvfile);
        newRow = next(reader);
        firstColumn = [];
        secondColumn = [];
        secondColumn.append('REGION');
        for row in reader:
          firstColumn.append(row[0]);
          secondColumn.append(row[1]);
        result += " ".join(firstColumn) + ' ';
        result += ':=\n';
        result += " ".join(secondColumn) + ' ';
        result += '\n';       
    elif (sheetNames[i] in ['ModelPeriodEmissionLimit']): #8 #all the parameters that do not have variables
      result += 'param ' + sheetNames[i] + ' default 999999 := \n';
    elif (sheetNames[i] in ['ModelPeriodExogenousEmission', 'AnnualExogenousEmission', 'OperationalLifeStorage']): #8 #all the parameters that do not have variables
      result += 'param ' + sheetNames[i] + ' default 0 := \n';    
    elif (sheetNames[i] in []): #8 #all the parameters that do not have variables
      result += 'param ' + sheetNames[i] + ' default 0 := \n';     
    elif (sheetNames[i] in ['TotalTechnologyModelPeriodActivityLowerLimit']): #8 #all the parameters that do not have variables
      result += 'param ' + sheetNames[i] + ' default 0 := \n';
    elif (sheetNames[i] in ['DepreciationMethod']): #8 #all the parameters that do not have variables
      result += 'param ' + sheetNames[i] + ' default 1 := \n';
    elif (sheetNames[i] in ['OperationalLife']): #8 #all the parameters that do not have variables
      result += 'param ' + sheetNames[i] + ' default 1 : \n';   
      with open('CSVFiles/' + sheetNames[i] + '.csv', newline='') as csvfile:
        reader = csv.reader(csvfile);
        newRow = next(reader);
        firstColumn = [];
        secondColumn = [];
        secondColumn.append('REGION');
        for row in reader:
          firstColumn.append(row[0]);
          secondColumn.append(row[1]);
        result += " ".join(firstColumn) + ' ';
        result += ':=\n';
        result += " ".join(secondColumn) + ' ';
        result += '\n';   
    elif (sheetNames[i] in ['DiscountRate']): #default value
      with open('CSVFiles/' + sheetNames[i] + '.csv', newline='') as csvfile:
        reader = csv.reader(csvfile);
        for row in reader:
          result += 'param ' + sheetNames[i] + ' default 0.1 := \n';
    result += ';\n';
  return result;

def modifyNames(sheetNames): #I change the name of the sheets in the xlsx file to match with the csv actual ones
  modifiedNames = sheetNames.copy();
  for i in range(len(modifiedNames)):
    if (modifiedNames[i] == "TotalAnnualMaxCapacityInvestmen"):
      modifiedNames[i] = "TotalAnnualMaxCapacityInvestment"
    elif (modifiedNames[i] == "TotalAnnualMinCapacityInvestmen"):
      modifiedNames[i] = "TotalAnnualMinCapacityInvestment";
    elif (modifiedNames[i] == "TotalTechnologyAnnualActivityLo"):
      modifiedNames[i] = "TotalTechnologyAnnualActivityLowerLimit"
    elif (modifiedNames[i] == "TotalTechnologyAnnualActivityUp"):
      modifiedNames[i] = "TotalTechnologyAnnualActivityUpperLimit";
    elif (modifiedNames[i] == "TotalTechnologyModelPeriodActLo"):
      modifiedNames[i] = "TotalTechnologyModelPeriodActivityLowerLimit";
    elif (modifiedNames[i] == "TotalTechnologyModelPeriodActUp"):
      modifiedNames[i] = "TotalTechnologyModelPeriodActivityUpperLimit";
  return modifiedNames;

main();


# In[3]:


with open("C:/Users/pappis/Box Sync/dESA/06 Projects/2018-12_JRC_TEMBA/03. Work/02. Modelling/Python script_Ioannis/output/output.txt", "a") as myfile:
    myfile.write("end;\n")


# In[ ]:




