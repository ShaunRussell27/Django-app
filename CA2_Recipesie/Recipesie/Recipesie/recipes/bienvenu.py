from django.views.generic import TemplateView

class Bienvenu(TemplateView):
    template_name:str = "bienvenu.html"