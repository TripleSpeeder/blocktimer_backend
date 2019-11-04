from django.http import HttpResponse
from django.shortcuts import render
from blocktimer.utils.BlockImporter import BlockImporter

def import_blocks(request):
    blockImporter = BlockImporter()
    blockImporter.importBlocks()
    message = "Imported %d blocks." % (blockImporter.imported)
    return HttpResponse(message, status=201)
