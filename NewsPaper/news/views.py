from datetime import datetime
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import Post, Category, Author
from .filters import PostFilter
from .forms import PostForm, SubForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from .signals import check_post_today


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'post'
    queryset = Post.objects.order_by('-post_time_create')
    paginate_by = 3
    form_class = PostForm

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

class PostCreate(PermissionRequiredMixin, CreateView):
    template_name = 'post_create.html'
    permission_required = ('news.add_post',)
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        cats_id_list = list(map(int, request.POST.getlist('post_category')))
        kat = Category.objects.filter(pk__in=cats_id_list)
        new_post = Post(post_type=request.POST['post_type'],
                       post_title=request.POST['post_title'],
                       post_text=request.POST['post_text'],
                       post_author=Author.objects.get(pk=request.POST['post_author']),
                       )

        if check_post_today(sender=Post, instance=new_post, **kwargs) < 3:
            new_post.save()
            for cat in kat:
                new_post.post_category.add(cat)

        return redirect('/news/')

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        author = Author.objects.get(author=user)
        initial['post_author'] = author
        return initial

class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'post_create.html'
    permission_required = ('news.change_post',)
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDelete(PermissionRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    permission_required = ('news.delete_post',)
    queryset = Post.objects.all()
    success_url = '/news/'


class Search(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'post'
    ordering = ['-post_time_create']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())

        return context

class Subscribe(PermissionRequiredMixin, CreateView):

    template_name = 'subscribe.html'
    permission_required = ('news.add_post',)
    form_class = SubForm
    success_url = '/'

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        return initial
