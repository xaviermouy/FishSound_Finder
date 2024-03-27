.. FishSound Finder documentation master file, created by
   sphinx-quickstart on Tue Jan  5 22:09:22 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to FishSound Finder!
============================================

**FishSound Finder** is an open source python software to automatically detect and classify fish sounds in 
passive acoustic recordings. It is based on the python libraries `ecosound <https://ecosound.readthedocs.io/en/latest/>`_ and 
`ketos <https://docs.meridian.cs.dal.ca/ketos/>`_. FishSound Finder was trained to detect typical low frequency (< 1kHz) isolated grunts and knocks produced by fish. 
Future versions will also include the capability to detect sounds from specific fish species (e.g. haddock).
It was originally developed to analyze fish sounds found in coastal British Columbia (Canada) but proved to also work well in other parts of the world (e.g. Florida, USA).
Detection outputs from FishSound Finder are compatible with the popular bioacoustics software `Raven <https://ravensoundsoftware.com/>`_.

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
FishSound Finder has been tested on a number of different environments and is considered stable. We are keen to keep improving FishSound Finder and 
encourage users to get in touch with us to provide feedback and report issues/bugs.

Contributors
------------

Lead developper:

* `Xavier Mouy <https://xaviermouy.weebly.com/>`__

Collaborators:

* `Dana Haggarty <https://profils-profiles.science.gc.ca/en/profile/dana-haggarty-phd-msc>`__

* `Francis Juanes <https://juaneslab.weebly.com/>`__

* `Stephanie Archer <https://lumcon.edu/stephanie-archer/>`__

* `Philina English <https://ecophilina.wordpress.com/>`__

* `Sarah Dudas <https://sogdatacentre.ca/people/researchers/sarah-dudas/>`__

* `Darienne Lancaster <https://www.researchgate.net/scientific-contributions/Darienne-Lancaster-2163078290>`__


Analysts :


* Cierra Hart

* Courtney Evans

* Emie Woodburn

* Erik Archer 


License
-------
FishSound Finder is licensed under the open source `BSD-3-Clause License <https://choosealicense.com/licenses/bsd-3-clause/>`__.
