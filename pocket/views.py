from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
import models
import re


def index(request):
    if request.method == 'POST':
        # print request.GET, request.POST, request.FILES

        name = request.POST.pop('name', None)
        if not name or not name[0]:
            return HttpResponseBadRequest('"name" parameter missing.')
        name = name[0]

        batch = models.Batch(name=name)

        things = []

        for key, value in request.POST.items():
            things.append(models.Thing(
                name=key,
                type='T',
                text=value
            ))

        for key, file in request.FILES.items():
            is_img = bool(re.match(r'.*\.(jpe|jpg|jpeg|gif|png)$', file.name))
            things.append(models.Thing(
                name=key,
                type='I' if is_img else 'F',
                file=file
            ))

        batch.save()

        for thing in things:
            thing.batch = batch
            thing.save()

        return HttpResponse('Done')
    else:
        batches = models.Batch.objects.prefetch_related('things').order_by('-date_added')

        return render(request, 'index.html', dict(batches=batches))
