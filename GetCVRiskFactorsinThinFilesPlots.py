# -*- coding: utf-8 -*-
"""
Extracts lists of dictionaries from the infividual THIN files. Better written and correct plotting.
Run in directory with the .txt files
Created on Fri Mar 25 12:16:35 2016

@author: Paula
"""

import matplotlib.pyplot as plt
import seaborn as sns
sns.set(color_codes=True)
import json
#-----------------------------------------------------------------------------------------#

# Functions to read in main THIN files

def read_THINpatients(patientsfile):
    """
    Read Thin patients file: "Patient_a000X.txt" and crate a list of dictionaries for each line
    """
    file = open(patientsfile, 'r')
    patientData = file.readlines()
    file.close

    patientCodes =['patid','patflag', 'yob','famnum','sex',  'regdate','regstat',  'xferdate','regrea',  'deathdate','deathinfo','accept','institute','marital','dispensing','prscexempt','sysdate']
    patientEndCharacters = [4,5,13,19,20,28,30,38,40,48,49,50,51,53,54,56,65]
    
    patientsDictList = []
    for line in patientData:
       dictPatient1 ={}
       start = 0
       for n in range(len(patientCodes)):
           end = patientEndCharacters[n]
           dictPatient1[patientCodes[n]] = line[start:end]
           start = end 
       patientsDictList. append(dictPatient1)

    return patientsDictList
    

def read_THINmedical(medfile):
    """
    Read Thin medical file: "Medical_a000X.txt" and crate a list of dictionaries for each line
    """
    file = open(medfile, 'r')
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
    return medicalDictList
    
def read_Ahd(adhfile):
    """
    Read Thin additional healt data file: "Ahd_a000X.txt" and crate a list of dictionaries for each line
    """
    file = open(adhfile, 'r')
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
    return ahdDictList
    

def create_patient_cvrisk_dict(patient_dict,medical_dict,med_risk_dict_codes):
    patients_cvrisk_factors = {}
    for patients in patient_dict:
        patient_cv_dict = {}
        patient_cv_dict['sex'] = patients['sex']
        patient_cv_dict['marital'] = patients['marital']
        patient_cv_dict['age'] = int(patients['yob'][0:4])
        for codekey in med_risk_dict_codes.keys():
            positive_factors = []
            for entry in medical_dict:
                if entry['medcode'] in med_risk_dict_codes[codekey] and entry['patid'] in patients['patid']:
                    positive_factors.append(entry['eventdate'])
                if positive_factors:
                    patient_cv_dict[codekey] = positive_factors
        patients_cvrisk_factors[patients['patid']] = patient_cv_dict
    return  patients_cvrisk_factors
    
def create_patient_data_dict(patient_dict,adh_dict,ahd_risk_dict_code):
    patients_cv_data = {}
    for patients in patient_dict:
        patient_cv_dict = {}
        patient_cv_dict['sex'] = patients['sex']
        patient_cv_dict['marital'] = patients['marital']
        patient_cv_dict['age'] = int(patients['yob'][0:4])
        for codekey in ahd_risk_dict_codes.keys():
            positive_factors = []
            for entry in adh_dict:
                if entry['patid'] == patients['patid'] and entry['ahdcode'] in ahd_risk_dict_code[codekey]:
                    positive_factors.append(entry['eventdate'])
            if positive_factors:
                patient_cv_dict[codekey] = positive_factors
        patients_cv_data[patients['patid']] = patient_cv_dict  
    return patients_cv_data
    
def add_practiceID_to_patientID(old_dictionary, prefix):
    newdict = {} 
    for oldkey in old_dictionary.keys():
        newkey = prefix+ oldkey
        newdict[newkey] = old_dictionary[oldkey]
    return newdict

#-----------------------------------------------------------------------------------------#

#Categories for relevant parameters according to AHA data structure
#Create dictionaries with all codes related to each category

