# Generated by Django 2.2.24 on 2022-03-27 21:00

from django.db import migrations, models

def update_status(apps, schema_editor):
    """ Checks if completed tasks should be set to 'failed' due to failed or unreachable results """
    # We can't import the model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    db_alias = schema_editor.connection.alias
    result_model = apps.get_model('api', 'Result')

    updated = 0
    for result in result_model.objects.filter(ignore_errors=False, status__in=['failed', 'unreachable']).all():
        if result.task.status == 'completed':
            result.task.status = 'failed'
            result.task.save()
            updated += 1

    if updated >= 1:
        # When running the migration, print a notification as such:
        # Applying api.0012_task_status... <this>
        print(f' updated status for {str(updated)} task(s) based on failed or unreachable results')


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_playbook_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('completed', 'completed'), ('expired', 'expired'), ('failed', 'failed'), ('running', 'running'), ('unknown', 'unknown')], default='unknown', max_length=25),
        ),
        migrations.RunPython(update_status)
    ]
