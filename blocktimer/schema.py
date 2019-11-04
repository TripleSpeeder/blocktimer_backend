import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from graphql import GraphQLError

from blocktimer.models import Block

class BlockType(DjangoObjectType):
    class Meta:
        model = Block


class Query(ObjectType):
    block = graphene.Field(BlockType,
                           timestamp=graphene.Int(),
                           height=graphene.Int())

    def resolve_block(self, info, **kwargs):
        timestamp = kwargs.get('timestamp')
        height = kwargs.get('height')

        if timestamp is not None:
            try:
                return Block.objects.from_timestamp(timestamp)
            except Block.DoesNotExist:
                raise GraphQLError('No block found around timestamp %d' % timestamp)

        if height is not None:
            try:
                return Block.objects.get(height=height)
            except Block.DoesNotExist:
                raise GraphQLError('No block found with height %d' % height)

        raise GraphQLError('No timestamp or height provided')

    # To get a list of all blocks:
    # blocks = graphene.List(BlockType)
    # def resolve_blocks(self, info, **kwargs):
    #     return Block.objects.all()


schema = graphene.Schema(query=Query)