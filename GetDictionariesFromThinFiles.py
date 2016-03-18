# -*- coding: utf-8 -*-
"""
Extracts lists of dictionaries from the infividual THIN files on Fri Mar 18 08:23:48 2016
Run in directory with the .txt files
@author: Paula
"""

#Packages for better arrays and plotting we might need later
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(color_codes=True)

#Read in file with patient info
file = open('Patient_a0001.txt', 'r')
patientData = file.readlines()
file.close

#Info of patient columns
patientCodes =['patid','patflag', 'yob','famnum','sex',  'regdate','regstat',  'xferdate','regrea',  'deathdate','deathinfo','accept','institute','marital','dispensing','prscexempt','sysdate']
patientEndCharacters = [4,5,13,19,20,28,30,38,40,48,49,50,51,53,54,56,65]

#Create dictionaries for each line (= patient) and append to one patient dictionaries list
patientsDictList = []
for line in patientData:
    dictPatient1 ={}
    start = 0
    for n in range(len(patientCodes)):
        end = patientEndCharacters[n]
        dictPatient1[patientCodes[n]] = line[start:end]
        start = end 
        patientsDictList. append(dictPatient1)

#Read in the file with the medical info
file = open('Medical_a0001.txt', 'r')
medicalData = file.readlines()
file.close

#Names of medical entries columns
medCodes = ['patid','eventdate','enddate','datatype','medcode','medflag','staffid','source','episode','nhsspec','locate','textid','category','priority','medinfo','inprac','private','medid','consultid','sysdate','modified']
medEndCharacters = [4,12,20,22,29,30,34,35,36,39,41,48,49,50,51,52,53,57,61,69,70]
#Create dictionaries for each line (= entry) and append to one patient dictionaries list
medicalDictList = []
for line in medicalData:
    dictMed1 = {}
    start = 0
    for n in range(len(medCodes)):
        end = medEndCharacters[n]
        dictMed1[medCodes[n]] = line[start:end]
        start = end 
        medicalDictList. append(dictMed1)


#Read in the file with additional health data (ahd)
file = open('Ahd_a0001.txt', 'r')
ahdData = file.readlines()
file.close   

#Names of ahd file columns
ahdCodes = ['patid','eventdate','ahdcode','ahdflag','data1','data2','data3','data4' ,'data5','data6','medcode','source','nhsspec','locate','staffid','textid','category','ahdinfo','inprac','private','ahdid','consultid','sysdate','modified']
ahdDictList = []
ahdEndCharacters = [4,12,22,23,36,49,62,75,88,101,108,109,112,114,118,125,126,127,128,129,133,137,145,146]
for line in ahdData:
    ahdDict1 ={}
    start = 0
    for n in range(len(ahdCodes)):
        end = ahdEndCharacters[n]
        ahdDict1[ahdCodes[n]] = line[start:end]
        start = end 
        ahdDictList.append(ahdDict1)
        
