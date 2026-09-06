from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views

admin.site.site_header='UNIBEN IEPRTS Administration'
admin.site.site_title='UNIBEN IEPRTS Admin'
admin.site.index_title='Infrastructure & Environmental Reporting and Tracking Administration'

urlpatterns=[
    path('admin/',admin.site.urls),
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('report-problem/',views.problem_log,name='logprob'),
    path('process-problem/',views.process_problem,name='process'),
    path('track-report/',views.track_issue,name='track_issue'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('manage-reports/',views.manage_reports,name='manage_reports'),
    path('manage-reports/<int:pk>/',views.report_detail,name='report_detail'),
    path('api/subcategories/<int:category_id>/',views.subcategories_api,name='subcategories_api'),
    path('api/problem-types/<int:subcategory_id>/',views.problem_types_api,name='problem_types_api'),
    path('login/',views.Login.as_view(),name='login'),
    path('logout/',views.Logout.as_view(),name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
