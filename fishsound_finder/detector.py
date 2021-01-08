    # -*- coding: utf-8 -*-
"""
Created on Fri May  8 15:54:29 2020

@author: xavier.mouy
"""

from ecosound.core.audiotools import Sound
from ecosound.core.spectrogram import Spectrogram
from ecosound.detection.detector_builder import DetectorFactory
from ecosound.measurements.measurer_builder import MeasurerFactory
import ecosound.core.tools
import time
import os
import pickle
import platform
import numpy as np
import sys
import argparse
import yaml
import logging


def cli_args():
    """
    Define all the command line arguments.

    Returns
    -------
    parser : argparse object
        Input arguments object for the CLI.

    """
    # parsing of the input arguments
    parser = argparse.ArgumentParser(prog='fish-sound-detector',
                                     description='Run the fish sound detector',
                                     epilog="To load input arguments from a "
                                     "file, use @ followed by the path of the"
                                     " text file containing all arguments (e.g"
                                     ". python fish-sound-detector.py "
                                     "@args_file_example.txt)",
                                     fromfile_prefix_chars='@',
                                     )
    parser.add_argument("input",
                        type=str,
                        action='store',
                        help="file or directory to process")
    parser.add_argument("output",
                        type=str,
                        action='store',
                        help="output directory")
    parser.add_argument("cfgfile",
                        type=str,
                        action='store',
                        help="configuration file (.yaml)")
    parser.add_argument("model",
                        type=str,
                        action='store',
                        help="classification model file (.sav)")
    parser.add_argument("-d", "--deployment_file",
                        type=str,
                        action='store',
                        required=False,
                        help="deployment info file (.csv)")
    parser.add_argument("-e", "--extension",
                        type=str,
                        action='store',
                        required=False,
                        default=".wav",
                        help="extension of the sound files to process "
                        "(default: '.wav')")
    parser.add_argument("-f", "--force",
                        action="store_true",
                        default=False,
                        help="force reprocessing recordings whose netcdf"
                        " files already exist in the output folder")
    parser.add_argument("-p", "--pamlab",
                        action="store_true",
                        default=False,
                        help="also outputs results in the PAMlab annotation"
                        " format")
    parser.add_argument("-r", "--raven",
                        action="store_true",
                        default=True,
                        help="also outputs results in the RAVEN annotation"
                        " format")
    return parser


def load_config_file(config_file):
    """
    Load config file.

    Parameters
    ----------
    config_file : str
        Path of the yaml file with all the parameters for the detector.

    Returns
    -------
    config : dict
        Parsed parameters.

    """
    # Loads config  files
    yaml_file = open(config_file)
    config = yaml.load(yaml_file, Loader=yaml.FullLoader)
    return config


def set_logger(outdir):
    """
    Set up the logs.

    Configure the error and info logs

    Parameters
    ----------
    outdir : str
        Path of the folder where the logs will be saved.

    Returns
    -------
    logger : logger object
        Allows to add error or info to the logs.

    """
    # Create a custom logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # Create debug logger
    info_handler = logging.FileHandler(os.path.join(outdir, 'full_log.txt'))
    info_handler.setLevel(logging.DEBUG)
    info_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    info_handler.setFormatter(info_format)
    logger.addHandler(info_handler)
    # Create error logger
    error_handler = logging.FileHandler(os.path.join(outdir, 'errors_log.txt'))
    error_handler.setLevel(logging.ERROR)
    error_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    error_handler.setFormatter(error_format)
    logger.addHandler(error_handler)
    return logger


