import graphene
import django_filters
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from graphene import InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from comments.models import Comment
from djangraph.api_utils import create_update, get_object
from .models import Post


class CommentFilter(django_filters.FilterSet):
    class Meta:
        model = Comment
        fields = ['user', 'body', 'parent_post', 'parent_comment']

    order_by = django_filters.OrderingFilter(
        fields=(
            ('updated_at', 'updated_at'),
            ('-updated_at', '-updated_at'),
            ('created_at', 'created_at'),
            ('-created_at', '-created_at'),
        )
    )


class CommentNode(DjangoObjectType):
    pid = graphene.String()
    class Meta:
        model = Comment
        interfaces = (graphene.relay.Node, )


class CommentInput(InputObjectType):
    body = graphene.String(required=True)


class Query(graphene.ObjectType):
    get_comment = graphene.relay.Node.Field(CommentNode)
    get_comments = DjangoFilterConnectionField(CommentNode, filterset_class=CommentFilter, parent_comment_id=graphene.String(), parent_post_id=graphene.String())

    # def resolve_get_post(self, info, **kwargs):
    #     id = kwargs.get('id')
    #     return get_object(Post, id)


    def resolve_get_comments(self, info, **kwargs):
        parent_post_id = kwargs.get('parent_post_id')
        parent_comment_id = kwargs.get('parent_comment_id')
        if parent_post_id:
            post = get_object(Post, parent_post_id)
            return post.comments
        if parent_comment_id:
            comment = get_object(Comment, parent_comment_id)
            return comment.comments
        return CommentFilter(data=kwargs, queryset=Comment.objects.all()).qs


class CreateComment(graphene.relay.ClientIDMutation):

    class Input:
        data = graphene.Argument(CommentInput)
        user_id = graphene.String(require=True)
        post_id = graphene.String(require=False)
        comment_id = graphene.String(require=False)

    comment = graphene.Field(CommentNode)
    error = graphene.List(graphene.String)

    def mutate_and_get_payload(root, info, **input):
        post_id = input.get('post_id')
        comment_id = input.get('comment_id')
        if not post_id and not comment_id:
            return CreateComment(comment=None, error=['post_id or comment_id are required.'])
        comment_data = input.get('data')
        user_id = input.get('user_id')
        user = get_object(User, user_id)
        if post_id:
            post = get_object(Post, post_id)
            comment_data['parent_post'] = post
        else:
            comment = get_object(Comment, comment_id)
            comment_data['parent_comment'] = comment

        comment_data['user'] = user # info.context.user or None
        comment = Comment()
        new_comment = create_update(comment, comment_data)
        return CreateComment(comment=new_comment)


class UpdateComment(graphene.relay.ClientIDMutation):

    class Input:
        data = graphene.Argument(CommentInput)
        id = graphene.String(required=True)

    errors = graphene.List(graphene.String)
    comment = graphene.Field(CommentNode)

    def mutate_and_get_payload(root, info, **input):
        try:
            comment_data = input.get('data')
            comment_instance = get_object(Comment, input.get('id'))
            if comment_instance:
                comment = create_update(comment_instance, comment_data)
                return UpdateComment(comment=comment)
        except ValidationError as e:
            return UpdateComment(comment=None, errors=e)


class DeleteComment(graphene.relay.ClientIDMutation):
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    class Input:
        id = graphene.String(required=True)

    def mutate_and_get_payload(root, info, **input):
        comment = get_object(Comment, input.get('id'))
        try:
            comment.delete()
            success = True
            return DeleteComment({success})
        except ValidationError as e:
            return DeleteComment(errors=e)


class Mutation(graphene.AbstractType):
    create_comment = CreateComment.Field()
    update_comment = UpdateComment.Field()
    delete_comment = DeleteComment.Field()
