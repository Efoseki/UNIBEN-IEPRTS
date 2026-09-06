from django.core.management.base import BaseCommand
from management_utils.models import Category,SubCategory,ProblemType,Department

DATA={
'Infrastructure':['Building and Structural Defects','Electrical and Power Problems','Water Supply and Plumbing Problems','Roads, Walkways and Parking Facilities','Classroom and Lecture Theatre Facilities','Hostel and Residential Facilities','Toilet and Sanitary Facilities','ICT Facilities','Streetlights and Outdoor Lighting','Drainage and Flood-Control Infrastructure','Laboratory and Workshop Facilities','Security and Safety Infrastructure','Other Infrastructure Problems'],
'Environmental':['Waste Management and Refuse Disposal','Environmental Cleanliness','Drainage and Flooding','Air Pollution','Water Pollution','Noise Pollution','Vegetation and Landscaping','Pests and Disease Vectors','Public Health and Environmental Hazards','Odour and Offensive Smells','Erosion and Land Degradation','Other Environmental Problems']}
DEPARTMENTS=[('WORKS','Works / Physical Planning'),('ENV','Environmental Services'),('ICT','ICT Services'),('SEC','Security Services'),('STUAFF','Student Affairs'),('OTHER','Other Responsible Unit')]

class Command(BaseCommand):
    help='Load reference data for UNIBEN IEPRTS.'
    def handle(self,*args,**opts):
        for cname,subs in DATA.items():
            c,_=Category.objects.get_or_create(name=cname)
            c.active=True; c.save()
            for sname in subs:
                s,_=SubCategory.objects.get_or_create(category=c,name=sname)
                ProblemType.objects.get_or_create(subcategory=s,name='General '+sname)
        for code,name in DEPARTMENTS:
            Department.objects.get_or_create(code=code,defaults={'name':name})
        self.stdout.write(self.style.SUCCESS('UNIBEN IEPRTS reference data loaded.'))
