"""The data module describes the conditions and collection of data regarding experimental animals.

Data (or :class:`~mousedb.data.Measurement`) can be stored for any type of :class:`~mousedb.data.Experiment`.  Conceptually, several pieces of data belong to an experiment (for example several :class:`~mousedb.animal.Animal` are measured at some time) and several :class:`~mousedb.data.Experiment` belong to a :class:`~mousedb.data.Study`.  

Measurements can be stored independent of experiments and experiments can be performed outside of the context of a study.  It is however, perfered that measurements are stored within an experiment and experiments are stored within studies as this will greatly facilitate the organization of the data.

Studies
+++++++
In general studies are a collection of experiments.  This is a large class which can contain several class:`~mousedb.data.Experiment` objects.  Within a study two classes control how data is stored, :class:`~mousedb.data.Treatment` and :class:`~mousedb.data.Cohort`.  

Treatments
++++++++++

A :class:`~mousedb.data.Treatment` is a group of class:`~mousedb.animal.Animal` that are grouped together based on some manipulation, which could be a class:`~mousedb.data.Pharmaceutical`, class:`~mousedb.data.Diet`, class:`~mousedb.data.Implantation` or some other manipulation.  Generally a class:`~mousedb.data.Study` will have two or more class:`~mousedb.data.Treatment` groups.

Cohorts
+++++++

For the same :class:`~mousedb.data.Treatment` groups, within a :class:`~mousedb.data.Study`, there may be several independent replicates of those treatment.  A replicate are called :class:`~mousedb.data.Cohort`.  For example, there could be a :class:`~mousedb.data.Treatment` in which some mice get a particular :class:`~mousedb.data.Diet`, while other mice get a diffferent :class:`~mousedb.data.Diet`.  These two :class:`~mousedb.data.Treatment` groups are designated within a cohort.  Later on, using different :class:`~mousedb.animal.Animal` sets, this :class:`~mousedb.data.Study` will be repeated.  While the :class:`~mousedb.data.Treatment` groupings are the same, the different series' of :class:`~mousedb.data.Experiment` will be separated by being part of a different :class:`~mousedb.data.Cohort`.

Experiments
+++++++++++

An experiment is a collection of measurements for a given set of animals.  In general, an experiment is defined as a number of measurements take in a given day.

Measurements
++++++++++++

A measurement is an animal, an assay and a measurement value.  It can be associated with an experiment, or can stand alone as an individual value.  Measurements can be viewed in the context of a study, an experiment, a treatment group or an animal by going to the appropriate page.
"""
