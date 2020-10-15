# -*- coding: utf-8 -*-

import wave
import pyaudio
import time


class CODAMA_REC():

    def __init__(self):
        self.devindex_mic = -1
        self.fnameRec = 'sndRec.wav'

        self.ch_Mic = 1
        self.qb_Mic = 2
        self.fq_Mic = 16000

    def SetFileName(self, fname):
        self.fnameRec = fname

    def CreateWaveFile(self):
        self.wfrec = wave.open(self.fnameRec, 'wb')
        self.wfrec.setnchannels(self.ch_Mic)
        self.wfrec.setsampwidth(self.qb_Mic)
        self.wfrec.setframerate(self.fq_Mic)
        print("record file is ")
        print(self.fnameRec, self.ch_Mic, self.qb_Mic, self.fq_Mic)

    def sndrec(self, in_data, frame_count, time_info, status):
        self.wfrec.writeframes(in_data)
        return(None, pyaudio.paContinue)

    def getDeviceIndex(self):

        info = self.p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')

        for i in range(0, numdevices):
            name = self.p.get_device_info_by_host_api_device_index(0, i).get('name')
            if name[0:7] == "Yukai e":
                if (self.p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                    self.devindex_mic = i
                    print('codama Mic index is', self.devindex_mic)

    def RECORD(self):
        self.p = pyaudio.PyAudio()

        self.getDeviceIndex()

        if (self.devindex_mic == -1):
            print("can't open XVF3510 as Input Device")
            while True:
                time.sleep(1)

        self.CreateWaveFile()

        self.stmrec = self.p.open(
            format=self.p.get_format_from_width(self.qb_Mic),
            channels=self.ch_Mic,
            rate=self.fq_Mic,
            input=True,
            frames_per_buffer=1024,
            stream_callback=self.sndrec,
            input_device_index=self.devindex_mic
        )

        self.stmrec.start_stream()

        while self.stmrec.is_active():
            cmd = input('when want to stop, type"exit"')
            if cmd == 'exit':
                break

        self.stmrec.stop_stream()
        self.stmrec.close()
        self.p.terminate()
        self.wfrec.close()

    def START(self):
        self.p = pyaudio.PyAudio()
        self.getDeviceIndex()

        if (self.devindex_mic == -1):
            print("can't open codama as Input Device")
            while True:
                time.sleep(1)

        self.CreateWaveFile()
        self.stmrec = self.p.open(
            format=self.p.get_format_from_width(self.qb_Mic),
            channels=self.ch_Mic,
            rate=self.fq_Mic,
            input=True,
            frames_per_buffer=1024,
            stream_callback=self.sndrec,
            input_device_index=self.devindex_mic
        )
        self.stmrec.start_stream()

    def check_active(self):
        return self.stmrec.is_active()

    def STOP(self):
        self.stmrec.stop_stream()
        self.stmrec.close()
        self.p.terminate()
        self.wfrec.close()


def main():
    DeviceIn = CODAMA_REC()
    DeviceIn.SetFileName('./record/sndRec_codama.wav')
    DeviceIn.RECORD()


if __name__ == '__main__':
    main()