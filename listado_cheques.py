from asyncore import write
from logging.config import dictConfig
import sys
import csv
import time
from datetime import datetime

fileName = sys.argv[1] + ".csv"
dni = sys.argv[2]
output = sys.argv[3]
chequeType = sys.argv[4]
chequeStatus = None
dateRange = None 

if (len(sys.argv) > 5):
    if (sys.argv[5].find(":") != -1):
        print("hola")
        dateRange = sys.argv[5]
    else:
        chequeStatus = sys.argv[5]

if (len(sys.argv) > 6):
    dateRange = sys.argv[6]
 
def simple_filter(chequeList, filterType, target):
    newList = []
    for element in chequeList:
        if (element[filterType] == target):
            newList.append(element)
    return newList

def date_range_filter(chequeList, min, max):
    newList = []
    for element in chequeList:
        timestamp = datetime.fromtimestamp(float(element[6])).date()
        minDate = datetime.strptime(min, "%d-%m-%Y").date()
        maxDate = datetime.strptime(max, "%d-%m-%Y").date()
        if (timestamp >= minDate and timestamp <= maxDate):
            newList.append(element)
    return newList

def check_repetition(chequeList):
    newList = []
    for i in range(len(chequeList)):
        for j in range(i +1, len(chequeList)):
            if (chequeList[i][3] == chequeList[j][3]):
                if (chequeList[i][0] == chequeList[j][0]):
                    newList.append(chequeList[i])
                    newList.append(chequeList[j])
                    return newList                  
    return newList


chequeFile = open("test.csv", "r")
reader = csv.reader(chequeFile)
cheques = list(reader)
chequeFile.close()
cheques.pop(0)
cheques = simple_filter(cheques, 8, dni).copy()

check = check_repetition(cheques)

if (len(check) > 0):
    print("ERROR: Numero de cheque repetido")
    for element in check:
        print(element)
else:
    cheques = simple_filter(cheques, 9, chequeType).copy()
    if (chequeStatus is not None):
        cheques = simple_filter(cheques, 10, chequeStatus)

    if (dateRange is not None):
        print(dateRange)
        dates = dateRange.split(':')
        cheques = date_range_filter(cheques, dates[0], dates[1]).copy()
    
    if (len(cheques) > 0):
        if (output == "PANTALLA"):
            print("AVISO: Cheques encontrados")
            for element in cheques:
                print(element)
        else:
            newFile = open(("DNI_" + dni + " " + "FECHA_" + datetime.now().strftime("%d-%m-%Y HORA_%Hh-%Mm") + ".csv"), "w", newline="")
            writer = csv.writer(newFile)
            writer.writerow(["NumeroCuentaOrigen","Valor","FechaOrigen", "FechaPago"])

            for element in cheques:
                writer.writerow([element[3], element[5], element[6], element[7]])
    else:
        print("AVISO: No se encontraron cheques con los valores ingresados")
