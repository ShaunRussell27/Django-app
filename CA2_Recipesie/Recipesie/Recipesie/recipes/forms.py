#imports
from django import forms
from django.utils import timezone
from recipes.models import Recipe, Tag, Ingredient, RecipeTag, RecipeIngredient


class RecipeSearchForm(forms.Form):
    """
    Search form for Part 3.
    - query: must be at least 1 character
    - search_by: decides which field we search (name/tag/ingredient/contributor/numbers)
    """
    SEARCH_BY_CHOICES = [
        ("name", "Recipe name"),
        ("ingredient", "Recipe Ingredient"),
        ("tag", "Recipe Tag"),
        ("contributor", "Contributor email"),
        ("nsteps", "Number of steps"),
        ("minutes", "Minutes to make"),
        ("ningredients", "Number of ingredients"),
    ]

    search_by = forms.ChoiceField(choices=SEARCH_BY_CHOICES)
    query = forms.CharField(min_length=1, required=True)

    def clean_query(self):
        q = (self.cleaned_data.get("query") or "").strip()
        if not q:
            raise forms.ValidationError("Please enter at least 1 character to search.")
        return q

    def clean(self):
        cleaned = super().clean()
        search_by = cleaned.get("search_by")
        q = cleaned.get("query")

        # Numeric validation for numeric searches
        if search_by in {"nsteps", "minutes", "ningredients"} and q:
            if not q.isdigit():
                raise forms.ValidationError("Please enter a numeric value for this search.")
        return cleaned

    search_by = forms.ChoiceField(
        choices=SEARCH_BY_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    query = forms.CharField(
        min_length=1,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )


class RecipeForm(forms.ModelForm):
    # because Recipe.tags and Recipe.ingredients use "through", we handle them manually
    # part 4
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control"})
    )
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control"})
    )

    class Meta:
        model = Recipe
        fields = ["name", "minutes", "nsteps", "ningredients", "description", "steps"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter recipe name"}),
            "minutes": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Minutes", "step": 1}),
            "nsteps": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Number of steps", "step": 1}),
            "ningredients": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Number of ingredients", "step": 1}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "High level description", "rows": 4}),
            "steps": forms.Textarea(attrs={"class": "form-control", "placeholder": "Preparation steps", "rows": 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Pre-fill m2m selections when editing
        if self.instance and self.instance.pk:
            self.fields["tags"].initial = self.instance.tags.all()
            self.fields["ingredients"].initial = self.instance.ingredients.all()

    def save(self, commit=True, user=None):
        """
        Save Recipe + manually handle Tag/Ingredient through tables.
        contributor + date_submitted are set automatically here.
        """
        recipe = super().save(commit=False)

        if not recipe.pk:
            # create
            recipe.date_submitted = timezone.now().date()
            if user is not None and user.is_authenticated:
                recipe.contributor = user

        if commit:
            recipe.save()

            # update through tables
            RecipeTag.objects.filter(recipe=recipe).delete()
            RecipeIngredient.objects.filter(recipe=recipe).delete()

            for t in self.cleaned_data.get("tags", []):
                RecipeTag.objects.create(recipe=recipe, tag=t)

            for i in self.cleaned_data.get("ingredients", []):
                RecipeIngredient.objects.create(recipe=recipe, ingredient=i)

        return recipe

class RecipeImageForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['recipe_img']

