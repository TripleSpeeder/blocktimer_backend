from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from blocktimer.models import Block
from web3.auto import w3

class Command(BaseCommand):
    help = 'Imports blocks into the database'

    def add_arguments(self, parser):
        parser.add_argument('-f','--from', help='first block to import', type=int, required=True)
        parser.add_argument('-t', '--to', help='last block to import', type=int, required=True)

    def handle(self, *args, **options):
        startBlock = options['from']
        endBlock = options['to']

        # check web3 connection
        if (not w3.isConnected()):
            raise CommandError('Could not connect web3')

        # check valid parameters
        if endBlock < startBlock:
            raise CommandError('Negative block range provided')

        latestBlock = w3.eth.blockNumber
        if endBlock > latestBlock:
            raise CommandError('Requested block %d higher than current latest block %d' % (endBlock, latestBlock))

        self.stdout.write('Starting import of block %d to %d' %(options['from'], options['to']))

        for blockNumber in range(startBlock, endBlock+1):
            blockdata = w3.eth.getBlock(blockNumber)
            height = blockdata.number
            hash = blockdata.hash.hex()
            timestamp = blockdata.timestamp
            # self.stdout.write('Block %d (%r) from %d' % (height, hash, timestamp))
            try:
                Block.objects.create(height=height, timestamp=timestamp, hash=hash)
            except IntegrityError as e:
                self.stdout.write(self.style.WARNING('Block %d already exsting!' % height))


