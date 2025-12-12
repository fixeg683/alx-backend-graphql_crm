from django.http import HttpResponse
from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return HttpResponse("<h2>GraphQL CRM API</h2><p>Visit <a href='/graphql'>/graphql</a></p>")

urlpatterns = [
    path("", home),  # 👈 add this line
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
