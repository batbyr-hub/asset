# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AllDocumentary(models.Model):
    department_id = models.IntegerField()
    employee_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'all_documentary'


class AssetDetailsData(models.Model):
    assetslipid = models.IntegerField(db_column='AssetSlipID', blank=True, null=True)
    assetgroupname = models.CharField(db_column='AssetGroupName', max_length=50, blank=True, null=True)
    assetname = models.CharField(db_column='AssetName', max_length=250, blank=True, null=True)
    assetbarcode = models.CharField(db_column='AssetBarCode', max_length=200, blank=True, null=True)
    returnis = models.CharField(db_column='ReturnIs', max_length=200, blank=True, null=True)
    seleccion = models.CharField(db_column='Seleccion', max_length=200, blank=True, null=True)
    lenghtcable = models.IntegerField(db_column='LenghtCable', blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'asset_details_data'


class AssetFirmData(models.Model):
    assetpackagedataid = models.CharField(db_column='assetPackageDataId', max_length=200)
    userid = models.CharField(db_column='userId', max_length=200)
    status = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'asset_firm_data'


class AssetPackageData(models.Model):
    id = models.AutoField('id', primary_key=True, db_index=True)
    assetslipid = models.IntegerField(db_column='AssetSlipID', blank=True, null=True)
    locationfrom = models.CharField(db_column='LocationFrom', max_length=100, blank=True, null=True)
    locationto = models.CharField(db_column='LocationTo', max_length=100, blank=True, null=True)
    createddate = models.DateField(db_column='CreatedDate')
    location_id = models.CharField(db_column='Location_ID', max_length=200, blank=True, null=True)
    locationfrom_id = models.CharField(db_column='LocationFrom_ID', max_length=200, blank=True, null=True)
    userfrom = models.CharField(db_column='UserFrom', max_length=200, blank=True, null=True)
    userto = models.CharField(db_column='UserTo', max_length=200, blank=True, null=True)
    gazar = models.CharField(max_length=200, blank=True, null=True)
    reasonvalue = models.CharField(db_column='ReasonValue', max_length=200, blank=True, null=True)
    uploadfile = models.TextField(db_column='UploadFile', blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'asset_package_data'


class AssetPermission(models.Model):
    employee_id = models.IntegerField(blank=True, null=True)
    user_id = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)
    confirmation = models.CharField(max_length=6, blank=True, null=True)
    confirmed = models.CharField(max_length=200, blank=True, null=True)
    confirmed_date = models.CharField(max_length=200)
    level = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'asset_permission'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group_id', 'permission_id'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type_id = models.IntegerField()
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type_id', 'codename'),)


class AuthUser(models.Model):
    username = models.CharField(unique=True, max_length=150)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=254)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user_id = models.IntegerField()
    group_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user_id', 'group_id'),)


class AuthUserUserPermissions(models.Model):
    user_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user_id', 'permission_id'),)


class AziinDugaar(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.IntegerField()
    price = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'aziin_dugaar'


class Company(models.Model):
    id = models.AutoField('id', primary_key=True, db_index=True)
    name = models.CharField(max_length=200)

    class Meta:
        # managed = False
        db_table = 'company'


class Department(models.Model):
    id = models.AutoField('id', primary_key=True, db_index=True)
    parent_id = models.IntegerField()
    sign_leader_id = models.IntegerField(blank=True, null=True)
    leader_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=200)
    eoffice = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'department'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Employee(models.Model):
    id = models.AutoField('id', primary_key=True, db_index=True)
    department_id = models.IntegerField()
    job_position_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    family_name = models.CharField(max_length=200, blank=True, null=True)
    surname = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    sex = models.IntegerField(blank=True, null=True)
    birth_date = models.CharField(max_length=200, blank=True, null=True)
    register_number = models.CharField(max_length=200, blank=True, null=True)
    image_url = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    current_state_id = models.IntegerField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'employee'


class EmployeeAlternates(models.Model):
    id = models.AutoField('id', primary_key=True, db_index=True)
    employee_id = models.IntegerField()
    alternate_employee_id = models.IntegerField()
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'employee_alternates'


class EmployeeStates(models.Model):
    name = models.CharField(max_length=200)
    type = models.IntegerField()
    need_alternate = models.IntegerField(blank=True, null=True)
    note = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'employee_states'


class Jobposition(models.Model):
    id = models.AutoField('id', primary_key=True, db_index=True)
    department_id = models.IntegerField()
    level_group_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=200)
    fullname = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'jobposition'


class JobpositionLevelGroup(models.Model):
    name = models.CharField(max_length=200)
    note = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'jobposition_level_group'


