'''The veterinary app contains models for MedicalCondition, MedicalIssue and MedicalTreatment.'''

from django.db import models
from django.template.defaultfilters import slugify

from mousedb.animal.models import Animal

class MedicalIssue(models.Model):
    '''This model contains details about a particular medical issue.
    
    There is links to the :class:`~mousedb.animal.models.Animal`, the :class:`~mousedb.veterinary.models.MedicalCondition` and the :class:`~mousedb.veterinary.models.MedicalTreatment` choice.
    The required fields are the animal and the condition.
    There are also fields for the diagnosis date, veterinary code, treatment start and treatment end dates (not required).'''
    
    animal = models.ForeignKey(Animal)
    condition = models.ForeignKey('MedicalCondition', help_text = "The medical problem")
    treatment = models.ForeignKey('MedicalTreatment', blank=True, null=True, help_text = "The course of treatment")
    diagnosis = models.DateField(blank=True, null=True, help_text = "When this problem was noticed")
    code = models.CharField(max_length=25,blank=True, null=True, help_text = "Veterinary Code")
    treatment_start = models.DateField(blank=True, null=True, help_text = "When treatment began")
    treatment_end = models.DateField(blank=True, null=True, help_text = "When treatment ceased")
    
    def __unicode__(self):
        '''The unicode representation is the animal field combined with the condition field.'''    
        return u'%s - %s' % (self.animal, self.condition) 
        
    @models.permalink
    def get_absolute_url(self):
        '''The url of a medical issue is **/veterinary/medical-issue/<id#>/**.'''
        return ('medical-issue-detail', [str(self.id)])             
    
class MedicalCondition(models.Model):
    '''This model contains details about different types of medical conditions.
    
    The only required field is the name.
    There are auto-generated slug field and created and updated fields.
    The slug field is not updated upon repeated saves, only on the first save for persistence.
    There is also an optional notes field for extra information.'''
    
    name = models.CharField(max_length = 100, unique=True)
    slug = models.SlugField(max_length = 100, editable=False)
    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        '''The unicode representation is the name field.'''    
        return u'%s' % self.name
        
    @models.permalink
    def get_absolute_url(self):
        '''The url of a medical issue is **/veterinary/medical-condition/<slug>/**.'''    
        return ('medical-condition-detail', [str(self.slug)])            
    
    def save(self, *args, **kwargs):
        '''The save method is over-ridden to generate and save the slug field.  This is only done with create, not update.'''
        if not self.id:
            self.slug = slugify(self.name)
        super(MedicalCondition, self).save(*args, **kwargs)    
    
class MedicalTreatment(models.Model):
    '''This model defines details about a medical treatment.
    
    There is one required field (name), the treatment name and one auto-generated field (slug).'''   
    
    name = models.CharField(max_length = 100, unique=True)
    slug = models.SlugField(max_length = 100, editable=False)
    
    def __unicode__(self):
        '''The unicode representation is the name field.'''
        return u'%s' % self.name 
        
    @models.permalink
    def get_absolute_url(self):
        '''The url of a medical issue is **/veterinary/medical-treatment/<slug>/**.'''    
        return ('medical-treatment-detail', [str(self.slug)])             
            
    def save(self, *args, **kwargs):
        '''The save method is over-ridden to generate and save the slug field.  This is only done with create, not update.'''
        if not self.id:
            self.slug = slugify(self.name)
        super(MedicalTreatment, self).save(*args, **kwargs)
