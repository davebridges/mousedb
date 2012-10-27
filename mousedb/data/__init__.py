"""The data module describes the conditions and collection of data regarding experimental animals.

Data (or :class:`~mousedb.data.models.Measurement`) can be stored for any type of :class:`~mousedb.data.models.Experiment`.  Conceptually, several pieces of data belong to an experiment (for example several :class:`~mousedb.animal.models.Animal` are measured at some time) and several :class:`~mousedb.data.models.Experiment` belong to a :class:`~mousedb.data.models.Study`.  

Measurements can be stored independent of experiments and experiments can be performed outside of the context of a study.  It is however, perfered that measurements are stored within an experiment and experiments are stored within studies as this will greatly facilitate the organization of the data.

Studies
+++++++
In general studies are a collection of experiments.  This is a large class which can contain several :class:`~mousedb.data.models.Experiment` objects.  Within a study two classes control how data is stored, :class:`~mousedb.data.models.Treatment` and :class:`~mousedb.data.models.Cohort`.  

Treatments
++++++++++

A :class:`~mousedb.data.models.Treatment` is a group of :class:`~mousedb.animals.models.Animal` that are grouped together based on some manipulation, which could be a :class:`~mousedb.data.models.Pharmaceutical`, :class:`~mousedb.data.models.Diet`, :class:`~mousedb.data.models.Implantation` or some other manipulation.  Generally a :class:`~mousedb.data.models.Study` will have two or more :class:`~mousedb.data.models.Treatment` groups.

Cohorts
+++++++

For the same :class:`~mousedb.data.models.Treatment` groups, within a :class:`~mousedb.data.models.Study`, there may be several independent replicates of those treatment.  A replicate are called :class:`~mousedb.data.models.Cohort`.  For example, there could be a :class:`~mousedb.data.models.Treatment` in which some mice get a particular :class:`~mousedb.data.models.Diet`, while other mice get a diffferent :class:`~mousedb.data.models.Diet`.  These two :class:`~mousedb.data.models.Treatment` groups are designated within a cohort.  Later on, using different :class:`~mousedb.animal.models.Animal` sets, this :class:`~mousedb.data.models.Study` will be repeated.  While the :class:`~mousedb.data.models.Treatment` groupings are the same, the different series' of :class:`~mousedb.data.models.Experiment` will be separated by being part of a different :class:`~mousedb.data.models.Cohort`.

Experiments
+++++++++++

An experiment is a collection of measurements for a given set of animals.  In general, an experiment is defined as a number of measurements take in a given day.

Measurements
++++++++++++

A measurement is an animal, an assay and a measurement value.  It can be associated with an experiment, or can stand alone as an individual value.  Measurements can be viewed in the context of a study, an experiment, a treatment group or an animal by going to the appropriate page.
"""
