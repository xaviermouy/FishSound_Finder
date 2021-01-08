Installing FishSound Finder
===========================

Short version
-------------

FishSound Finder can be installed from `PyPI <https://pypi.org/project/echopype/>`_:

.. code-block:: console

   $ pip install fishsound_finder

It is recommended to install FishSound Finder in a separate python 3.7 conda environment.

Longer version (python beginners)
---------------------------------
If you are not very familiar with python and don't have python already installed on your machine, the following instructions will help you get everything setup.

1. **Install Anaconda:**

	The easiest way to install python on your machine is to use Anaconda. It is an easy-to-install package manager, environment manager, and Python distribution that will make your
	life much easier. To install Anaconda follow the instructions on their website `here <https://docs.anaconda.com/anaconda/install/>`_.

2. **Create a new virtual environment:**

	a. Open Anaconda Navigator (see `instructions <https://docs.anaconda.com/anaconda/navigator/getting-started>`_)	
	b. Create a new virtual environment with Python 3.7 (see `instructions <https://docs.anaconda.com/anaconda/navigator/getting-started/#managing-environments>`_)

3. **Install FishSound Finder:**

	Open a terminal window in the virtual environment (see `here <https://i0.wp.com/mikelynchgames.com/wp-content/uploads/2019/01/anacondaterminallaunch.png>`_) and type:
	
	.. code-block:: console		
	
	    $ pip install fishsound_finder


4. **Test that FishSound Finder installed correctly:**

	In the same terminal window type:
	
	.. code-block:: console		
	
	    $ fishsound_finder

	
	If everything is correctly installed, it should print the help information in the temirnal window:
	
	.. code-block:: console	
	    
		$ fishsound_finder
		
		usage: fishsound_finder [-h] [-d DEPLOYMENT_FILE] [-e EXTENSION] [-f] [-p]
								   [-r]
								   input output cfgfile model

		Run fishsound_finder

		positional arguments:
		  input                 file or directory to process
		  output                output directory
		  cfgfile               configuration file (.yaml)
		  model                 classification model file (.sav)

		optional arguments:
		  -h, --help            show this help message and exit
		  -d DEPLOYMENT_FILE, --deployment_file DEPLOYMENT_FILE
								deployment info file (.csv)
		  -e EXTENSION, --extension EXTENSION
								extension of the sound files to process (default:
								'.wav')
		  -f, --force           force reprocessing recordings whose netcdf files
								already exist in the output folder
		  -p, --pamlab          also outputs results in the PAMlab annotation format
		  -r, --raven           also outputs results in the RAVEN annotation format

		To load input arguments from a file, use @ followed by the path of the text
		file containing all arguments (e.g. python fishsound_finder.py
		@args_file_example.txt)

