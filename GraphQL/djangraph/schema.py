import graphene
import graphql_jwt

import posts.schema
import comments.schema
import users.schema
import profiles.schema
import user_groups.schema
import search.schema
import votes.schema


class Query(posts.schema.Query,
            comments.schema.Query,
            users.schema.Query,
            profiles.schema.Query,
            user_groups.schema.Query,
            search.schema.Query,
            votes.schema.Query,
            graphene.ObjectType):
    pass


class Mutation(posts.schema.Mutation,
               comments.schema.Mutation,
               users.schema.Mutation,
               profiles.schema.Mutation,
               user_groups.schema.Mutation,
               votes.schema.Mutation,
               graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
