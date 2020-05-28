from django.conf.urls import url, include

from exam.api.subscriber import ping, subscriber_status, add, substract


api_urlpatterns = [
    url(r'^ping/$', ping),
    url(r'^status/$', subscriber_status),
    url(r'^add/$', add),
    url(r'^substract/$', substract),
]

urlpatterns = [
    url(r'^api/', include(api_urlpatterns))
]
