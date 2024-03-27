"""
FishSound Finder

This script runs a fish sound detector on continuous audio data.

Usage:
    The script is executed in the terminal with the following command:
        python detector.py --audio_folder=<path_to_audio_data> --output_folder <path_to_results_folder> --model_file=<path_to_kt_file> --threshold=<threshold_value>

    To see the full list of command lines arguments, type:
        python detector.py --help

Outputs:
    - NetCDF4 (.nc) files with detection results that can be read with the
      library ecosound. There is one .nc file for each audio file processed.
    - Raven Annotation Table (.txt) file with detection results that can be
      visualized with the software Raven. There is one .txt file for each audio
      file processed.
    - SQLite database file (.sql) with detection results for all the files
      processed. The .sqlite file can be opened using ecosound or SQLiteStudio.
    - errors_log.txt: Log of errors that occured during the processing. This
      file stays empty if there is no errors.
    - full_log.txt: Log contaning, the input parameters used, the files that
      were processed, the computing time, and the number of detections per file

@author: Xavier Mouy
         email: xavier.mouy@outlook.com
         website: https://xaviermouy.weebly.com/

License: BSD 3-Clause
"""

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=Warning)
from silence_tensorflow import silence_tensorflow
silence_tensorflow()
import os
import tempfile
import argparse
import pandas as pd
import shutil
import ketos.neural_networks
from ketos.neural_networks.dev_utils.detection import compute_avg_score
from ecosound.core.annotation import Annotation
from ecosound.core.audiotools import Sound
from ecosound.core.spectrogram import Spectrogram, adjust_FFT_size
import ecosound.core.tools
import numpy as np
import scipy
from datetime import datetime
import uuid
import platform
import logging
import time
import sqlite3
import sys
from fishsound_finder._version import __version__

def cli_args():
    # parsing of the input arguments
    parser = argparse.ArgumentParser(prog='fishsound_finder',
                                     description='Run the fish sound detector',
                                     epilog="To load input arguments from a "
                                     "file, use @ followed by the path of the"
                                     " text file containing all arguments (e.g"
                                     ". python fishsound_finder.py "
                                     "@args_file_example.txt)",
                                     fromfile_prefix_chars='@',
                                     )
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    parser._action_groups.append(optional)
    # define command line arguments
    required.add_argument(
        "--audio_folder",
        type=str,
        required=True,
        default=None,
        help="Path to the folder containing the audio files to process.",
    )
    required.add_argument(
        "--output_folder",
        type=str,
        required=True,
        default=None,
        help="Path of the folder where the results will be written.",
    )
    required.add_argument(
        "--model_file",
        type=str,
        required=True,
        default=None,
        help="Classification model file (.kt).",
    )
    required.add_argument(
        "--threshold",
        type=float,
        required=True,
        default=0.5,
        help="Minimum score for a detection to be accepted (ranging from 0 to 1). Default is 0.5.",
    )
    optional.add_argument(
        "--channel",
        type=int,
        default=1,
        help="Audio channel to use. Default is 1.",
    )
    optional.add_argument(
        "--extension",
        type=str,
        default=".wav",
        help='Extension of audio files to process. Default is ".wav".',
    )
    optional.add_argument(
        "--batch_size",
        type=int,
        default=512,  
        help="The number of segments to hold in memory at one time. Default is 512. Decrease in case of memory errors.",
    )
    optional.add_argument(
        "--step_sec",
        type=float,
        default=0.05,
        help="Step size (in seconds) used for the sliding window. Default is 0.05.",
    )
    optional.add_argument(
        "--smooth_sec",
        type=float,
        default=0,
        help="Length of score averaging window (in seconds). Default is 0.",
    )
    optional.add_argument(
        "--min_dur_sec",
        type=float,
        default=None,
        help="Minimum duration allowed for detections (in seconds). Default is None",
    )
    optional.add_argument(
        "--max_dur_sec",
        type=float,
        default=None,
        help="Maximum duration allowed for detections(in seconds). Default is None.",
    )
    optional.add_argument(
        "--class_id",
        type=int,
        default=1,
        help="Class ID to use. Default is 1.",
    )
    optional.add_argument(
        "--tmp_dir",
        type=str,
        default=None,
        help="Path of temporary folder for the model and audio data. Default: created tmp folder in the output directory",
    )
    optional.add_argument(
        "--deployment_file",
        type=str,
        default=None,
        help="deployment_info.csv with metadata.",
    )
    optional.add_argument(
        "--deployment_id",
        type=str,
        default=None,
        help="Identification of the deployment being processed (for book keeping).",
    )
    optional.add_argument(
        '--recursive',
        default=False,
        action=argparse.BooleanOptionalAction,
        help="Process files from all folders and sub-folders. Default is False.",
    ),
    return parser

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
    info_handler = logging.FileHandler(os.path.join(outdir, "full_log.txt"))
    info_handler.setLevel(logging.DEBUG)
    info_format = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    info_handler.setFormatter(info_format)
    logger.addHandler(info_handler)
    # Create error logger
    error_handler = logging.FileHandler(os.path.join(outdir, "errors_log.txt"))
    error_handler.setLevel(logging.ERROR)
    error_format = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    error_handler.setFormatter(error_format)
    logger.addHandler(error_handler)
    return logger

