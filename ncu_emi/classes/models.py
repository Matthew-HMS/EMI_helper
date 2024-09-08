from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.AutoField(db_column='User_id', primary_key=True)  # Field name made lowercase.
    user_name = models.CharField(db_column='User_name', max_length=45)  # Field name made lowercase.
    user_account = models.CharField(db_column='User_account', unique=True, max_length=45)  # Field name made lowercase.
    user_pw = models.CharField(db_column='User_pw', max_length=128)  # Field name made lowercase.
    is_active = models.IntegerField()
    last_login = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
        
class Class(models.Model):
    class_id = models.AutoField(db_column='Class_id', primary_key=True)  # Field name made lowercase.
    class_name = models.CharField(db_column='Class_name', max_length=45, blank=True, null=True)  # Field name made lowercase.
    user_user = models.ForeignKey('User', models.DO_NOTHING, db_column='User_User_id')  # Field name made lowercase.
    class_path = models.CharField(db_column='Class_path', max_length=45, blank=True, null=True)  # Field name made lowercase.
    vector_store_id = models.CharField(db_column='Vector_store_id', max_length=45,blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'class'

class Ppt(models.Model):
    ppt_id = models.AutoField(db_column='PPT_id', primary_key=True)  # Field name made lowercase.
    ppt_name = models.CharField(db_column='PPT_name', max_length=45, blank=True, null=True)  # Field name made lowercase.
    ppt_path = models.CharField(db_column='PPT_path', max_length=45, blank=True, null=True)  # Field name made lowercase.
    ppt_local_path = models.CharField(db_column='PPT_local_path', max_length=100, blank=True, null=True)  # Field name made lowercase.
    class_class = models.ForeignKey('Class', models.DO_NOTHING, db_column='Class_Class_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ppt'