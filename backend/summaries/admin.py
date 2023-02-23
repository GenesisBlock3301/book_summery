from django.contrib import admin
from .models import Summary, Comment, Reply, Author


@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = ("user", "author", 'book_title', "summary_content", "is_like")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "summary", 'comment_content', "is_like")


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ("user", "comment", 'reply_content', "is_like")
    
    
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id","author_name", "author_bio")
