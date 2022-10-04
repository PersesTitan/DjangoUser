import json
import random
import uuid
from http.cookies import SimpleCookie
from django.test import TestCase

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
        global blog
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

            blog = Blog.objects.create(
                title=f"Test{author_id}",
                content=f"content{author_id}",
                member=member
            )

        cls.blog = blog

    def test_view_singup(self):
        request = client.get("/singup/")
        self.assertEqual(request.status_code, 200)

    def test_view_find_member(self):
        request = client.get("/members/")
        print()
        message = "Member List"
        count.log(p.auto_hr(message))
        print("\n".join(str(request.content)[16:-4].split("}, {")))
        self.assertEqual(request.status_code, 200)

    # 데이터 불러오는 로직
    def test_view_find_blog(self):
        request = client.get("/blogs/")
        print()
        message = "Blog List"
        count.log(p.auto_hr(message))
        print("\n".join(str(request.content)[13:-4].split("}, {")))
        self.assertEqual(request.status_code, 200)

    # 게시판 조회
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
        member = get_object_or_404(Member, login_id=self.userName)
        # 수동 쿠기 저장
        UUID = str(uuid.uuid4())
        uniq_check(UUID, member.id)
        client.cookies['id'] = UUID
        response = client.get('/login/', follow=True)
        self.assertEqual(response.status_code, 200)

    def Test_create_board_no_login(self):
        message = "no login create board"
        print()
        count.log(p.auto_hr(message))

        value = {"title": "title copy", "content": "content copy"}
        request = client.post("/blog-create/", json.dumps(value), "application/json")
        self.assertEqual(request.status_code, 302)  # 302 : 로그인을 위해서 로그인 페이지로 연결

    # 게시판 생성
    def Test_create_board(self):
        message = "create board"
        print()
        count.log(p.auto_hr(message))

        UUID = client.cookies.get('id').value
        value = {"title": "title copy", "content": "content copy", "id": UUID}
        request = client.post("/blog-create/", json.dumps(value), "application/json")
        p.red("생성된 블로그")
        print(json.loads(request.content))
        self.assertEqual(request.status_code, 201)
        return json.loads(request.content)["id"]  # 생성한 게시판

    # 게시판 수정 로그인을 안했을때 ( title 변경 )
    def Test_edit_board_no_login(self, board_id):
        message = "no login edit board"
        print()
        count.log(p.auto_hr(message))

        p.red("수정전 값")

        value = {"title": "title Test Change", "content": None}
        requests = client.patch(f"/blogs/{board_id}/", json.dumps(value), "application/json")
        p.red("수정된 값")
        print(json.loads(requests.content))
        self.assertEqual(requests.status_code, 302)  # 302 : 로그인을 위해서 로그인 페이지로 연결

    # 게시판 수정 ( title 변경 )
    def Test_edit_board(self, board_id):
        message = "edit board"
        print()
        count.log(p.auto_hr(message))

        UUID = client.cookies.get("id").value
        change_title = "title Test Change"
        value = {"title": change_title, "content": None, "id": UUID}
        requests = client.patch(f"/blogs/{board_id}/", json.dumps(value), "application/json")

        request_value = json.loads(requests.content)
        self.assertEqual(request_value["title"], change_title)  # 값이 변경 되었는지 확인
        self.assertIsNotNone(request_value["content"])  # 값이 None 인지 확인
        self.assertEqual(request_value["content"], "content copy")  # 값이 그대로인지 확인
        self.assertEqual(requests.status_code, 200)  # 상태 코드 확인

    def Test_delete_board(self, board_id):
        message = "delete board"
        print()
        count.log(p.auto_hr(message))

        UUID = client.cookies.get("id").value
        value = {"id": UUID}
        request = client.delete(f"/blogs/{board_id}/", json.dumps(value), "application/json")
        self.assertEqual(request.status_code, 200)  # 상태 코드 확인
        self.assertEqual(json.loads(request.content)["message"], "삭제가 완료되었습니다.")  # 메세지 확인

    # 로그인 로직
    # 게시판 생성 로직
    # 게시판 겟수 확인
    def test_board(self):
        test_member = get_object_or_404(Member, login_id=self.userName)
        test_id = test_member.id
        # 로그인을 안했을때
        self.Test_create_board_no_login()  # 생성 시도
        self.Test_edit_board_no_login(self.blog.id)  # 편집 시도

        self.Test_login_member()  # 로그인 로직
        # 쿠기 저장 확인 로직
        self.assertEqual(test_id, ID_REPOSITORY[client.cookies.get('id').value])
        board_id = self.Test_create_board()  # 게시판 생성 로직, 생성한 데이터 넘겨 받기
        # 게시판 겟수 확인
        self.assertEqual(2, len(Blog.objects.filter(member=test_member)))
        self.Test_edit_board(board_id)  # 게시판 수정 로직
        self.Test_delete_board(board_id)  # 게시판 삭제 로직
        # 게시판 겟수 확인
        self.assertEqual(1, len(Blog.objects.filter(vis=True).filter(member=test_member)))

    # 데이터 삭제 로직
    @classmethod
    def tearDownClass(cls):
        Member.objects.all().delete()
        Blog.objects.all().delete()
