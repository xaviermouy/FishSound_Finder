Installing FishSound Finder
===========================

Short version
-------------

FishSound Finder can be installed from `PyPI <https://pypi.org/project/echopype/>`__ :

.. code-block:: console

   $ pip install fishsound_finder

It is recommended to install FishSound Finder in a separate python 3.9 conda environment.

Longer version (python beginners)
---------------------------------
If you are not very familiar with python and don't have python already installed on your machine, the following instructions will help you get everything setup.

1. **Install Anaconda:**

	The easiest way to install python on your machine is to use Anaconda. It is an easy-to-install package manager, environment manager, and Python distribution that will make your
	life much easier. To install Anaconda follow the instructions on their website `here <https://docs.anaconda.com/anaconda/install/>`__.

2. **Create a new virtual environment:**

	a. Open Anaconda Navigator (see `instructions <https://docs.anaconda.com/anaconda/navigator/getting-started>`__)	
	b. Create a new virtual environment with Python 3.9 (see `instructions <https://docs.anaconda.com/anaconda/navigator/getting-started/#managing-environments>`__)

3. **Install FishSound Finder:**

	Open a terminal window in the virtual environment (see `here <https://i0.wp.com/mikelynchgames.com/wp-content/uploads/2019/01/anacondaterminallaunch.png>`__) and type:
	
	.. code-block:: console		
	
	    $ pip install fishsound_finder

	It will download and install FishSound Finder along with all its dependencies. It may take a few minutes to complete.
	
	
4. **Test that FishSound Finder installed correctly:**

	In the same terminal window type:
	
	.. code-block:: console		
	
	    $ fishsound_finder

	
	If everything is correctly installed, it should print the help information in the temirnal window:
	
	.. code-block:: console	
	    
		usage: fishsound_finder [-h] --audio_folder AUDIO_FOLDER --output_folder OUTPUT_FOLDER --model_file MODEL_FILE --threshold THRESHOLD [--channel CHANNEL] [--extension EXTENSION] [--batch_size BATCH_SIZE] [--step_sec STEP_SEC]
                        [--smooth_sec SMOOTH_SEC] [--min_dur_sec MIN_DUR_SEC] [--max_dur_sec MAX_DUR_SEC] [--class_id CLASS_ID] [--tmp_dir TMP_DIR] [--deployment_file DEPLOYMENT_FILE] [--deployment_id DEPLOYMENT_ID]         
                        [--recursive | --no-recursive]

		Run fishsound_finder

		required arguments:
		
		  --audio_folder AUDIO_FOLDER          Path to the folder containing the audio files to process.                        
		  --output_folder OUTPUT_FOLDER        Path of the folder where the results will be written.
		  --model_file MODEL_FILE              Classification model file (.kt).
		  --threshold THRESHOLD                Minimum score for a detection to be accepted (ranging from 0 to 1). Default is 0.5.


		optional arguments:
		  -h, --help                           Show this help message and exit
		  --channel CHANNEL                    Audio channel to use. Default is 1.
		  --extension EXTENSION                Extension of audio files to process. Default is ".wav".
		  --batch_size BATCH_SIZE              The number of segments to hold in memory at one time. Default is 512. Decrease in case of memory errors.
		  --step_sec STEP_SEC                  Step size (in seconds) used for the sliding window. Default is 0.05.
		  --smooth_sec SMOOTH_SEC              Length of score averaging window (in seconds). Default is 0.
		  --min_dur_sec MIN_DUR_SEC            Minimum duration allowed for detections (in seconds). Default is None
		  --max_dur_sec MAX_DUR_SEC            Maximum duration allowed for detections(in seconds). Default is None.
		  --class_id CLASS_ID                  Class ID to use. Default is 1.
		  --tmp_dir TMP_DIR                    Path of temporary folder for the model and audio data. Default: created tmp folder in the output directory
		  --deployment_file DEPLOYMENT_FILE    deployment_info.csv with metadata.
		  --deployment_id DEPLOYMENT_ID        Identification of the deployment being processed (for book keeping).
		  --recursive, --no-recursive          Process files from all folders and sub-folders. Default is False. (default: False)

		To load input arguments from a file, use @ followed by the path of the text
		file containing all arguments (e.g. fishsound_finder @args_file_example.txt)

