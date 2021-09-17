from django.urls import path

from . import views

app_name = "dsrs"

'''FROM CARLOS: This list contains the handler to manage the 'resources/percentile' request.
It also contains a handler to manage a request to 'resources/upload-dsrs', which presents the 
user a form to select the data that the user would want to store into the DB.'''

urlpatterns = [
    path('upload-dsrs/',                        views.UploadDsrFilesForm.as_view(), name='upload-dsrs'),
    path('upload-dsrs/success/',                views.success,                      name='success'),
    path('percentile/<int:percentile_value>/',  views.percentile,                   name='percentile'),
]