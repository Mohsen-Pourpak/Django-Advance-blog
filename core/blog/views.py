from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.shortcuts import get_object_or_404
from django.views.generic import (
    TemplateView,
    RedirectView,
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    # FormView,
)
from .models import Post
from .forms import PostForm
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
# function base view to show template

""" def indexview(request):
    # a function base view to show index page
        return render(request,'index.html')
 """


class IndexView(TemplateView):
    """
    a class base view to show index page
    """

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "ali"
        context["posts"] = Post.objects.all()
        return context


"""
Function Base View for redirect test
def RedirectToYoutube(request):
    return redirect('https://www.youtube.com/')
"""


class RedirectToYoutube(RedirectView):
    url = "https://www.youtube.com/"

    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs["pk"])
        print(post)
        return super().get_redirect_url(*args, **kwargs)


class PostListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = "blog.view_post"
    model = Post  # == (queryset = Post.objects.all())
    context_object_name = "posts"  # change context name's default "object" to "posts"
    paginate_by = 5
    ordering = "id"

    # def get_queryset(self):
    #     posts = Post.objects.filter(status=True)
    #     return posts


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


"""
class PostCreateView(FormView):
    template_name = 'contact.html'
    form_class = PostForm
    success_url = '/blog/post/'

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        return super().form_valid(form)
"""


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # fields = ['author', 'title', 'content', 'status', 'category',]
    form_class = PostForm  # Same as "fields", but must define is forms.py
    success_url = "/blog/post/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = "/blog/post/"


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = "/blog/post/"


@api_view()
def api_post_list_view(request):
    return Response("ok")
