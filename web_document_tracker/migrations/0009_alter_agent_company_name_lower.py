# Generated by Django 5.0.3 on 2024-05-10 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_document_tracker', '0008_agent_company_name_lower_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='company_name_lower',
            field=models.CharField(blank=True, editable=False, max_length=67),
        ),
    ]
