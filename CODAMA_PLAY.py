# -*- coding: utf-8 -*-

import wave
import pyaudio
import time


class CODAMA_PLAY():

    def __init__(self):
        self.devindex = -1
        self.fname = './record/sayaka.wav'

        self.ch = 2
        self.qb = 2
        self.fq = 16000

    def SetFileName(self, fname):
        self.fname = fname

    def openWaveFile(self):
        self.wf = wave.open(self.fname, 'rb')
        self.ch = self.wf.getnchannels()
        self.qb = self.wf.getsampwidth()
        self.fq = self.wf.getframerate()
        print("codama plays")
        print(self.fname, self.ch, self.qb, self.fq)

    def sndplay(self, in_data, frame_count, time_info, status):
        self.buf = self.wf.readframes(frame_count)
        return(self.buf, pyaudio.paContinue)

    def getDeviceIndex(self):

        info = self.p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
            name = self.p.get_device_info_by_host_api_device_index(0, i).get('name')
#           if (name[0:15]) == "スピーカー (4- Yukai":
#                self.devindex = i
            if("codama" in name):
                if("Yukai" in name):
                    self.devindex = i

    def PLAY(self):
        self.p = pyaudio.PyAudio()

        self.getDeviceIndex()

        if (self.devindex == -1):
            print("can't open CODAMA speaker")
            while True:
                time.sleep(1)

        self.openWaveFile()

        self.stmout = self.p.open(
            format=self.p.get_format_from_width(self.qb),
            channels=self.ch,
            rate=self.fq,
            output=True,
            stream_callback=self.sndplay,
            output_device_index=self.devindex
        )

        self.stmout.start_stream()
        while self.stmout.is_active():
            cmd = input('when want to stop, type"exit"')
            if cmd == 'exit':
                break

        self.stmout.stop_stream()
        self.stmout.close()

        self.p.terminate()
        self.wf.close()

    def START(self):
        self.p = pyaudio.PyAudio()

        self.getDeviceIndex()

        if (self.devindex == -1):
            print("can't open codama speaker")
            while True:
                time.sleep(1)

        self.openWaveFile()

        self.stmout = self.p.open(
            format=self.p.get_format_from_width(self.qb),
            channels=self.ch,
            rate=self.fq,
            output=True,
            stream_callback=self.sndplay,
            output_device_index=self.devindex
        )

        self.stmout.start_stream()

    def chek_active(self):
        return self.stmout.is_active()

    def STOP(self):
        self.stmout.stop_stream()
        self.stmout.close()

        self.p.terminate()
        self.wf.close()


def main():
    DeviceOut = CODAMA_PLAY()
    DeviceOut.SetFileName('./sound/sayaka.wav')
    DeviceOut.PLAY()


if __name__ == '__main__':
    main()
