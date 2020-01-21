from django.conf import settings
from django.http import HttpResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from helusers.admin_site import admin
from secure_graphene.depth import DepthAnalysisBackend

from kukkuu.views import SentryGraphQLView

gql_backend = DepthAnalysisBackend(
    max_depth=settings.KUKKUU_QUERY_MAX_DEPTH, execute_params={"executor": None}
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "graphql",
        csrf_exempt(
            SentryGraphQLView.as_view(graphiql=settings.DEBUG, backend=gql_backend)
        ),
    ),
]


#
# Kubernetes liveness & readiness probes
#
def healthz(*args, **kwargs):
    return HttpResponse(status=200)


def readiness(*args, **kwargs):
    return HttpResponse(status=200)


urlpatterns += [path("healthz", healthz), path("readiness", readiness)]
