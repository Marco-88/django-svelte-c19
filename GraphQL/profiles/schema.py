import django_filters
import graphene
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from graphene import InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_file_upload.scalars import Upload

from djangraph.api_utils import get_object, create_update
from djangraph.constants import GENRES
from users.models import Profile


class ProfileNode(DjangoObjectType):
    genres = graphene.List(graphene.String)

    class Meta:
        model = Profile
        interfaces = (graphene.relay.Node,)

    def resolve_image(self, info):
        if self.image:
            return info.context.build_absolute_uri(self.image.url)
        return None


class ProfileInput(InputObjectType):
    description = graphene.String()
    genres = graphene.List(graphene.String)
    dark = graphene.Boolean(default=True)
    birthdate = graphene.types.datetime.Date()
    image = Upload()


class ProfileFilter(django_filters.FilterSet):
    class Meta:
        model = Profile
        fields = ['genres', 'user']


class Query(graphene.ObjectType):
    get_profile = graphene.relay.Node.Field(ProfileNode)
    get_profiles = DjangoFilterConnectionField(ProfileNode, filterset_class=ProfileFilter)


class UpdateProfile(graphene.relay.ClientIDMutation):
    class Input:
        data = graphene.Argument(ProfileInput)
        user_id = graphene.String(required=True)

    errors = graphene.List(graphene.String)
    profile = graphene.Field(ProfileNode)

    def mutate_and_get_payload(root, info, **input):
        try:
            user = get_object(User, input.get('user_id'))
            profile_data = input.get('data')
            profile_instance = user.profile
            print(profile_data.__dict__)
            if profile_instance:
                exception = ['id']
                if not profile_data['image']:
                    exception.append('image')
                profile = create_update(profile_instance, profile_data, exception)
                return UpdateProfile(profile=profile)
        except ValidationError as e:
            return UpdateProfile(profile=None, errors=e)


class Mutation(graphene.AbstractType):
    update_profile = UpdateProfile.Field()
