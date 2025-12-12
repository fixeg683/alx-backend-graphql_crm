import graphene
from graphene_django.types import DjangoObjectType
from .models import Customer   # Or your actual model

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ("id", "name", "email")  # adjust to your fields

class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)

    def resolve_all_customers(root, info):
        return Customer.objects.all()

class Mutation(graphene.ObjectType):
    pass
