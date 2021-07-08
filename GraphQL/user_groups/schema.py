import django_filters
import graphene
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from graphene import InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_file_upload.scalars import Upload
from graphql import GraphQLError

from djangraph.api_utils import get_object, create_update, get_pk_from_node_id
from djangraph.constants import GENRES
from user_groups.models import UserGroup
from users.models import Profile
from users.schema import UserNode


class GroupNode(DjangoObjectType):
    genres = graphene.List(graphene.String)
    users = graphene.List(UserNode)
    owner = graphene.Field(UserNode)
    user_id = graphene.String()

    class Meta:
        model = UserGroup
        filter_fields = {
            'id': ['exact', 'contains'],
            'owner': ['exact'],
            'users': ['icontains'],
        }
        interfaces = (graphene.relay.Node,)

    def resolve_image(self, info):
        if self.image:
            return info.context.build_absolute_uri(self.image.url)
        return None

    def resolve_users(self, info):
        if self.users:
            return self.users.all()


class GroupInput(InputObjectType):
    name = graphene.String(required=True)
    owner_id = graphene.String(required=True)
    usernames = graphene.List(graphene.String)
    description = graphene.String(required=True)
    genres = graphene.List(graphene.String)
    image = Upload()
    uid = graphene.ID()


class GroupFilter(django_filters.FilterSet):
    class Meta:
        model = UserGroup
        fields = ['genres', 'users', 'name', 'owner']


class Query(graphene.ObjectType):
    get_group = graphene.relay.Node.Field(GroupNode)
    get_groups = DjangoFilterConnectionField(GroupNode, user_id=graphene.String())

    def resolve_get_groups(self, info, **kwargs):
        user_id = kwargs.get('user_id')
        if user_id:
            user = get_object(User, user_id)
            groups = UserGroup.objects.filter(users__id=user.id)
            return groups
        return UserGroup.objects.all()


class CreateGroup(graphene.relay.ClientIDMutation):
    class Input:
        data = graphene.Argument(GroupInput)

    group = graphene.Field(GroupNode)
    errors = graphene.List(graphene.String)

    def mutate_and_get_payload(root, info, **input):
        try:
            data = input.get('data')
            group_data = {
                "name": data.name,
                "owner": get_object(User, data.owner_id),
                "users": User.objects.filter(username__in=data.usernames) if len(data.usernames) > 0 else [],
                "image": data.image,
                "description": data.description,
                "genres": data.genres
            }
            group_instance = UserGroup.objects.create(owner=get_object(User, data.owner_id))
            group = create_update(group_instance, group_data, exception=['id', 'users'])
            print(group.__dict__)
            return CreateGroup(group=group)
        except ValidationError as e:
            return CreateGroup(group=None, errors=e)


class JoinGroup(graphene.relay.ClientIDMutation):
    class Input:
        user_id = graphene.String()
        group_id = graphene.String()

    group = graphene.Field(GroupNode)
    errors = graphene.List(graphene.String)

    def mutate_and_get_payload(root, info, **input):
        try:
            user_id = input.get('user_id')
            group_id = input.get('group_id')

            group = get_object(UserGroup, group_id)
            user = get_object(User, user_id)

            if user in group.users.all():
                raise GraphQLError('You are already a member!')

            group.users.add(user)
            group.save()
            return JoinGroup(group=group)
        except ValidationError as e:
            return JoinGroup(group=None, errors=e)
        except GraphQLError as e:
            print(e)
            return JoinGroup(group=None, errors=e)


class RemoveMember(graphene.relay.ClientIDMutation):
    class Input:
        user_id = graphene.String()
        group_id = graphene.String()

    user = graphene.Field(UserNode)
    group = graphene.Field(GroupNode)
    errors = graphene.List(graphene.String)

    def mutate_and_get_payload(root, info, **input):
        try:
            user_id = input.get('user_id')
            group_id = input.get('group_id')

            user = get_object(User, user_id)
            group = get_object(UserGroup, group_id)

            if user not in group.users.all():
                raise GraphQLError('You are not a member!')

            group.users.remove(user)
            group.save()
            return RemoveMember(group=group, user=user)
        except ValidationError as e:
            return RemoveMember(group=None, errors=e)


class DeleteGroup(graphene.relay.ClientIDMutation):
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    class Input:
        id = graphene.String(required=True)

    def mutate_and_get_payload(root, info, **input):
        group = get_object(UserGroup, input.get('id'))
        try:
            group.delete()
            success = True
            return DeleteGroup({success})
        except ValidationError as e:
            return DeleteGroup(errors=e)


class Mutation(graphene.AbstractType):
    create_group = CreateGroup.Field()
    join_group = JoinGroup.Field()
    remove_member = RemoveMember.Field()
    delete_group = DeleteGroup.Field()
