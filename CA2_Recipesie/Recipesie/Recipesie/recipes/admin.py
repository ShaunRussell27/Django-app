#from django.contrib import admin

#from recipes.models import Tag, Ingredient, Recipe, RecipeTag,\
    #RecipeIngredient,Review

# Register your models here.
#admin.site.register(Tag)
#admin.site.register(Ingredient)
#admin.site.register(Recipe)
#admin.site.register(RecipeIngredient)
#admin.site.register(RecipeTag)
#admin.site.register(Review)
from django.contrib import admin
from recipes.models import (
    Tag,
    Ingredient,
    Recipe,
    RecipeTag,
    RecipeIngredient,
    Review
)
from recipes.admin_site import recipes_admin_site

@admin.register(Ingredient, site=recipes_admin_site)
class IngredientAdmin(admin.ModelAdmin):
    # Page 4: search for character chains
    list_display = ['ingredient']
    search_fields = ['ingredient']


@admin.register(Tag, site=recipes_admin_site)
class TagAdmin(admin.ModelAdmin):
    # Page 9: search for character chains
    list_display = ['tag']
    search_fields = ['tag']


@admin.register(RecipeIngredient, site=recipes_admin_site)
class RecipeIngredientAdmin(admin.ModelAdmin):
    # Page 5: show "recipe (ingredient)" + filters
    list_display = ['recipe_ingredient_display']
    list_filter = ['recipe', 'ingredient']

    def recipe_ingredient_display(self, obj):
        return f"{obj.recipe.name} ({obj.ingredient.ingredient})"
    recipe_ingredient_display.short_description = "Recipe Ingredient"


@admin.register(RecipeTag, site=recipes_admin_site)
class RecipeTagAdmin(admin.ModelAdmin):
    # Page 6: show "recipe (tag)" + filters
    list_display = ['recipe_tag_display']
    list_filter = ['recipe', 'tag']

    def recipe_tag_display(self, obj):
        return f"{obj.recipe.name} ({obj.tag.tag})"
    recipe_tag_display.short_description = "Recipe Tag"


@admin.register(Recipe, site=recipes_admin_site)
class RecipeAdmin(admin.ModelAdmin):
    # list page (matches lecturer spec on page 7)
    list_display = ['name', 'minutes', 'nsteps', 'contributor_email']
    list_filter = ['contributor']
    date_hierarchy = 'date_submitted'

    # edit page: remove submitted date + contributor (and hide name like lecturer screenshot)
    exclude = ['date_submitted', 'contributor', 'name']

    # group fields into sections like the lecturer screenshot
    fieldsets = (
        ("Recipe Metrics", {
            "fields": ("minutes", "nsteps", "ningredients"),
        }),
        ("Descriptive Information", {
            "fields": ("description", "steps"),
        }),
    )

    def contributor_email(self, obj):
        return obj.contributor.email
    contributor_email.short_description = "Contributor email"


@admin.register(Review, site=recipes_admin_site)
class ReviewAdmin(admin.ModelAdmin):
    # Page 8: creator (rating) recipe + date hierarchy + filters
    list_display = ['review_display']
    list_filter = ['recipe', 'rating', 'creator']
    date_hierarchy = 'date_created'

    def review_display(self, obj):
        return f"{obj.creator.email} ({obj.rating}) {obj.recipe.name}"
    review_display.short_description = "Review"