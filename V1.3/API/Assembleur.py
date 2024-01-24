import numpy as np
from numpy.core.numeric import full 
import pandas as pd
import os
from os.path import isfile, join
import csv
import sys
import time
import platform
import datetime

class api():

    def __init__(self):

        self._platform = platform.system()
        self.currentPath = os.path.dirname(__file__)

        self.fieldnames = ["bidopen", "bidclose", "bidhigh", "bidlow", "askclose", "askhigh", "asklow"]

        self.constructor()

    def constructor(self):

        def searcher(self):

            def dir(self):

                dir_backup = self.currentPath.replace("/API","") + str(u"/DATA/BACKUP/")
                all_date = [ name for name in os.listdir(dir_backup) if os.path.isdir(os.path.join(dir_backup, name)) ]
                all_date = sorted(all_date, key=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))

                return all_date
                    
            def file(self, path):

                instruments = [f for f in os.listdir(path) if isfile(join(path, f))]
                
                try:
                    instruments.remove(".DS_Store")
                except:
                    pass
                try:
                    instruments.remove(" ")
                except:
                    pass

                return instruments

            all_date = dir(self)

            path = self.currentPath.replace("/API","") + str(u"/DATA/ALL/" + "/BASE/")

            for date in range(len(all_date)):
                instruments_all = file(self,self.currentPath.replace("/API","") + str(u"/DATA/ALL/" + "/BASE"))
                instruments_new = file(self,self.currentPath.replace("/API","") + str(u"/DATA/BACKUP/" + all_date[date] + "/BASE"))
                print(instruments_new)
                print(instruments_all)
                for name_new in list(instruments_new):
                    name_all = ""
                    for name_all in list(instruments_all):
                        if name_all == name_new:
                            print(name_all, name_new)
                            data_all = self.read_csv(self.currentPath.replace("/API","") + str(u"/DATA/ALL/" + "/BASE/" + name_all))
                            data_new = self.read_csv(self.currentPath.replace("/API","") + str(u"/DATA/BACKUP/" + str(all_date[date]) + str("/BASE/")) + str(name_new))
                            print(all_date[date])
                            constructor_engine(data_all, data_new, path, name_new.replace(".csv", ""))
                            break
                    data_new = self.read_csv(self.currentPath.replace("/API","") + str(u"/DATA/BACKUP/" + str(all_date[date]) + str("/BASE/")) + str(name_new))
                    if name_all != name_new and len(data_new) > 0:
                        data_new_array = []
                        for data in self.fieldnames:
                            data_new_array.append(data_new[data])
                        data_new_array = np.array(data_new_array)
                        api.create_cvs(path, name_new.replace(".csv", ""), self.fieldnames, data_new_array) 


        def constructor_engine(data_old_load, data_new_load, path, name):

            count = 0
            essais = 0
            data_new_loc = 0

            data_old = []
            data_new = []
            
            for data in self.fieldnames:
                data_old.append(data_old_load[data])
                data_new.append(data_new_load[data])

            data_old_loc = int(len(data_old[0]))
            if len(data_new[0]) > 0:
                for data_old_loc in range(len(data_old[0])):
                    if data_old[0][data_old_loc] == data_new[0][data_new_loc]:
                        essais += 1
                        for z in range(len(data_old[0])-data_new_loc):
                            if data_old[0][data_old_loc+z] == data_new[0][data_new_loc+z]:
                                count += 1
                                if z == 100:
                                    break
                            else:
                                count=0
                                break
                        if z == 100:
                            break

            print(f'essais : {essais}, resultat : {data_old_loc}')

            data_all = np.concatenate((np.array(data_old)[:,:data_old_loc], np.array(data_new)), axis=1)

            api.create_cvs(path, name, self.fieldnames, data_all)

        searcher(self)

    def read_csv(self, path):
        file_csv = pd.read_csv(path)
        return file_csv

    def create_cvs(path, name, fieldnames, entry):

        fullpath = str(path)+str(name)+str('.csv')

        with open(fullpath, "w") as csvfile:

            print('{0} in creation'.format(fullpath))
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for x in range(entry.shape[1]):
                writer.writerow(dict(zip(fieldnames, entry[:,x])))

x = api()