# Info in Medical file --> ReadcodesSample.txt
med_risk_dict_codes = {}
med_risk_dict_codes['ethnicgroup'] =  ['9i3..00','9i4..00','9i5..00','9i6..00','9i61.00','9i7..00','9i8..00','9i9..00','9iA..00','9iA4.00','9iA8.00','9iB..00','9iC..00','9iD..00','9iD0.00','9iE..00','9iF..00','9iF1.00','9iF2.00','9iF3.00','9iF9.00','9iFB.00','9iFC.00','9iFF.00','9iFH.00','9iG..00']
med_risk_dict_codes['recentemergad'] = ['L6A1..00','6A1..11']
med_risk_dict_codes['autoimmune'] = ['D110.00','N040.00','M154.00','M154100','M154700','J521.11','F20..00','1434.00','14F2.00']   
med_risk_dict_codes['badback'] = ['14G4.00','16C..00','16C2.00','16C3.00','16C5.00','16C6.00','16C9.00','16CZ.00','1D24.11']
med_risk_dict_codes['bleeding'] = ['J573.11','42j..00','158..00','K56y111','K59yx11','K5E..00']
med_risk_dict_codes['thrombosis'] = ['F423811','G5yy800','G74..00''G74z.00','G801.11','G802000','SP12200','12C5.11','1JH..00','G5yy800']
med_risk_dict_codes['bowelproblem'] = ['J521.11','J50zz15','3930.00','3932.00','J4...11','J4...12','J40..11','J41..12','J410.00','J410100','J410300']
med_risk_dict_codes['cancer'] = ['B....11','B10z.11','B11..00','B11..11','B13..00','B133.00','B134.00','B13z.11','B141.12','B17..00','B170.00','B1z0.11','B224100','B22z.00','B22z.11','B3...11','B32..00','B33..11','B33..13','B34..00','B34..11','B40..00','B41..00','B41..11','B42..00','B430200','B440.00','B440.11','B450100','B46..00','B48..00','B5...11','B53..00','B565.00','B570.00','B577.11','B585.00','B590.11','B5z..00','B620.00','B627.00','B630.00','B64..00','B641.00','B65..00','B650.00','B651.00','B8..00']
med_risk_dict_codes['dentalproblem'] = ['J024.11','J025000','J026.00','J027.11','J031.11','J043.11','J043.14','J043C00','J046.00','J046300','J046400','J046500','J05..00']
med_risk_dict_codes['diabetes'] = ['1252.00','1434.00','66A8.00','66AJ.00','66Aj.00','66Ap.00','66AP.00','66Aq.00','66AQ.00','66AR.00','66AS.00','66AT.00','66AU.00','66AZ.00','8B3l.00','C10..00','C100011','C100112','C106.12','C108.00','C109.00','C10E.00','C10EM00','C10F.00','C10FJ00']
med_risk_dict_codes['neuroproblem'] = ['B927.00','1296.00','1473.00','667..00','F25..00','R003z11','F251400','R004000','R004100','R004200']
med_risk_dict_codes['eyeproblem'] = ['148..00','1481.00','1482.00','1486.00','B8..00 ','1B81.00','1B81.11','1B84.00']
med_risk_dict_codes['fertilityproblem' ]= ['1AZ2.00','1AZ2.11','K26..00']
med_risk_dict_codes['genitalinfect'] = ['41.00','A781200','A781212','K5...00','K420900','43eE.00','43j1.00']
med_risk_dict_codes['heartproblem']= ['14A..11','14A7.11','14A9.00','14AN.00']
med_risk_dict_codes['liverdisease'] = ['14C5.00','25G..11','25G4.00','A701.00','A701.11','A703.00','A70z000','J61..00','J610.00','J613.00','J61y100','J623.00','J633.00','J63y200']
med_risk_dict_codes['HIV' ]= ['43C3.11']
med_risk_dict_codes['incontinence'] = ['16F..00','1A23.00','1A26.00']
med_risk_dict_codes['inherited'] = ['1231.00','124..00','124..11','124..12','1241.12','1243.00','1243.11','1245.11','1248.00','1251.00','1252.00','1262.00','1262.11','1268.00','127..00','128..00','1281.00','1285.00','1289.00','1291.00','1296.00','1297.00','12A1.00','12C..13','12C..14','12C1.00','12C2.00','12C3.00','12C4.00','12C4.11','12C4.12','12C5.00','12C5.11','12C5.12','12C8.00','12D2.00','12D4.00','12F..12','12G2.00','12H..00','12H1.00','12I..11']
med_risk_dict_codes['breathingproblem'] = ['R060600','R060800','1738.00','1739.00','173a.00','173A.00','173b.00','173B.00','173C.00','173c.00','12D2.00','14B4.00','663..00','663..11','663..12','663V100','663V200','663V300']
med_risk_dict_codes['muscletrouble'] = ['N23y400','N23yE00','N241000','N241012','N241100']
med_risk_dict_codes['osteoporosis'] = ['66a..00','66a2.00', 'N330.00','N330B00']      
med_risk_dict_codes['majoroperations'] = ['14N..00','14N..11','TB0y.00','SP12200','SP25000','SP25500','SP2y200']
med_risk_dict_codes['renaldiseases'] = ['14D..11','1Z1..00','1Z12.00','1Z13.00','1Z14.00','K10..00','K13z.00','K132.00']
med_risk_dict_codes['tuberculosis'] = ['A1...00','1411.00']
med_risk_dict_codes['mentalillness'] = ['9H8..00']
med_risk_dict_codes['gynaecoproblem'] = ['157..00','157..11','1571.00','1572.00','1574.11','158..00','158..11','158..12','1581.00','1583.00','1592.11','15C..00','15D..00','15E..00','15F..00','15H..00']
med_risk_dict_codes['gynaecosurgery' ]= ['1599.00']
med_risk_dict_codes['lvh' ]= ['324..00']
med_risk_dict_codes['angina'] = ['G33..00','G311.13','G311100']
med_risk_dict_codes['stroke'] = ['14A7.12','G66..00','G66..12']
med_risk_dict_codes['pvd'] = ['G73z.00','G73..00','G73..11','9m1..00']
med_risk_dict_codes['medicalhypert'] = ['662O.00','8CR4.00']
med_risk_dict_codes['genitalcircumcision'] = ['7C24200','ZV50212']
med_risk_dict_codes['atrialfibrillation'] = ['14AN.00','G573.00','G573000','G573200']
med_risk_dict_codes['asthma'] = ['14B4.00','173A.00','173c.00']
med_risk_dict_codes['anti'] = ['66Q..11','88A5.00']
med_risk_dict_codes['bloodpressure'] = ['246..11','246..12','2465.00','2469.00','246A.00','246a.00','246D.00','246d.00']
med_risk_dict_codes['allergicrhinitis'] = ['H17..00','H171.00','H172.00','12D4.00','H170.11','H172.11']
med_risk_dict_codes['hypertension'] = ['662..12','14A2.00']
med_risk_dict_codes['brain'] = ['R140300']
med_risk_dict_codes['cholesterol'] = ['1262.11']
med_risk_dict_codes['vegetarian'] = ['13A1.00']

