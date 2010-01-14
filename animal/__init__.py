"""The animal app contains and controls the display of data about animals.

Animals are tracked as individual entities, and given associations to breeding cages to follow ancestry, and strains.

Animal
++++++
Most parameters about an animal are set within the animal object.  Here is where the animals strain, breeding, parentage and many other parameters are included.  Animals have foreignkey relationships with both Strain and Breeding, so an animal may only belong to one of each of those.  As an example, a mouse cannot come from more than one Breeding set, and cannot belong to more than one strain.

Backcrosses and Generations
---------------------------
For this software, optional tracking of backcrosses and generations is available and is stored as an attribute of an animal.  When an inbred cross is made against a pure background, the backcross increases by 1.  When a heterozygote cross is made, the generation increases by one.  As an example, for every time a mouse in a C57/BL6 background is crossed against a wildtype C57/B6 mouse, the backcross (but not the generation) increases by one.  For every time a mutant strain is crosses against itself (either vs a heterozygote or homozygote of that strain), the generation will increase by one.  Backcrosses should typically be performed against a separate colony of purebred mouse, rather than against wild-type alleles of the mutant strain.

Breeding Cages
++++++++++++++
A breeding cage is defined as a set of one or more male and one or more female mice.  Because of this, it is not always clear who the precise parentage of an animal is.  If the parentage is known, then the Mother and Father fields can be set for a particular animal.

Strains
+++++++
A strain is a set of mice with a similar genetics.  Importantly strains are separated from Backgrounds.  For example, one might have mice with the genotype ob/ob but these mice may be in either a C57-Black6 or a mixed background.  This difference is set at the individual animal level.  
The result of this is that a query for a particular strain may then need to be filtered to a specific background.
"""
