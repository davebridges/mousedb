"""
This is file containing custom model fields.

This is modified from http://stackoverflow.com/questions/3397400/django-model-field-for-storing-a-list-of-floats/3398546#3398546

There is also a class to uniquely slugify a field
"""
import re
from django.db.models import CharField
from django.core import validators
from django.template.defaultfilters import slugify

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^mousedb\.custom_fields\.CommaSeparatedFloatField"])

comma_separated_float_list_re = re.compile('^([-+]?\d*\.?\d+[,\s]*)+$')
validate_comma_separated_float_list = validators.RegexValidator(
              comma_separated_float_list_re, 
              (u'Enter only floats separated by commas.'), 'invalid')

class CommaSeparatedFloatField(CharField):
    """A custom field for comma separated float values."""
    default_validators = [validate_comma_separated_float_list]
    description = ("Comma-separated floats")

    def formfield(self, **kwargs):
        defaults = {
            'error_messages': {
                'invalid': (u'Enter only floats separated by commas.'),
            }
        }
        defaults.update(kwargs)
        return super(CommaSeparatedFloatField, self).formfield(**defaults)
        
def SlugifyUniquely(value, model, slugfield="slug"):
        """Returns a slug on a name which is unique within a model's table

        This code suffers a race condition between when a unique
        slug is determined and when the object with that slug is saved.
        It's also not exactly database friendly if there is a high
        likelyhood of common slugs being attempted.

        A good usage pattern for this code would be to add a custom save()
        method to a model with a slug field along the lines of:

                from django.template.defaultfilters import slugify

                def save(self):
                    if not self.id:
                        # replace self.name with your prepopulate_from field
                        self.slug = SlugifyUniquely(self.name, self.__class__)
                super(self.__class__, self).save()

        Original pattern discussed at
        http://www.b-list.org/weblog/2006/11/02/django-tips-auto-populated-fields
        
        This code was taken from https://code.djangoproject.com/wiki/SlugifyUniquely 
        """
        suffix = 0
        potential = base = slugify(value)
        while True:
                if suffix:
                        potential = "-".join([base, str(suffix)])
                if not model.objects.filter(**{slugfield: potential}).count():
                        return potential
                # we hit a conflicting slug, so bump the suffix & try again
                suffix += 1        


