MouseDB Concepts
================

Data storage for MouseDB is separated into packages which contain information about animals, and information collected about animals.  There is also a separate module for timed matings of animals.  This document will describe the basics of how data is stored in each of these modules.

Animal Module
-------------
Animals are tracked as individual entities, and given associations to breeding cages to follow ancestry, and strains.

Animal
++++++
Most parameters about an animal are set within the animal object.  Here is where the animals strain, breeding, parentage and many other parameters are included.  Animals have foreignkey relationships with both Strain and Breeding, so an animal may only belong to one of each of those.  As an example, a mouse cannot come from more than one Breeding set, and cannot belong to more than one strain.

Backcrosses and Generations
...........................
For this software, optional tracking of backcrosses and generations is available and is stored as an attribute of an animal.  When an inbred cross is made against a pure background, the backcross increases by 1.  When a heterozygote cross is made, the generation increases by one.  As an example, for every time a mouse in a C57/BL6 background is crossed against a wildtype C57/B6 mouse, the backcross (but not the generation) increases by one.  For every time a mutant strain is crosses against itself (either vs a heterozygote or homozygote of that strain), the generation will increase by one.  Backcrosses should typically be performed against a separate colony of purebred mouse, rather than against wild-type alleles of the mutant strain.

Breeding Cages
++++++++++++++
A breeding cage is defined as a set of one or more male and one or more female mice.  Because of this, it is not always clear who the precise parentage of an animal is.  If the parentage is known, then the Mother and Father fields can be set for a particular animal.  In the case of Active, if an End field is specified, then the Active field is set to False.  In the case of Cage, if a Cage is provided, and animals are specified under Male or Females for a Breeding object, then the Cage field for those animals is set to that of the breeding cage.  The same is true for both Rack and Rack Position.

Strains
+++++++
A strain is a set of mice with a similar genetics.  Importantly strains are separated from Backgrounds.  For example, one might have mice with the genotype ob/ob but these mice may be in either a C57-Black6 or a mixed background.  This difference is set at the individual animal level.  
The result of this is that a query for a particular strain may then need to be filtered to a specific background.


Data Module
-----------
Data (or measurements) can be stored for any type of measurement.  Conceptually, several pieces of data belong to an experiment (for example several mice are measured at some time) and several experiments belong to a study.  Measurements can be stored independent of experiments and experiments can be performed outside of the context of a study.  It is however, perfered that measurements are stored within an experiment and experiments are stored within studies as this will greatly facilitate the organization of the data.

Studies
+++++++
In general studies are a collection of experiments.  These can be grouped together on the basis of animals and/or treatment groups.  A study must have at least one treatment group, which defines the animals and their conditions.

Experiments
+++++++++++
An experiment is a collection of measurements for a given set of animals.  In general, an experiment is defined as a number of measurements take in a given day.

Measurements
++++++++++++
A measurement is an animal, an assay and a measurement value.  It can be associated with an experiment, or can stand alone as an individual value.  Measurements can be viewed in the context of a study, an experiment, a treatment group or an animal by going to the appropriate page.

Timed Matings Module
--------------------
Timed matings are a specific type of breeding set.  Generally, for these experiments a mating cage is set up and pregnancy is defined by a plug event.  Based on this information, the age of an embryo can be estimated.  When a breeding cage is defined, one option is to set this cage as a timed mating cage (ie Timed_Mating=True).  If this is the case, then a plug event can be registered and recorded for this mating set.  If the mother gives birth then this cage is implicitly set as a normal breeding cage.

Groups Module
-------------
This app defines generic Group and License information for a particular installation of MouseDB.  Because every page on this site identifies both the Group and data restrictions, at a minimum, group information must be provided upon installation (see installation instructions).
