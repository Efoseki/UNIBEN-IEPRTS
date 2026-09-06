from django.conf import settings
from django.db import models
from django.utils import timezone
import uuid

STATUS_CHOICES=[('submitted','Submitted'),('review','Under Review'),('assigned','Assigned'),('progress','In Progress'),('resolved','Resolved'),('closed','Closed'),('rejected','Rejected')]
SEVERITY_CHOICES=[('low','Low'),('medium','Medium'),('high','High'),('critical','Critical')]

class Department(models.Model):
    name=models.CharField(max_length=150,unique=True)
    code=models.CharField(max_length=20,unique=True)
    active=models.BooleanField(default=True)
    def __str__(self): return f'{self.code} - {self.name}'

class Profile(models.Model):
    ROLE_CHOICES=[('student','Student'),('staff','Staff'),('officer','Department Officer'),('management','Management'),('admin','Administrator')]
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='profile')
    role=models.CharField(max_length=20,choices=ROLE_CHOICES,default='student')
    department=models.ForeignKey(Department,null=True,blank=True,on_delete=models.SET_NULL,related_name='profiles')
    phone=models.CharField(max_length=30,blank=True)
    def __str__(self): return self.user.get_full_name() or self.user.username

class Category(models.Model):
    name=models.CharField(max_length=80,unique=True)
    description=models.TextField(blank=True)
    active=models.BooleanField(default=True)
    class Meta: verbose_name_plural='Categories'
    def __str__(self): return self.name

class SubCategory(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='subcategories')
    name=models.CharField(max_length=120)
    active=models.BooleanField(default=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=['category','name'],name='unique_subcategory')]
        verbose_name_plural='Sub-categories'
    def __str__(self): return f'{self.category} - {self.name}'

class ProblemType(models.Model):
    subcategory=models.ForeignKey(SubCategory,on_delete=models.CASCADE,related_name='problem_types')
    name=models.CharField(max_length=150)
    active=models.BooleanField(default=True)
    class Meta: constraints=[models.UniqueConstraint(fields=['subcategory','name'],name='unique_problem_type')]
    def __str__(self): return self.name

class ProblemReport(models.Model):
    STATUS=STATUS_CHOICES
    SEVERITY=SEVERITY_CHOICES
    reference=models.CharField(max_length=50,unique=True,editable=False)
    reporter=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,related_name='problem_reports')
    anonymous=models.BooleanField(default=False)
    category=models.ForeignKey(Category,on_delete=models.PROTECT)
    subcategory=models.ForeignKey(SubCategory,on_delete=models.PROTECT)
    problem_type=models.ForeignKey(ProblemType,on_delete=models.PROTECT,null=True,blank=True)
    title=models.CharField(max_length=200)
    description=models.TextField()
    location=models.CharField(max_length=200)
    building=models.CharField(max_length=200,blank=True)
    landmark=models.CharField(max_length=200,blank=True)
    severity=models.CharField(max_length=20,choices=SEVERITY_CHOICES,default='medium')
    latitude=models.DecimalField(max_digits=9,decimal_places=6,null=True,blank=True)
    longitude=models.DecimalField(max_digits=9,decimal_places=6,null=True,blank=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='submitted')
    assigned_department=models.ForeignKey(Department,null=True,blank=True,on_delete=models.SET_NULL,related_name='assigned_reports')
    assigned_officer=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,related_name='assigned_problem_reports')
    expected_resolution_date=models.DateField(null=True,blank=True)
    resolution_summary=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['-created_at']
    def save(self,*args,**kwargs):
        if not self.reference:
            self.reference=f'UNIBEN-IEPRTS-{timezone.now():%Y%m%d}-{uuid.uuid4().hex[:6].upper()}'
        super().save(*args,**kwargs)
    def __str__(self): return self.reference

class ProblemImage(models.Model):
    report=models.ForeignKey(ProblemReport,on_delete=models.CASCADE,related_name='images')
    image=models.ImageField(upload_to='problem_reports/%Y/%m/')
    caption=models.CharField(max_length=200,blank=True)
    uploaded_at=models.DateTimeField(auto_now_add=True)

class ReportUpdate(models.Model):
    report=models.ForeignKey(ProblemReport,on_delete=models.CASCADE,related_name='updates')
    author=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.SET_NULL)
    old_status=models.CharField(max_length=20,choices=STATUS_CHOICES,blank=True)
    new_status=models.CharField(max_length=20,choices=STATUS_CHOICES,blank=True)
    note=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['created_at']

class Notification(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='notifications')
    report=models.ForeignKey(ProblemReport,null=True,blank=True,on_delete=models.CASCADE)
    title=models.CharField(max_length=180)
    message=models.TextField()
    is_read=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']
