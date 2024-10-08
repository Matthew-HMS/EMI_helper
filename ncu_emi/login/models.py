# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150)

#     class Meta:
#         managed = False
#         db_table = 'auth_group'


# class AuthGroupPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),)


# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
#     codename = models.CharField(max_length=100)

#     class Meta:
#         managed = False
#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)


# class AuthUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.IntegerField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.IntegerField()
#     is_active = models.IntegerField()
#     date_joined = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'auth_user'


# class AuthUserGroups(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_user_groups'
#         unique_together = (('user', 'group'),)


# class AuthUserUserPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_user_user_permissions'
#         unique_together = (('user', 'permission'),)


class Class(models.Model):
    class_id = models.IntegerField(db_column='Class_id', primary_key=True)  # Field name made lowercase.
    class_name = models.CharField(db_column='Class_name', max_length=45, blank=True, null=True)  # Field name made lowercase.
    user_user = models.ForeignKey('User', models.DO_NOTHING, db_column='User_User_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'class'


# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.PositiveSmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'django_admin_log'


# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)

#     class Meta:
#         managed = False
#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)


# class DjangoMigrations(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'django_migrations'


# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'django_session'


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
    user_pw = models.CharField(db_column='User_pw', max_length=128)  # Field name made lowercase.
    is_active = models.IntegerField()
    last_login = models.DateTimeField(blank=True, null=True)
    
    def set_password(self, raw_password):
        import hashlib
        self.user_pw = hashlib.sha256(raw_password.encode()).hexdigest()

    def check_password(self, raw_password):
        import hashlib
        return self.user_pw == hashlib.sha256(raw_password.encode()).hexdigest()

    class Meta:
        managed = False
        db_table = 'user'
    