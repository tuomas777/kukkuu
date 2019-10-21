import graphene

import children.schema


class Query(graphene.ObjectType):
    # at least one query field is required by GraphQL spec
    dummy = graphene.Boolean()


class Mutation(graphene.ObjectType):
    submit_child = children.schema.SubmitChildMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
