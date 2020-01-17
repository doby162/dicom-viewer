import zipfile
from contextlib import contextmanager
import png
from functools import reduce
import os
from multiprocessing import Pool

import numpy as np
from django.db import models
from django.core.files.base import ContentFile

from slicer.dicom_import import dicom_datasets_from_zip, combine_slices


class ImageSeries(models.Model):
    dicom_archive = models.FileField(upload_to="dicom/")
    voxel_file = models.FileField(upload_to="voxels/")
    image_folder = models.CharField(max_length=16)
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

        self.image_folder = str(self.voxel_file).split("_")[-1]
        if "/" in self.image_folder:
            self.image_folder = "default"

        super().save(*args, **kwargs)

        image_dump_folder = "media/image_dumps/" + self.image_folder
        if not os.path.isdir(image_dump_folder):
            try:
                os.makedirs(image_dump_folder)
            except OSError:
                pass

        with cd(image_dump_folder):
            p = Pool(5)
            vectorized_process_voxels = np.vectorize(self.process_voxels)
            self.voxel_sheets = vectorized_process_voxels(self.voxels)
            list(p.map(self.process_image, range(len(self.voxel_sheets))))

    class Meta:
        verbose_name_plural = 'Image Series'

    def process_voxels(self, voxel):
        # coerce the input data to a format that agrees with pypng
        return min(2047, int(abs(voxel)))

    def process_image(self, image_num):
        sheet = self.voxel_sheets[image_num]
        f = open(str(image_num).zfill(3) + '.png', 'wb')
        w = png.Writer(len(sheet[0]), len(sheet), bitdepth=11)
        w.write(f, sheet.tolist())
        f.close()

#TODO: make a file for helper funcs
@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)
