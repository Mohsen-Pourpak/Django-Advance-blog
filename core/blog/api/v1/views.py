from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from rest_framework import status
from rest_framework.views import APIView

from .serializers import PostSerializer
from blog.models import Post

data = {
    "id":1,
    "title": "best practice"
}


"""
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
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
"""


class PostList(APIView):
    """
        getting a list of posts and creating a new post.
    """
    permission_classes = [#IsAuthenticated,
                          IsAuthenticatedOrReadOnly
                          ]
    serializer_class = PostSerializer

    def get(self, request):
        """ retrieve a list of posts. """
        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)  # "many" is for making instance for showing to serializer
        return Response(serializer.data)

    def post(self,request):
        """ creating a post by providing data."""
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


"""
@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
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
"""

class PostDetail(APIView):
    """
    getting detail of posts and edit them.
    """

    permission_classes = [#IsAuthenticated,
                          IsAuthenticatedOrReadOnly
                          ]
    serializer_class = PostSerializer

    def get(self, request, pk):
        """ retrieving th post data """
        post = Post.objects.get(pk=pk, status=True)
        if request.method=="GET":
            try:
                serializer = self.serializer_class(post)
                return Response(serializer.data)
            except Post.DoesNotExist:
                return Response({"detail": "object does not exist"}, status=status.HTTP_404_NOT_FOUND)  
            
    def put(self, request, pk):
        """ edit the exist data. """
        post = Post.objects.get(pk=pk, status=True)
        serializer = PostSerializer(post,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request, pk):
        """ delete the post object """
        post = Post.objects.get(pk=pk, status=True)
        try:
            post.delete()
            return Response({"detail": "ITEM REMOVED SUCCESSFULLY~!"}, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response({"detail": "object does not exist"}, status=status.HTTP_404_NOT_FOUND)  
        