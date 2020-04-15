from graphene import relay
from graphene_django import DjangoConnectionField, DjangoObjectType
from graphql_jwt.decorators import login_required
from projects.models import Project


class ProjectNode(DjangoObjectType):
    class Meta:
        model = Project
        interfaces = (relay.Node,)

    @classmethod
    @login_required
    def get_queryset(cls, queryset, info):
        return super().get_queryset(queryset, info)

    @classmethod
    @login_required
    def get_node(cls, info, id):
        return super().get_node(info, id)


class Query:
    projects = DjangoConnectionField(ProjectNode)
    project = relay.Node.Field(ProjectNode)
