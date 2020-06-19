from django.db import models
from uuid import uuid4
import os
from . import settings
CHUNKUPLOADPATH = settings.CHUNKUPLOADPATH

def get_file_path(instance, filename):
    #ext = filename.split('.')[-1]
    #filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(CHUNKUPLOADPATH, instance.uploadid + '.part')

class fileupload(models.Model):
    thefile = models.FileField(upload_to=get_file_path)
    uploadid = models.CharField(max_length=255, unique=True)
    filename = models.CharField(max_length=255, blank=True)
    uploadat = models.DateField(auto_now_add=True)

    def __str__(self):
        return 'fileUploadModel'
