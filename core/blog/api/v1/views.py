from rest_framework.decorators import api_view
from rest_framework.response import Response


data = {
    "id":1,
    "title": "best practice"
}


@api_view()
def PostList(request):
    return Response("ok")


@api_view()
def PostDetail(request,pk):
    return Response(data)