import graphene
import languages.schema
import projects.schema

import children.schema
import events.schema
import users.schema
import venues.schema


class Mutation(
    children.schema.Mutation,
    users.schema.Mutation,
    events.schema.Mutation,
    venues.schema.Mutation,
    graphene.ObjectType,
):
    pass


class Query(
    children.schema.Query,
    users.schema.Query,
    projects.schema.Query,
    events.schema.Query,
    venues.schema.Query,
    languages.schema.Query,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
