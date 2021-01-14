.. FishSound Finder documentation master file, created by
   sphinx-quickstart on Tue Jan  5 22:09:22 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to FishSound Finder!
============================================

**FishSound Finder** is an open source python software to automatically detect and classify fish sounds in 
passive acoustic recordings. It is based on the high-level python library `Ecosound <https://ecosound.readthedocs.io/en/latest/>`_.
Currently, FishSound Finder is specifically configured to detect fish sounds recorded in coastal British Columbia, Canada, but
future versions will also include detectors for specific fish species and other parts of the world 
(e.g. `haddock sounds in the North Atlantic <https://asa.scitation.org/doi/10.1121/2.0001257>`_). Detection outputs from FishSound Finder
are compatible with the popular bioacoustics software `Raven <https://ravensoundsoftware.com/>`_ and 
`PAMlab <https://static1.squarespace.com/static/52aa2773e4b0f29916f46675/t/5be5b07088251b9f59268184/1541779574284/PAMlab+Brochure.pdf>`_.

.. image:: _static/detection_example.png

.. toctree::
   :maxdepth: 2
   :caption: Content:
   
   FishSound Finder <introduction.rst>
   Installation <installation.rst>
   Usage <usage.rst>
   Tutorial <example.rst>
   Contributing <contributing.rst>
   Credits <credits.rst>
   	
Status
------
FishSound Finder very much a work in progress and is still under heavy development. 
At this stage, it is recommended to contact the main contributor before using
FishSound Finder for your projects.

Contributors
------------

`Xavier Mouy <https://xaviermouy.weebly.com/>`_ (@XavierMouy) leads this project as part of his PhD in the `Juanes Lab <https://juaneslab.weebly.com/>`_ 
at the University of Victoria (British Columbia, Canada). `Stephanie Archer <https://lumcon.edu/stephanie-archer/>`_ (@ArcherEcology), and 
`Philina English <https://ecophilina.wordpress.com/>`_ (@ecophilina) provided large passive acoustic and manual annotation datasets for training 
and testing the fish sound classifier for British Columbia. Emie Woodburn and Courtney Evans also provided manually annotated fish sounds.

License
-------
FishSound Finder is licensed under the open source `BSD-3-Clause License <https://choosealicense.com/licenses/bsd-3-clause/>`_.
