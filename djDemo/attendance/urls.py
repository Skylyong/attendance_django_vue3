from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls import url

from attendance import views, sqlOperate


router = DefaultRouter()
# router.register('attendance', views.AttendanceViewSet)
# router.register('seeData', views.seeData)

urlpatterns = [
    # path('', include(router.urls)),
    url(r'^login/$', views.login),
    url(r'^submitApplication/$', views.submitApplication),
    url(r'^getApplicationHistory/$', views.getApplicationHistory),
    url(r'^getWorkerAccountMessage/$', views.getWorkerAccountMessage),
    url(r'^delApplication/$', views.delApplication),
    url(r'^approvalApplication/$', views.approvalApplication),
    url(r'^getPoolData/$', views.getPoolData),
    # url('^get_no_approve_history_count/$', views.get_no_approve_history_count)
    url(r'^getUserPoolData/$', views.getUserPoolData),
    url(r'^getOverTimeData/$', views.getOverTimeData),
    url(r'^getOverTimeUserData/$', views.getOverTimeUserData),
    url(r'^resetPwd/$', views.resetPwd),
]
