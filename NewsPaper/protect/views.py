from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from news.models import CategoryUser


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'
    context_object_name = 'category'
    queryset = CategoryUser.objects.all()
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['category'] = CategoryUser.objects.all()
        return context
