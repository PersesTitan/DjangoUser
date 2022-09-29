import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from blog.models import Blog


# Create your views here.
# title, content
def make_board(board):
    return {"title": board.title, "content": board.content, "vis": board.vis}


@method_decorator(csrf_exempt, name='dispatch')
class Create(View):
    def post(self, request):
        data = json.loads(request.body)
        title = data["title"]
        content = data["content"]
        Blog(
            title=title,
            content=content
        ).save()
        return JsonResponse({"title": title, "content": content}, status=201)


class Find(View):
    # +) 검색 로직
    def get(self, request):
        li = list(map(dict, Blog.objects.values()))
        return JsonResponse({"blog": li}, status=200)


# 1개 찾기 OR 특정 게시판 편집
@method_decorator(csrf_exempt, name='dispatch')
class FindOne(View):
    def get(self, request, blog_id):
        blog = get_object_or_404(Blog, pk=blog_id)
        return JsonResponse({blog.id: make_board(blog)}, status=200)

    # 편집
    def patch(self, request, blog_id):
        data = json.loads(request.body)
        title = data["title"]
        content = data["content"]
        b = Blog.objects.get(pk=blog_id)
        b.title = title
        b.content = content
        b.save()
        return JsonResponse({"title": title, "content": content}, status=200)

    # 보이지 않게 처리
    def delete(self, request, blog_id):
        b = Blog.objects.get(pk=blog_id)
        b.vis = False
        b.save()
        return JsonResponse({}, status=200)
