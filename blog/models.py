from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class Author(models.Model):
    
    # required to associate Author model with User model (Important)
    user = models.OneToOneField(User, null=True, blank=True)

    # additional fields
    activation_key = models.CharField(max_length=255, default=1)
    email_validated = models.BooleanField(default=False)
    
    # name = models.CharField(max_length=100, unique=True,
    #                         verbose_name='Author Name')
    # email = models.EmailField(unique=True)
    # active = models.BooleanField(default=False)
    # created_on = models.DateTimeField(auto_now_add=True)
    # last_logged_in = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    author = models.ForeignKey(Author)  # one-t-many-relationship


    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("blog:post_by_category", kwargs={"category_slug": self.slug})


class Tag(models.Model):
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    author = models.ForeignKey(Author)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("blog:post_by_tag", kwargs={"tag_slug": self.slug})
    


class Post(models.Model):
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True,
                            help_text='Slug will be generated automatically from the title of the post')
    # content = models.TextField()
    content = RichTextUploadingField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:post_detail",
                       kwargs={"pk": self.pk, "post_slug": self.slug})
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class Feedback(models.Model):
    
    name = models.CharField(max_length=200,
                            help_text="Name of sender")
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "FeedBack"
    
    def __str__(self):
        return self.name
