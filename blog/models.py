from django.db import models


class Tags(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Blog(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="categories"
    )
    tags = models.ManyToManyField(Tags)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    short_desc = models.TextField()
    details = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.title} | {self.category.name}"


class BlogImage(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="images/blogs/")

    def __str__(self):
        return f"Image for {self.blog.title}"


class Reel(models.Model):
    title = models.CharField(max_length=255)
    video = models.FileField(upload_to="reels/")
    caption = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ["-created_at"]
