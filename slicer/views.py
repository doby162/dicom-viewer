from django.shortcuts import render
import os
from .models import ImageSeries


def image_series_list(request):
    image_series_array = []
    for image_series in ImageSeries.objects.all():
        image_folder = str(image_series.voxel_file).split("_")[-1]
        # TODO replace this logic duplication from the save function
        # by adding a field to the model
        image_series.image_folder = image_folder
        image_series_array.append(image_series)

    return render(request, 'image_series_list.html', {
        'all_image_series': image_series_array,
    })

def image_viewer(request):
    id = str(request).split("/")[-1]
    id = id.split("'")[0]

    images = os.listdir("media/image_dumps/" + id)

    return render(request, 'image_viewer.html', {
        #folder name for specific series
        "folder":id,
        "images":images,
    })
