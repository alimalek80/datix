from django.db import models
from django.utils.text import slugify
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = MarkdownxField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    # Relationships
    category = models.ForeignKey(
        Category,
        related_name='posts',
        on_delete=models.SET_DEFAULT,
        default=1
    )

    subcategory = models.ForeignKey(
        Subcategory,
        related_name='posts',
        on_delete=models.SET_NULL,
        null=True,
        blank = True
    )

    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            num = 1
            while Post.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{base_slug}-{num}'
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    @property
    def formatted_markdown(self):
        """
        Convert the Markdown content to HTML.
        """
        return markdownify(self.content)

    def __str__(self):
        return self.title


