"""This module describes the Strain, Animal, Breeding and Cage data models.

This module stores all data regarding a particular laboratory animal.  Information about experimental data and timed matings are stored in the data and timed_matings packages.  This module describes the database structure for each data model."""

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
    """A data model describing a mouse strain.  

    This is separate from the background of a mouse.  For example a ob/ob mouse on a mixed or a black-6 background still have the same strain.  The background is defined in the animal and breeding cages.  Strain and Strain_slug are required.
    """
    Strain = models.CharField(max_length = 100)
    Strain_slug = models.SlugField(max_length = 20, help_text="Strain name with no spaces, for use in URI's")
    Source = models.TextField(max_length = 500, blank = True)
    Comments = models.TextField (max_length = 500, blank = True)
    def __unicode__(self):
        return u'%s' % self.Strain
    def get_absolute_url(self):
        return "/mousedb/strain/%s" % self.Strain_slug

class Animal(models.Model):
    """A data model describing an animal.

    This data model describes a wide variety of parameters of an experimental animal.  This model is linked to the Strain and Cage models via 1:1 relationships.  If the parentage of a mouse is known, this can be identified (the breeding set may not be clear on this matter). Mice are automatically marked as not alive when a Death date is provided and the object is saved.  Strain, Background and Genotype are required field.  By default, querysets are ordered first by strain then by MouseID.
    """
    MouseID = models.IntegerField(max_length = 10, blank = True, null=True)
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
    Backcross = models.IntegerField(max_length = 5, null=True, blank=True, help_text="Leave blank for mixed background")
    Generation = models.IntegerField(max_length=5, null=True, blank=True)
    Breeding = models.ForeignKey('Breeding', blank=True, null=True)
    Father = models.ForeignKey('Animal', null=True, blank=True, related_name='father')
    Mother = models.ForeignKey('Animal', null=True, blank=True, related_name='mother')
    Markings = models.CharField(max_length = 100, blank=True)					
    Notes = models.TextField(max_length = 500, blank=True)
    Alive = models.BooleanField(default=True)
    def __unicode__(self):
        """This defines the unicode string of a mouse.
If a eartag is present then the string reads some_strain-Eartag #some_number. If an eartag is not present then the mouse is labelled as use some_number, where this number is the internal database identification number and not an eartag.
"""
        if self.MouseID:
            return u'%s-EarTag #%i' % (self.Strain, self.MouseID)
        elif self.id:
             return u'%s (%i)' % (self.Strain, self.id)
        else:
             return u'MOUSE'
    @models.permalink
    def get_absolute_url(self):
        return ('animal-detail', [str(self.id)])
    def save(self):
        if self.Death:
            self.Alive = False
        super(Animal, self).save()
    class Meta:
        ordering = ['Strain', 'MouseID']

class Breeding(models.Model):
    """This data model stores information about a particular breeding set

    A breeding set may contain one ore more males and females and must be defined via the progeny strain.  For example, in the case of generating a new strain, the strain indicates the new strain not the parental strains.  A breeding cage is defined as one male with one or more females.  If the breeding set is part of a timed mating experiment, then Timed_Mating must be selected.  Breeding cages are automatically inactivated upon saving when a End date is provided.  The only required field is Strain.  By default, querysets are ordered by Strain, then Start.
    """
    Females = models.ManyToManyField(Animal, blank=True, related_name="breeding_females")
    Male = models.ManyToManyField(Animal, related_name="breeding_males", blank=True) #should be males, but will have to check through the code to make sure this is ok to change
    Strain = models.ForeignKey(Strain, help_text="The strain of the progeny")
    Cage = models.CommaSeparatedIntegerField(max_length=100, blank=True, null=True)
    CageID = models.ForeignKey('Cage', blank=True, null=True)
    BreedingName = models.CharField(max_length=50, blank=True, verbose_name="Breeding Set Name")
    Start = models.DateField(blank=True, null=True)
    End = models.DateField(blank=True, null=True)
    Crosstype = models.CharField(max_length=10, choices = CROSS_TYPE, blank=True)
    Notes = models.TextField(max_length=500, blank=True)
    Rack = models.CharField(max_length = 15, blank = True)
    Rack_Position = models.CharField(max_length = 15, blank = True, verbose_name="Rack Position") 
    Active = models.BooleanField(default=True)
    Timed_Mating = models.BooleanField(default=False, help_text="Is this cage a timed mating cage?")
    def __unicode__(self):
        return u'%s Breeding Cage: %s starting on %s'  %(self.Strain, self.Cage, self.Start)
    @models.permalink
    def get_absolute_url(self):
        return ('breeding-detail', [str(self.id)])
    def save(self):
        """The save function for a breeding cage has to automatic over-rides, Active and the Cage for the Breeder.
        
        In the case of Active, if an End field is specified, then the Active field is set to False.
        In the case of Cage, if a Cage is provided, and animals are specified under Male or Females for a Breeding object, then the Cage field for those animals is set to that of the breeding cage.  The same is true for both Rack and Rack Position."""
        if self.End:
            self.Active = False
        #if self.Cage:
        #    if self.Females:               
        #        for female_breeder in self.Females:
        #            female_breeder.Cage = self.Cage
        #            female_breeder.save()
        #    if self.Male:
        #        for male_breeder in self.Male:
        #            male_breeder.Cage = self.Cage
        #            male_breeder.save()
        super(Breeding, self).save()
        #if self.Rack:
        #    if self.Male:
        #        self.Male.Rack = self.Rack
        #        self.Male.save()
        #    if self.Females:
        #        if hasattr(self.Females, '__iter__') == True:     #This is required to determine of self.animals is a queryset or a single instance                     
        #            for female_breeder in self.Females:
        #                female_breeder.Rack = self.Rack
        #                female_breeder.save()
        #            else: 
        #                self.Females.Rack = self.Rack
        #                self.Females.save()
        #if self.Rack_Position:
        #    if self.male:
        #        self.male.Rack_Position = self.Rack_Position
        #        self.male.save()
        #    if self.females:
        #        if hasattr(self.females, '__iter__') == True:     #This is required to determine of self.animals is a queryset or a single instance                     
        #            for female_breeder in self.females:
        #                female_breeder.Rack_Position = self.Rack_Position
        #                female_breeder.save()
        #            else: 
        #                self.females.Rack_Position = self.Rack_Position
        #                self.females.save()
        #super(Breeding, self).save()
    class Meta:
        ordering = ['Strain', 'Start']
		
class Cage(models.Model):
    """This data model stores information about a particular cage.  

    This model, which is not yet implemented will be used by both breeding and non-breeding cages and will facilitate easier tracking and storage of cages.  To implement this, it will be necessary to automatically generate a new cage (if a novel barcode is entered), or to use a current cage if the barcode is already present in the database
    """
    Barcode = models.IntegerField(primary_key=True)
    Rack = models.CharField(max_length = 15, blank = True)
    Rack_Position = models.CharField(max_length = 15, blank = True)
    def __unicode__(self):
        return u'%i'  % self.Barcode
