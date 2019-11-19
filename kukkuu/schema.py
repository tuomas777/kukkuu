import graphene

import children.schema
import users.schema


class Query(children.schema.Query, users.schema.Query, graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    submit_children_and_guardian = (
        children.schema.SubmitChildrenAndGuardianMutation.Field()
    )


schema = graphene.Schema(query=Query, mutation=Mutation)
