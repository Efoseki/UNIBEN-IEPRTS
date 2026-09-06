from django.db import migrations, models

def normalize_infrastructure_category(apps, schema_editor):
    Category=apps.get_model('management_utils','Category')
    old=Category.objects.filter(name='Infrastructural').first()
    new=Category.objects.filter(name='Infrastructure').first()
    if old and not new:
        old.name='Infrastructure'
        old.save(update_fields=['name'])
    elif old and new:
        SubCategory=apps.get_model('management_utils','SubCategory')
        ProblemReport=apps.get_model('management_utils','ProblemReport')
        ProblemReport.objects.filter(category=old).update(category=new)
        for sub in SubCategory.objects.filter(category=old):
            if not SubCategory.objects.filter(category=new,name=sub.name).exists():
                sub.category=new
                sub.save(update_fields=['category'])
        old.delete()

class Migration(migrations.Migration):
    dependencies=[('management_utils','0001_initial')]
    operations=[
        migrations.AlterField(model_name='problemreport',name='reference',field=models.CharField(editable=False,max_length=50,unique=True)),
        migrations.AddField(model_name='problemreport',name='expected_resolution_date',field=models.DateField(blank=True,null=True)),
        migrations.AddField(model_name='problemreport',name='resolution_summary',field=models.TextField(blank=True)),
        migrations.RunPython(normalize_infrastructure_category,migrations.RunPython.noop),
    ]
