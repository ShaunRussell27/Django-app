from django.contrib.admin import AdminSite

class RecipesieAdminSite(AdminSite):
    site_header = "Recipiesie Administration Site"
    site_title = "Recipiesie Admin"
    index_title = "Recipesie Admin Facility"

recipes_admin_site = RecipesieAdminSite(name='recipes_admin')


