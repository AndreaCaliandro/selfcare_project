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
filename = 'Patient_a0001.txt' 
sub_dir = '/Users/pettorin/Dropbox/S2DS/selfcare/s2ds/PrimarySelfCare/primarycaredata/THINData'
fh = open(os.path.join(sub_dir, filename), "r")

"Input values:"
#Patient file input values
patient_parts = (4,1,8,6,1,8,2,8,2,8,1,1,1,2,1,2,8) # lengths of the parts for this file
patient_parts_number = len(patient_parts) # how many parts there are


"Patient file"
patient_fields = list()
patient_keys = list()
"Patient fields we want:"
patid = list()

"lines splitted and appended to a list: filling the patient fields we want"
count = 0
for line in fh:
    print line
        
    patient_fields = [line[int(sum(patient_parts[:i])):sum(patient_parts[:i+1])].strip() for i in range(len(patient_parts))]
    print patient_fields
    patid.append(patient_fields[0])

"printing the patient fields we want"    
print patid


    

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
