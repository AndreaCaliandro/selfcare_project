# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import pymongo
import datetime
from pymongo import MongoClient
client = MongoClient()

"Reading the data files:"
filename = 'Patient_a0001.txt' 
sub_dir = '/Users/pettorin/Dropbox/S2DS/selfcare/s2ds/PrimarySelfCare/primarycaredata/THINData'
fh = open(os.path.join(sub_dir, filename), "r")

"Input values:"
#Patient file input values
patient_parts = (4,1,8,6,1,8,2,8,2,8,1,1,1,21,2,8)
patient_parts_number = len(patient_parts)
# counting the number of columns in the first row in an awful way
ncol = 0
count = 0
for line in fh:
        count = count + 1
        ncol = len(line)
        if count == 1:
            break
        
#method that takes a line of maxcol total columns and splits it into (unequal) parts
def slice_it(li, maxcol, parts):
    stop = 0
    start = 0
    while(stop < maxcol):
        for j in parts:
            stop = start + j            
            yield li[start:stop]
            start = stop 

"Slicing lines:"
# Patient file
patient_fields = list()
patient_keys = list()

count = 0
for line in fh:
    print line
    for patient_field in slice_it(line, ncol, patient_parts):
        fields = patient_field.split()
        for field in fields:
            patient_fields.append(field)
            print patient_fields
#            for field in patient_fields:
#                patient_keys = field
#                print patient_keys
    if count == 0:
        break
    else:
        count = count + 1

 
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