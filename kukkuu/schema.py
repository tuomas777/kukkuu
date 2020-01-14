import graphene

import children.schema
import users.schema


class Query(children.schema.Query, users.schema.Query, graphene.ObjectType):
    pass


class Mutation(children.schema.Mutation, users.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
