from rest_framework import (
    viewsets,
)


from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)


from rest_framework.filters import SearchFilter, OrderingFilter


from django_filters.rest_framework import DjangoFilterBackend

from .paginations import DefaultPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer, CategorySerializer
from blog.models import Post, Category


# Example for @api_view GET and POST.
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


# Example for @api_view GET, PUT and DELETE.
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


# Example for GET and POST methods with APIView.
'''class PostList(APIView):
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
'''


# Example for getting detail of a post with APIView including GET, PUT and DELETE.
'''
class PostDetail(APIView):
    """
    getting detail of posts and edit them.
    """

    permission_classes = [#IsAuthenticated,
                          IsAuthenticatedOrReadOnly
                          ]
    serializer_class = PostSerializer

    def get(self, request, pk):
        """ retrieving the post data """
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
'''


# Example for getting a list of posts with the Generic APIViews and mixins.
'''
class PostList(ListCreateAPIView):
    """
        getting a list of posts and creating a new post.
    """
    permission_classes = [#IsAuthenticated,
                          IsAuthenticatedOrReadOnly
                          ]
    serializer_class = PostSerializer
    queryset = Post.objects.filter()

'''


# Example for getting details of a post with the Generic APIViews and mixins including all the methods.
'''class PostDetail(#RetrieveAPIView,
                 #RetrieveUpdateAPIView,
                 RetrieveUpdateDestroyAPIView):
    """
    getting detail of posts and edit them.
    """

    permission_classes = [#IsAuthenticated,
                          IsAuthenticatedOrReadOnly
                          ]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
'''


class PostModelViewSet(viewsets.ModelViewSet):
    """
    getting a list of posts and creating a new post.
    """

    permission_classes = [  # IsAuthenticated,
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        "category": ["exact", "in"],
        "author": ["exact"],
        "status": ["exact"],
    }
    search_fields = [
        "title",
        "content",
    ]
    ordering_fields = ["published_date"]
    pagination_class = DefaultPagination

    # Extra actions for simple router instance.
    """    
    @action(method=["get"], detail=False)
    def get_ok(self, request):
        return Response({"detail":"ok"})
    """


class CategoryModletViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
