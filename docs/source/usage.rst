Using FishSound Finder
======================

FishSound Finder can be used using its command line interface. It requires 4 required arguments and 12 optional arguments. The detection results are written as
netCDF4 (.nc) files and Raven annotations tables (.txt).

Required arguments
--------------------

* **--audio_folder**:    Path of the input file or directory to process. 
* **--output_folder**:   Path of the output directory where the results will be written. 
* **--model_file**:      Path of the classification model file to use (.kt).  
* **--threshold**:       Minimum classification score accepted (from 0 to 1).

The .kt model files are provided for each detector on FishSound Finder's `GitHub page <https://github.com/xaviermouy/FishSound_Finder/tree/master/models/>`__. 

Optional arguments
------------------

* **--help**:               Show this help message and exit
* **--channel**:            Audio channel to use. Default is 1.
* **--extension**:          Extension of audio files to process. Default is ".wav".
* **--batch_size**:         The number of segments to hold in memory at one time. Default is 512. Increase to speed up the processing. Decrease in case of memory errors.
* **--step_sec**:           Step size (in seconds) used for the sliding window. Default is 0.05.
* **--smooth_sec**:         Length of score averaging window (in seconds). Default is 0.
* **--min_dur_sec**:        Minimum duration allowed for detections (in seconds). Default is None
* **--max_dur_sec**:        Maximum duration allowed for detections(in seconds). Default is None.
* **--class_id**:           Class ID to use. Default is 1.
* **--tmp_dir**:            Path of temporary folder for the model and audio data. Default: created tmp folder in the output directory
* **--deployment_file**:    Path of the deployment file. The deployment file is in the csv format and contains metadata about the deployment being analyzed. It can be created using the ecosound function ecosound.metadata.write_template, or by modifying the deployment file example located on GitHub `here <https://raw.githubusercontent.com/xaviermouy/FishSound_Finder/master/data/deployment_info.csv>`__. While using a deployment file is optional, it is highly recommended to use one, as it embeds all the metadata in the detection results which can facilitate the analysis of the results.
deployment_info.csv with metadata.
* **--deployment_id**:      Identification of the deployment being processed (for book keeping).
* **--recursive**:          Process files from all folders and sub-folders. Default is False. (default: False)


Example
-------

The command below runs FishSound Finder on the .wav files located in the .\data folder using the metadata in the .\data\deployment_info.csv file. Results are written in the .\results folder. 

.. code-block:: console

   $ fishsound_finder --audio_folder=".\data"  --output_folder=".\results" --model_file=".\models\FishNet_model_BC202403.kt" --deployment_file=".\data\deployment_info.csv" 


It is also possible to have all the input arguments in a separate text file and run FishSound Finder using the @ command.

For a more detailed example, see the :ref:`Tutorial<tutorial>` section.
