from django.db import models
from mousedb.animal.models import Animal, Strain
from mousedb.custom_fields import CommaSeparatedFloatField

FEEDING_TYPES = (
	('fed', 'Fed'),
	('fasted', 'Fasted')
)

INJECTIONS = (
	('Insulin', 'Insulin'),
	('Glucose', 'Glucose'),
	('Pyruvate', 'Pyruvate'),
	('Glucagon', 'Glucagon')
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
    
    """This class describes Experiment objects.
    
    This object describes the aspects of an experiment done on several :class:`~mousedb.animal.models.Animal` objects.
    This object describes the conditions under which the experiment ws done.
    The results of the experiment are contained in :class:`~experimentdb.data.models.Measurement` objects and grouped together in :class:`~experimentdb.models.Treatment` objects.
    Experiments may or may not be part of a :class:`~experimentdb.data.models.Study`.
    The required fields for this object are date, :class:`~experimentdb.data.models.Researchers` and feeding state.
    The optional fields are notes, time, experimentID, fasting_time, injection and concentration and the :class:`~experimentdb.data.models.Study`.    
    """
    
    date = models.DateField()
    notes = models.TextField(max_length = 500, blank=True)
    time = models.TimeField(help_text="Time of the experiment in 24h format", blank=True, null=True)
    researchers = models.ManyToManyField('Researcher')
    experimentID = models.SlugField(max_length=50, help_text="ie DB-2008-11-11-A", blank=True)
    feeding_state = models.CharField(max_length=20, default = 'fed', choices = FEEDING_TYPES)
    fasting_time = models.IntegerField(help_text = "in hours", null = True, blank = True)
    injection = models.CharField(max_length=20, choices=INJECTIONS, blank=True)
    concentration = models.CharField(max_length=20, blank=True)
    study = models.ForeignKey('Study', blank=True, null=True)
    
    def __unicode__(self):
        """The unicode representation of an experiment is date-feeding_state, for example **2012-01-01-Fed**."""
        return u'%s-%s' % (self.date, self.feeding_state) 
	
    @models.permalink
    def get_absolute_url(self):
        """The absolute url of an experiment is  `/mousedb/experiment/id </mousedb/experiment/id>`."""
        return ('experiment-detail', [str(self.id)])

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
	
    def age(self):
        age =  self.experiment.date - self.animal.Born
        return age.days
    
    def get_absolute_url(self):
        return self.animal.get_absolute_url()

	
class Researcher(models.Model):
	first_name = models.CharField(max_length = 50)
	last_name = models.CharField(max_length = 50)
	name_slug = models.SlugField(max_length = 100)
	email = models.EmailField()
	active = models.BooleanField(default = True)
	def __unicode__(self):
		return u'%s %s' % (self.first_name, self.last_name)


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
	@models.permalink
	def get_absolute_url(self):
		return ('study-detail', [str(self.id)])
	
class Treatment(models.Model):
    '''This model defines the groupings of mice for an experiment.
    
    The purpose of treatment groups is to associate together animals which are treated similarly in a study.
    A treatment group is generally defined by its specific conditions, including:
    
    * :class:`~mousedb.data.models.Diet` 
    * :class:`~mousedb.data.models.Environment`
    * :class:`~mousedb.data.models.Implantation` (optional)
    * :class:`~mousedb.data.models.Transplantation` (optional)   
    * :class:`~mousedb.data.models.Pharmaceutical` (optional)

    The required fields are the associated :class:`~mousedb.data.models.Study`, the name (treatment), the     * :class:`~mousedb.data.models.Animal` objects in this group and the  :class:`~mousedb.data.models.Researcher` objects in the group.
    There is also an optional notes field.    
    '''
    
    treatment = models.CharField(max_length=50, 
        help_text="The name of the treatment group.")
    study = models.ForeignKey('Study', 
        help_text="The associated study in which these groups belong.")
    animals = models.ManyToManyField(Animal, 
        help_text="In the case of transplants this is the recipient.")
    diet = models.ForeignKey('Diet', 
        help_text="The food in this group.")
    environment = models.ForeignKey('Environment', default = 1, 
        help_text="The physical environment for this group.")
    implantation  = models.ManyToManyField('Implantation', 
        blank=True, null=True,
        help_text="Whether something is implanted for this group.")
    transplantation  = models.ForeignKey('Transplantation', 
        blank=True, null=True,
        help_text="Whether this group is tranplanted with something.")
    pharmaceutical = models.ManyToManyField('Pharmaceutical', 
        blank=True, null=True,
        help_text="Whether this group is treated with some pharmaceutical.")
    researchers = models.ManyToManyField('Researcher',
        help_text="Which researchers are responsible for this group.")
    notes = models.TextField(max_length=500, blank=True)
    
    def __unicode__(self):
        '''The unicode representation of a :class:`~mousedb.data.models.Treatment` is the treatment field.'''
        return u'%s' %(self.treatment)

    @models.permalink
    def get_absolute_url(self):
        '''The url for a treatment-detail is **/treatment/<id>**.'''
        return ('treatment-detail', [str(self.id)])

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


