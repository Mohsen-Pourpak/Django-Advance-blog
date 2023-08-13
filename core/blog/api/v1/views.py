from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer
from blog.models import Post

data = {
    "id":1,
    "title": "best practice"
}


@api_view(["GET", "POST"])
def PostList(request):
    if request.method == "GET":
        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)  # "many" is for making instance for showing to serializer
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

@api_view(["GET", "PUT", "DELETE"])
def PostDetail(request,pk):
    post = Post.objects.get(pk=pk, status=True)
    if request.method=="GET":
        try:
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response({"detail": "object does not exist"}, status=status.HTTP_404_NOT_FOUND)  
    elif request.method=="PUT":
        serializer = PostSerializer(post,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    elif request.method=="DELETE":
        try:
            post.delete()
            return Response({"detail": "ITEM REMOVED SUCCESSFULLY~!"}, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response({"detail": "object does not exist"}, status=status.HTTP_404_NOT_FOUND)  