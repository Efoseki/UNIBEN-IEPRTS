from django.contrib import admin
from .models import Category, Department, Notification, ProblemImage, ProblemReport, ProblemType, Profile, ReportUpdate, SubCategory

class ProblemImageInline(admin.TabularInline):
    model=ProblemImage
    extra=0
class ReportUpdateInline(admin.TabularInline):
    model=ReportUpdate
    extra=0
    readonly_fields=('created_at',)

@admin.register(ProblemReport)
class ProblemReportAdmin(admin.ModelAdmin):
    list_display=('reference','title','category','severity','status','assigned_department','assigned_officer','created_at')
    list_filter=('category','severity','status','assigned_department','created_at')
    search_fields=('reference','title','description','location','building','landmark')
    readonly_fields=('reference','created_at','updated_at')
    inlines=(ProblemImageInline,ReportUpdateInline)
    fieldsets=(('Tracking',{'fields':('reference','status','severity','expected_resolution_date')}),('Problem details',{'fields':('category','subcategory','problem_type','title','description','location','building','landmark','latitude','longitude')}),('Reporter',{'fields':('reporter','anonymous')}),('Assignment and resolution',{'fields':('assigned_department','assigned_officer','resolution_summary')}),('System timestamps',{'fields':('created_at','updated_at')}))

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin): list_display=('code','name','active'); search_fields=('code','name')
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin): list_display=('name','active'); search_fields=('name',)
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin): list_display=('name','category','active'); list_filter=('category','active'); search_fields=('name',)
@admin.register(ProblemType)
class ProblemTypeAdmin(admin.ModelAdmin): list_display=('name','subcategory','active'); search_fields=('name',)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin): list_display=('user','role','department','phone'); list_filter=('role','department')
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin): list_display=('user','title','report','is_read','created_at'); list_filter=('is_read','created_at')
