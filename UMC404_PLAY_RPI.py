# -*- coding: utf-8 -*-
#
#   WIN10 PC 環境ではドライバが用意されており、それを用いれば、CH1-2,CH3-4の2系統のステレオチャンネルを独立して制御可能
#   Linux(RPi)では、ドライバが用意されておらず、4chの入出力として扱う必要がある。
#   Audacity等で2CHのWAVEファイルを出力すると、CH1-2から出力される。
#   RPi専用にスクリプトを書き直す。
#
#   環境音と評価音を同時に発音するためには、USB AudioI/Fを2系統用意する必要がある。
#
#


import wave
import pyaudio
import time


class UMC404_PLAY_RPI():

    def __init__(self):
        self.devindex = -1
        self.fname = 'snd.wav'

        self.ch12 = 2
        self.qb12 = 2
        self.fq12 = 16000

    def SetFileName(self, fname12):
        self.fname12 = fname12

    def openWaveFile(self):
        self.wf12 = wave.open(self.fname12, 'rb')
        self.ch12 = self.wf12.getnchannels()
        self.qb12 = self.wf12.getsampwidth()
        self.fq12 = self.wf12.getframerate()
        print("CH1-2 plays")
        print(self.fname12, self.ch12, self.qb12, self.fq12)

    def sndplay12(self, in_data, frame_count, time_info, status):
        self.buf12 = self.wf12.readframes(frame_count)
        return(self.buf12, pyaudio.paContinue)

    def getDeviceIndex(self):

        info = self.p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
            name = self.p.get_device_info_by_host_api_device_index(0, i).get('name')
            if("UMC404HD" in name):
                if (self.p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                    self.devindex_12 = i

    def PLAY(self):
        self.p = pyaudio.PyAudio()
        self.getDeviceIndex()

        if (self.devindex_12 == -1):
            print("can't open UMC404HD")
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

        self.stmo12.start_stream()

        while self.stmo12.is_active():
            cmd = input('when want to stop, type"exit"')
            if cmd == 'exit':
                break

        self.stmo12.stop_stream()
        self.stmo12.close()

        self.p.terminate()
        self.wf12.close()

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
        self.stmo12.start_stream()

    def chek_active(self):
        return self.stmo12.is_active()

    def STOP(self):
        self.stmo12.stop_stream()
        self.stmo12.close()

        self.p.terminate()
        self.wf12.close()


def main():
    DeviceOut = UMC404_PLAY_RPI()
    DeviceOut.SetFileName('./sound/stereo_nisseki_x4.wav')
    DeviceOut.PLAY()


if __name__ == '__main__':
    main()
