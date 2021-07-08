import graphene
import django_filters
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from graphene import InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from djangraph.api_utils import create_update, get_object
from .models import Post


class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = ['title', 'body']

    order_by = django_filters.OrderingFilter(
        fields=(
            ('updated_at', 'updated_at'),
            ('-updated_at', '-updated_at'),
            ('created_at', 'created_at'),
            ('-created_at', '-created_at'),
        )
    )


class PostNode(DjangoObjectType):
    pid = graphene.String()
    class Meta:
        model = Post
        interfaces = (graphene.relay.Node, )


class PostInput(InputObjectType):
    title = graphene.String(required=True)
    body = graphene.String(required=True)


class Query(graphene.ObjectType):
    get_post = graphene.relay.Node.Field(PostNode)
    get_posts = DjangoFilterConnectionField(PostNode, filterset_class=PostFilter)

    # def resolve_get_post(self, info, **kwargs):
    #     id = kwargs.get('id')
    #     return get_object(Post, id)


    def resolve_get_posts(self, info, **kwargs):
        return PostFilter(data=kwargs, queryset=Post.objects.all()).qs


class CreatePost(graphene.relay.ClientIDMutation):

    class Input:
        data = graphene.Argument(PostInput)
        user_id = graphene.String(require=True)

    post = graphene.Field(PostNode)

    def mutate_and_get_payload(root, info, **input):
        post_data = input.get('data')
        user_id = input.get('user_id')
        user = get_object(User, user_id)
        post_data['user'] = user # info.context.user or None
        post = Post()
        new_post = create_update(post, post_data)
        return CreatePost(post=new_post)


class UpdatePost(graphene.relay.ClientIDMutation):

    class Input:
        data = graphene.Argument(PostInput)
        id = graphene.String(required=True)

    errors = graphene.List(graphene.String)
    post = graphene.Field(PostNode)

    def mutate_and_get_payload(root, info, **input):
        try:
            post_data = input.get('data')
            post_instance = get_object(Post, input.get('id'))
            if post_instance:
                post = create_update(post_instance, post_data)
                return UpdatePost(post=post)
        except ValidationError as e:
            return UpdatePost(post=None, errors=e)


class DeletePost(graphene.relay.ClientIDMutation):
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    class Input:
        id = graphene.String(required=True)

    def mutate_and_get_payload(root, info, **input):
        post = get_object(Post, input.get('id'))
        try:
            post.delete()
            success = True
            return DeletePost({success})
        except ValidationError as e:
            return DeletePost(errors=e)


class Mutation(graphene.AbstractType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
