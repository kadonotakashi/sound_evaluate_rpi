# -*- coding: utf-8 -*-

import wave
import pyaudio
import time


class UMC404_PLAY():

    def __init__(self):
        self.devindex_12 = -1
        self.devindex_34 = -1
        self.fname12 = 'snd12.wav'
        self.fname34 = 'snd34.wav'

        self.ch12 = 2
        self.qb12 = 2
        self.fq12 = 16000
        self.ch34 = 2
        self.qb34 = 2
        self.fq34 = 16000

    def SetFileName(self, fname12, fname34):
        self.fname12 = fname12
        self.fname34 = fname34

    def openWaveFile(self):
        self.wf12 = wave.open(self.fname12, 'rb')
        self.ch12 = self.wf12.getnchannels()
        self.qb12 = self.wf12.getsampwidth()
        self.fq12 = self.wf12.getframerate()
        print("CH1-2 plays")
        print(self.fname12, self.ch12, self.qb12, self.fq12)

        self.wf34 = wave.open(self.fname34, 'rb')
        self.ch34 = self.wf34.getnchannels()
        self.qb34 = self.wf34.getsampwidth()
        self.fq34 = self.wf34.getframerate()
        print("CH3-4 plays")
        print(self.fname34, self.ch34, self.qb34, self.fq34)

    def sndplay12(self, in_data, frame_count, time_info, status):
        self.buf12 = self.wf12.readframes(frame_count)
        return(self.buf12, pyaudio.paContinue)

    def sndplay34(self, in_data, frame_count, time_info, status):
        self.buf34 = self.wf34.readframes(frame_count)
        return(self.buf34, pyaudio.paContinue)

    def getDeviceIndex(self):

        info = self.p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
            name = self.p.get_device_info_by_host_api_device_index(0, i).get('name')
            if (name[0:7]) == "OUT 1-2":
                self.devindex_12 = i
            if (name[0:7]) == "OUT 3-4":
                self.devindex_34 = i

    def PLAY(self):
        self.p = pyaudio.PyAudio()

        self.getDeviceIndex()

        if (self.devindex_12 == -1):
            print("can't open UMC404HD CH1,2")
            while True:
                time.sleep(1)

        if (self.devindex_34 == -1):
            print("can't open UMC404HD CH3,4")
            while True:
                time.sleep(1)

        self.openWaveFile()

        self.stmo12 = self.p.open(
            format=self.p.get_format_from_width(self.qb12),
            channels=self.ch12,
            rate=self.fq12,
            output=True,
            stream_callback=self.sndplay12,
            output_device_index=self.devindex_12
        )

        self.stmo34 = self.p.open(
            format=self.p.get_format_from_width(self.qb34),
            channels=self.ch34,
            rate=self.fq34,
            output=True,
            stream_callback=self.sndplay34,
            output_device_index=self.devindex_34
        )

        self.stmo12.start_stream()
        self.stmo34.start_stream()

        while self.stmo12.is_active():
            cmd = input('when want to stop, type"exit"')
            if cmd == 'exit':
                break

        self.stmo12.stop_stream()
        self.stmo12.close()
        self.stmo34.stop_stream()
        self.stmo34.close()

        self.p.terminate()
        self.wf12.close()
        self.wf34.close()

    def START(self):
        self.p = pyaudio.PyAudio()

        self.getDeviceIndex()

        if (self.devindex_12 == -1):
            print("can't open UMC404HD CH1,2")
            while True:
                time.sleep(1)

        if (self.devindex_34 == -1):
            print("can't open UMC404HD CH3,4")
            while True:
                time.sleep(1)

        self.openWaveFile()

        self.stmo12 = self.p.open(
            format=self.p.get_format_from_width(self.qb12),
            channels=self.ch12,
            rate=self.fq12,
            output=True,
            stream_callback=self.sndplay12,
            output_device_index=self.devindex_12
        )

        self.stmo34 = self.p.open(
            format=self.p.get_format_from_width(self.qb34),
            channels=self.ch34,
            rate=self.fq34,
            output=True,
            stream_callback=self.sndplay34,
            output_device_index=self.devindex_34
        )

        self.stmo12.start_stream()
        self.stmo34.start_stream()

    def chek_active(self):
        return self.stmo12.is_active()

    def STOP(self):
        self.stmo12.stop_stream()
        self.stmo12.close()
        self.stmo34.stop_stream()
        self.stmo34.close()

        self.p.terminate()
        self.wf12.close()
        self.wf34.close()


def main():
    DeviceOut = UMC404_PLAY()
    DeviceOut.SetFileName('./sound/金魚のトロッコ.wav', './sound/吾輩は高瀬舟.wav')
    DeviceOut.PLAY()


if __name__ == '__main__':
    main()
