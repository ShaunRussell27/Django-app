from django.db import models
from django.contrib import auth

class Tag(models.Model):
    """This is the tag linked to the recipe"""
    tag = models.CharField \
        (max_length=32, \
         help_text="The name of the tag")
    def __str__(self):
        return self.tag

class Ingredient(models.Model):
    """This is an ingredient in the recipe"""
    ingredient = models.CharField \
        (max_length=45, \
         help_text="The name of the ingredient")
    def __str__(self):
        return self.ingredient

class Recipe(models.Model):
    """This is a Recipe"""
    name = models.CharField \
        (max_length=65, \
         help_text="The name of the recipe")
    minutes = models.IntegerField(help_text="The preparation time in min")
    nsteps = models.IntegerField(help_text="The number of steps in the recipe preparation")
    steps = models.TextField(help_text="The description of the steps involved in the preparation")
    description = models.TextField(help_text="High level description of the recipe")
    date_submitted = models.DateField(null=True, \
                                    help_text="The date the recipe was submitted")
    ningredients= models.IntegerField(help_text="The number of ingredients in the recipe")
    contributor = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', through="RecipeTag")
    ingredients = models.ManyToManyField('Ingredient', through="RecipeIngredient")

    recipe_img = models.ImageField(
        upload_to='images/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

class RecipeTag(models.Model):
    """Table for the many to many relationships between recipes and the tags"""
    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

class RecipeIngredient(models.Model):
    """Table for the many to many relationships between recipes and the ingredients"""
    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)


class Review(models.Model):
    """Reviews for the different movies"""
    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE, \
                              help_text="The Recipe that this review is for.")
    rating = models.IntegerField(help_text="The rating the reviewer has given.")
    creator = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
    content = models.TextField(help_text="The Review text for the recipe")
    date_created = models.DateTimeField(auto_now_add=True, \
                                        help_text="The date and time the review was created.")
    date_edited = models.DateTimeField(null=True, \
                                       help_text="The date and time the review was last edited.")



