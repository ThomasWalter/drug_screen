Analysis of the drug screen
===========================

.. role:: red

8/08/2016: First step: data set for a new classifier for the drug screen data
------------------------------------------------------------------------------

.. _plateview: http://olympia.biomedicale.univ-paris5.fr/plates/

We have noticed that appliction of the mitocheck-classifier seems to
be sub-optimal. Therefore, I train a new classifier on the drug
data. 

First, I had to select the movies. This was done with the help of the
plate views on plateview_

There I selected spots for different drugs, some spots with no or
little effect (including also empty), most spots however with either
medium or strong effect. The objective is to avoid missing interesting
morphologies. Altogether, I selected 28 conditions, all with 2
fields (56 movies). Each movie was selected in triplicates (from
labteks LT0900_01, LT0900_02, LT0900_05). 

10/08/2016: Technical issues
----------------------------

There were several technical issues. 

First, the channel naming varied with the plate (either ``Cy3`` or
``b_cy3``). I therefore renamed, so that the channel is now always
``Cy3``. 
This is done with the script ``src/rename_files.py``


Second, there is sometimes a high background. In principle, this does
not hurt for the segmentation, as the background is removed. But
CellCognition does a conversion to 8bit images, which is the same for
all movies. Consequently, images with a high background might actually
experience a reduction of the dynamic range. I therefore subtracted
the offset of all images by subtracting the 5%-percentile from each
image ``src/offset_correction.py`` 

12/08/2016: Annotation of morphologies
--------------------------------------

I annotated morphologies, from these movies. Several
observations: 

- There were conditions in which the prometaphases looked very
  different from what has been in the training set. The nuclei were
  very small and chromatine very condensed, so that they can be easily
  confounded with apoptotic nuclei. This was typically followed by
  decondensation (with polylobed or grape shaped nuclei as a
  consequence). 
- There were some conditions, where a particular polylobed morphology
  appeared (with a kidney shape). This shape does not seem to relate
  to segregation defects, and thus not to mitotic phenotypes. It is
  possible that this morphology also exists in the Mitocheck data
  set. 
- There were no dynamic nuclei, no elongated nuclei, very few
  binuclear nuclei, few artefact classes (splitting worked nicely!). 
- As we use a split strategy, it is difficult to detect the polylobed
  systematically. Sometimes they are not split however, so that I
  could annotate some. This problem has already occurred in the
  Mitocheck data set (for which we also applied a split algorithm,
  which was necessary for the tracking). 

This rises a number of questions. 

1. What do we do with classes that are apparently not present (in the
   sample I looked at)? Are they maintained in the classifier or do we
   just remove them from the profiles (eventually putting them to zero)?  
2. If we maintain classes that were not annotated in the data set,
   this would refer to using a combined classifier. For this, we need to
   join classifiers by combining arff-files (see below).  
3. Do we reprocess the mitocheck data set (only classification!) in
   order to find kidney-shaped nuclei (by a combined classifier)?  

Regarding question (1), I think that both alternatives can be
tested. For this, I built a classifier with only those morphologies
that were actually present in the drug data set (2420 nuclei). This is
the corresponding classifier (I removed the image data from version
control): ``cecog_classifiers/classifier_2016_08_10_only_observed_classes``. 

This is in any case a working solution. The kidney class can be either
removed or joined with polylobed or interphase, or maintained in the
drug-screen data and not in the mitocheck data set. As a matter of
fact, we could argue that this kind of situation is typical when
comparing screens, and that the EMD allows us to compare profiles with
different classes, as long as we can define a cost matrix between the
classes.  

In order to build a joined classifier, I made a script that joins two
arff files: ``src/join_classifiers.py``

This seems to work, but at the moment, I cannot train the classifier
in CellCognition without picking. I need to check this still. 

Finally, we have to decide, what to do with the kidney-shape class. My
feeling is that if we find a new class in the mitocheck data and if
this class allows us to find the molecular targets of this drug, this
will be a strong argument and a nice result. But there are many
"ifs": it might be that this morphology will actually introduce more
problems than benefits. I think we can take the risk and look what's
coming out. 

There are also still some technical issues related to the compilation
on the cluster: the system has been updated, and at the moment
cellcognition does not run because of several dependencies. I
re-compiled qt and PyQt. At the moment I am blocked by lxml (for which
I need the assistance of IT). 

