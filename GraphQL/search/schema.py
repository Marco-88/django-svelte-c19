import graphene
from django.contrib.auth.models import User
from django.db.models import Q
from graphql import GraphQLError
from user_groups.models import UserGroup
from user_groups.schema import GroupNode
from posts.models import Post
from posts.schema import PostNode
from users.schema import UserNode


class SearchResult(graphene.Union):
    class Meta:
        types = [PostNode, UserNode, GroupNode]


class Query(graphene.ObjectType):
    search = graphene.List(SearchResult, text=graphene.String(), types=graphene.List(graphene.String), first=graphene.Int())

    def resolve_search(self, info, **kwargs):
        text = kwargs.get('text')
        if text:
            types = kwargs.get('types')
            first = kwargs.get('first')
            items = []
            for type in types:
                if ('User' == type):
                    users = User.objects.filter(username__icontains=text).order_by('username')[:first - len(items)]
                    for user in users:
                        items.append(user)
                elif ('Group' == type):
                    groups = UserGroup.objects.filter(name__icontains=text).order_by('name')[:first - len(items)]
                    for group in groups:
                        items.append(group)
                elif ('Post' == type):
                    posts = Post.objects.filter(Q(title__icontains=text) | Q(body__icontains=text)).order_by('-updated_at')[:first - len(items)]
                    for post in posts:
                        items.append(post)
            return items
        raise GraphQLError('No text to search for')