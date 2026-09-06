from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from management_utils.models import Category, Department, Notification, ProblemImage, ProblemReport, ProblemType, Profile, ReportUpdate, SubCategory

class Login(LoginView):
    template_name='users/login.html'
    redirect_authenticated_user=True

class Logout(LogoutView):
    next_page='/'


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form=UserCreationForm(request.POST or None)
    for field in form.fields.values():
        field.widget.attrs['class']='form-control'
    if request.method=='POST' and form.is_valid():
        user=form.save()
        Profile.objects.get_or_create(user=user,defaults={'role':'student'})
        login(request,user)
        messages.success(request,'Your account has been created. You can now submit and track reports.')
        return redirect('dashboard')
    return render(request,'users/register.html',{'form':form})


def _manager(user):
    if not user.is_authenticated:
        return False
    if user.is_staff or user.is_superuser:
        return True
    try:
        return user.profile.role in {'officer','management','admin'}
    except Profile.DoesNotExist:
        return False


def home(request):
    stats=ProblemReport.objects.values('status').annotate(total=Count('id'))
    counts={x['status']:x['total'] for x in stats}
    progress=counts.get('progress',0)+counts.get('assigned',0)+counts.get('review',0)
    return render(request,'index.html',{'total':sum(counts.values()),'resolved':counts.get('resolved',0)+counts.get('closed',0),'progress':progress})

# @login_required
def problem_log(request):
    cats=Category.objects.filter(active=True).order_by('name')
    return render(request,'problem_log.html',{'categories':cats})

@login_required
def process_problem(request):
    if request.method!='POST':
        return redirect('logprob')
    category=get_object_or_404(Category,pk=request.POST.get('category'),active=True)
    sub=get_object_or_404(SubCategory,pk=request.POST.get('subcategory'),category=category,active=True)
    ptype=None
    if request.POST.get('problem_type'):
        ptype=get_object_or_404(ProblemType,pk=request.POST['problem_type'],subcategory=sub,active=True)
    report=ProblemReport.objects.create(
        reporter=request.user,
        anonymous=request.POST.get('anonymous')=='on',
        category=category,subcategory=sub,problem_type=ptype,
        title=request.POST.get('title','').strip(),description=request.POST.get('description','').strip(),
        location=request.POST.get('location','').strip(),building=request.POST.get('building','').strip(),landmark=request.POST.get('landmark','').strip(),
        severity=request.POST.get('severity','medium'),latitude=request.POST.get('latitude') or None,longitude=request.POST.get('longitude') or None,
    )
    for f in request.FILES.getlist('images'):
        ProblemImage.objects.create(report=report,image=f)
    ReportUpdate.objects.create(report=report,author=request.user,new_status='submitted',note='Problem report submitted and tracking reference generated.')
    Notification.objects.create(user=request.user,report=report,title='Report submitted',message=f'Your report {report.reference} has been received and can now be tracked.')
    messages.success(request,f'Report submitted successfully. Your tracking reference is {report.reference}.')
    return redirect(f"{reverse('track_issue')}?reference={report.reference}")


def track_issue(request):
    report=None
    ref=(request.GET.get('reference') or request.POST.get('reference') or '').strip()
    if ref:
        report=ProblemReport.objects.filter(reference__iexact=ref).select_related('category','subcategory','problem_type','assigned_department').prefetch_related('updates','images').first()
    return render(request,'track_issue.html',{'report':report,'reference':ref})

@login_required
def dashboard(request):
    manager_mode=_manager(request.user)
    if manager_mode:
        if request.user.is_superuser or request.user.is_staff or getattr(getattr(request.user,'profile',None),'role',None) in {'management','admin'}:
            reports=ProblemReport.objects.all()
        else:
            dept=getattr(getattr(request.user,'profile',None),'department',None)
            reports=ProblemReport.objects.filter(Q(assigned_officer=request.user)|Q(assigned_department=dept)).distinct() if dept else ProblemReport.objects.filter(assigned_officer=request.user)
    else:
        reports=ProblemReport.objects.filter(reporter=request.user)
    reports=reports.select_related('category','assigned_department').order_by('-updated_at')
    total=reports.count()
    open_count=reports.exclude(status__in=['resolved','closed','rejected']).count()
    resolved=reports.filter(status__in=['resolved','closed']).count()
    visible_reports=reports[:100]
    return render(request,'dashboard.html',{'reports':visible_reports,'total':total,'open':open_count,'resolved':resolved,'manager_mode':manager_mode})

