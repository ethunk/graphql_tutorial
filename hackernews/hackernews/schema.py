import graphene

import links.schema


schema = graphene.Schema(query=Query, mutation=Mutation)


class Query(links.schema.Query, graphene.ObjectType):
    pass


class Mutation(links.schema.Mutation, graphene.ObjectType):
    pass
