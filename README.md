# Slicer Coding Challenge

## Background

Some imaging modalities, such as a basic x-ray, produce a single two-dimensional image. Other modalities, such as a CT or MRI produce a three-dimensional image. When viewing a three-dimensional images on a screen, radiologists will usually look at one "slice" of the three-dimensional volume at a time.

Most medical images (e.g., x-rays, CTs, MRIs, and ultrasounds) are stored using the DICOM file format. Typically, there is an individual DICOM-file for each "slice" of a 3D image. Thus, an x-ray may have a single DICOM file, while a CT may have 100s of associated DICOM files which collectively store the data for a single 3D image. Often, the set of related DICOM files are stored in a zip archive for convenience, which we will refer to as a "DICOM zip archive".

We assume that you are familiar with Python, Django, NumPy, and basic JavaScript. If you are unfamiliar with any of these technologies, we recommend that you spend some time familiarizing yourself with them before working on this project. The Django tutorial is particularly good. A detailed understanding of the DICOM format should not be required.

## Overview

The goal of this project is to complete a basic web-based medical image viewer. This viewer will allow you to view one slice of a CT or MRI at a time and move between slices of a single 3D volume.

The scaffolding for the image viewer is already in place. You will be filling in a couple of key missing pieces.

We have included code that converts a "DICOM zip archive" into a 3D NumPy array. It then saves this NumPy array, and some meta data, using a Django model. As described in more detail below, you can use the Django admin to save DICOM zip archives in the database.

We have also included a basic web-page that lists the DICOM zip archives present in the database.

## Part I - Save PNGs for Each Slice

In the first part of this exercise, you will add code to the "DICOM zip archive" parser so that, in addition to the NumPy array and meta data, it will also save a PNG file for each slice of the viewer.

Update `ImageSeries`'s custom save method so that it dumps a set of PNGs---one for each axial slice of the data.  (You can assume that the third dimension of the voxel array is the axial dimension.)

## Part II - Add a Slice Viewer Page

In the second part of this exercise, you will be creating a web-page, which will be linked to from the existing list page, an which will allow the user to view individual image slices from the DICOM zip archive.

To do this, create a new Django view and template that displays the set of PNGs you generated.

Ensure that only one PNG is displayed at a time, and include a mechanism that allows the user to quickly step through the stack of images (e.g. a slider), *without requiring a full page reload* to view each new image.

## Setup

You must have python 3 installed.

All of the python requirements are listed in `requirements.txt`.  You can install them using:

    pip install -r requirements.txt

Once you have installed everything, be sure to run the Django migrations, and to create a super user (so you can login to the admin).  You can do this by running:

    python manage.py migrate
    python manage.py createsuperuser

You can start the Django development server, using:

    python manage.py runserver

Once the development server is running you can login to the Django admin by navigating to http://127.0.0.1:8000/admin and logging in as the superuser you just created.

## Upload Test Dataset via the Django Admin

You can download a zip archive with a set of test DICOM files [here](https://github.com/innolitics/example-files/raw/master/example-lung-ct.zip).

You can find many more example DICOM sets online---for example at the [Cancer Imaging Archive](http://www.cancerimagingarchive.net)---but this one data set should be sufficient.

To upload test datasets, login to the Django admin (see above) and then navigate to the image series page and click the "add" button in the top-right corner, and upload the sample zip-archives containing DICOM files.

After uploading the sample dataset in the Django admin, you should see it in the "home" page of the site (e.g. http://127.0.0.1:8000/).  There should be one row for each archive you uploaded.  The "View" link in the table won't do anything yet, but you it will soon!

## Other Details

*As you code, create logical commits with good commit messages.*

To submit your solution, please zip up your entire repository, and email it to `info@innolitics.com`.

If you have any questions about the requirements, ask!  Part of being a good engineer is knowing when to clarify requirements.

## Notes

Really, it would be better to generate the images in a separate task, outside of the request-response cycle.  For example, using a tool like celery.  This added too much complexity for this project.
