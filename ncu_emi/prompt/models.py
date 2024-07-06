from django.db import models

# Create your models here.
class Prompt(models.Model):
    prompt_id = models.IntegerField(db_column='Prompt_id', primary_key=True)  # Field name made lowercase.
    prompt_name = models.CharField(db_column='Prompt_name', max_length=45, blank=True, null=True)  # Field name made lowercase.
    prompt_content = models.CharField(db_column='Prompt_content', max_length=45, blank=True, null=True)  # Field name made lowercase.
    user_user = models.ForeignKey('User', models.DO_NOTHING, db_column='User_User_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'prompt'

class User(models.Model):
    user_id = models.AutoField(db_column='User_id', primary_key=True)  # Field name made lowercase.
    user_name = models.CharField(db_column='User_name', max_length=45)  # Field name made lowercase.
    user_account = models.CharField(db_column='User_account', unique=True, max_length=45)  # Field name made lowercase.
    user_pw = models.CharField(db_column='User_pw', max_length=45)  # Field name made lowercase.
    is_active = models.IntegerField()
    last_login = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'