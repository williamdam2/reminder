from os.path import exists
from ..models import *
from datetime import datetime
import csv
import os
# is_exist = exists("log.csv")

# print(is_exist)

def write_log(machine,user):
    now = datetime.now()
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = BASE_DIR+"\\log\\"+machine.macId+"_"+now.strftime("%Y")+".csv"
    is_exist = exists(filename)
    # print(is_exist)
    csv_header = ['Time','User','Mac_ID','Model','Line','Status','Config','LOT_ID','Software','Detail']
    
    with open(filename,'a+',newline='',encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        if(not is_exist):
            writer.writerow(csv_header)
        data_row = [now.strftime("'%Y-%m-%d %H:%M:%S"),user,machine.macId,machine.model,machine.line,machine.status,machine.buildConfig,machine.lotId,machine.sw,machine.curDetail]
        writer.writerow(data_row)