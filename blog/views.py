from django.shortcuts import get_object_or_404, render
from django.shortcuts import render,redirect
from django.views.generic import ListView,TemplateView,CreateView,DeleteView,DetailView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView,BaseDeleteView
from ckeditor.fields import RichTextField 
from django import forms
from django.forms import ModelMultipleChoiceField,CheckboxSelectMultiple
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
from .models import Author, Post
from .forms import CreatePostForm,AuthorForm,UpdatePostForm

class AddPost(CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'create_post.html'
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(AddPost, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, *args, **kwargs):
        return super(AddPost, self).dispatch(*args, **kwargs)

class PostListView(ListView):
    model=Post
    template_name='home.html'

class PostDetailView(DetailView):
    model=Post
    slug_field='slug'
    template_name='detailView.html'
    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, *args, **kwargs):
        return super(PostDetailView, self).dispatch(*args, **kwargs)

"""
class PostUpdateView(UpdateView):
    model=Post
    slug_field='slug'
    template_name='updatePost.html'
    form_class=UpdatePostForm
    success_url = reverse_lazy('home')
    fields=['title','body_text','author']
    Post.author.add()

    def get_form_kwargs(self):
        kwargs = super(PostUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, *args, **kwargs):
        return super(PostUpdateView, self).dispatch(*args, **kwargs)

"""
def update_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    context ={'title','body_text','author'}
 
    # fetch the object related to passed id
    obj = get_object_or_404(Post, slug = slug)
 
    # pass the object as instance in form
    form = UpdatePostForm(request.POST or None, instance = obj)
 
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        return redirect("home")

    return render(request, "updatePost.html",{'form':form})

class PostDeleteView(DeleteView):
    model=Post
    success_url ="/"
    template_name="confirmDelete.html"
    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, *args, **kwargs):
        return super(PostDeleteView, self).dispatch(*args, **kwargs)

def registerAuthor(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    if Author.objects.filter(user=request.user):
        return redirect("home")

    else:
        form=AuthorForm()
        error=""
        if request.method == "POST":
            form=AuthorForm(request.POST) 
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                error="no"
                return redirect("home")
        return render(request,"authorRegister.html",{'form': form})