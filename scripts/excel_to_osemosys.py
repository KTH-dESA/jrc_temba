#!/usr/bin/env python
# coding: utf-8
"""
Extract data from Excel spreadsheets (.xls and .xlsx)
Import the csv file that I want as an output, need to convert the xls format to csv format
To create the csv outputs (per sheet) in a folder called CSV files
"""
import xlrd
import csv
import os
import sys


def main(filepath, input_workbook, output_file):
    """Read the xlsx file
    """
    csv_from_excel(filepath, input_workbook, output_file)


def csv_from_excel(filepath, input_workbook, output_file):
    """Read the workbook and
    """
    workBook = xlrd.open_workbook(os.path.join(filepath, input_workbook))
    sheetNames = workBook.sheet_names()  # I read all the sheets in the xlsx file
    # I modify the names of the sheets since some do not match with the actual ones
    modifiedSheetNames = modifyNames(sheetNames)

    # Create all the csv files in a new folder called CSVFiles
    for i in range(len(sheetNames)):
        sh = workBook.sheet_by_name(sheetNames[i])  # all the sheet names
        if not os.path.exists("CSVFiles"):
            os.makedirs("CSVFiles")  # creates the csv folder

        # Open the sheet name in the xlsx file and write it in csv format
        with open('CSVfiles/' + modifiedSheetNames[i] + '.csv', 'w', newline='') as your_csv_file:
            wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

            for rownum in range(sh.nrows):  # reads each row in the csv file
                if (all(isinstance(n, float) for n in sh.row_values(rownum))):
                    # function to convert all float numbers to integers....need to check it!!
                    wr.writerow(list(map(int, sh.row_values(rownum))))
                else:
                    wr.writerow(sh.row_values(rownum))

    # I create a txt file - string that contains the csv files
    fileOutput = parseCSVFilesAndConvert(modifiedSheetNames)
    with open(output_file, "w") as text_file:
        text_file.write(fileOutput)
        text_file.write("end;\n")

    workBook.release_resources()  # release the workbook-resources
    del workBook


