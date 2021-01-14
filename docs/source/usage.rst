Using FishSound Finder
======================

FishSound Finder can be used using its command line interface. It requires 4 positional arguments and 6 optional arguments. The detection results are written as
netCDF4 (.nc) files with the option to also output Raven and Pamlab annotations tables.

Positional arguments
--------------------

1. Path of the input file or directory to process.
2. Path of the output directory where the results will be written.
3. Path of the configuration (.yaml) file indicating all the parameters needed for the detector and classifier.
4. Path of the classification model (.sav file) to use.

Both the configuration .yaml file and the .sav model file are provided for each detector on FishSound Finder's `GitHub page <https://github.com/xaviermouy/FishSound_Finder/tree/master/models/>`_. 
For the fish detection in British Columbia the configuration and model files are located `here <https://github.com/xaviermouy/FishSound_Finder/tree/master/models/british-columbia_generic_config>`_.

Optional arguments
------------------

* **-h**:                   Shows the help message and exits.
* **-d <DEPLOYMENT_FILE>**: Path of the deployment file. The deployment file is in the csv format and contains metadata about the deployment being analyzed. It can be created using the ecosound function ecosound.metadata.write_template, or by modifying the deployment file example located on GitHub `here <https://github.com/xaviermouy/FishSound_Finder/blob/master/example/deployment_info.csv>`_. While using a deployment	file is optional, it is highly recommended to use one, as it embeds all the metadata in the detection results which can facilitate the analysis of the results.
* **-e <EXTENSION>**:       Extension of the sound files to process. The default is '.wav'.
* **-f**:                   Forces the reprocessing of recordings whose netcdf files already exist in the output directory. If this option is not set, files already processed will be skipped.
* **-r**:                   Outputs detection results as Raven tables (.txt files) in addition to the netcdf files.
* **-p**:                   Outputs detection results as PAMlab tables (.log files) in addition to the netcdf files.


Example
-------

The command below runs FishSound Finder on the .wav files located in the .\my_data folder using the metadata in the .\deployment_info.csv file. It will output
detection results as netCDF4, Raven, and PAMlab files.   

.. code-block:: console

   $ fishsound_finder ".\my_data" ".\my_outputs" ".\config.yaml" ".\RF50_model_20201208T223420.sav" -d"./deployment_info.csv" -e".wav" -f -r -p


It is also possible to have all the input arguments in a separate text file and run FishSound Finder using the @ command.


.. code-block:: console

   $ fishsound_finder @argument_file.txt


In this case, the text file 'argument_file.txt' contains one input argument per line (see example `here <https://github.com/xaviermouy/FishSound_Finder/blob/master/example/args_file_example.txt>`_). 

For a more detailed example, see the :ref:`Tutorial<tutorial>` section.
