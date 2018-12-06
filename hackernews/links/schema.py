import graphene
from graphene_django import DjangoObjectType

from .models import Link


class LinkType(DjangoObjectType):
    class Meta:
        model = Link


class Query(graphene.ObjectType):
    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        return(Link.objects.all())


class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()

    class Arguments:
        url = graphene.String()  # Data sent by the user/frontend to the server
        description = graphene.String()  # Data sent by the user/frontend to the server

    def mutate(self, info, url, description):
        # Creates a new link object/record in the database using the params passed from the frontend to the server
        link = Link(url=url, description=description)
        link.save()

        return CreateLink(  # Returns an object/class with data back to the frontend
            id=link.id,
            url=link.url,
            description=link.description,
        )


class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
