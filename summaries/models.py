
from django.db import models
from accounts.models import User


class Common(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Author(Common):
    author_name = models.CharField(max_length=255, null=True)
    author_bio = models.TextField()
    
    def __str__(self):
        return self.author_name
    

class Summary(Common):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=255, null=True)
    summary_content = models.TextField()
    is_like = models.BooleanField(default=False)
    
    def __str__(self):
        return self.summary_content[:100]+"..."
    

class Comment(Common):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    summary = models.ForeignKey(Summary, on_delete=models.CASCADE)
    comment_content = models.TextField()
    is_like = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.id)


class Reply(Common):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reply_content = models.TextField()
    is_like = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)+" "+str(self.user.id)
    
    
    
