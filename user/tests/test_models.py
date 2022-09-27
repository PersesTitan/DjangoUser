import datetime
import re
from unittest import TestCase
from datetime import datetime

import pytz

from color_print import p
from color_print.p import CountLog
from user.models import Member

count = CountLog()


class ModelsTest(TestCase):

    @classmethod
    def setUpTest(cls):
        print("Model Test")
        pass

    def setUp(self):
        print("Model Test Start")
        pass

    # id 중복 체크
    def test_user_id(self):
        message = "Id Unique Check"
        count.log(p.auto_hr(message))
        li = list()
        for i in Member.objects.all():
            li.append(i.id)
        self.assertEqual(len(li), len(set(li)))

    # login_id 중복 체크
    def test_user_login_id(self):
        message = "Login Id Unique Check"
        count.log(p.auto_hr(message))
        li = list()
        for i in Member.objects.all():
            li.append(i.login_id)
        self.assertEqual(len(li), len(set(li)))

    # create_date 가 지금 보다 크지 않을때
    def test_date(self):
        message = "Date Check"
        count.log(p.auto_hr(message))
        now = datetime.now().replace(tzinfo=pytz.utc)
        for i in Member.objects.all():
            self.assertTrue(i.create_date < now)

    # Email Type Check
    def test_email(self):
        message = "Email Type Check"
        count.log(p.auto_hr(message))
        for i in Member.objects.all():
            self.assertTrue(re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$").match(i.email))

    def test_phone_number(self):
        message = "Phone Number Check"
        count.log(p.auto_hr(message))
        for i in Member.objects.all():
            self.assertTrue(re.compile("^\\d{2,3}-\\d{4}-\\d{4}$").match(i.phone_number))
