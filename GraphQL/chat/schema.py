import graphene
import django_filters
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from graphene import InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from chat.models import Message, Chat
from djangraph.api_utils import create_update, get_object, delete
from users.schema import UserNode


class MessageFilter(django_filters.FilterSet):
    class Meta:
        model = Message
        fields = ['user', 'body', 'created_at', 'updated_at']

    order_by = django_filters.OrderingFilter(
        fields=(
            ('updated_at', 'updated_at'),
            ('-updated_at', '-updated_at'),
            ('created_at', 'created_at'),
            ('-created_at', '-created_at'),
        )
    )


class MessageNode(DjangoObjectType):

    class Meta:
        model = Chat
        interfaces = (graphene.relay.Node, )


class MessageInput(InputObjectType):

    user = graphene.Field(UserNode, required=True)
    body = graphene.String(required=True)


class ChatFilter(django_filters.FilterSet):
    class Meta:
        model = Chat


class ChatNode(DjangoObjectType):

    class Meta:
        model = Chat
        interfaces = (graphene.relay.Node, )


class ChatInput(InputObjectType):
    title = graphene.String(required=True)
    users = graphene.List(graphene.Field(UserNode), required=True)


class Query(graphene.ObjectType):
    get_message = graphene.relay.Node.Field(MessageNode)
    get_messages = DjangoFilterConnectionField(MessageNode, filterset_class=MessageFilter)
    get_chat = graphene.relay.Node.Field(ChatNode)
    get_chats = DjangoFilterConnectionField(ChatNode, filterset_class=ChatFilter)


class CreateMessage(graphene.relay.ClientIDMutation):

    class Input:
        data = graphene.Argument(MessageInput)

    message = graphene.Field(MessageNode)
    error = graphene.List(graphene.String)

    def mutate_and_get_payload(root, info, **input):
        message_data = input.get('data')
        message = Message()
        new_message = create_update(message, message_data)
        return CreateMessage(message=new_message)


class DeleteMessage(graphene.relay.ClientIDMutation):
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    class Input:
        id = graphene.String(required=True)

    def mutate_and_get_payload(root, info, **input):
        return delete(Message, DeleteMessage, input.get('id'))


class CreateChat(graphene.relay.ClientIDMutation):

    class Input:
        data = graphene.Argument(ChatInput)

    chat = graphene.Field(ChatNode)
    error = graphene.List(graphene.String)

    def mutate_and_get_payload(root, info, **input):
        chat_data = input.get('data')
        chat = Chat()
        new_chat = create_update(chat, chat_data)
        return CreateChat(chat=new_chat)


class DeleteChat(graphene.relay.ClientIDMutation):
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    class Input:
        id = graphene.String(required=True)

    def mutate_and_get_payload(root, info, **input):
        return delete(Chat, DeleteChat, input.get('id'))
        # chat = get_object(Chat, input.get('id'))
        # try:
        #     chat.delete()
        #     success = True
        #     return DeleteChat({success})
        # except ValidationError as e:
        #     return DeleteChat(errors=e)


class Mutation(graphene.AbstractType):
    create_message = CreateChat.Field()
    delete_message = DeleteChat.Field()
    create_chat = CreateChat.Field()
    delete_chat = DeleteChat.Field()
