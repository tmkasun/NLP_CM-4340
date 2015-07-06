__author__ = 'tmkasun'

import requests
from bs4 import BeautifulSoup
from config import config
from pymongo import MongoClient


def get_string(data):
    return data.string.strip()

# Initialization of enviroment

client = MongoClient('localhost', 27017)
university_db = client.uni

cookie = config.api['cookie']
base_url = config.api['base_url']
iframe_url = config.api['iframe_url']

fit_student_id_start = 9321 #9183
fit_student_id_end = 9370 #9319


stats = open(u'stats.txt', 'w+')

success_list = []
failed_list = []
for learn_studentId in range(fit_student_id_start, fit_student_id_end + 1):
    base_request = requests.get(base_url.format(learn_studentId), cookies=cookie)
    student_data_result = requests.get(iframe_url.format(learn_studentId), cookies=cookie)
    html_cont = student_data_result.content

    soup = BeautifulSoup(html_cont, "html.parser")

    table_data = soup.find_all('td', class_='noramlTableCell')

    student_info = {
        'reg_number': '{}'.format(get_string(table_data[6])),
        'nic': '{}'.format(get_string(table_data[26])),
        'permanent_address': '{}'.format(get_string(table_data[18])),
        'department_code': '{}'.format(get_string(table_data[4])),
        'gender': '{}'.format(get_string(table_data[22])),
        'name': {
            'full': '{}'.format(get_string(table_data[14])),
            'with_initials': '{}'.format(get_string(table_data[16]))
        }
    }

    if student_info['reg_number'] == '':
        print("DEBUG: reg_number: {} , learn id = {}".format(student_info['reg_number'], learn_studentId))
        failed_list.append(learn_studentId)
        continue
    status = university_db.students.insert_one(student_info)
    success_list.append(student_info)
    stats.write("ID {} Successfully added, Index number = {}\n".format(learn_studentId, student_info['reg_number']))

stats.write("#Failed items ---------\n")
for item_index in range(len(failed_list)):
    stats.write("{}. Failed LearnOrg_StudentId = {}\n".format(item_index+1, failed_list[item_index]))

print("Total insertions  = {} \n\t Failed records = {}".format(len(success_list), len(failed_list)))
stats.close()
client.close()