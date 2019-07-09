from django.conf.urls import url
from media import views
urlpatterns = [
    url(r'^$',views.index),
    url(r'^get_program_info/$',views.get_program_info),
    url(r'^get_segment_info/$',views.get_segment_info),
    url(r'^edit_segment_description/$',views.edit_segment_description),
    url(r'^get_page_program/$',views.get_page_program),
    url(r'^edit_program_subtitle/$',views.edit_program_subtitle),
    url(r'^main/$',views.main),
    url(r'^get_series_by_type/$', views.get_series_by_type),
    url(r'^main_search/$', views.main_search),
    url(r'^profile_index/$', views.profile_index),
    url(r'^upload_files/$', views.upload_files),
    url(r'^edit_series_info/$', views.edit_series_info),
]