def decimate(
        infile,
        out_dir,
        sampling_rate_hz,
        filter_order=8,
        filter_type="iir",
        channel=1,
):
    # init audio file
    audio_data = Sound(infile)
    # load audio data
    audio_data.read(channel=channel - 1, detrend=True)
    # decimate
    if sampling_rate_hz <= audio_data.file_sampling_frequency:
        audio_data.decimate(sampling_rate_hz)
        # detrend
        audio_data.detrend()
        # normalize
        audio_data.normalize(method='amplitude')
        # write new file
        outfilename = os.path.basename(os.path.splitext(infile)[0]) + ".wav"
        audio_data.write(os.path.join(out_dir, outfilename))
    else:
        raise Exception("The sampling frequency of the recording is too low.")
    return outfilename

def calc_spectrogram(infile, spec_config):
    # load audio data
    sound = Sound(infile)
    sound.read(channel=0)
    # Calculates  spectrogram
    spectro = Spectrogram(spec_config['window'],
                          spec_config['window_func'],
                          spec_config['window'],
                          spec_config['step'],
                          sound.waveform_sampling_frequency,
                          unit='sec',
                          verbose=False,
                          )
    spectro.compute(sound,
                    spec_config['dB'],
                    spec_config['use_dask'],
                    spec_config['dask_chunks'],
                    )
    # Crop unused frequencies
    spectro.crop(frequency_min=spec_config['freq_min'],
                 frequency_max=spec_config['freq_max'],
                 inplace=True,
                 )
    # Denoise
    spectro.denoise(spec_config['denoiser'][0]['name'],
                    window_duration=spec_config['denoiser'][0]['window_duration_sec'],
                    use_dask=spec_config['denoiser'][0]['use_dask'],
                    dask_chunks=tuple(spec_config['denoiser'][0]['dask_chunks']),
                    inplace=True)
    return spectro

def classify_spectro_segments_ketos(spectro, model, spec_config, args):
    # run classification model
    step_bins = int(np.ceil(args.step_sec / spectro.time_res()))
    duration_bins = int(np.ceil(spec_config['duration'] / spectro.time_res()))
    spectro_dur_bin = int(spectro.data.shape[0])
    spectro_data = spectro.get_data().data
    seg_indices = list(range(0, spectro_dur_bin - duration_bins, step_bins))
    seg_times_sec = np.dot(seg_indices, spectro.time_res())
    batch_size = args.batch_size
    seg_indices_batches = [seg_indices[i:i + args.batch_size] for i in range(0, len(seg_indices), batch_size)]
    first_batch = True
    for seg_indices_batch in seg_indices_batches:
        batch_data = []
        for idx in seg_indices_batch:
            batch_data.append(spectro_data[idx:idx + duration_bins, :])
        batch_data = np.array(batch_data)
        if first_batch:
            scores = model.run_on_batch(batch_data, return_raw_output=True)
        else:
            scores = np.concatenate((scores, model.run_on_batch(batch_data, return_raw_output=True)))
        first_batch = False
    batch_data = []
    return scores, seg_times_sec

