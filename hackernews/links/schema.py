import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from django.db.models import Q

from .models import Link, Vote
from users.schema import UserType


class LinkType(DjangoObjectType):
    class Meta:
        model = Link


class VoteType(DjangoObjectType):
    class Meta:
        model = Vote


class Query(graphene.ObjectType):
    # Add the search parameter inside our links field
    links = graphene.List(LinkType, search=graphene.String())
    votes = graphene.List(VoteType)

    # Change the resolver
    def resolve_links(self, info, search=None, **kwargs):
        # The value sent with the search parameter will be in the args variable
        if search:
            filter = (
                Q(url__icontains=search) |
                Q(description__icontains=search)
            )
            return Link.objects.filter(filter)

        return Link.objects.all()

    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()


class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()
    posted_by = graphene.Field(UserType)

    class Arguments:
        url = graphene.String()  # Data sent by the user/frontend to the server
        description = graphene.String()  # Data sent by the user/frontend to the server

    def mutate(self, info, url, description):
        # Creates a new link object/record in the database using the params passed from the frontend to the server
        user = info.context.user or None
        link = Link(
            url=url,
            description=description,
            posted_by=user,
        )
        link.save()

        return CreateLink(  # Returns an object/class with data back to the frontend
            id=link.id,
            url=link.url,
            description=link.description,
            posted_by=link.posted_by,
        )


class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    link = graphene.Field(LinkType)

    class Arguments:
        link_id = graphene.Int()

    def mutate(self, info, link_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged to vote!')

        link = Link.objects.filter(id=link_id).first()
        if not link:
            raise Exception('Invalid Link!')

        Vote.objects.create(
            user=user,
            link=link,
        )

        return CreateVote(user=user, link=link)


class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    create_vote = CreateVote.Field()
