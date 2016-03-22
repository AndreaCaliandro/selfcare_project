from numpy import *
import os

userpath = '/home/andrea/Desktop/'
ancilirypath= 'Dropbox/selfcare/s2ds/PrimarySelfCare/primarycaredata/THINDataAncillaryFiles'
dbfilepath = 'Dropbox/selfcare/s2ds/PrimarySelfCare/primarycaredata/THINData/'

AnciliaryNames = {'LookupTables':'THINLookupsSample.txt',
                  'Readcodes':'ReadcodesSample.txt',
                  'NHSspec':'NHSspeciality.txt',
                  'Comments':'THINCommentsSample.txt'}


class THINdb:
    "A class to decode the THIN database. Specifically the Patient, Medical, Therapy, and AHD files"

    def __init__(self, ancilirypath=userpath+ancilirypath):
        self.ancilirypath = ancilirypath
        self.LookupTables()
        self.Readcodes()
        self.NHS()
        self.Comments()

        self.PatientDic = {}
        self.MedicalDic = {}
    #----------------------------------------#


    def LookupTables(self):
        self.LookupTablesDic = {}
        filepath = self.ancilirypath+'/'+AnciliaryNames['LookupTables']
        fieldsize = [11,3,101]
        with open(filepath) as fp:
            for line in fp:
                fields = fieldsplit(line, fieldsize)
                self.LookupTablesDic.setdefault(fields[0],{}).update({fields[1]:fields[2]})
    #-----------------------------------------------------------------------------------------#


    def Readcodes(self):
        self.MedcodeDic = {}
        filepath = self.ancilirypath+'/'+AnciliaryNames['Readcodes']
        fieldsize = [7,60]
        with open(filepath) as fp:
            for line in fp:
                fields = fieldsplit(line, fieldsize)
                self.MedcodeDic.update({fields[0]:fields[1]})
    #-----------------------------------------------------------------------------------------#

    def NHS(self):
        self.NHSdic = {}
        filepath = self.ancilirypath+'/'+AnciliaryNames['NHSspec']
        fieldsize = [3,80]
        with open(filepath) as fp:
            for line in fp:
                fields = fieldsplit(line, fieldsize)
                self.NHSdic.update({fields[0]:fields[1]})
    #-----------------------------------------------------------------------------------------#


    def Comments(self):    
        self.CommentsDic = {}
        filepath = self.ancilirypath+'/'+AnciliaryNames['Comments']
        fieldsize = [7,6000]
        with open(filepath) as fp:
            for line in fp:
                fields = fieldsplit(line, fieldsize)
                self.CommentsDic.update({fields[0]:fields[1]})
    #-----------------------------------------------------------------------------------------#


    def AnciliarySwitch(self, ancnum, code, codvalue):
        "0:LookupTables, 1:Medcode, 2:NHS, 3:Comment"
        switcher = {
            0: self.LookupTablesDic[code][codvalue] if self.LookupTablesDic.has_key(code) else '',
            1: self.MedcodeDic[codvalue] if self.MedcodeDic.has_key(codvalue) else '',
            2: self.NHSdic[codvalue] if self.NHSdic.has_key(codvalue) else codvalue,
            3: self.CommentsDic[codvalue] if self.CommentsDic.has_key(codvalue) else ''
        }
        return switcher.get(ancnum)
    #-----------------------------------------------------------------------------------------#

    
    def Patient(self, PatientFile):
        "Read and decode the Patient files. There is only one record for each patient"

        self.PatientCodes =['patid','patflag', 'yob','famnum','sex',
                'regdate','regstat', 'xferdate','regrea',
                'deathdate','deathinfo','accept','institute',
                'marital','dispensing','prscexempt','sysdate']
        fieldsize = [4,1,8,6,1,8,2,8,2,8,1,1,1,2,1,2,8]
        with open(PatientFile) as fp:
            for line in fp:
                fields = fieldsplit(line, fieldsize)
                self.PatientDic.setdefault(fields[0],{}).update({self.PatientCodes[i]:fields[i]
                                                                 for i in range(len(self.PatientCodes))})
    #-----------------------------------------------------------------------------------------#


    def HumanR_Patient(self,patid):
        "Print in a human readable form the info contained in a Patient line"

        CodeMeaning = {'patid':'PatientID',
                       'patflag':'Integrity flag',
                       'yob':'Year of birth',
                       'famnum':'Id shared by patients living at same address',
                       'sex':'Sex of Patient',
                       'regdate':'Patients registration date',
                       'regstat':'Registration status',
                       'xferdate':'Date of transfer out of practice',
                       'regrea':'Extended registration information',
                       'deathdate':'Patients date of death',
                       'deathinfo':'Death information',
                       'accept':'Registration acceptance type',
                       'institute':'Residential Institute',
                       'marital':'Marital status',
                       'dispensing':'Dispensing patient',
                       'prscexempt':'Prescription exemption',
                       'sysdate':'System date'}

        Header = ['Field', 'key', 'value', 'Explanation']
        table = [Header]
        for code in self.PatientCodes:
            codvalue = self.PatientDic[patid][code]
            if len(codvalue)>0:
                row = [CodeMeaning[code],
                       code,
                       codvalue,
                       self.LookupTablesDic[code][codvalue] if self.LookupTablesDic.has_key(code) else '']
                table.append(row)
        print PrettyPrint(table)
    #---------------------------------------------------------------------------------------------------------#

    
    def Medical(self, MedicalFile):
        "There are many records per patient as a new record is generated with each new 'event'"
        "that is experienced by the patient."

        self.MedicalCodes = ['patid','eventdate','enddate','datatype','medcode','medflag','staffid',
                             'source','episode','nhsspec','locate','textid','category','priority',
                             'medinfo','inprac','private','medid','consultid','sysdate','modified']
        fieldsize = [4,8,8,2,7,1,4,1,1,3,2,7,1,1,1,1,1,4,4,8,1]
        with open(MedicalFile) as fp:
            for line in fp:
                fields = fieldsplit(line, fieldsize)
