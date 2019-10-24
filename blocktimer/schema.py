import graphene
from django.db.models import F, Func
from graphene_django.types import DjangoObjectType, ObjectType
from blocktimer.models import Block

class BlockType(DjangoObjectType):
    class Meta:
        model = Block


class Query(ObjectType):
    block = graphene.Field(BlockType, timestamp=graphene.Int())

    def resolve_block(self, info, **kwargs):
        timestamp = kwargs.get('timestamp')

        if timestamp is not None:
            return Block.objects.from_timestamp(timestamp)
        return None

    # To get a list of all blocks:
    # blocks = graphene.List(BlockType)
    # def resolve_blocks(self, info, **kwargs):
    #     return Block.objects.all()


schema = graphene.Schema(query=Query)