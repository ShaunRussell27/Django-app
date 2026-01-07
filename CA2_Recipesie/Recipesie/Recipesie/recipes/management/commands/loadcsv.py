import csv
import re
from ctypes.wintypes import tagPOINT

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from recipes.models import Tag,Ingredient,Recipe, RecipeTag, RecipeIngredient, Review


class Command(BaseCommand):
    help = 'Load the reviews data from a CSV file.'

    def add_arguments(self, parser):
        parser.add_argument('--csv', type=str)

    @staticmethod
    def row_to_dict(row, header):
        if len(row) < len(header):
            row += [''] * (len(header) - len(row))
        print("", dict([(header[i], row[i]) for i, head in enumerate(header) if head]))
        return dict([(header[i], row[i]) for i, head in enumerate(header) if head])

    def handle(self, movie=None, *args, **options):
        m = re.compile(r'content:(\w+)')
        header = None
        models = dict()
        try:
            with open(options['csv']) as csvfile:
                model_data = csv.reader(csvfile)
                for i, row in enumerate(model_data):
                    if max([len(cell.strip()) for cell in row[1:] + ['']]) == 0 and m.match(row[0]):
                        model_name = m.match(row[0]).groups()[0]
                        models[model_name] = []
                        header = None
                        continue

                    if header is None:
                        header = row
                        continue

                    row_dict = self.row_to_dict(row, header)
                    if set(row_dict.values()) == {''}:
                        continue
                    models[model_name].append(row_dict)

        except FileNotFoundError:
            raise CommandError('File "{}" does not exist'.format(options['csv']))

        for data_dict in models.get('Tag', []):
            p, created = Tag.objects.get_or_create(tag=data_dict['tag_tag'])

            if created:
                print('Created Tag "{}"'.format(p.tag))

        for data_dict in models.get('Ingredient', []):
            p, created = Ingredient.objects.get_or_create(ingredient=data_dict['ingredient_ingredient'])

            if created:
                print('Created Ingredient "{}"'.format(p.ingredient))

        for data_dict in models.get('Recipe', []):
            contributor, created = User.objects.get_or_create(email=data_dict['recipe_contributor'],
                                                              username=data_dict['recipe_contributor'])
            if created:
                print('Created Contributor "{}"'.format(contributor.email))

            b, created = Recipe.objects.get_or_create(name=data_dict['recipe_name'], \
                                                       contributor=contributor, \
                                                      defaults={
                                                          'minutes': data_dict['recipe_minutes'],
                                                          'nsteps': data_dict['recipe_nsteps'],
                                                          'steps': data_dict['recipe_steps'],
                                                          'description': data_dict['recipe_description'],
                                                          'date_submitted': data_dict['recipe_date_submitted'],
                                                          'ningredients': data_dict['recipe_ningredients']
                                                      })

            if created:
                 print('Created Recipe "{}"'.format(b.name))


        for data_dict in models.get('RecipeTag', []):
             recipe = Recipe.objects.get(name=data_dict['recipetag_recipe'])
             tag = Tag.objects.get(tag=data_dict['recipetag_tag'])
             bc, created = RecipeTag.objects.get_or_create(recipe=recipe,
                                                            tag=tag)
             if created:
                 print('Created RecipeTag {}"'.format(recipe.name, tag.tag))

        for data_dict in models.get('RecipeIngredient', []):
             recipe = Recipe.objects.get(name=data_dict['recipeingredient_recipe'])
             ingredient = Ingredient.objects.get(ingredient=data_dict['recipeingredient_ingredient'])
             bc, created = RecipeIngredient.objects.get_or_create(recipe=recipe,
                                                            ingredient=ingredient)
             if created:
                 print('Created RecipeIngredient {}"'.format(recipe.name, ingredient.ingredient))


        for data_dict in models.get('Review', []):
            creator, created = User.objects.get_or_create(email=data_dict['review_creator'],
                                                          username=data_dict['review_creator'])

            if created:
                print('Created Creator"{}"'.format(creator.email))
            recipe = Recipe.objects.get(name=data_dict['review_recipe'])

            review, created = Review.objects.get_or_create(content=data_dict['review_content'],
                                                           recipe=recipe,
                                                           creator=creator,
                                                           defaults={
                                                               'rating': data_dict['review_rating'],
                                                               'date_created': data_dict['review_date_created'],
                                                               'date_edited': data_dict['review_date_edited']
                                                           })
            if created:
                print('Created Review: "{}" -> "{}"'.format(recipe.name, creator.email))

        print("Import complete")