from . models import Post
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, RedirectView

# Create your views here.
# fuction base view to show template
'''
def indexview(request):
    """
    a function base view to show index page
    """
    return render(request,'index.html')
'''

class IndexView(TemplateView):
    """
    a class base view to show index page
    """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "ali"
        context["posts"] = Post.objects.all()
        return context
    
'''
Function Base View for redirect test
def RedirectToYoutube(request):
    return redirect('https://www.youtube.com/')
'''

class RedirectToYoutube(RedirectView):
    url = 'https://www.youtube.com/'

    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        print(post)
        return super().get_redirect_url(*args, **kwargs)