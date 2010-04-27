from django.db import models
from mousedb.animal.models import Animal, Strain

FEEDING_TYPES = (
	('fed', 'Fed'),
	('fasted', 'Fasted')
)

INJECTIONS = (
	('Insulin', 'Insulin'),
	('Glucose', 'Glucose')
)

ORDERING = (
	('LSI Purchasing', 'LSI Purchasing'),
	('M-Marketsite', 'M-Marketsite')
)

DOSAGE_TYPE = (
	('Tail Vein', 'Tail Vein'),
	('Interperitoneal', 'Interperitoneal'),
	('Oral', 'Oral')
)


class Experiment(models.Model):
	date = models.DateField()
	notes = models.TextField(max_length = 500, blank=True)
	researchers = models.ManyToManyField('Researcher')
	animals = models.ManyToManyField(Animal)
	experimentID = models.SlugField(max_length=50, help_text="ie DB-2008-11-11-A", blank=True)
	feeding_state = models.CharField(max_length=20, default = 'fed', choices = FEEDING_TYPES)
	fasting_time = models.IntegerField(help_text = "in hours", null = True, blank = True)
	injection = models.CharField(max_length=20, choices=INJECTIONS, blank=True)
	concentration = models.CharField(max_length=20, blank=True)
	study = models.ForeignKey('Study', blank=True, null=True)
	def __unicode__(self):
		return u'%s-%s' % (self.date, self.feeding_state) 
	def get_absolute_url(self):
		return "/mousedb/experiment/%i" % self.id
	class Meta:
		ordering = ['-date']


class Assay(models.Model):
	assay = models.CharField(max_length = 100)
	assay_slug = models.SlugField(max_length=25)
	notes = models.TextField(max_length = 500, blank = True)
	measurement_units = models.CharField(max_length = 100)
	def __unicode__(self):
		return u'%s' % self.assay		


class Measurement(models.Model):
	animal = models.ForeignKey(Animal)
	experiment = models.ForeignKey(Experiment)
	assay = models.ForeignKey(Assay)
	values = models.CommaSeparatedIntegerField(blank=True, null=True, max_length=255, help_text="use for time courses, (comma separated values with no spaces)")
	def __unicode__(self):
		return u'%s %s' % (self.animal, self.assay)

	
class Researcher(models.Model):
	first_name = models.CharField(max_length = 50)
	last_name = models.CharField(max_length = 50)
	name_slug = models.SlugField(max_length = 100)
	email = models.EmailField()
	active = models.BooleanField(default = True)
	def __unicode__(self):
		return u'%s %s' % (self.first_name, self.last_name)
	def get_absolute_url(self):
		return "/researcher/%s" % self.name_slug

class Study(models.Model): 
	description = models.CharField(max_length=200)
	start_date = models.DateField(blank=True, null=True)
	stop_date = models.DateField(blank=True, null=True)
	strain = models.ManyToManyField(Strain)
	notes = models.TextField(max_length=500, blank=True)
	def __unicode__(self):
		return u'%s' % self.description
	class Meta:
		verbose_name_plural = "Studies"
	def get_absolute_url(self):
		return "/study/%s" % self.id
	
class Treatment(models.Model):
	treatment = models.CharField(max_length=50)
	study = models.ForeignKey('Study')
	animals = models.ManyToManyField(Animal, help_text="In the case of transplants this is the recipient")
	diet = models.ForeignKey('Diet')
	environment = models.ForeignKey('Environment', default = 1)
	implantation  = models.ManyToManyField('Implantation', blank=True, null=True)
	transplantation  = models.ForeignKey('Transplantation', blank=True, null=True)
	pharmaceutical = models.ManyToManyField('Pharmaceutical', blank=True, null=True)
	researchers = models.ManyToManyField('Researcher')
	notes = models.TextField(max_length=500, blank=True)
	def __unicode__(self):
		return u'%s' %(self.treatment)
	def get_absolute_url(self):
		return "/experimentdb/treatment/%i" % self.id

class Vendor(models.Model):
	vendor = models.CharField(max_length=100)
	website = models.URLField(blank=True, null=True)
	email = models.EmailField(blank=True, null=True)
	ordering = models.CharField(max_length=100, blank=True, choices=ORDERING)
	notes = models.TextField(max_length=500, blank=True)
	def __unicode__(self):
		return u'%s' % self.vendor

class Diet(models.Model):
	vendor = models.ForeignKey('Vendor')
	description = models.CharField(max_length=100, blank=True)
	product_id = models.CharField(max_length=100, blank=True)
	fat_content = models.IntegerField(blank=True, null=True, help_text="% of calories from fat")
	protein_content = models.IntegerField(blank=True, null=True, help_text="% of calories from protein")
	carb_content = models.IntegerField(blank=True, null=True, help_text="% of calories from carbohydrates")
	irradiated = models.BooleanField()
	notes = models.TextField(max_length=500, blank=True)
	def __unicode__(self):
		return u'%s' % self.description

class Environment(models.Model):
	building = models.CharField(max_length=100)
	room = models.CharField(max_length=15)
	temperature = models.IntegerField(help_text="in Farenheit")
	humidity = models.IntegerField(blank=True, null=True)
	contact = models.ManyToManyField('Researcher', blank=True, null=True)
	notes = models.TextField(max_length=500, blank=True)
	def __unicode__(self):
		return u'%s %s' % (self.building, self.room)

class Implantation(models.Model):
	implant = models.CharField(max_length=100)
	vendor = models.ForeignKey('Vendor')
	product_id = models.CharField(max_length=25)
	surgeon = models.ManyToManyField('Researcher', blank=True, null=True)
	notes = models.TextField(max_length=500, blank=True)
	def __unicode__(self):
		return u'%s' % self.implant

class Pharmaceutical(models.Model):
	drug = models.CharField(max_length=100)
	dose = models.CharField(max_length=100, help_text="include units")
	recurrance = models.CharField(max_length=100)
	mode = models.CharField(max_length=100, choices=DOSAGE_TYPE)
	vendor = models.ForeignKey('Vendor')
	notes = models.TextField(max_length=500, blank=True)
	def __unicode__(self):
		return u'%s at %s, %s' % (self.drug, self.dose, self.recurrance)

class Transplantation(models.Model):
	tissue = models.CharField(max_length=100)
	transplant_date = models.DateField()
	donor = models.ManyToManyField(Animal)
	surgeon = models.ManyToManyField('Researcher', blank=True, null=True)
	notes = models.TextField(max_length=500, blank=True)
	def __unicode__(self):
		return u'%s on %d' % (self.tissue, self.transplant_date)