#                if self.MedicalDic.has_key((fields[17],fields[3])):
#                    for f in range(len(self.MedicalCodes)):
#                        print self.MedicalCodes[f], self.MedicalDic[(fields[17],fields[3])][self.MedicalCodes[f]], fields[f]
#                    break

                
                self.MedicalDic.setdefault(fields[0],{}).update({fields[17]:{fields[3]:{self.MedicalCodes[i]:fields[i] for i in range(len(self.MedicalCodes))}}})
    #---------------------------------------------------------------------------------------------------------#

    
    def HumanR_Medical(self, patid, medid=False, datatype=False):
        if medid==False or datatype==False:
            self.HumanR_Medical_patid(patid)
        else: self.HumanR_Medical_table(patid, medid, datatype)
    #---------------------------------------------------------------------------------------------------------#

    
    def HumanR_Medical_patid(self, patid):
        "For each entry of the same patient print the eventdate, datatype, medid"

        Header = ['eventdate', 'datatype', 'Explanation', 'medid']
        table = [Header]
        for medid in self.MedicalDic[patid].keys():
            for datatype in self.MedicalDic[patid][medid].keys():
                dic = self.MedicalDic[patid][medid][datatype]
                row = [dic['eventdate'],
                       dic['datatype'],
                       self.LookupTablesDic['datatype'][datatype],
                       dic['medid']]
                table.append(row)
        print PrettyPrint(table)
        print 'Number of entries for Patient %s = %d' %(patid, len(table)-1)
    #---------------------------------------------------------------------------------------------------------#

      
    
    def HumanR_Medical_table(self, patid, medid, datatype):
        "Print in a human readable form the info contained in a Patient line"
        
        CodeMeaning = {'patid':['PatientID',0],
                       'eventdate':['Event date',0],
                       'enddate':['Event end date (00000000 if no date recorded)',0],
                       'datatype':['Structured data type',0],
                       'medcode':['Medical code (anc. Readcodes)',1],
                       'medflag':['Integrity flag',0],
                       'staffid':['ID of person entering record',0],
                       'source':['Origin of record',0],
                       'episode':['Episode type',0],
                       'nhsspec':['Secondary care speciality (anc. NHSspecialty)',2],
                       'locate':['Location of consultation',0],
                       'textid':['Comment (anc. THINcomments)',3],
                       'category':['Category of medical entry',0],
                       'priority':['Priority 1 = life-threatening conditions',0],
                       'medinfo':['AIS extra information',0],
                       'inprac':['Event recorded in practice (Y/N)',0],
                       'private':['Private (Y) or NHS (N) treatment',0],
                       'medid':['Medical record identifier',0],
                       'consultid':['Consult link to same therapy AHD consultation',0],
                       'sysdate':['System date',0],
                       'modified':['Flag to indicate if record has been edited by GP (Y/N)',0]}

        #AnciliaryEnum = [self.LookupTablesDic, self.MedcodeDic, self.NHSdic, self.CommentsDic]
        Header = ['Field', 'key', 'value', 'Explanation']
        table = [Header]
        for code in self.MedicalCodes:
            codvalue = self.MedicalDic[patid][medid][datatype][code]
            if len(codvalue)>0:
                #AncDic = AnciliaryEnum[CodeMeaning[code][1]]
                ancnum = CodeMeaning[code][1]
                row = [CodeMeaning[code][0],
                       code,
                       codvalue,
                       self.AnciliarySwitch(ancnum, code, codvalue)]
                       #self.LookupTablesDic[code][codvalue] if self.LookupTablesDic.has_key(code) else '']
                       #AncDic[code][codvalue] if AncDic.has_key(code) else '']
                table.append(row)
        print PrettyPrint(table)
    #---------------------------------------------------------------------------------------------------------#

    

    
def fieldsplit(line, fieldsize):
    "Return a list of the string splitted in fields of fixed number of characters defined by fieldsize"

    fieldsize = insert(array(fieldsize).cumsum(),0,0)
    return [line[fieldsize[i]:fieldsize[i+1]].strip() for i in range(len(fieldsize)-1)]
#---------------------------------------------------------------------------------------#


def PrettyPrint(table, justify = "L"):

    columnWidth = len(table[0])*[0]
    # find max column width
    for row in table:
        for i in range(len(row)):
            width = len(str(row[i]))
            if width > columnWidth[i]:
                columnWidth[i] = width

    nrow = len(table)
    outputStr = ""
    rowList = nrow*[0]
    for j in range(nrow):
        row = table[j]
        rowList[j] = []
        for i in range(len(row)):
            if justify == "R": # justify right
                rowList[j].append(str(row[i]).rjust(columnWidth[i]))
            elif justify == "L": # justify left
                rowList[j].append(str(row[i]).ljust(columnWidth[i]))
            elif justify == "C": # justify center
                rowList[j].append(str(row[i]).center(columnWidth[i]))

    vline = [((array(columnWidth)+5).sum()-5)*'-']
    rowList.insert(0, vline)
    rowList.insert(2, vline)
    rowList.append(vline)
    for j in range(len(rowList)):
        outputStr += '|  ' + '  |  '.join(rowList[j]) + "  |\n"

    return outputStr
#---------------------------------------------------------------------------------------#
