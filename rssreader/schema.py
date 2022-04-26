import graphene
import rss.schema 

class Query(rss.schema.Query, graphene.ObjectType):
    pass

class Mutation(rss.schema.Mutation, graphene.ObjectType):
    pass
   
schema = graphene.Schema(query = Query, mutation=Mutation)

