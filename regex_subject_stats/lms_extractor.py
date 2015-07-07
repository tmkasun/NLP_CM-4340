__author__ = 'tmkasun'

import requests
from bs4 import BeautifulSoup
from config import config
from pymongo import MongoClient
import re

client = MongoClient(config.api['db_host'], config.api['db_port'])  # TODO: remove this and use above client


def get_coordinates(permanent_address):
    geo_db = client[config.api['geo_db']]
    geo_collection = geo_db[config.api['geo_collection']]

    student_db = client[config.api['student_db']]
    student_collection = student_db[config.api['student_collection']]

    all_students = student_collection.find()

    geo_location = None
    address_sections = permanent_address.split(',')
    main_town = address_sections.pop().strip('. \r\n')
    high_order_city = address_sections.pop().strip('. \r\n')  # Strip to remove whitespace and `.`
    if len(high_order_city) < 2:
        print(high_order_city)
        high_order_city = address_sections.pop().strip('. \r\n')
        print("DEBUG:new = {}".format(high_order_city))

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
            print('DEBUG: No result found!')
            geo_location = False
    if geo_result.count() != 0:
        geo_location = geo_result.next()

    return geo_location


def get_string(data):
    return data.string.strip()

# Initialization of enviroment

university_db = client.uni

cookie = config.api['cookie']
base_url = config.api['base_url']
iframe_url = config.api['iframe_url']

fit_student_id_start = 10204 #9183  # 9321
fit_student_id_end = 10345 #9370  # 9319

stats = open(u'stats.txt', 'w+')

success_list = []
failed_list = []
location_mismatched = []
last_success_reg_number = ''
it_pattern = re.compile(r'IT .*')
for learn_studentId in range(fit_student_id_start, fit_student_id_end + 1):
    base_request = requests.get(base_url.format(learn_studentId), cookies=cookie)
    student_data_result = requests.get(iframe_url.format(learn_studentId), cookies=cookie)
    html_cont = student_data_result.content

    soup = BeautifulSoup(html_cont, "html.parser")

    table_data = soup.find_all('td', class_='noramlTableCell')


    reg_number = get_string(table_data[6])
    department_code = get_string(table_data[4])

    if (reg_number == '') or (not re.match(it_pattern, department_code)):
        print(department_code)
        print("DEBUG: Inval reg or pattern miss reg_number: {} , learn id = {}".format(last_success_reg_number, learn_studentId))
        failed_list.append({'learn_studentId': learn_studentId, 'reg_number': last_success_reg_number})
        continue

    location = get_coordinates(get_string(table_data[18]))
    student_info = {
        'reg_number': '{}'.format(reg_number),
        'nic': '{}'.format(get_string(table_data[26])),
        'permanent_address': '{}'.format(get_string(table_data[18])),
        'location': location,
        'department_code': '{}'.format(department_code),
        'gender': '{}'.format(get_string(table_data[22])),
        'name': {
            'full': '{}'.format(get_string(table_data[14])),
            'with_initials': '{}'.format(get_string(table_data[16]))
        }
    }
    print("Current ID = {}".format(learn_studentId))
    if not location:
        print("DEBUG: No location  matches")
        location_mismatched.append({'learn_studentId': learn_studentId, 'reg_number': student_info['reg_number']})

    status = university_db.students.insert_one(student_info)
    last_success_reg_number = student_info['reg_number']
    success_list.append(student_info)
    stats.write("ID {} Successfully added, Index number = {}\n".format(learn_studentId, student_info['reg_number']))

stats.write("#Failed items ---------\n")
for item_index in range(len(failed_list)):
    stats.write("{}. Failed LearnOrg_StudentId = {} suspect reg number - {}\n".format(item_index + 1, failed_list[item_index]['learn_studentId'],failed_list[item_index]['reg_number']))

stats.write("#Location mismatches ---------\n")
for item_index in range(len(location_mismatched)):
    stats.write("{}. Failed Locations LearnOrg_StudentId = {} suspect reg number - {}\n".format(item_index + 1, location_mismatched[item_index]['learn_studentId'],location_mismatched[item_index]['reg_number']))


print("Total insertions  = {} \n\t Failed records = {}".format(len(success_list), len(failed_list)))
stats.close()
client.close()


