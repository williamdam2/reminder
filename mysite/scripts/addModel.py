from reminder.models import *
import csv
from django.contrib.auth import User

def add():
    with open('reminder/model_input/machines.csv',encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)
            macTypeTem=MachineType(macType=row[1])
            machine = MachineStatus(
                macId=row[0],
                macType = macTypeTem,
                line=row[2],
                model=row[3],
                status=row[4],
                buildConfig=row[5],
                lotId=row[6],
                curDetail=row[7], 
                updated=row[8],
                sw=row[8])
            machine.save()