#Info in Ahd file --> AHDCodesSample.txt
ahd_risk_dict_codes = {}
ahd_risk_dict_codes['bloodgroup'] = ['1012000000']
ahd_risk_dict_codes['bloodpressure'] = ['1005010500']
ahd_risk_dict_codes['alcoholintake'] = ['003050000']
ahd_risk_dict_codes['smoke'] = ['1003040000']
ahd_risk_dict_codes['bloodglucose'] = ['1001400067']
ahd_risk_dict_codes['bmi'] = ['1005010200']
ahd_risk_dict_codes['serumcholes'] = ['1001400017']
ahd_risk_dict_codes['ldl'] = ['1001400035']
ahd_risk_dict_codes['hemoglobin'] = ['1001400027']
ahd_risk_dict_codes['fastinglu'] = ['001400139']

#-----------------------------------------------------------------------------------------#

# Read in files and merge

patients0001_dicts = read_THINpatients('Patient_a0001.txt')
patients0002_dicts = read_THINpatients('Patient_a0002.txt')

medical0001_dicts = read_THINmedical('Medical_a0001.txt')
medical0002_dicts = read_THINmedical('Medical_a0002.txt')

adh0001_dicts = read_Ahd('Ahd_a0001.txt')
adh0002_dicts = read_Ahd('Ahd_a0001.txt')    

#Create new dictionary with all patients and their appearances of all the risk factors in med file
#takes long to run
patients001_cvrisk_factors = create_patient_cvrisk_dict(patients0001_dicts,medical0001_dicts,med_risk_dict_codes)
patients002_cvrisk_factors = create_patient_cvrisk_dict(patients0002_dicts,medical0002_dicts,med_risk_dict_codes)

#Create new dictionary with all patients and their appearances of all cv data in ahd file
#takes long to run
patients001_cv_data = create_patient_data_dict(patients0001_dicts,adh0001_dicts,ahd_risk_dict_codes)
patients002_cv_data = create_patient_data_dict(patients0002_dicts,adh0002_dicts,ahd_risk_dict_codes)

