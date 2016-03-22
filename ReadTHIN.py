import THINdb

obj = THINdb.THINdb()
obj.Patient(THINdb.userpath+THINdb.dbfilepath+'Patient_a0001.txt')   #Create the Patient dictionary
obj.Patient(THINdb.userpath+THINdb.dbfilepath+'Patient_a0002.txt')
PatientDic = obj.PatientDic

obj.Medical(THINdb.userpath+THINdb.dbfilepath+'Medical_a0001.txt')   #Create the Medical dictionary
obj.Medical(THINdb.userpath+THINdb.dbfilepath+'Medical_a0002.txt')
MedicalDic = obj.MedicalDic

#obj.AHD(THINdb.userpath+THINdb.dbfilepath+'Ahd_a0001.txt')   #Create the AHD dictionary
#obj.AHD(THINdb.userpath+THINdb.dbfilepath+'Ahd_a0002.txt')
#AHDdic = obj.AHDdic