@user_passes_test(_manager,login_url='login')
def manage_reports(request):
    reports=ProblemReport.objects.select_related('category','subcategory','assigned_department','assigned_officer')
    if not (request.user.is_staff or request.user.is_superuser or getattr(getattr(request.user,'profile',None),'role',None) in {'management','admin'}):
        dept=getattr(getattr(request.user,'profile',None),'department',None)
        reports=reports.filter(Q(assigned_officer=request.user)|Q(assigned_department=dept)).distinct() if dept else reports.filter(assigned_officer=request.user)
    q=request.GET.get('q','').strip(); status=request.GET.get('status','').strip(); category=request.GET.get('category','').strip()
    if q: reports=reports.filter(Q(reference__icontains=q)|Q(title__icontains=q)|Q(description__icontains=q)|Q(location__icontains=q))
    if status: reports=reports.filter(status=status)
    if category: reports=reports.filter(category_id=category)
    return render(request,'manage_reports.html',{'reports':reports.order_by('-created_at')[:250],'q':q,'status':status,'category':category,'status_choices':ProblemReport.STATUS,'categories':Category.objects.filter(active=True)})

@user_passes_test(_manager,login_url='login')
def report_detail(request,pk):
    report=get_object_or_404(ProblemReport.objects.select_related('category','subcategory','problem_type','assigned_department','assigned_officer','reporter').prefetch_related('images','updates__author'),pk=pk)
    if not (request.user.is_staff or request.user.is_superuser or getattr(getattr(request.user,'profile',None),'role',None) in {'management','admin'}):
        dept=getattr(getattr(request.user,'profile',None),'department',None)
        if report.assigned_officer_id!=request.user.id and (not dept or report.assigned_department_id!=dept.id):
            messages.error(request,'You are not authorized to process this report.')
            return redirect('manage_reports')
    if request.method=='POST':
        old_status=report.status
        new_status=request.POST.get('status',report.status)
        dept_id=request.POST.get('assigned_department') or None
        officer_id=request.POST.get('assigned_officer') or None
        note=request.POST.get('note','').strip()
        report.status=new_status
        report.assigned_department_id=dept_id
        report.assigned_officer_id=officer_id
        report.expected_resolution_date=request.POST.get('expected_resolution_date') or None
        report.resolution_summary=request.POST.get('resolution_summary','').strip()
        report.save()
        ReportUpdate.objects.create(report=report,author=request.user,old_status=old_status,new_status=new_status,note=note)
        if report.reporter:
            Notification.objects.create(user=report.reporter,report=report,title=f'Report update: {report.reference}',message=f'Status: {report.get_status_display()}. {note}')
        messages.success(request,'The response and tracking update have been saved.')
        return redirect('report_detail',pk=report.pk)
    officers=User.objects.filter(Q(is_staff=True)|Q(profile__role__in=['officer','management','admin'])).distinct().order_by('first_name','username')
    return render(request,'report_detail.html',{'report':report,'status_choices':ProblemReport.STATUS,'departments':Department.objects.filter(active=True).order_by('name'),'officers':officers})


def subcategories_api(request,category_id):
    return JsonResponse(list(SubCategory.objects.filter(category_id=category_id,active=True).order_by('name').values('id','name')),safe=False)

def problem_types_api(request,subcategory_id):
    return JsonResponse(list(ProblemType.objects.filter(subcategory_id=subcategory_id,active=True).order_by('name').values('id','name')),safe=False)
