from django.db import models
from django.template.defaultfilters import slugify

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

    The required fields are the associated :class:`~mousedb.data.models.Study`, the name (treatment), the :class:`~mousedb.data.models.Animal` objects in this group and the  :class:`~mousedb.data.models.Researcher` objects in the group.
    There is also an optional notes field.    
    '''
    
    treatment = models.CharField(max_length=50, 
        help_text="The name of the treatment group.")
    study = models.ForeignKey('Study', blank=True, null=True, 
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
    '''This class defines a drug treatment.
    
    Each object is specific to a particular vendor, dose and mode of delivery.
    For other doses, generate additional Pharmaceutical objects.    
    The required fields are **drug**, **dose**, **recurrance**, **mode** and **vendor**.
    '''
    
    DOSAGE_TYPE = (
	('Tail Vein', 'Tail Vein Injection'),
	('Interperitoneal', 'Interperitoneal Injection'),
	('Oral', 'Oral Gavage'),
    ('Water', 'Drug in Water'),
    ('Food', 'Drug in Food'))
    

    drug = models.CharField(max_length=100, help_text="Name of drug")
    dose = models.CharField(max_length=100, help_text="Dose per animal (include units)")
    recurrance = models.CharField(max_length=100, help_text="How often is the drug delivered")
    mode = models.CharField(max_length=100, choices=DOSAGE_TYPE, help_text="How is the drug delivered.")
    vendor = models.ForeignKey('Vendor', help_text="From whom is the drug obtained.")
    notes = models.TextField(max_length=500, blank=True, null=True, help_text="Notes about this drug regimen.")
	
    def __unicode__(self):
        '''The unicode representation is for example "Drug at 1mg/kg, daily.'''
        return u'%s at %s, %s' % (self.drug, self.dose, self.recurrance)
        
    @models.permalink
    def get_absolute_url(self):
        """The absolute url of a :class:`~mousedb.drug.models.Pharmaceutical` is  **/parameter/pharmaceutical/<id>**."""
        return ('pharmaceutical-detail', [str(self.id)])        

class Transplantation(models.Model):
	tissue = models.CharField(max_length=100)
	transplant_date = models.DateField(blank=True, null=True)
	donor = models.ManyToManyField(Animal)
	surgeon = models.ManyToManyField('Researcher', blank=True, null=True)
	notes = models.TextField(max_length=500, blank=True)
	def __unicode__(self):
		return u'%s' % self.tissue
		
class Cohort(models.Model):
    '''A Cohort is a group of :class:`~mousedb.animal.models.Animals`.
    
    Generally a cohort is an experimental replicate of a :class:`~mousedb.data.models.Treatment` as part of a :class:`~mousedb.data.models.Study`.
    Cohorts are also generally defined by starting and ending dates.
    A cohort would generally comprise both :class:`~mousedb.data.models.Treatment` groups being compared.
    The required fields are **name** (which must be unique to this cohort) and **animals**.
    '''
    
    name = models.CharField(max_length=25, unique=True, help_text="What is the name of this cohort")
    animals = models.ManyToManyField(Animal, help_text="Which animals comprise this cohort.")
    start_date = models.DateField(blank=True, null=True, help_text="What date did the treatments/comparason start")
    end_date = models.DateField(blank=True, null=True, help_text="What date did the treatments/comparason end")
    treatment_groups = models.ManyToManyField('Treatment', blank=True, null=True, help_text="Which treatment groups are involved?")
    notes = models.TextField(blank=True, null=True, help_text="Extra notes about this cohort.")
    slug = models.SlugField(editable=False)
    
    def __unicode__(self):
        '''The unicode representation of a :class:`~mousedb.data.models.Cohort` is the name.'''
        return u'%s' % self.name
        
    def save(self, *args, **kwargs):
        '''The slug field is autopopulated during the save from the name field.'''
        if not self.id:
            self.slug = slugify(self.name)
        super(Cohort, self).save(*args, **kwargs)        

   # @models.permalink
    #def get_absolute_url(self):
        #'''The url for a treatment-detail is **/cohort/<slug>**.'''
        #return ('treatment-detail', [str(self.slug)])

