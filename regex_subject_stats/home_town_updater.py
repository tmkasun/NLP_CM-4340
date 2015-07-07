__author__ = 'tmkasun'

from pymongo import MongoClient
from config import config
import re

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