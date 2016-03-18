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
# counting the number of columns in the first row in an awful way
ncol = 0
count = 0
for line in fh:
        count = count + 1
        ncol = len(line)
        if count == 1:
            break



"Slicing lines:"
# Patient file
patient_fields = list()
patient_keys = list()
patid = list()


"lines splitted and appended to a list"
count = 0
for line in fh:
    print line
        
    #Try this. There are few differences in the final fields, but I think the problem is how the 'patient_parts' are defined
    # works now, thanks
    patient_fields = [line[int(sum(patient_parts[:i])):sum(patient_parts[:i+1])].strip() for i in range(len(patient_parts))]
    print patient_fields
    patid.append(patient_fields[0])
    
print patid


    
#general method that takes a line of maxcol total columns and splits it into (unequal) parts
#def slice_it(li, maxcol, parts):
#    stop = 0
#    start = 0
#    while(stop < maxcol):
#        for j in parts:
#            stop = start + j            
#            yield li[start:stop]
#            start = stop 
#    for patient_field in slice_it(line, ncol, patient_parts):
#        fields = patient_field.split()
#        for field in fields:
#            patient_fields.append(field)
#    print patient_fields
#            for field in patient_fields:
#                patient_keys = field
#                print patient_keys
#    if count == 1:
#        break
#    else:
#        count = count + 1

#split = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]        
#patient_fields_all = split(patient_fields, patient_parts_number)
#print patient_fields_all


 
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
