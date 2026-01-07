from django.shortcuts import render
from recipes.models import Recipe,Ingredient,Tag, RecipeTag, RecipeIngredient, Review
from statistics import median
from recipes.forms import RecipeSearchForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from recipes.forms import RecipeForm
from recipes.models import Recipe
from django.contrib.auth.decorators import login_required

from .models import Recipe
from .forms import RecipeImageForm

# My views here:.
#Calculates median for the available ratings of the recipe
def median_rating (reviews_ratings):
    return median(reviews_ratings)

def recipes_list(request):
    recipes = Recipe.objects.all()
    recipe_list = list()
    for recipe in recipes:
        reviews = recipe.review_set.all()
        tags=recipe.tags.all()
        ingredients = recipe.ingredients.all()
        if reviews:
            review_ratings = list()
            for review in reviews:
                review_ratings.append(review.rating)
            recipe_rating = str(round(median_rating(review_ratings), 2))
            number_of_reviews = str(len(reviews))
        else:
            recipe_rating = None
            number_of_reviews="0"

        # if tags:
        #     tag_list = list()
        #     for company in production_companies:
        #         production_companies_list.append(company.production_company)
        #
        # if genres:
        #     genres_list = list()
        #     for genre in genres:
        #         genres_list.append(genre.genre)

        recipe_list.append({'recipe': recipe,\
                           'tags': tags, \
                           'ingredients': ingredients, \
                           'recipe_rating': recipe_rating,\
                          'number_of_reviews':number_of_reviews})

    context={
            'recipe_list': recipe_list
        }

    return render(request, 'recipes_list.html', context)

def details_reviews(request):
    recipe_id = request.GET.get("recipe_id")
    print(recipe_id)
    recipe=Recipe.objects.get(id=recipe_id)
    print(recipe.name)
    reviews = recipe.review_set.all()
    print(reviews)

    context={
        'recipe':recipe,\
        'reviews': reviews,
    }

    return render(request,'recipes_reviews.html', context)




def search_recipes(request):
    """
    Part 3 Search:
    - text searches: case-insensitive STARTSWITH (istartswith)
    - numeric searches: <= value
    - no duplicates (distinct)
    - show errors for empty / non-numeric
    """
    results = Recipe.objects.none()
    form = RecipeSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            search_by = form.cleaned_data["search_by"]
            q = form.cleaned_data["query"]

            if search_by == "name":
                results = Recipe.objects.filter(name__istartswith=q)

            elif search_by == "ingredient":
                # Ingredient model field is `ingredient`
                results = Recipe.objects.filter(
                    ingredients__ingredient__istartswith=q
                ).distinct()

            elif search_by == "tag":
                # Tag model field is `tag`
                results = Recipe.objects.filter(
                    tags__tag__istartswith=q
                ).distinct()

            elif search_by == "contributor":
                # Contributor is a FK to auth user; search by email
                results = Recipe.objects.filter(
                    contributor__email__istartswith=q
                ).distinct()

            elif search_by == "nsteps":
                results = Recipe.objects.filter(nsteps__lte=int(q))

            elif search_by == "minutes":
                results = Recipe.objects.filter(minutes__lte=int(q))

            elif search_by == "ningredients":
                results = Recipe.objects.filter(ningredients__lte=int(q))

    return render(request, "recipes/search.html", {
        "form": form,
        "results": results
    })

def recipe_edit(request, pk=None):
    """
    Part 4:
    - If pk is provided -> edit that recipe
    - If pk is None -> create a new recipe
    - Show success message after save
    """
    recipe = None
    if pk is not None:
        recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            saved = form.save(user=getattr(request, "user", None))

            if pk is None:
                messages.success(request, "Recipe created successfully.")
            else:
                messages.success(request, "Recipe updated successfully.")

            return redirect("recipe_edit", pk=saved.pk)
    else:
        form = RecipeForm(instance=recipe)

    return render(request, "recipes/recipe_form.html", {
        "form": form,
        "recipe": recipe,
    })

@login_required
def recipe_image_upload(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == "POST":
        form = RecipeImageForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, "Recipe image updated successfully.")
            # redirect back to search page (or wherever you want)
            return redirect('recipes_search')  # change if your search url name is different
    else:
        form = RecipeImageForm(instance=recipe)

    return render(request, "recipes/recipe_image.html", {
        "recipe": recipe,
        "form": form
    })