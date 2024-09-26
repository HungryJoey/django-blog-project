from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('myapp', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='author',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.user'),
        ),
    ]