#Add practive IDs to patient IDs in all dictionaries. Important to have same prefix in data and risk factor dictionary
new_patients001_cvrisk_factors = add_practiceID_to_patientID(patients001_cvrisk_factors, 'p001_')
new_patients001_cv_data = add_practiceID_to_patientID(patients001_cv_data, 'p001_')

new_patients002_cvrisk_factors = add_practiceID_to_patientID(patients002_cvrisk_factors, 'p002_')
new_patients002_cv_data = add_practiceID_to_patientID(patients002_cv_data, 'p002_')

#Join into practice files into one 
all_patients_cvrisk_factors = new_patients001_cvrisk_factors.copy()
all_patients_cvrisk_factors.update(new_patients002_cvrisk_factors)

all_patient_cv_data = new_patients001_cv_data.copy()
all_patient_cv_data.update(new_patients002_cv_data)


#Save dictionaries as JSON objects 
with open('all_patients_cvrisk_factors.json', 'w') as f:
    json.dump(all_patients_cvrisk_factors, f)

with open('all_patient_cv_data.json', 'w') as f:
    json.dump(all_patient_cv_data, f)



#Create big overview plot of all the data
risk_codes = med_risk_dict_codes.keys()
risk_codes.remove('vegetarian')
risk_codes.remove('inherited')
#Create overview plot to show all cardiovascular relevant measurements and risk factors for 1 clinic
sns.set_style("white") 
sns.despine()
sns.set_context("talk")
for n in range(len(all_patient_cv_data.keys())):
#    if all_patient_cv_data[all_patient_cv_data.keys()[n]]['sex'] is '1':
#        lm = plt.scatter(1990,n, color = "deepskyblue", marker = '*')
#    elif all_patient_cv_data[all_patient_cv_data.keys()[n]]['sex'] is '2':    
#        lm = plt.scatter(1990,n, color = "hotpink", marker = '*')
    if 'bloodpressure' in all_patient_cv_data[all_patient_cv_data.keys()[n]].keys():
        for bpdate in all_patient_cv_data[all_patient_cv_data.keys()[n]]['bloodpressure']:
            if int(bpdate[0:4]) > 1984:
                plot_date = float(bpdate[0:4])+float(bpdate[4:6])/13
                lm = plt.scatter(plot_date,n, color = "lightcoral", s = 9)
    if 'bmi' in all_patient_cv_data[all_patient_cv_data.keys()[n]].keys():
        for bmidate in all_patient_cv_data[all_patient_cv_data.keys()[n]]['bmi']:
            if int(bmidate[0:4]) > 1984:
                plot_date = float(bmidate[0:4])+float(bmidate[4:6])/13
                lm = plt.scatter(plot_date,n, color = "darkcyan", s = 7)
    if 'serumcholes' in all_patient_cv_data[all_patient_cv_data.keys()[n]].keys():
        for scdate in all_patient_cv_data[all_patient_cv_data.keys()[n]]['serumcholes']:
            if int(scdate[0:4]) > 1984:
                plot_date = float(scdate[0:4])+float(scdate[4:6])/13
                lm = plt.scatter(plot_date,n, color = "gold", s = 7) 
    if 'bloodglucose' in all_patient_cv_data[all_patient_cv_data.keys()[n]].keys():
        for bgdate in all_patient_cv_data[all_patient_cv_data.keys()[n]]['bloodglucose']:
            if int(bgdate[0:4]) > 1984:
                plot_date = float(bgdate[0:4])+float(bgdate[4:6])/13
                lm = plt.scatter(plot_date,n, color = "purple", s = 7)  
    
    for factor in risk_codes:
        if factor in all_patients_cvrisk_factors[all_patient_cv_data.keys()[n]].keys():
            for factordate in all_patients_cvrisk_factors[all_patient_cv_data.keys()[n]][factor]:
                if int(factordate[0:4]) > 1984:
                    plot_date = float(factordate[0:4])+float(factordate[4:6])/13
                    lm = plt.scatter(plot_date,n, color = "black", s = 1)

plt.xlabel('Event date')
plt.ylabel('Patients')
sns.despine()             
axes = lm.axes
axes.set_ylim(-2,4002)
axes.set_xlim(1984,2011)
plt.savefig('patientsall_1984-2010.eps', format='eps', dpi=800)




