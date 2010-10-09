"""This defines the data model for the timed_mating app.

Currently the only data model is for PlugEvents."""

from django.db import models
from django.contrib.auth.models import User

from mousedb.animal.models import Animal, Strain, Breeding

class PlugEvents(models.Model):
    """This defines the model for PlugEvents.

    A PlugEvent requires a date.  All other fields are optional.
    Upon observation of a plug event, the PlugDate, Breeding Cage, Femalem, Male, Researcher and Notes can be set.
    Upon sacrifice of the mother, then genotyped alive and dead embryos can be entered, along with the SacrificeDate, Researcher and Notes."""
    Breeding = models.ForeignKey(Breeding, blank=True, null=True)
    PlugDate = models.DateField()
    PlugFemale = models.ForeignKey(Animal, blank=True, related_name='PlugFemale', null=True)
    PlugMale = models.ForeignKey(Animal, blank=True, related_name='PlugMale', null=True)
    SacrificeDate = models.DateField(blank=True, null=True)
    Researcher = models.ForeignKey(User, blank=True, null=True, default='6')
    WT_Alive = models.IntegerField(blank=True, null=True, help_text="Surviving WT Embryos")
    HET_Alive = models.IntegerField(blank=True, null=True, help_text="Surviving HET Embryos")
    KO_Alive = models.IntegerField(blank=True, null=True, help_text="Surviving KO Embryos")
    WT_Dead = models.IntegerField(blank=True, null=True, help_text="Nonviable WT Embryos")
    HET_Dead = models.IntegerField(blank=True, null=True, help_text="Nonviable HET Embryos")
    KO_Dead = models.IntegerField(blank=True, null=True, help_text="Nonviable KO Embryos")
    Active = models.BooleanField(default=True)
    Notes = models.TextField(max_length=250, blank=True)
    def __unicode__(self):
        return u'Plug Event - %i' % self.id
    def get_absolute_url(self):
        return "/timedmating/plug/%i" % self.id
    def save(self):
        """Over-rides the default save function for PlugEvents.

        If a sacrifice date is set for an object in this model, then Active is set to False."""
        if self.SacrificeDate:
            self.Active = False
        super(PlugEvents, self).save()
    class Meta:
        verbose_name = "Plug Events"
        verbose_name_plural = "Plug Events"
	
