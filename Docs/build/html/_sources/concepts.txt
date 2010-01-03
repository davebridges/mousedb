MouseDB Concepts
================

Data storage for MouseDB is separated into packages which contain information about animals, and information collected about animals.  There is also a separate module for timed matings of animals.  This document will describe the basics of how data is stored in each of these modules.

Animal Module
-------------
Animals are tracked as individual entities, and given associations to breeding cages to follow ancestry, and strains.

Animal
++++++
Most parameters about an animal are set within the animal object.  Here is where the animals strain, breeding, parentage and many other parameters are included.  Animals have foreignkey relationships with both Strain and Breeding, so an animal may only belong to one of each of those.  As an example, a mouse cannot come from more than one Breeding set, and cannot belong to more than one strain.

Breeding Cages
++++++++++++++
A breeding cage is defined as a set of one or more male and one or more female mice.  Because of this, it is not always clear who the precise parentage of an animal is.  If the parentage is known, then the Mother and Father fields can be set for a particular animal.

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




