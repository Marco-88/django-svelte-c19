from base64 import b64decode

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from graphql_relay.node.node import from_global_id

from user_groups.models import UserGroup
from profiles.models import Profile


def get_object(object_name, relayId, otherwise=None):
    try:
        return object_name.objects.get(pk=from_global_id(relayId)[1])
    except:
        return otherwise


def get_pk_from_node_id(node_id: str):
    """Gets pk from node_id"""
    model_with_pk = b64decode(node_id).decode('utf-8')
    model_name, pk = model_with_pk.split(":")
    return pk


def create_update(instance, args, exception=['id']):
    if instance:
        [setattr(instance, key, value) for key, value in args.items() if key not in exception]
    if type(instance) == User:
        instance.set_password(args['password'])
    if type(instance) == UserGroup:
        for user in args['users']:
            instance.users.add(user)
    instance.save()
    return instance


def delete(model, mutation, id):
    instance = get_object(model, id)
    try:
        instance.delete()
        success = True
        return mutation({success})
    except ValidationError as e:
        return mutation(errors=e)