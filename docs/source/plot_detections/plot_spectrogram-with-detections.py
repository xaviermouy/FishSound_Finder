from ecosound.core.measurement import Measurement
from ecosound.core.annotation import Annotation
from ecosound.core.audiotools import Sound
from ecosound.core.spectrogram import Spectrogram
from ecosound.visualization.grapher_builder import GrapherFactory
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

# load detections
detection_file = r".\FS_plot_AMAR173.4.20190920T004248Z.wav.nc"
detec = Annotation()
detec.from_netcdf(detection_file)

# load audio file (first 15 sec only)
audio_file = r".\FS_plot_AMAR173.4.20190920T004248Z.wav"
sound = Sound(audio_file)
#sound.read(channel=0, chunk=[24, 37], unit='sec', detrend=True)
sound.read(channel=0, unit='sec', detrend=True)

# Calculate spectrogram
frame = 2048
nfft = 4096
step = 400
window_type = 'hann'
spectro = Spectrogram(frame, window_type, nfft, step, sound.waveform_sampling_frequency, unit='samp')
spectro.compute(sound, dB=False)

# Generate plot with waveform and spectrogram
graph = GrapherFactory('SoundPlotter', title='Recording', frequency_max=1400, start_time=966)
graph.add_data(sound) # add waveform data
graph.add_data(spectro) # add spectrogram
graph.add_annotation(detec, panel=0, color='green', label='Detections') # overlay detections on waveform plot
graph.add_annotation(detec, panel=1, color='green', label='Detections') # overlay detections on spectrogram plot
graph.colormap = 'binary'
graph.show()

print('s')