from django.urls import path
from graphene_django.views import GraphQLView
from helusers.admin_site import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql", GraphQLView.as_view(graphiql=True)),
]
