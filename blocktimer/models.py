from datetime import datetime
from django.db import models
from django.db.models import F, Func

class BlockManager(models.Manager):
    def from_timestamp(self, timestamp):
        # first try exact match.
        try:
            return Block.objects.get(timestamp=timestamp)
        except Block.DoesNotExist:
            # Need to find the block with timestamp closest to provided value
            # define searchrange. Add 4 minutes in both directions, should produce plenty results
            searchRange = range(timestamp - 240, timestamp + 240)
            # Django magic:
            #   - get all blocks which timestamp is within searchrange
            #   - annotate blocks with the absolute timedelta to the requested timestamp
            #   - order results by the annotated delta value (ascending)
            #   - Return first result (which is the block with the smallest delta)
            block = Block.objects.filter(timestamp__range=(searchRange.start, searchRange.stop))\
                .annotate(delta=Func((F('timestamp') - timestamp), function='ABS'))\
                .order_by('delta')\
                .first()
            if block == None:
                raise Block.DoesNotExist
            else:
                return block


class Block(models.Model):
    height = models.PositiveIntegerField(primary_key=True)
    timestamp = models.PositiveIntegerField(blank=False, unique=True, db_index=True)
    hash = models.CharField(blank=False, unique=True, max_length=66)
    objects = BlockManager()

    def __str__(self):
        return '#%d, mined: %s UTC (timestamp: %d)' %(self.height, self.datetime, self.timestamp)

    @property
    def datetime(self):
        return datetime.fromtimestamp(self.timestamp)
