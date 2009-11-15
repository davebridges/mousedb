from django.db import models
import datetime

GENOTYPE_CHOICES = (
	('+/+', 'Wild-Type'),
	('-/+', 'Heterozygous'),
	('-/-', 'Knockout'),
	('N.D.', 'Not Determined')
)

GENDER_CHOICES = (
	('M', 'Male'),
	('F', 'Female'),
	('N.D.', 'Not Determined')
)

CROSS_TYPE = (
	('WT vs HET', 'Wild-Type vs Heterozygote'),
	('HET vs HET', 'Heterozygote vs Heterozygote'),
	('KO vs HET', 'Knockout vs Heterozygote'),
	('KO vs WT', 'Knockout vs Wild-Type'),
	('WT vs WT', 'Wild-Type vs Wild-Type')
)

BACKGROUND_CHOICES = (
	('C57BL/6-BA', 'C57BL/6-BA'),
	('C57BL/6-LY5.2', 'C57BL/S-LY5.2'),
	('Mixed', 'Mixed')
)

CAUSE_OF_DEATH = (
	('Unknown', 'Unknown'),
	('Sacrificed', 'Sacrificed'),
	('Accidental', 'Accidental')
)

class Strain(models.Model):
	Strain = models.CharField(max_length = 100)
	Strain_slug = models.SlugField(max_length = 20)
	Source = models.TextField(max_length = 500, blank = True)
	Comments = models.TextField (max_length = 500, blank = True)
	def __unicode__(self):
		return u'%s' % self.Strain
	def get_absolute_url(self):
		return "/strain/%s" % self.Strain_slug

class Animal(models.Model):
	MouseID	= models.IntegerField(max_length = 10, blank = True, null=True)
	Cage = models.IntegerField(max_length = 15, blank = True, null=True)
	CageID = models.ForeignKey('Cage', blank=True, null=True)
	Rack = models.CharField(max_length = 15, blank = True)
	Rack_Position = models.CharField(max_length = 15, blank = True)
	Strain = models.ForeignKey(Strain)
	Background = models.CharField(max_length = 25, choices = BACKGROUND_CHOICES)
	Genotype = models.CharField(max_length = 10, choices = GENOTYPE_CHOICES, default = 'N.D.')
	Gender = models.CharField(max_length = 5, choices = GENDER_CHOICES, default = 'N.D.')
	Born = models.DateField(blank = True, null=True)
	Weaned = models.DateField(blank = True, null=True)
	Death = models.DateField(blank = True, null=True)
	Cause_of_Death = models.CharField(max_length = 50, choices = CAUSE_OF_DEATH, blank=True)
	Backcross = models.IntegerField(max_length = 5, null=True, blank=True)
	Generation = models.IntegerField(max_length=5, null=True, blank=True)
	Breeding = models.ForeignKey('Breeding', blank=True, null=True)
	Father = models.ForeignKey('Animal', null=True, blank=True, related_name='father')
	Mother = models.ForeignKey('Animal', null=True, blank=True, related_name='mother')
	Markings = models.CharField(max_length = 100, blank=True)					
	Notes = models.TextField(max_length = 500, blank=True)
	Alive = models.BooleanField(default=True)
	def __unicode__(self):
		if self.MouseID:		
			return u'%s-EarTag #%i' % (self.Strain, self.MouseID)
		else:
			return u'%s (%i)' % (self.Strain, self.id)
	def get_absolute_url(self):
		return '%i' % (self.id)
	def save(self):
		if self.Death:
			self.Alive = False
		super(Animal, self).save()
	class Meta:
		ordering = ['MouseID']

class Breeding(models.Model):
	Females = models.ManyToManyField(Animal, related_name='females', blank=True)
	Male = models.ManyToManyField(Animal, related_name='male', blank=True)
	Strain = models.ForeignKey(Strain)
	Cage = models.CommaSeparatedIntegerField(max_length=100, blank=True, null=True)
	CageID = models.ForeignKey('Cage', blank=True, null=True)
	BreedingName = models.CharField(max_length=50, blank=True)
	Start = models.DateField(blank=True, null=True)
	End = models.DateField(blank=True, null=True)
	Crosstype = models.CharField(max_length=10, choices = CROSS_TYPE, blank=True)
	Notes = models.TextField(max_length=500, blank=True)
	Rack = models.CharField(max_length = 15, blank = True)
	Rack_Position = models.CharField(max_length = 15, blank = True) 
	Active = models.BooleanField(default=True)
	Timed_Mating = models.BooleanField(default=False, help_text="Is this cage a timed mating cage?")
	def __unicode__(self):
		return u'%s Breeding Cage: %s starting on %s'  %(self.Strain, self.Cage, self.Start)
	def get_absolute_url(self):
		return "/breeding/%i" % (self.id)
	def save(self):
		if self.End:
			self.Active = False
		super(Breeding, self).save()
	class Meta:
		ordering = ['Cage']
		
class Cage(models.Model):
	Barcode = models.IntegerField(primary_key=True)
	Rack = models.CharField(max_length = 15, blank = True)
	Rack_Position = models.CharField(max_length = 15, blank = True)
	
	