def classify_spectro_segments(spectro, model, spec_config, args):
    # run classification model
    step_bins = int(np.ceil(args.step_sec / spectro.time_resolution))
    duration_bins = int(np.ceil(spec_config['duration'] / spectro.time_resolution))
    spectro_data = spectro.spectrogram
    spectro_dur_bin = int(spectro_data.shape[1])
    seg_indices = list(range(0, spectro_dur_bin - duration_bins, step_bins))
    seg_times_sec = np.dot(seg_indices, spectro.time_resolution)
    batch_size = args.batch_size
    seg_indices_batches = [seg_indices[i:i + args.batch_size] for i in range(0, len(seg_indices), batch_size)]
    first_batch = True
    for seg_indices_batch in seg_indices_batches:
        batch_data = []
        for idx in seg_indices_batch:
            batch_data.append(spectro_data[:, idx:idx + duration_bins].T)
        batch_data = np.array(batch_data)
        if first_batch:
            scores = model.run_on_batch(batch_data, return_raw_output=True)
        else:
            scores = np.concatenate((scores, model.run_on_batch(batch_data, return_raw_output=True)))
        first_batch = False
    batch_data = []
    return scores, seg_times_sec

def define_detections(scores, seg_times_sec, spec_config, audio_repr, file, args):
    scores = np.concatenate(([0], scores, [0]))
    # extract detections start and stop times
    start_indices = [i for i in range(1, len(scores)) if
                     (scores[i] >= args.threshold) & (scores[i - 1] < args.threshold)]
    end_indices = [i - 1 for i in range(1, len(scores)) if
                   (scores[i] < args.threshold) & (scores[i - 1] >= args.threshold)]
    if len(start_indices) != len(end_indices):
        raise ('Error while defining detection start and stop times')
    if len(start_indices) > 0:  # if any detections
        start_indices = [x - 1 for x in start_indices]
        end_indices = [x - 1 for x in end_indices]
        scores = scores[1:-1]
        detec_start_times_sec = [seg_times_sec[i] for i in start_indices]
        detec_end_times_sec = [seg_times_sec[i] for i in end_indices]
        detec_end_times_sec = [i + audio_repr[0]['spectrogram']['duration'] for i in detec_end_times_sec]
        detec_scores = [np.median(scores[i:j + 1]) for i, j in zip(start_indices, end_indices)]
    else:
        detec_start_times_sec = []
        detec_end_times_sec = []
        detec_scores = []
        # detection scores (based on median of score values)

    # Save as ecosound annotation object
    if len(detec_start_times_sec) > 0:  # only if there are detections
        annot = Annotation()
        annot_data = annot.data
        try:
            file_timestamp = ecosound.core.tools.filename_to_datetime(
                file
            )[0]
            timestamp = True
        except:
            print("Time stamp format not recognized")
            timestamp = False
        annot_data["time_max_offset"] = detec_end_times_sec  # end_list
        annot_data["time_min_offset"] = detec_start_times_sec
        annot_data["frequency_min"] = spec_config["freq_min"]
        annot_data["frequency_max"] = spec_config["freq_max"]
        annot_data["audio_file_dir"] = os.path.dirname(file)  # args.audio_folder
        annot_data["audio_file_name"] = os.path.splitext(os.path.basename(file))[0]  # files_list
        annot_data["audio_file_extension"] = args.extension
        annot_data["label_class"] = "FS"
        annot_data["confidence"] = detec_scores  # confidence_list
        annot_data["software_name"] = "FishSound_Finder"
        annot_data["entry_date"] = datetime.now()
        if timestamp:
            annot_data["audio_file_start_date"] = file_timestamp
            annot_data["time_min_date"] = pd.to_datetime(
                file_timestamp
                + pd.to_timedelta(annot_data["time_min_offset"], unit="s")
            )
            annot_data["time_max_date"] = pd.to_datetime(
                file_timestamp
                + pd.to_timedelta(annot_data["time_max_offset"], unit="s")
            )
        annot_data["from_detector"] = True
        annot_data["duration"] = (
                annot_data["time_max_offset"] - annot_data["time_min_offset"]
        )
        annot_data["uuid"] = annot_data.apply(
            lambda _: str(uuid.uuid4()), axis=1
        )
        annot_data["operator_name"] = platform.uname().node
        annot.data = annot_data
        # insert metadata
        if args.deployment_file:
            annot.insert_metadata(args.deployment_file)
        elif args.deployment_id:
            annot.insert_metadata_blank()
            annot.insert_values(deployment_ID=args.deployment_id)
        else:
            annot.insert_metadata_blank()
        annot.insert_values(audio_channel=str(args.channel))
        # sort chronologically
        annot.data.sort_values(
            "time_min_offset",
            ascending=True,
            inplace=True,
            ignore_index=True,
        )
        annot.check_integrity()
    else:  # no detections
        annot = Annotation()
    return annot

