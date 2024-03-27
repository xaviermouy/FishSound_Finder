FishSound Finder
================

Why FishSound Finder?
---------------------

Some fish produce sounds to find mates, defend their territory, or keep cohesion within their group.
Scientists can use these sounds to detect the presence, the diversity, and potentially the number of fish in an environment,
over large areas and long time periods. However, manually going through passive acoustic recordings to find fish sounds is a long, costly,
and tedious process that limits the usefulness of passive acoustics for monitoring fish. The objective of FishSound Finder is to make
that process easier and more efficient by automatically finding fish sounds in acoustic recordings. Of course, automatic
detectors are not perfect and still require some degree of manual analysis. However, this approach makes the analysis of large datasets
more feasible. Some fish sound detectors have been developed by the scientific community over the years, however they are not often made
open-source, which limits their usability. By making FishSound Finder open-source, we hope that ecologists that are not so
familiar with acoustics will be able to integrate more easily passive acoustics in their own study. It is also our hope that more people
can contribute to the source code to improve the performance and add new functionalities to FishSound Finder.  

What can I use it for?
----------------------
FishSound Finder can be used for many different things. If you are working on fish sounds in a laboratory setting (i.e., tanks), it can make the
annotation of fish sounds more efficient. If you are working in a natural setting (e.g. lakes, rivers, ocean), it can be used to study fish sound
repertoire, fish occurrence, or biodiversity over several month of data and over several locations. Such large scale studies are just not feasible without the use of 
automatic detectors. Examples of large scale studies using fish sounds include monitoring of sensitive habitats for marine conservation 
(e.g. glass sponge reefs off British Columbia, `Archer et al., 2018 <http://www.int-res.com/abstracts/meps/v595/p245-252/>`__) or detection of spawning events for fisheries management 
(e.g. haddock in the Gulf of Maine, `Rountree et al., 2020 <https://asa.scitation.org/doi/pdf/10.1121/2.0001257>`__).

Does it work in all environments?
---------------------------------
It was initially developped to detect fish sounds from the Northeast Pacific but was also succesfully tested in other parts of the world (e.g. Florida, USA).
Using FishSound Finder outside of the Northeast Pacific will typically require to use lower confidence thresholds. It is anticipated that in the future, FishSound Finder will have the option to
detect species-specific sounds. Most likely candidates are haddock sounds in the Northwest Atlantic 
(`Mouy et al. 2018 <https://asa.scitation.org/doi/10.1121/1.5036179>`__), and lingcod sounds off British Columbia 
(`Mouy et al., 2019 <https://asa.scitation.org/doi/10.1121/1.5136904>`__). 

How does it work?
-----------------

FishSound Finder uses signal processing and deep learning techniques. The process is as follows.
 
1. The spectrogram of the sound recording is computed. 
2. A median filter is applied to each row (frequency band) of the spectrogram to remove tonal sounds and increase the signal-to-noise ratio of acoustic transients. 
3. A deep convolutional neural network (ResNet18) is then analysing consecutive sections of the spectrogram (typically 0.2 s at a time) to calculate the probability that a fish sound is present. Sections of the spectrogram that have a probability greater than the user-defined threshold will be defined as "detections". The ResNet model was trained on about 20,000 manually annotated fish and non-fish sounds collected at 7 different locations is the Strait of Georgia (British Columbia) by different model of recorders (AMAR, SoundTrap, IcListen). 

A peer-reviewed scientific publication fully describing the approach and performance results is in the works and will be published in the near future.

Who can use it?
--------------------
Anyone interested in studying the underwater sounds and marine ecology can use FishSound Finder. No programming knowledge are required to run it. Reading the
:ref:`tutorial section<Tutorial>` of this documentation should be enough to get you started. FishSound Finder is also compatible with standard bioacoustic analysis tools such as
Raven (Cornell University). More advanced users/developers can also look at the source code to better understand it and modify
it as they need. 

Requirements
------------
FishSound Finder requires to have Python 3.9 installed on your machine(s). It is based on the high-level python library 
`ecosound <https://ecosound.readthedocs.io/en/latest/>`__ and `ketos <https://docs.meridian.cs.dal.ca/ketos/>`_ which themselves are built on top of lower-level python libraries such as numpy, scipy, dask, tensorflow,
pandas and Xarray.

Contributors
------------

Xavier Mouy leads this project in collaboration with Dana Haggarty (DFO), Francis Juanes (UVic), Stephanie Archer (LUMCON), Philina English (DFO), Sarah Dudas (DFO) and Darienne Lancaster (UVIC).
Aislyn Adams, Cierra Hart, Courtney Evans, Emie Woodburn, and Erik Archer also provided manually annotated fish sounds. 