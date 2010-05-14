from django.db import models

TITLE_CHOICES = (
	('Dr.','Dr.'),
	('Mr.','Mr.'),
	('Ms.','Ms.'),
	('Mrs.','Mrs.'),
	('Prof.','Prof'),
)

class Group(models.Model):
	group = models.CharField(max_length = 100, help_text="Name of this Group, i.e. Saltiel Laboratory")
	group_slug = models.SlugField(max_length=30, blank=True, help_text = "Short Name of this Group")
	group_url = models.URLField(verify_exists=True, blank=True, verbose_name="Group Website")
	license = models.ForeignKey('License', blank=True, null=True, help_text = "Data Availability License")
	contact_title = models.CharField(max_length=10, choices=TITLE_CHOICES, blank=True, verbose_name="Contact (Title)")
	contact_first = models.CharField(max_length=20, blank=True, verbose_name="Contact (First Name)")
	contact_last = models.CharField(max_length=30, blank=True, verbose_name="Contact (Last Name)")
	contact_email = models.EmailField(blank=True, verbose_name="Contact (Email)")
	def __unicode__(self):
		return u"%s" % self.group

class License(models.Model):
	license = models.CharField(max_length=100)
	website = models.URLField(verify_exists=True, blank=True)
	notes = models.TextField(max_length=100, blank=True)
	def __unicode__(self):
		return u"%s" % self.license
	
	

