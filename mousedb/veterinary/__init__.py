'''The veterinary app is for medical issues associated with animals.

The primary functions of this app are to:

* Store data about mice which have some medical problem
* Describe the problem including its duration.
* Store details about the treatment of that problem.

As such there are three data structures in this app including :class:`~mousedb.veterinary.models.MedicalIssue`, the master model with links to:

* :class:`~mousedb.veterinary.MedicalCondition, which generically describes the condition.
* :class:`~mousedb.veterinary.MedicalTreatment, which describes the treatment response.

The goal of this app is to more accurately systematize medical data, and to link that data back to differences in strains or mice.``'''