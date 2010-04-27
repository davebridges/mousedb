from django.db import models

TITLE_CHOICES = (
	('Dr.','Dr.'),
	('Mr.','Mr.'),
	('Ms.','Ms.'),
	('Mrs.','Mrs.'),
	('Prof.','Prof'),
)

class Group(models.Model):
    """This defines the data structure for the Group model.

    The only required field is group.
    All other fields (group_slug, group_url, license, contact_title, contact_first, contact_last and contact_email) are optional."""
    group = models.CharField(max_length = 100, help_text="Name of this Group, i.e. Smith Laboratory")
    group_slug = models.SlugField(max_length=30, blank=True, help_text = "Shortened Name of this Group")
    group_url = models.URLField(verify_exists=True, blank=True, verbose_name="Group Website")
    license = models.ForeignKey('License', blank=True, null=True, help_text = "Data Availability License")
    contact_title = models.CharField(max_length=10, choices=TITLE_CHOICES, blank=True, verbose_name="Contact (Title)")
    contact_first = models.CharField(max_length=20, blank=True, verbose_name="Contact (First Name)")
    contact_last = models.CharField(max_length=30, blank=True, verbose_name="Contact (Last Name)")
    contact_email = models.EmailField(blank=True, verbose_name="Contact (Email)")
    def __unicode__(self):
        return u"%s" % self.group

class License(models.Model):
    """This defines the data structure for the License model.

    The only required field is license.
    If the contents of this installation are being made available using some licencing criteria this can either be defined in the notes field, or in an external website."""
    license = models.CharField(max_length=100)
    website = models.URLField(verify_exists=True, blank=True, help_text="Website defining License information") 
    notes = models.TextField(max_length=100, blank=True)
    def __unicode__(self):
        return u"%s" % self.license
	
	

