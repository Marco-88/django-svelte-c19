import graphene
import django_filters
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from graphene import InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from comments.models import Comment
from djangraph.api_utils import create_update, get_object
from posts.models import Post
from .models import PostVote, CommentVote


class PostVoteFilter(django_filters.FilterSet):
    class Meta:
        model = PostVote
        fields = ['vote', 'user', 'post']


class PostVoteNode(DjangoObjectType):
    class Meta:
        model = PostVote
        interfaces = (graphene.relay.Node, )


class CommentVoteFilter(django_filters.FilterSet):
    class Meta:
        model = CommentVote
        fields = ['vote', 'user', 'comment']


class CommentVoteNode(DjangoObjectType):
    class Meta:
        model = CommentVote
        interfaces = (graphene.relay.Node, )


class Query(graphene.ObjectType):
    get_post_vote = graphene.relay.Node.Field(PostVoteNode)
    get_post_votes = DjangoFilterConnectionField(PostVoteNode, filterset_class=PostVoteFilter)
    get_comment_vote = graphene.relay.Node.Field(CommentVoteNode)
    get_comment_votes = DjangoFilterConnectionField(CommentVoteNode, filterset_class=CommentVoteFilter)


class CreatePostVote(graphene.relay.ClientIDMutation):
    class Input:
        vote = graphene.String(require=True)
        post_id = graphene.String(require=True)
        user_id = graphene.String(require=True)

    post_vote = graphene.Field(PostVoteNode)

    def mutate_and_get_payload(root, info, **input):
        vote = input.get('vote')
        post_id = input.get('post_id')
        post = get_object(Post, post_id)
        user_id = input.get('user_id')
        user = get_object(User, user_id)

        new_vote = PostVote.objects.filter(post_id=post.id, user_id=user.id)

        if len(new_vote) < 1:
            new_vote = PostVote()
        else:
            new_vote = new_vote[0]
            if new_vote.vote == vote:
                vote = 'NONE'

        vote_data = {
            'vote': vote,
            'post': post,
            'user': user
        }

        vote_instance = create_update(new_vote, vote_data)
        return CreatePostVote(post_vote=vote_instance)


class CreateCommentVote(graphene.relay.ClientIDMutation):
    class Input:
        vote = graphene.String(require=True)
        comment_id = graphene.String(require=True)
        user_id = graphene.String(require=True)

    comment_vote = graphene.Field(CommentVoteNode)

    def mutate_and_get_payload(root, info, **input):
        vote = input.get('vote')
        comment_id = input.get('comment_id')
        comment = get_object(Comment, comment_id)
        user_id = input.get('user_id')
        user = get_object(User, user_id)

        new_vote = CommentVote.objects.filter(comment_id=comment.id, user_id=user.id)

        if len(new_vote) < 1:
            new_vote = CommentVote()
        else:
            new_vote = new_vote[0]
            if new_vote.vote == vote:
                vote = 'NONE'

        vote_data = {
            'vote': vote,
            'comment': comment,
            'user': user
        }

        vote_instance = create_update(new_vote, vote_data)
        return CreateCommentVote(comment_vote=vote_instance)


class Mutation(graphene.AbstractType):
    create_post_vote = CreatePostVote.Field()
    create_comment_vote = CreateCommentVote.Field()

