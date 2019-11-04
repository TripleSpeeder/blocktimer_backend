import math
from web3 import Web3
from django.conf import settings
from blocktimer.models import Block
import logging

logger = logging.getLogger(__name__)


class BlockImporter:
    def __init__(self):
        self.imported = 0

    def importBlocks(self, startBlock=None, numBlocks=None):

        # web3 connection
        if 'IPC_PROVIDERSTRING' in dir(settings):
            provider = Web3.IPCProvider(settings.IPC_PROVIDERSTRING)
        else:
            provider = Web3.WebsocketProvider(settings.WEBSOCKET_PROVIDERSTRING)
        w3 = Web3(provider)
        if (not w3.isConnected()):
            logger.error('Could not connect web3')
            raise Exception('Could not connect web3')

        # Get latest block as of now
        latestBlock = w3.eth.blockNumber

        # Startblock
        if not startBlock:
            startBlock = Block.objects.last().height + 1

        # Number of blocks
        if not numBlocks:
            numBlocks = latestBlock - startBlock

        # check valid parameters
        endBlock = startBlock + numBlocks

        if endBlock > latestBlock:
            logger.info('Clamping endBlock %d to current latest block %d.' % (endBlock, latestBlock))
            endBlock = latestBlock

        logger.info('Starting import of block %d to %d (%d blocks)' %(startBlock, endBlock, (endBlock-startBlock)))

        batch = []
        batchSize = 1200
        batchCount = 1
        totalBatches = math.ceil((endBlock - startBlock) / batchSize)
        for blockNumber in range(startBlock, endBlock):
            blockdata = w3.eth.getBlock(blockNumber)
            batch.append(Block(height=blockdata.number,
                               hash=blockdata.hash.hex(),
                               timestamp=blockdata.timestamp))
            if len(batch) >= batchSize:
                logger.info('Comitting batch %d of %d with %d blocks' % (batchCount, totalBatches, len(batch)))
                Block.objects.bulk_create(batch)
                self.imported += len(batch)
                batch.clear()
                batchCount += 1

        if len(batch) > 0:
            logger.info('Comitting batch %d of %d with %d blocks' % (batchCount, totalBatches, len(batch)))
            Block.objects.bulk_create(batch)
            self.imported += len(batch)
            batch.clear()

        return
