import concurrent.futures

from neurosdk.scanner import Scanner
from em_st_artifacts.utils import lib_settings
from em_st_artifacts.utils import support_classes
from em_st_artifacts import emotional_math
from neurosdk.cmn_types import *
from time import sleep
from PyQt5.QtCore import QThread, pyqtSignal

from src.core.log_config import logger
from src.brainbit.connect import ScanDevices


class MentalData:
    def __init__(self, rel_attention, rel_relaxation):
        self.rel_attention = rel_attention
        self.rel_relaxation = rel_relaxation


class RegSignals(QThread):
    mental_data_received = pyqtSignal(MentalData)

    def __init__(self, device):
        super().__init__()
        self.device = device
        self.scanner = Scanner([SensorFamily.LEBrainBit])

    def device_connection(self):
        return self.scanner.create_sensor(self.device)

    def run(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.device_connection)
            sensor = future.result()
            logger.info("Device connected")

        if sensor.is_supported_feature(SensorFeature.Signal):
            sensor.signalDataReceived = self.on_signal_received

        # init emotions lib
        self.calibration_length = 8
        self.nwins_skip_after_artifact = 10

        self.mls = lib_settings.MathLibSetting(sampling_rate=250,
                                               process_win_freq=25,
                                               fft_window=1000,
                                               n_first_sec_skipped=4,
                                               bipolar_mode=True,
                                               channels_number=4,
                                               channel_for_analysis=3)
        self.ads = lib_settings.ArtifactDetectSetting(hanning_win_spectrum=True, num_wins_for_quality_avg=125)
        self.sads = lib_settings.ShortArtifactDetectSetting(ampl_art_extremum_border=25)
        self.mss = lib_settings.MentalAndSpectralSetting()

        self.math = emotional_math.EmotionalMath(self.mls, self.ads, self.sads, self.mss)
        self.math.set_calibration_length(self.calibration_length)
        self.math.set_mental_estimation_mode(False)
        self.math.set_skip_wins_after_artifact(self.nwins_skip_after_artifact)
        self.math.set_zero_spect_waves(True, 0, 1, 1, 1, 0)
        self.math.set_spect_normalization_by_bands_width(True)

        if sensor.is_supported_command(SensorCommand.StartSignal):
            sensor.exec_command(SensorCommand.StartSignal)
            print("Start signal")
            self.math.start_calibration()
            sleep(120)
            sensor.exec_command(SensorCommand.StopSignal)
            print("Stop signal")

    def on_signal_received(self, sensor, data):
        raw_channels = []
        for sample in data:
            left_bipolar = sample.T3 - sample.O1
            right_bipolar = sample.T4 - sample.O2
            raw_channels.append(support_classes.RawChannels(left_bipolar, right_bipolar))

        self.math.push_data(raw_channels)
        self.math.process_data_arr()
        if not self.math.calibration_finished():
            logger.info(f'Artifacted: {self.math.is_both_sides_artifacted()}')
            logger.info(f'Calibration percents: {self.math.get_calibration_percents()}')
        else:
            logger.info(f'Artifacted: {self.math.is_artifacted_sequence()}')
            mental_data = self.math.read_mental_data_arr()
            self.mental_data_received.emit(MentalData(mental_data[0].rel_attention, mental_data[0].rel_relaxation))