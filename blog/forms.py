from django import forms
from .models import Post, Category, Subcategory, Tag

class PostForm(forms.ModelForm):
    new_category = forms.CharField(
        max_length=100,
        required=False,
        label="New Category",
        help_text = "Enter a new category if it doesn't exist. "
    )

    new_subcategory = forms.CharField(
        max_length=100,
        required=False,
        label="New Subcategory",
        help_text="Enter a new subcategory if it doesn't exist."
    )

    tag_names = forms.CharField(
        max_length=255,
        required=False,
        label="Tags (comma-separated)",
        help_text="Enter up to 5 tags separated by commas (e.g., Python, Django, Web)."
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category', 'subcategory', 'tag_names']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate the category and subcategory dropdowns
        self.fields['category'].queryset = Category.objects.all()
        self.fields['subcategory'].queryset = Subcategory.objects.all()

    def clean_tag_names(self):
        tag_names = self.cleaned_data.get('tag_names')
        if tag_names:
            tags = [tag.strip() for tag in tag_names.split(',') if tag.strip()]
            if len(tags) > 5:
                raise forms.ValidationError("You can add a maximum of 5 tags.")
            return tags
        return []

    def save(self, commit=True):
        # Save the post instance
        post = super().save(commit=False)

        # Handle new category
        new_category_name = self.cleaned_data.get('new_category')
        if new_category_name:
            category, created = Category.objects.get_or_create(name=new_category_name)
            post.category = category

        # Handle new subcategory
        new_subcategory_name = self.cleaned_data.get('new_subcategory')
        if new_subcategory_name and post.category:
            subcategory, created = Subcategory.objects.get_or_create(
                name=new_subcategory_name,
                category=post.category
            )
            post.subcategory = subcategory

        if commit:
            post.save()

        # Handle tags
        tag_names = self.cleaned_data.get('tag_names')
        if tag_names:
            tags = []
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                tags.append(tag)
            post.tags.set(tags)

        return post