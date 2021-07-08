from django.contrib import admin

from votes.models import CommentVote, PostVote

admin.site.register(PostVote)
admin.site.register(CommentVote)
