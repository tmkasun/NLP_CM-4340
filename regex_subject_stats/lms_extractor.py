__author__ = 'tmkasun'

import requests
import re

cookies = dict(PHPSESSID='uullf27nsenm4p35i1jnhh9pr6')
url = u'http://lms.mrt.ac.lk/student_enrolment_window.php?stu_UserID=10204'
request_result = requests.get(url, cookies=cookies)
cont = request_result.content

pattern1 = re.compile('UNIVERISTY OF MORATUWA - STUDENT ENROLLMENTS')

a = re.search(pattern1,cont)

print(a)