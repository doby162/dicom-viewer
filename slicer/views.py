from django.shortcuts import render

from .models import ImageSeries


def image_series_list(request):
    return render(request, 'image_series_list.html', {
        'all_image_series': ImageSeries.objects.all(),
    })

def image_viewer(request):
    id = str(request).split("/")[-1]
    id = id.split("'")[0]
    return render(request, 'image_viewer.html', {
        #folder name for specific series
        "id":id,
    })
