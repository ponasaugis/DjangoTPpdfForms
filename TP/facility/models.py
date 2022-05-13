from django.db import models
from django.urls import reverse

# Create your models here.

class Project(models.Model):
    project_name = models.CharField('Project', max_length=255, unique=True, help_text="Enter project name")

    def __str__(self):
        return self.project_name

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'



class Agent(models.Model):
    first_name = models.CharField('First name', max_length=255, null=False, help_text="Enter first name")
    last_name = models.CharField('Last name', max_length=255, null=False, help_text="Enter last name")
    ccms_id = models.CharField('CCMS ID', max_length=255, unique=True, null=False, help_text="Enter CCMS ID")
    phone = models.CharField('Phone', max_length=255, null=False, help_text="Enter phone number")
    email = models.EmailField('Email', max_length=255, null=False, help_text="Enter email address")
    country = models.CharField('Country', max_length=255, null=False, help_text="Enter country")
    city = models.CharField('City', max_length=255, null=False, help_text="Enter city")
    street = models.CharField('Street', max_length=400, null=False, help_text="Enter street and building number.")
    project_id = models.ForeignKey('Project', related_name='agents', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.ccms_id} '

    def get_absolute_url(self):
        return reverse('agent-detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Agent'
        verbose_name_plural = 'Agents'


class Manufacturers(models.Model):
    manufacturer = models.CharField('Manufacturer', max_length=255, unique=True, help_text="Enter manufacturer name")

    def __str__(self):
        return f'{self.manufacturer}'

    class Meta:
        verbose_name = 'Manufacturer'
        verbose_name_plural = 'Manufacturers'

class EqModels(models.Model):
    eq_model = models.CharField('Model', max_length=255, unique=True, help_text="Enter model name")

    def __str__(self):
        return f'{self.eq_model}'

    class Meta:
        verbose_name = 'Model'
        verbose_name_plural = 'Models'

class Types(models.Model):
    type = models.CharField('Type', max_length=255, unique=True, help_text="Enter type of equipement")

    def __str__(self):
        return f'{self.type}'

    class Meta:
        verbose_name = 'Equipement type'
        verbose_name_plural = 'Equipement types'


class Equipement(models.Model):
    manufacturer_id = models.ForeignKey('Manufacturers', related_name='manufactequipements', on_delete=models.SET_NULL,null=True)
    eqModels_id = models.ForeignKey('EqModels', related_name='modelsequipements', on_delete=models.SET_NULL, null=True)
    types_id = models.ForeignKey('Types', related_name='typesequipements', on_delete=models.SET_NULL, null=True)
    price = models.FloatField(help_text='Kaina', null=True)

    def __str__(self):
        return f'{self.manufacturer_id} {self.eqModels_id}'

    class Meta:
        verbose_name = 'Equipement'
        verbose_name_plural = 'Equipements'


class Order(models.Model):
    date_created = models.DateField(auto_now_add=True)
    comment = models.CharField('Comment', max_length=2000, blank=True)
    agent_id = models.ForeignKey('Agent', related_name='ordersall', on_delete=models.SET_NULL, null=True)

    def order_details(self):
        return ', '.join(line.equipement_id.manufacturer_id.manufacturer + ' ' + line.equipement_id.eqModels_id.eq_model + ' S/N-' + '"' + line.sn + '"' for line in OrderLine.objects.filter(order_id=self.id)[:3])

    @property
    def total(self):
        order_line = OrderLine.objects.filter(order_id=self.id)
        suma = 0
        for line in order_line:
            suma += line.equipement_id.price
        return suma

    @property
    def totalVat(self):
        order_line = OrderLine.objects.filter(order_id=self.id)
        suma = 0
        for line in order_line:
            suma += line.equipement_id.price
        suma = suma / 100
        suma = suma * 21
        return suma

    @property
    def totalWithoutVat(self):
        order_line = OrderLine.objects.filter(order_id=self.id)
        suma = 0
        for line in order_line:
            suma += line.equipement_id.price
        suma1 = suma / 100
        suma2 = suma1 * 21
        suma3 = suma - suma2
        return suma3


    def __str__(self):
        return f'{self.id} {self.agent_id} {self.date_created}'

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderLine(models.Model):
    sn = models.CharField('Serial number', max_length=400, unique=True, null=True, help_text="Enter serial number")
    order_id = models.ForeignKey('Order', related_name='orderlines', on_delete=models.SET_NULL, null=True)
    equipement_id = models.ForeignKey('Equipement', related_name='ordersline', on_delete=models.SET_NULL,
                                        null=True)

    STATUS = (
        ('g', 'Given'),
        ('r', 'Returned'),

    )

    status = models.CharField(
        max_length=1,
        choices=STATUS,
        blank=True,
        default='r',
        help_text='Status',
    )

    def __str__(self):
        return f' {self.order_id} {self.equipement_id} {self.sn}'

    class Meta:
        verbose_name = 'Order line'
        verbose_name_plural = 'Order lines'

