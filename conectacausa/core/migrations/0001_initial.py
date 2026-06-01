from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=160)),
                ('org', models.CharField(max_length=160)),
                ('desc', models.TextField()),
                ('goal', models.DecimalField(decimal_places=2, max_digits=12)),
                ('deadline', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='DonorUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=160)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password_hash', models.CharField(max_length=256)),
                ('role', models.CharField(default='donor', max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Allocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('pct', models.PositiveSmallIntegerField()),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allocations', to='core.campaign')),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('date', models.DateField(default=django.utils.timezone.localdate)),
                ('anonymous', models.BooleanField(default=False)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donations', to='core.campaign')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donations', to='core.donoruser')),
            ],
            options={
                'ordering': ['-date', '-id'],
            },
        ),
        migrations.CreateModel(
            name='SpendLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('cat', models.CharField(max_length=120)),
                ('desc', models.CharField(blank=True, max_length=240)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spend_logs', to='core.campaign')),
            ],
            options={
                'ordering': ['-date', '-id'],
            },
        ),
    ]
