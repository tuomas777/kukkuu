import graphene
from django.apps import apps
from graphene import relay
from graphene_django import DjangoConnectionField, DjangoObjectType
from languages.models import Language

LanguageTranslation = apps.get_model("languages", "LanguageTranslation")


class LanguageTranslationType(DjangoObjectType):
    class Meta:
        model = LanguageTranslation
        exclude = ("id", "master")


class LanguageNode(DjangoObjectType):
    name = graphene.String()

    class Meta:
        model = Language
        interfaces = (relay.Node,)
        fields = ("alpha_3_code", "name", "translations")

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.prefetch_related("translations")


class Query:
    language = relay.Node.Field(LanguageNode)
    languages = DjangoConnectionField(LanguageNode)
