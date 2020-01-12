import zipfile
import png
from functools import reduce

import numpy as np
from django.db import models
from django.core.files.base import ContentFile

from slicer.dicom_import import dicom_datasets_from_zip, combine_slices


class ImageSeries(models.Model):
    dicom_archive = models.FileField(upload_to="dicom/")
    voxel_file = models.FileField(upload_to="voxels/")
    patient_id = models.CharField(max_length=64, null=True)
    study_uid = models.CharField(max_length=64)
    series_uid = models.CharField(max_length=64)

    @property
    def voxels(self):
        with self.voxel_file as f:
            voxel_array = np.load(f)
        return voxel_array

    def save(self, *args, **kwargs):
        with zipfile.ZipFile(self.dicom_archive, 'r') as f:
            dicom_datasets = dicom_datasets_from_zip(f)

        voxels, _ = combine_slices(dicom_datasets)
        content_file = ContentFile(b'')  # empty zero byte file
        np.save(content_file, voxels)
        self.voxel_file.save(name='voxels', content=content_file, save=False)
        self.patient_id = dicom_datasets[0].PatientID
        self.study_uid = dicom_datasets[0].StudyInstanceUID
        self.series_uid = dicom_datasets[0].SeriesInstanceUID
        super(ImageSeries, self).save(*args, **kwargs)

        image_num = 0
        for voxel_sheet in self.voxels:
            image_num += 1
            processed_voxels = self.process_voxel_sheet(voxel_sheet)
            f = open('test' + str(image_num) + '.png', 'wb')
            w = png.Writer(len(processed_voxels[0]), len(processed_voxels), bitdepth=8)
            w.write(f, processed_voxels)
            f.close()

    class Meta:
        verbose_name_plural = 'Image Series'

    def process_voxel_sheet(self, voxel_sheet):
        # coerce the input data to a format that agrees with pypng
        # TODO: this data has to be heavily compressed to fit in bytes for
        # pypng. Investigate the possibility that it doesn't have to be.
        inverted = []
        for voxels in voxel_sheet:
            new_voxel = []
            for datum in voxels:
                datum = datum / 8
                datum = abs(datum)
                datum = int(datum)
                datum = min(255, datum)
                new_voxel.append(datum)
            inverted.append(new_voxel)
        return inverted
