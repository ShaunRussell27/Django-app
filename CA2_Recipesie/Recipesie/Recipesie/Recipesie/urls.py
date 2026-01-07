"""
URL configuration for Recipesie project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from recipes.admin_site import recipes_admin_site
from django.urls import path
import recipes.bienvenu
import recipes.views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views # Import auth views


urlpatterns = [
    path('', lambda request: redirect('Recipesie/home/')),
    # Default admin for Users and Groups
    # This URL uses the built-in admin.site instance
    # It is restricted to authentication models only (Users and Groups)
    path('admin/', admin.site.urls),\
    # Custom Recipesie admin site
    # This URL uses a separate AdminSite instance (recipes_admin_site)
    # Only recipe-related models are registered to this admin site
    # This separates recipe administration from user/group management
    path('Recipesie/admin/', recipes_admin_site.urls), \
    #public recipesie views
    path('Recipesie/home/', recipes.bienvenu.Bienvenu.as_view()),\
    path('Recipesie/recipes/', recipes.views.recipes_list),\
    path('Recipesie/recipes_reviews/detail/', recipes.views.details_reviews),
    #part3 search
    path('Recipesie/search/', recipes.views.search_recipes, name='recipes_search'),
    #part 4 edit and create
    path('Recipesie/recipes/update/<int:pk>/', recipes.views.recipe_edit, name='recipe_edit'),
    path('Recipesie/recipes/new/', recipes.views.recipe_edit, name='recipes_create'),
    #part 5 upload/update image
    path('Recipesie/recipes/image/<int:pk>/', recipes.views.recipe_image_upload, name='recipe_image'),
    #part 6
    path('accounts/', include(('django.contrib.auth.urls', 'auth'),namespace='accounts')),
    path('accounts/profile/', Recipesie.views.profile, name='profile'),\


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