def run_detector(infile, outdir, classif_model, config, deployment_file=None, extension=".wav", overwrite=False, netcdf= True, pamlab=False, raven=False):
    """
    Run the fish sound detector.

        Parameters
        ----------
        infile : str
            Path of the audio file to process.
        outdir : str
            Path of the output folder where the results will be written.
        classif_model : str
            Path and name of the classification model to use (.sav pickle file)
        config : dict
            Dict with all parameters from the yaml file.
        deployment_file : str, optional
            Path and name of the csv file with all the deployment information.
            The default is None.
        extension : str, optional
            Extension of the audio files to process. The default is ".wav".
        overwrite : bool, optional
            If set to True, overwrites results (i.e. netcdf files) even if they
            already exist in the outdir folder. The default is False.
        netcdf : bool, optional
            If set to True, saves results as netcdf4 files (.nc).
            The default is True.
        pamlab : bool, optional
            If set to True, saves results as PAMlab files (.log).
            The default is False.
        raven : bool, optional
            If set to True, saves results as Raven files (.txt).
            The default is False.

        Returns
        -------
        None.

    """
    outfile = os.path.join(outdir, os.path.split(infile)[1] + '.nc')
    if (os.path.exists(outfile) is False) or (os.path.exists(outfile) and overwrite):
        # load audio data
        sound = Sound(infile)
        sound.read(channel=config['AUDIO']['channel'], unit='sec')
        # Calculates  spectrogram
        print('Spectrogram')
        spectro = Spectrogram(config['SPECTROGRAM']['frame_sec'],
                              config['SPECTROGRAM']['window_type'],
                              config['SPECTROGRAM']['nfft_sec'],
                              config['SPECTROGRAM']['step_sec'],
                              sound.waveform_sampling_frequency,
                              unit='sec',
                              )
        spectro.compute(sound,
                        config['SPECTROGRAM']['dB'],
                        config['SPECTROGRAM']['use_dask'],
                        config['SPECTROGRAM']['dask_chunks'],
                        )
        # Crop unused frequencies
        spectro.crop(frequency_min=config['SPECTROGRAM']['fmin_hz'],
                     frequency_max=config['SPECTROGRAM']['fmax_hz'],
                     inplace=True,
                     )
        # Denoise
        print('Denoise')
        spectro.denoise(config['DENOISER']['denoiser_name'],
                        window_duration=config['DENOISER']['window_duration_sec'],
                        use_dask=config['DENOISER']['use_dask'],
                        dask_chunks=tuple(config['DENOISER']['dask_chunks']),
                        inplace=True)
        # Detector
        print('Detector')
        file_timestamp = ecosound.core.tools.filename_to_datetime(infile)[0]
        detector = DetectorFactory(config['DETECTOR']['detector_name'],
                                   kernel_duration=config['DETECTOR']['kernel_duration_sec'],
                                   kernel_bandwidth=config['DETECTOR']['kernel_bandwidth_hz'],
                                   threshold=config['DETECTOR']['threshold'],
                                   duration_min=config['DETECTOR']['duration_min_sec'],
                                   bandwidth_min=config['DETECTOR']['bandwidth_min_hz']
                                   )
        detections = detector.run(spectro,
                                  start_time=file_timestamp,
                                  use_dask=config['DETECTOR']['use_dask'],
                                  dask_chunks=tuple(config['DETECTOR']['dask_chunks']),
                                  debug=False,
                                  )
        # Maasurements
        print('Measurements')
        spectro_features = MeasurerFactory(config['MEASURER']['measurer_name'],
                                           resolution_time=config['MEASURER']['resolution_time_sec'],
                                           resolution_freq=config['MEASURER']['resolution_freq_hz'],
                                           interp=config['MEASURER']['interp'],
                                           )
        measurements = spectro_features.compute(spectro,
                                                detections,
                                                debug=False,
                                                verbose=False,
                                                use_dask=config['MEASURER']['use_dask'])

        # Add metadata
        if deployment_file:
            measurements.insert_metadata(deployment_file)

        # Add file informations
        file_name = os.path.splitext(os.path.basename(infile))[0]
        file_dir = os.path.dirname(infile)
        file_ext = os.path.splitext(infile)[1]
        measurements.insert_values(operator_name=platform.uname().node,
                                   audio_file_name=file_name,
                                   audio_file_dir=file_dir,
                                   audio_file_extension=file_ext,
                                   audio_file_start_date=ecosound.core.tools.filename_to_datetime(infile)[0]
                                   )
        # Classification
        print('Classification')
        if classif_model:
            features = classif_model['features']
            model = classif_model['model']
            Norm_mean = classif_model['normalization_mean']
            Norm_std = classif_model['normalization_std']
            classes_encoder = classif_model['classes']
            # data dataframe
            data = measurements.data
            n1 = len(data)
            # drop observations/rows with NaNs
            data = data.replace([np.inf, -np.inf], np.nan)
            data.dropna(subset=features,
                        axis=0,
                        how='any',
                        thresh=None,
                        inplace=True)
            n2 = len(data)
            print('Deleted observations (due to NaNs): ' + str(n1-n2))
            # Classification - predictions
            X = data[features]
            X = (X-Norm_mean)/Norm_std
            pred_class = model.predict(X)
            pred_prob = model.predict_proba(X)
            pred_prob = pred_prob[range(0, len(pred_class)), pred_class]
            # Relabel
            for index, row in classes_encoder.iterrows():
                pred_class = [row['label'] if i == row['ID'] else i for i in pred_class]
            # update measurements
            data['label_class'] = pred_class
            data['confidence'] = pred_prob
        # sort detections by ascending start date/time
        data.sort_values('time_min_offset',
                         axis=0,
                         ascending=True,
                         inplace=True)
        # save result as NetCDF file
        print('Saving')
        measurements.data = data
        if netcdf:
            measurements.to_netcdf(outfile)
        if pamlab:
            measurements.to_pamlab(outdir)
        if raven:
            measurements.to_raven(outdir)

    else:
        print('Recording already processed.')
        logging.info('Recording already processed.')


