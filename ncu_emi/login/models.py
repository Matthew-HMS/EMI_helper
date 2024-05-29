# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Class(models.Model):
    class_id = models.IntegerField(db_column='Class_id', primary_key=True)  # Field name made lowercase.
    class_name = models.CharField(db_column='Class_name', max_length=45, blank=True, null=True)  # Field name made lowercase.
    user_user = models.ForeignKey('User', models.DO_NOTHING, db_column='User_User_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'class'


class File(models.Model):
    file_id = models.IntegerField(db_column='File_id', primary_key=True)  # Field name made lowercase.
    file_name = models.CharField(db_column='File_name', max_length=45, blank=True, null=True)  # Field name made lowercase.
    file_path = models.CharField(db_column='File_path', max_length=45, blank=True, null=True)  # Field name made lowercase.
    class_class = models.ForeignKey(Class, models.DO_NOTHING, db_column='Class_Class_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'file'


class Ppt(models.Model):
    ppt_id = models.IntegerField(db_column='PPT_id', primary_key=True)  # Field name made lowercase.
    ppt_name = models.CharField(db_column='PPT_name', max_length=45, blank=True, null=True)  # Field name made lowercase.
    ppt_path = models.CharField(db_column='PPT_path', max_length=45, blank=True, null=True)  # Field name made lowercase.
    class_class = models.ForeignKey(Class, models.DO_NOTHING, db_column='Class_Class_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ppt'


class Pptword(models.Model):
    pptword_id = models.IntegerField(db_column='PPTWord_id', primary_key=True)  # Field name made lowercase.
    pptword_page = models.IntegerField(db_column='PPTWord_page', blank=True, null=True)  # Field name made lowercase.
    pptword_content = models.CharField(db_column='PPTWord_content', max_length=45, blank=True, null=True)  # Field name made lowercase.
    ppt_ppt = models.ForeignKey(Ppt, models.DO_NOTHING, db_column='PPT_PPT_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pptword'


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

    class Meta:
        managed = False
        db_table = 'user'
