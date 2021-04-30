from django.shortcuts import render
from django.views.generic.base import View, TemplateResponseMixin

class StudentHomeView(TemplateResponseMixin, View):
  template_name = 'students/home.html'

  def get(self, request, *args, **kwargs):
    return self.render_to_response({})
