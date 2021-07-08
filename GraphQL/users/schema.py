import django_filters
import graphene
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from graphene import InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError

from djangraph.api_utils import create_update, get_object
from profiles.models import Profile
from profiles.schema import ProfileNode


class UserNode(DjangoObjectType):
    profile = graphene.relay.node.Field(ProfileNode)

    class Meta:
        model = User
        interfaces = (graphene.relay.Node, )


class UserInput(InputObjectType):
    username = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = User
        fields = {
            'username': ['exact', 'icontains'],
            'email': ['exact'],
        }


class Query(graphene.ObjectType):
    get_viewer = graphene.Field(UserNode)
    get_user   = graphene.relay.Node.Field(UserNode)
    get_users  = DjangoFilterConnectionField(UserNode, filterset_class=UserFilter)

    def resolve_get_viewer(self, info, **kwargs):
        if info.context.user.is_authenticated:
            print()
            print(info.context.user)
            print()
            return info.context.user


class Register(graphene.relay.ClientIDMutation):

    class Input:
        data = graphene.Field(UserInput)

    user = graphene.Field(UserNode)

    def mutate_and_get_payload(root, info, **input):
        user_data = input.get('data')
        user = User()
        new_user = create_update(user, user_data)
        profile = Profile.objects.get_or_create(user=new_user)[0]
        new_user.profile = profile
        return Register(user=new_user)


class AddFriend(graphene.relay.ClientIDMutation):
    class Input:
        friend_id = graphene.String(required=True)

    errors = graphene.List(graphene.String)
    friend = graphene.Field(UserNode)

    def mutate_and_get_payload(root, info, **input):
        try:
            new_friend = get_object(User, input.get('friend_id'))
            profile_instance = info.context.user.profile

            if new_friend in profile_instance.friends.all():
                raise GraphQLError('You are already friends!')

            profile_instance.friends.add(new_friend)
            profile_instance.save()

            return AddFriend(friend=new_friend)
        except ValidationError as e:
            return AddFriend(friend=None, errors=e)


class RemoveFriend(graphene.relay.ClientIDMutation):
    class Input:
        friend_id = graphene.String(required=True)

    errors = graphene.List(graphene.String)
    friend = graphene.Field(UserNode)

    def mutate_and_get_payload(root, info, **input):
        try:
            old_friend = get_object(User, input.get('friend_id'))
            profile_instance = info.context.user.profile

            if old_friend not in profile_instance.friends.all():
                raise GraphQLError('You are not friends!')

            profile_instance.friends.remove(old_friend)
            profile_instance.save()

            return RemoveFriend(friend=old_friend)
        except ValidationError as e:
            return RemoveFriend(friend=None, errors=e)


class Mutation(graphene.AbstractType):
    register = Register.Field()
    add_friend = AddFriend.Field()
    remove_friend = RemoveFriend.Field()
