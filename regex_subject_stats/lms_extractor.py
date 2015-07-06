__author__ = 'tmkasun'

import requests
from bs4 import BeautifulSoup
from config import config
from pymongo import MongoClient
import re


def get_string(data):
    return data.string.strip()

# Initialization of enviroment

client = MongoClient(config.api['db_host'], config.api['db_port'])
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



client = MongoClient(config.api['db_host'], config.api['db_port'])  # TODO: remove this and use above client
geo_db = client[config.api['geo_db']]
geo_collection = geo_db[config.api['geo_collection']]

student_db = client[config.api['student_db']]
student_collection = student_db[config.api['student_collection']]

all_students = student_collection.find()

zero_matches = 0
high_matches = 0
for student in all_students:
    permanent_address = student['permanent_address']
    address_sections = permanent_address.split(',')
    main_town = address_sections.pop().strip('. \r\n')
    high_order_city = address_sections.pop().strip('. \r\n')  # Strip to remove whitespace and `.`
    if len(high_order_city) < 2:
        print(high_order_city)
        high_order_city = address_sections.pop().strip('. \r\n')
        print("new = {}".format(high_order_city))

    geo_result = geo_collection.find(
        {'name': re.compile(r'{}'.format(high_order_city), re.IGNORECASE), 'feature_code': re.compile(r'PP*')})

    while (len(address_sections) > 0) and (geo_result.count() == 0):
        high_order_city = address_sections.pop().strip('. \r\n')  # Strip to remove whitespace and `.`
        geo_result = geo_collection.find(
            {'name': re.compile(r'{}'.format(high_order_city), re.IGNORECASE), 'feature_code': re.compile(r'PP*')})

    if geo_result.count() == 0:
        sub_div = main_town.split(' ')[0]
        geo_result = geo_collection.find(
            {'name': re.compile(r'{}'.format(sub_div), re.IGNORECASE), 'feature_code': re.compile(r'PP*')})
        if geo_result.count() == 0:
            zero_matches += 1
            # print("--------DEBUG---------")
            # print(student)
            # print("--------END-DEBUG----------")
            # elif geo_result.count() > 10:
    #     high_matches +=1
    #     print("--------DEBUG-10---------")
    #     print(geo_result.count())
    #     print(address_sections)
    #     print(high_order_city)
    #     print("--------END-DEBUG-10---------")
    if geo_result.count() != 0:
        # print(student)
        student_collection.update({u'_id': student['_id']}, {'$set': {u'location': geo_result.next()}}, upsert=False)
        # print(geo_result.next())

print("--------------Summary-----------")
print("DEBUG: Total records = {}".format(all_students.count()))
print("DEBUG: No city matches = {}".format(zero_matches))
print("DEBUG: Over matches = {}".format(high_matches))