class NfilterNeedFirm(models.Model):
    nsn_id = models.CharField(max_length=255)
    head_id = models.CharField(max_length=255)
    firstfirm = models.CharField(db_column='firstFirm', max_length=255)  # Field name made lowercase.
    firstfirmdate = models.CharField(db_column='firstFirmDate', max_length=255)  # Field name made lowercase.
    firstfirmdescription = models.CharField(db_column='firstFirmDescription', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nfilter_need_firm'


class NfilterPermission(models.Model):
    department_id = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'nfilter_permission'


class NfilterSaveNumber(models.Model):
    user_id = models.CharField(max_length=255)
    numbertype = models.CharField(max_length=255)
    dia = models.CharField(max_length=255)
    zoriulalt = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255)
    numbers = models.CharField(max_length=500)
    code = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'nfilter_save_number'


class Numbertype(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=100)
    is_active = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'numbertype'


class Prefix(models.Model):
    prefix = models.IntegerField(blank=True, null=True)
    is_active = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    category = models.ForeignKey(Numbertype, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prefix'


class Prefixab(models.Model):
    prefix = models.IntegerField(blank=True, null=True)
    is_active = models.IntegerField()
    category_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'prefixab'


class SimpleDetailsData(models.Model):
    packagecode = models.CharField(db_column='packageCode', max_length=200)  # Field name made lowercase.
    productname = models.CharField(db_column='productName', max_length=200)  # Field name made lowercase.
    productcode = models.CharField(db_column='productCode', max_length=200)  # Field name made lowercase.
    unit = models.CharField(max_length=200)
    desiredsize = models.CharField(db_column='desiredSize', max_length=200)  # Field name made lowercase.
    allowedsize = models.CharField(db_column='allowedSize', max_length=200)  # Field name made lowercase.
    providedsize = models.CharField(db_column='providedSize', max_length=200)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'simple_details_data'


class SimplePackageData(models.Model):
    packagecode = models.AutoField(db_column='packageCode', primary_key=True)  # Field name made lowercase.
    userid = models.CharField(db_column='userId', max_length=200)  # Field name made lowercase.
    username = models.CharField(db_column='userName', max_length=200)  # Field name made lowercase.
    headid = models.CharField(db_column='headId', max_length=200)  # Field name made lowercase.
    createddate = models.CharField(db_column='createdDate', max_length=200)  # Field name made lowercase.
    haana = models.CharField(max_length=200)
    purpose = models.CharField(max_length=200)
    firstfirm = models.CharField(db_column='firstFirm', max_length=200)  # Field name made lowercase.
    secondfirm = models.CharField(db_column='secondFirm', max_length=200)  # Field name made lowercase.
    thirdfirm = models.CharField(db_column='thirdFirm', max_length=200)  # Field name made lowercase.
    status = models.CharField(max_length=200)
    treasurer = models.CharField(max_length=200)
    company_id = models.CharField(max_length=200)
    firstfirmdate = models.CharField(db_column='firstFirmDate', max_length=200)  # Field name made lowercase.
    secondfirmdate = models.CharField(db_column='secondFirmDate', max_length=200)  # Field name made lowercase.
    thirdfirmdate = models.CharField(db_column='thirdFirmDate', max_length=200)  # Field name made lowercase.
    firstfirmdescription = models.CharField(db_column='firstFirmDescription', max_length=200)  # Field name made lowercase.
    secondfirmdescription = models.CharField(db_column='secondFirmDescription', max_length=200)  # Field name made lowercase.
    thirdfirmdescription = models.CharField(db_column='thirdFirmDescription', max_length=200)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'simple_package_data'


class SimplePermission(models.Model):
    employee_id = models.IntegerField(blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)
    confirmation = models.CharField(max_length=6, blank=True, null=True)
    confirmed = models.CharField(max_length=200, blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'simple_permission'


class SimpleProducts(models.Model):
    nyaraviinturul = models.CharField(db_column='nyaraviinTurul', max_length=200, blank=True, null=True)  # Field name made lowercase.
    diamondcode = models.CharField(db_column='diamondCode', max_length=200, blank=True, null=True)  # Field name made lowercase.
    turul = models.CharField(max_length=200, blank=True, null=True)
    dedturul = models.CharField(db_column='dedTurul', max_length=200, blank=True, null=True)  # Field name made lowercase.
    ner = models.CharField(max_length=200, blank=True, null=True)
    hemjihnegj = models.CharField(db_column='hemjihNegj', max_length=200, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'simple_products'


class SimpleProductsType(models.Model):
    treasurers_id = models.CharField(max_length=200)
    type = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'simple_products_type'


class SimpleTreasurers(models.Model):
    employee_id = models.IntegerField(blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)
    treasurer_type_id = models.CharField(max_length=200)
    company_id = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'simple_treasurers'


class SimpleTreasurersType(models.Model):
    treasurer = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'simple_treasurers_type'


class User(models.Model):
    user_id = models.CharField(max_length=200)
    username = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15)
    email = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'user'
