# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
#import pymongo
#import datetime
#from pymongo import MongoClient
#client = MongoClient()

"Reading the data files:"

" ----- PATIENT FILE -------- "
filename = 'Patient_a0001.txt' 
sub_dir = '/Users/pettorin/Dropbox/S2DS/selfcare/s2ds/PrimarySelfCare/primarycaredata/THINData'
fh = open(os.path.join(sub_dir, filename), "r")

"Input values:"
#Patient file input values
patient_parts = (4,1,8,6,1,8,2,8,2,8,1,1,1,2,1,2,8) # lengths of the parts for this file
patient_parts_number = len(patient_parts) # how many parts there are

"Patient fields we want:"
patient_patid = list()

"lines splitted and appended to a list: filling the patient fields we want"
count = 0
for line in fh:
#    print line        
    patient_fields = [line[int(sum(patient_parts[:i])):sum(patient_parts[:i+1])].strip() for i in range(len(patient_parts))]
#    print patient_fields
    patient_patid.append(patient_fields[0])

"printing the patient fields we want"    
#print patient_patid

" ----- MEDICAL FILE -------- "
filename = 'Medical_a0001.txt' 
sub_dir = '/Users/pettorin/Dropbox/S2DS/selfcare/s2ds/PrimarySelfCare/primarycaredata/THINData'
fh = open(os.path.join(sub_dir, filename), "r")

"Input values:"
#Patient file input values
medical_parts = (4,8,8,2,7,1,4,1,1,3,2,7,1,1,1,1,1,4,4,8,1) # lengths of the parts for this file
medical_parts_number = len(medical_parts) # how many parts there are

"Patient fields we want:"
medical_patid = list()
medical_medcode = list()

"lines splitted and appended to a list: filling the patient fields we want"
count = 0
for line in fh:
#    print line        
    medical_fields = [line[int(sum(medical_parts[:i])):sum(medical_parts[:i+1])].strip() for i in range(len(medical_parts))]
#    print medical_fields
    medical_patid.append(medical_fields[0])
    medical_medcode.append(medical_fields[4])

"printing the patient fields we want"    
#print medical_medcode


" ----- AHD FILE -------- "
filename = 'Ahd_a0001.txt' 
sub_dir = '/Users/pettorin/Dropbox/S2DS/selfcare/s2ds/PrimarySelfCare/primarycaredata/THINData'
fh = open(os.path.join(sub_dir, filename), "r")

"Input values:"
#Patient file input values
ahd_parts = (4,8,10,1,13,13,13,13,13,13,7,1,3,2,4,7,1,1,1,1,4,4,8,1) # lengths of the parts for this file
ahd_parts_number = len(ahd_parts) # how many parts there are

"Patient fields we want:"
ahd_patid = list()
ahd_ahdcode = list()
ahd_data1 = list()
ahd_data2 = list()
ahd_data3 = list()
ahd_data4 = list()
ahd_data5 = list()
ahd_data6 = list()
ahd_medcode = list()

"lines splitted and appended to a list: filling the patient fields we want"
count = 0
for line in fh:
#    print line        
    ahd_fields = [line[int(sum(ahd_parts[:i])):sum(ahd_parts[:i+1])].strip() for i in range(len(ahd_parts))]
#    print medical_fields
    ahd_patid.append(ahd_fields[0])
    ahd_ahdcode.append(ahd_fields[2])   
    ahd_data1.append(ahd_fields[4])       
    ahd_data2.append(ahd_fields[5])           
    ahd_data3.append(ahd_fields[6])       
    ahd_data4.append(ahd_fields[7])       
    ahd_data5.append(ahd_fields[8])       
    ahd_data6.append(ahd_fields[9])       
    ahd_medcode.append(ahd_fields[10])

"printing the patient fields we want"    
print ahd_ahdcode


    

#testing
#db = client.test_database
#collection = db.test_collection

#post = {"author": "Mike",
#         "text": "My first blog post!",
#         "tags": ["mongodb", "python", "pymongo"],
#         "date": datetime.datetime.utcnow()}


#posts = db.posts
#post_id = posts.insert_one(post).inserted_id
#post_id
