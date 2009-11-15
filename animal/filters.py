from mousedb.animal.models import Animal
from filter import *

class AnimalFilter(FilterSet):
	class Meta:
		model = Animal
		fields = ['Strain','Background','Genotype','Gender','Alive']