def main():
    software_version=__version__
    nfiles_errors = 0
    # parse command line args
    parser = cli_args()
    # Display help if no arguments presented
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
    # Parse input arguments
    args = parser.parse_args()
    # convert smoothing window from seconds to frame numbers
    if args.smooth_sec == 0:
        smooth_bins = 1
    else:
        smooth_bins = round(args.smooth_sec / args.step_sec)
    is_even = True if smooth_bins % 2 == 0 else False
    if is_even:  # adjust smooth_bin so it is an odd number (required)
        smooth_bins += 1
    smooth_bins = int(smooth_bins)
    # recursive mode
    recursive = args.recursive
    # creates temp and output folders if not alreadey there
    if os.path.isdir(args.output_folder) is False:
        os.mkdir(args.output_folder)
    if args.tmp_dir is None:
        tmp_dir = tempfile.TemporaryDirectory(dir=args.output_folder).name
    else:
        if os.path.isdir(args.tmp_dir) is False:
            os.mkdir(args.tmp_dir)
        else:
            tmp_dir = tempfile.TemporaryDirectory(dir=args.tmp_dir).name
    tmp_dir_model = os.path.join(tmp_dir, 'model')
    tmp_dir_audio = os.path.join(tmp_dir, 'audio')
    tmp_dir_db = os.path.join(tmp_dir, 'db')
    # delete tmp folder if case it alsreday exists
    if os.path.isdir(tmp_dir) is True:
        shutil.rmtree(tmp_dir)
    # create tmp folders for that run
    os.mkdir(tmp_dir)
    os.mkdir(tmp_dir_model)
    os.mkdir(tmp_dir_audio)
    os.mkdir(tmp_dir_db)
    # sets database temp location
    database = os.path.join(args.output_folder, "detections_" + datetime.now().strftime("%Y%m%d%H%M%S") +".sqlite")
    # Set error logs
    logger = set_logger(args.output_folder)
    # load the classifier and the spectrogram parameters
    model, audio_repr = ketos.neural_networks.load_model_file(args.model_file, tmp_dir_model, load_audio_repr=True)
    spec_config = audio_repr[0]["spectrogram"]
    # list files to process
    if os.path.isfile(args.audio_folder):  # if a single file was provided
        files = [args.audio_folder]
    elif os.path.isdir(args.audio_folder):  # if a folder was provided
        files = ecosound.core.tools.list_files(
            args.audio_folder,
            args.extension,
            recursive=recursive,
            case_sensitive=True,
        )
    print(str(args))
    logger.info(str(args))
    logger.info("Files to process: " + str(len(files)))
    start_time_loop = time.time()
    # loop to process each file
    for idx, file in enumerate(files):
        try:
            logger.info(file)
            start_time = time.time()
            print(str(idx + 1) + r"/" + str(len(files)) + ": " + file)
            # check if file already processed
            out_file_nc = os.path.join(args.output_folder, os.path.split(file)[1])
            if os.path.exists(out_file_nc + ".nc") is False:
                # list files for SQL table for book keeping
                file_tab = pd.DataFrame({'File_processed': [os.path.split(file)[1]]})
                # Decimate
                temp_file_name = decimate(file, tmp_dir_audio, spec_config["rate"], channel=args.channel)
                # calc spectrogram
                spectro = calc_spectrogram(os.path.join(tmp_dir_audio, temp_file_name), spec_config)
                # run classification model
                scores, seg_times_sec = classify_spectro_segments(spectro, model, spec_config, args)
                # Smooth detection function by applying running mean
                scores = compute_avg_score(scores[:, args.class_id], win_len=int(smooth_bins))
                # define detections (start and stop times, metadata, etc)
                detec = define_detections(scores, seg_times_sec, spec_config, audio_repr, file, args)
                # add software version
                detec.insert_values(software_version=software_version)
                # filter detection based on min amd max duration (if defined)
                if args.min_dur_sec:
                    detec.filter('duration >= ' + str(args.min_dur_sec), inplace=True)
                if args.max_dur_sec:
                    detec.filter('duration <= ' + str(args.max_dur_sec), inplace=True)
                print(len(detec), " detections")
                logger.info(" %u detections" % (len(detec)))
                # save results
                if len(detec) > 0:
                    # save output to Raven
                    detec.to_raven(outdir=args.output_folder, single_file=False)
                    # save output to NetCDF
                    detec.to_netcdf(os.path.join(args.output_folder, os.path.split(file)[1]))
                    # save output to SQLite DB
                    conn = sqlite3.connect(database)
                    detec.data.to_sql(name="detections", con=conn, if_exists="append", index=False)
                    conn.close()
                else:  # No detection but still writes empty output filesy output files
                    # save output to Raven
                    detec.to_raven(
                        args.output_folder,
                        os.path.split(file)[1]
                        + ".chan"
                        + str(int(args.channel))
                        + ".Table.1.selections.txt",
                        single_file=False,
                    )
                    # save output to NetCDF
                    detec.to_netcdf(os.path.join(args.output_folder, os.path.split(file)[1]))
                # Save file name to SQLite
                conn = sqlite3.connect(database)
                file_tab.to_sql(
                    name="files_processed", con=conn, if_exists="append", index=False
                )
                conn.close()
                # display processing time
                proc_time_file = time.time() - start_time
                logger.info("--- Executed in %0.4f seconds ---" % (proc_time_file))
                print(f"Executed in {proc_time_file:0.4f} seconds")
                # delete temporary file
                os.remove(os.path.join(tmp_dir_audio, temp_file_name))
            else:
                logger.info('File already processed')
                print('File already processed')
        except BaseException as e:
            logger.error(file)
            logger.error("------------ >>>> Exception occurred <<<<< ------------", exc_info=True)
            print("<<<<<<<< An error occurred >>>>>>>>>: " + str(e))
            nfiles_errors += 1
    # delete tmp folder
    shutil.rmtree(tmp_dir)
    # Wrap-up logs
    proc_time_process = time.time() - start_time_loop
    logger.info("Process complete.")
    logger.info("--- All files processed in %0.4f seconds ---" % (proc_time_process))
    print(f"All files processed in {proc_time_process:0.4f} seconds")
    # warnings of errors:
    if nfiles_errors > 0:
        print(str(int(
            nfiles_errors)) + ' files had errors and were not processed. Check the error logs for more details.')
        logger.info(str(int(
            nfiles_errors)) + ' files had errors and were not processed. Check the error logs for more details.')
    # close logs
    logging.shutdown()

if __name__ == '__main__':
    main()