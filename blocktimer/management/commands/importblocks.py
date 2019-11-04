from django.core.management.base import BaseCommand
from blocktimer.utils.BlockImporter import BlockImporter
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Imports blocks into the database'

    def add_arguments(self, parser):
        parser.add_argument('-f','--from', help="first block to import. Defaults to 'last imported block + 1'", type=int)
        parser.add_argument('-n', '--num', help="how many blocks to import. Defaults to all missing blocks", type=int)

    def handle(self, *args, **options):
        blockImporter = BlockImporter()
        blockImporter.importBlocks(startBlock=options['from'], numBlocks=options['num'])
        return
