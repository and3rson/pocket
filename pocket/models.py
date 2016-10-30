from django.db import models
from django.utils.timezone import now


class Batch(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    date_added = models.DateTimeField(default=now, null=False, blank=False)

    def text_things(self):
        return [thing for thing in self.things.all() if thing.type == 'T']

    def file_things(self):
        return [thing for thing in self.things.all() if thing.type == 'F']

    def image_things(self):
        return [thing for thing in self.things.all() if thing.type == 'I']


class Thing(models.Model):
    TYPES = (
        ('I', 'Image'),
        ('F', 'File'),
        ('T', 'Text')
    )
    name = models.CharField(max_length=128, null=False, blank=False)
    type = models.CharField(max_length=1, choices=TYPES, null=False, blank=False)
    batch = models.ForeignKey('Batch', null=False, blank=False, related_name='things')

    text = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='files', null=True, blank=True)