# for loop pou trexei ola ta sheet name kai paragei to format se csv
def parseCSVFilesAndConvert(sheetNames):
    result = ''
    for i in range(len(sheetNames)):
        # 8 #all the     parameters thad do not have variables
        if (sheetNames[i] in ['STORAGE', 'EMISSION', 'MODE_OF_OPERATION',
                              'REGION', 'FUEL', 'TIMESLICE', 'TECHNOLOGY',
                              'YEAR']):
            result += 'set ' + sheetNames[i] + ' := '
            with open('CSVFiles/' + sheetNames[i] + '.csv', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    result += " ".join(row) + " "
                result += ";\n"
        # 24 #all the parameters     that have one variable
        elif (sheetNames[i] in ['AccumulatedAnnualDemand', 'CapitalCost',
                                'FixedCost', 'ResidualCapacity',
                                'SpecifiedAnnualDemand',
                                'TotalAnnualMinCapacity',
                                'TotalAnnualMinCapacityInvestment',
                                'TotalTechnologyAnnualActivityLowerLimit']):
            result += 'param ' + sheetNames[i] + ' default 0 := '
            result += '\n[REGION, *, *]:\n'
            result += insert_table(sheetNames[i])
        # 24 #all the parameters that have one variable
        elif (sheetNames[i] in ['TotalAnnualMaxCapacityInvestment']):
            result += 'param ' + sheetNames[i] + ' default 99999 := '
            result += '\n[REGION, *, *]:\n'
            result += insert_table(sheetNames[i])
        elif (sheetNames[i] in ['AvailabilityFactor']):
            result += 'param ' + sheetNames[i] + ' default 1 := '
            result += '\n[REGION, *, *]:\n'
            result += insert_table(sheetNames[i])
        elif (sheetNames[i] in ['TotalAnnualMaxCapacity',
                                'TotalTechnologyAnnualActivityUpperLimit']):
            result += 'param ' + sheetNames[i] + ' default 9999999 := '
            result += '\n[REGION, *, *]:\n'
            result += insert_table(sheetNames[i])
        elif (sheetNames[i] in ['AnnualEmissionLimit']):
            result += 'param ' + sheetNames[i] + ' default 99999 := '
            result += '\n[REGION, *, *]:\n'
            result += insert_table(sheetNames[i])
        elif (sheetNames[i] in ['YearSplit']):
            result += 'param ' + sheetNames[i] + ' default 0 :\n'
            result += insert_table(sheetNames[i])
        elif (sheetNames[i] in ['CapacityOfOneTechnologyUnit',
                                'EmissionsPenalty', 'REMinProductionTarget',
                                'RETagFuel', 'RETagTechnology',
                                'ReserveMargin', 'ReserveMarginTagFuel',
                                'ReserveMarginTagTechnology', 'TradeRoute']):
            result += 'param ' + sheetNames[i] + ' default 0 := ;\n'
        # 3 #all the parameters that have 2 variables
        elif (sheetNames[i] in ['SpecifiedDemandProfile']):
            result += 'param ' + sheetNames[i] + ' default 0 := \n'
            result += insert_two_variables(sheetNames, i)
        # 3 #all the parameters that have 2 variables
        elif (sheetNames[i] in ['VariableCost']):
            result += 'param ' + sheetNames[i] + ' default 9999999 := \n'
            result += insert_two_variables(sheetNames, i)
        # 3 #all the parameters that have 2 variables
        elif (sheetNames[i] in ['CapacityFactor']):
            result += 'param ' + sheetNames[i] + ' default 1 := \n'
            result += insert_two_variables(sheetNames, i)
        # 3 #all the parameters that have 3     variables
        elif (sheetNames[i] in ['EmissionActivityRatio', 'InputActivityRatio',
                                'OutputActivityRatio']):
            result += 'param ' + sheetNames[i] + ' default 0 := \n'
            with open('CSVFiles/' + sheetNames[i] + '.csv', newline='') as csvfile:
                reader = csv.reader(csvfile)
                newRow = next(reader)
                newRow.pop(0)
                newRow.pop(0)
                newRow.pop(0)
                year = newRow.copy()
                for row in reader:
                    result += '[REGION, ' + \
                        row.pop(0) + ', ' + row.pop(0) + ', *, *]:'
                    result += '\n'
                    result += " ".join(year) + " "
                    result += ':=\n'
                    result += " ".join(row) + " "
                    result += '\n'
                result += ';\n'
        # 8 #all the parameters that do not have variables
        elif (sheetNames[i] in ['TotalTechnologyModelPeriodActivityUpperLimit']):
            result += 'param ' + sheetNames[i] + ' default 9999999 : \n'
            result += insert_no_variables(sheetNames, i)
        elif (sheetNames[i] in ['CapacityToActivityUnit']):
            result += 'param ' + sheetNames[i] + ' default 1 : \n'
            result += insert_no_variables(sheetNames, i)
        # 8 #all the parameters that do not have variables
        elif (sheetNames[i] in ['TotalTechnologyAnnualActivityLowerLimit']):
            result += 'param ' + sheetNames[i] + ' default 0 := \n'
            result += insert_no_variables(sheetNames, i)
        # 8 #all the parameters that do not have variables
        elif (sheetNames[i] in ['ModelPeriodEmissionLimit']):
            result += 'param ' + sheetNames[i] + ' default 999999 := ;\n'
        # 8 #all the   parameters   that do not have variables
        elif (sheetNames[i] in ['ModelPeriodExogenousEmission', 'AnnualExogenousEmission', 'OperationalLifeStorage']):
            result += 'param ' + sheetNames[i] + ' default 0 := ;\n'
        elif (sheetNames[i] in []):  # 8 #all the parameters that do not have variables
            result += 'param ' + sheetNames[i] + ' default 0 := ;\n'
        # 8 #all the parameters that do not have variables
        elif (sheetNames[i] in ['TotalTechnologyModelPeriodActivityLowerLimit']):
            result += 'param ' + sheetNames[i] + ' default 0 := ;\n'
        # 8 #all the parameters that do not have variables
        elif (sheetNames[i] in ['DepreciationMethod']):
            result += 'param ' + sheetNames[i] + ' default 1 := ;\n'
        # 8 #all the parameters that do not have variables
        elif (sheetNames[i] in ['OperationalLife']):
            result += 'param ' + sheetNames[i] + ' default 1 : \n'
            result += insert_no_variables(sheetNames, i)
        elif (sheetNames[i] in ['DiscountRate']):  # default value
            with open('CSVFiles/' + sheetNames[i] + '.csv', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    result += 'param ' + sheetNames[i] + ' default 0.1 := ;\n'
    return result


def insert_no_variables(sheetNames, i):
    result = ""
    with open('CSVFiles/' + sheetNames[i] + '.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        firstColumn = []
        secondColumn = []
        secondColumn.append('REGION')
        for row in reader:
            firstColumn.append(row[0])
            secondColumn.append(row[1])
        result += " ".join(firstColumn) + ' '
        result += ':=\n'
        result += " ".join(secondColumn) + ' '
        result += ';\n'
    return result


def insert_two_variables(sheetNames, i):
    result = ""
    with open('CSVFiles/' + sheetNames[i] + '.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        newRow = next(reader)
        newRow.pop(0)
        newRow.pop(0)
        year = newRow.copy()
        for row in reader:
            result += '[REGION, ' + row.pop(0) + ', *, *]:'
            result += '\n'
            result += " ".join(year) + " "
            result += ':=\n'
            result += " ".join(row) + " "
            result += '\n'
        result += ';\n'
    return result


def insert_table(name):
    result = ""
    with open('CSVFiles/' + name + '.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        newRow = next(reader)
        newRow.pop(0)  # removes the first element of the row
        result += " ".join(newRow) + " "
        result += ':=\n'
        for row in reader:
            result += " ".join(row) + " "
            result += '\n'
        result += ';\n'
    return result


def modifyNames(sheetNames):
    """I change the name of the sheets in the xlsx file to match with the csv
    actual ones
    """
    modifiedNames = sheetNames.copy()
    for i in range(len(modifiedNames)):
        if (modifiedNames[i] == "TotalAnnualMaxCapacityInvestmen"):
            modifiedNames[i] = "TotalAnnualMaxCapacityInvestment"
        elif (modifiedNames[i] == "TotalAnnualMinCapacityInvestmen"):
            modifiedNames[i] = "TotalAnnualMinCapacityInvestment"
        elif (modifiedNames[i] == "TotalTechnologyAnnualActivityLo"):
            modifiedNames[i] = "TotalTechnologyAnnualActivityLowerLimit"
        elif (modifiedNames[i] == "TotalTechnologyAnnualActivityUp"):
            modifiedNames[i] = "TotalTechnologyAnnualActivityUpperLimit"
        elif (modifiedNames[i] == "TotalTechnologyModelPeriodActLo"):
            modifiedNames[i] = "TotalTechnologyModelPeriodActivityLowerLimit"
        elif (modifiedNames[i] == "TotalTechnologyModelPeriodActUp"):
            modifiedNames[i] = "TotalTechnologyModelPeriodActivityUpperLimit"
    return modifiedNames


if __name__ == '__main__':
    if len(sys.argv) != 4:
        msg = "Usage: python {} <filepath> <workbook_filename> <output_filepath>"
        print(msg.format(sys.argv[0]))
        sys.exit(1)
    else:
        try:
            main(sys.argv[1], sys.argv[2], sys.argv[3])
        except:
            sys.exit(1)
