import json
import random
import uuid
from http.cookies import SimpleCookie
from unittest import TestCase

import simplejson as simplejson
from django.db.models import Q
from django.shortcuts import get_object_or_404

from blog.models import Blog
from color_print import p
from user.models import Member
from django.test import Client

from user.tests.test_models import count
from user.views import ID_REPOSITORY, uniq_check

client = Client()


class ViewTest(TestCase):
    # 테스트 유저 이름
    userName = "Tester0"

    # @classmethod
    # def setUpTestData(cls):
    #     count = 100
    #     for author_id in range(count):
    #         Member.objects.create(
    #             login_id=f"Tester{author_id}",
    #             password="1234",
    #             email=f"{author_id}@test.com",
    #             phone_number=f"010-{author_id}111-{author_id}111",
    #             address=f"0000{author_id}",
    #             name="Tester"
    #         )

    @classmethod
    def setUpClass(cls):
        rand = lambda: random.randint(0, 9)
        count = 10
        for author_id in range(count):
            phone_random1 = f"{rand()}{rand()}{rand()}{rand()}"
            phone_random2 = f"{rand()}{rand()}{rand()}{rand()}"
            address_random = f"{rand()}{rand()}{rand()}{rand()}{rand()}"

            member = Member.objects.create(
                login_id=f"Tester{author_id}",
                password="1234",
                email=f"{author_id}@test.com",
                phone_number=f"010-{phone_random1}-{phone_random2}",
                address=f"{address_random}",
                name="Tester"
            )

            Blog.objects.create(
                title=f"Test{author_id}",
                content=f"content{author_id}",
                member=member
            )

    def test_view_singup(self):
        request = client.get("/singup/")
        self.assertEqual(request.status_code, 200)

    def test_view_find_member(self):
        request = client.get("/members/")
        print()
        message = "Member List"
        count.log(p.auto_hr(message))
        # print("\n".join(str(request.content)[16:-4].split("}, {")))
        self.assertEqual(request.status_code, 200)

    # 데이터 불러오는 로직
    def test_view_find_blog(self):
        request = client.get("/blogs/")
        print()
        message = "Blog List"
        count.log(p.auto_hr(message))
        # print("\n".join(str(request.content)[13:-4].split("}, {")))
        self.assertEqual(request.status_code, 200)

    # 게시판
    def test_check_member(self):
        request = client.get("/members/")
        data = json.loads(request.content)
        for i in data["members"]:
            member_id = i["id"]
            request = client.get("/users/" + str(member_id) + "/")
            self.assertEqual(request.status_code, 200)
        self.assertEqual(request.status_code, 200)

    # 로그인 로직
    def Test_login_member(self):
        message = self.userName + " Login"
        print()
        count.log(p.auto_hr(message))

        # value = {"id": userName, "password": "1234"}
        # request = client.post("/login/", json.dumps(value), "application/json")

        member = get_object_or_404(Member, login_id=self.userName)
        # 수동 쿠기 저장
        UUID = str(uuid.uuid4())
        uniq_check(UUID, member.id)
        client.cookies['id'] = UUID
        response = client.get('/login/', follow=True)
        self.assertEqual(response.status_code, 200)

    # 게시판 생성
    def Test_create_board(self):
        UUID = client.cookies.get('id').value
        value = {"title": "title copy", "content": "content copy", "member": ID_REPOSITORY[UUID]}
        request = client.post("/blog-create/", json.dumps(value), "application/json")
        self.assertEqual(request.status_code, 201)

    def test_board(self):
        test_member = get_object_or_404(Member, login_id=self.userName)
        test_id = test_member.id

        self.Test_login_member()  # 로그인 로직
        # 쿠기 저장 확인 로직
        self.assertEqual(test_id, ID_REPOSITORY[client.cookies.get('id').value])
        self.Test_create_board()  # 게시판 생성 로직
        # 게시판 겟수 확인
        self.assertEqual(2, len(Blog.objects.filter(member=test_member)))

    # 데이터 삭제 로직
    @classmethod
    def tearDownClass(cls):
        Member.objects.all().delete()
        Blog.objects.all().delete()
