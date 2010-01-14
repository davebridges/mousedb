"""The data module describes the conditions and collection of data regarding experimental animals.

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
"""
