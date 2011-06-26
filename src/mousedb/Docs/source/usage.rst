Users and Restriction
=====================
All pages in this database are restricted to logged-in users.  It is also recommended that data is secured by only allowing access of specific IP addresses.  For more details on this see the documentation for your webserver software (for example, for Apache see here http://httpd.apache.org/docs/2.2/howto/access.html).  Each database should have at least one superuser, and that user can create and designate permissions for other users.  When a user does not have the permissions to view a page or to edit something, the link to that page will not be visible and if they enter the address, they will be redirected to a login page.

Creating New Users
++++++++++++++++++
Create users by going to **../mousedb/admin/auth/user/add/** and filling in both pages of the form.  Permissions are set by going to **../mousedb/admin/auth/user/** selecting the user and manually moving the permissions from the box on the left to the box on the right.  If you want the user to have access to the admin site, select staff.  Only select superuser if you want that user to have all permissions.  Users can change passwords on the administration site as well.

Removing Users
++++++++++++++
Remove inactive users by selecting their username from the **../mousedb/admin/auth/user/** page and deselecting the active box.  Only delete a user if it was generated mistakenly and that the particular user had not been used to edit any data.

Animal Data Entry
=================

Newborn Mice or Newly Weaned Mice
+++++++++++++++++++++++++++++++++
1. Go to Breeding Cages Tab
2. Click on Add/Wean Pups Button
3. Each row is a new animal.  If you accidentaly enter an extra animal, check off the delete box then submit.
4. Leave extra lines blank if you have less than 10 mice to enter
5. If you need to enter more than 10 mice, enter the first ten and submit them.  Go back and enter up to 10 more animals (10 more blank spaces will appear)

Newborn Mice
++++++++++++
1. Enter Breeding Cage under Cage
2. Enter Strain
3. Enter Background (normally Mixed or C57BL/6-BA unless from the LY breeding cages in which case it is C57BL/6-LY5.2)
4. Enter Birthdate in format YYYY-MM-DD
5. Enter Generation and Backcross

Weaning Mice
++++++++++++
1. If not previously entered, enter data as if newborn mice
2. Enter gender
3. Enter Wean Date in format YYYY-MM-DD
4. Enter new Cage number for Cage

Cage Changes (Not Weaning)
++++++++++++++++++++++++++
1. Find mouse either from animal list or strain list
2. Click the edit mouse button
3. Change the Cage, Rack and Rack Position as Necessary

Genotyping or Ear Tagging
+++++++++++++++++++++++++
1. Find mouse either from animal list or strain list, or through breeding cage
2. Click the edit mouse button or the Eartag/Genotype/Cage Change/Death Button
3. Enter the Ear Tag and/or select the Genotype from the Pull Down List

Marking Mice as Dead
++++++++++++++++++++

Dead Mice (Single Mouse)
------------------------
1. Find mouse from animal list or strain list
2. Click the edit mouse button
3. Enter the death date in format YYYY-MM-DD
4. Choose Cause of Death from Pull Down List

Dead Mice (Several Mice)
------------------------
1. Find mice from breeding cages
2. Click the Eartag/Genotype/Cage Change/Death Button
3. Enter the death date in format YYYY-MM-DD
4. Choose the Cause of Death from Pull Down List



Studies and Experimental Setup
==============================
Set up a new study at /mousedb/admin/data/study/ selecting animals

You must put a description and select animals in one or more treatment groups

If you have more than 2 treatment groups save the first two, then two more empty slots will appear. For animals, click on the magnifying glass then find the animal in that treatment group and click on the MouseID. The number displayed now in that field will not be the MouseID, but don't worry its just a different number to describe the mouse. To add more animals, click on the magnifying glass again and select the next animal. There should be now two numbers, separated by commas in this field. Repeat to fill all your treatment groups. You must enter a diet and environment for each treatment. The other fields are optional, and should only be used if appropriate. Ensure for pharmaceutical, you include a saline treatment group. 


Measurement Entry
=================

Studies
+++++++
If this measurement is part of a study (ie a group of experiments) then click on the plus sign beside the study field and enter in the details about the study and treatment groups.  Unfortunately until i can figure out how to filter the treatment group animals in the admin interface, at each of the subsequent steps you will see all the animals in the database (soon hopefully it will only be the ones as part of the study group).

Experiment Details
++++++++++++++++++
- Pick experiment date, feeding state and resarchers
- Pick animals used in this experiment (the search box will filter results)
- Fasting state, time, injections, concentration, experimentID and notes are all optional

Measurements
++++++++++++
- There is room to enter 14 measurements.  If you need more rows, enter the first 14 and select "Save and Continue Editing" and 14 more blank spots will appear.
- Each row is a measurement, so if you have glucose and weight for some animal that is two rows entered.
- For animals, click on the magnifying glass then find the animal in that treatment group and click on the MouseID. The number displayed now in that field will not be the MouseID, but don't worry its just a different number to describe the mouse.
- For values, the standard units (defined by each assay) are mg for weights, mg/dL for glucose and pg/mL for insulin).  You must enter integers here (no decimal places).  If you have several measurements (ie several glucose readings during a GTT, enter them all in one measurement row, separated by commas and *NO spaces*).