def main():
    """
    Entry function for the Command Line Interface (CLI).

    Returns
    -------
    None.

    """
    # Define cli arguments
    parser = cli_args()
    # Display help if no arguments presented
    if len(sys.argv) < 2:
        parser.print_usage()
        parser.print_help()
        sys.exit(1)
    # Parse input arguments
    args = parser.parse_args()
    # Resign input argument to variable for readability
    infile = args.input
    outdir = args.output
    classif_model_file = args.model
    config_file = args.cfgfile
    deployment_file = args.deployment_file
    extension = args.extension
    overwrite = args.force
    pamlab = args.pamlab
    raven = args.raven
    # Set error logs
    logger = set_logger(outdir)
    # Load config file
    parameters = load_config_file(config_file)
    # Create output folder if it doesn't exist
    if os.path.isdir(outdir) is False:
        os.makedirs(outdir)
    # Load classif model
    classif_model = pickle.load(open(classif_model_file, 'rb'))
    # List files to process
    if os.path.isfile(infile):  # if a single file was provided
        files = [infile]
    elif os.path.isdir(infile):  # if a folder was provided
        files = ecosound.core.tools.list_files(infile,
                                               extension,
                                               recursive=False,
                                               case_sensitive=True)
    logger.info('Files to process: ' + str(len(files)))
    # Process each file
    start_time_loop = time.time()
    for idx,  file in enumerate(files):
        print(str(idx+1) + r'/' + str(len(files)) + ': ' + file)
        logger.info(file)
        start_time = time.time()
        try:
            run_detector(file, outdir, classif_model, parameters,
                         deployment_file=deployment_file,
                         extension=extension,
                         overwrite=overwrite,
                         pamlab=pamlab,
                         raven=raven)
        except BaseException as e:
            logger.error(file)
            logger.error("Exception occurred", exc_info=True)
            print('An error occured: ' + str(e))
        proc_time_file = time.time() - start_time
        logger.info("--- Executed in %0.4f seconds ---" % (proc_time_file))
        print(f"Executed in {proc_time_file:0.4f} seconds")
    # Wrap-up logs
    proc_time_process = time.time() - start_time_loop
    logger.info('Process complete.')
    logger.info("--- All files processed in %0.4f seconds ---" % (proc_time_process))
    print(f"All files processed in {proc_time_process:0.4f} seconds")


if __name__ == "__main__":
    main()
    print('----------------------------------------------')
    print('Process complete.')
