# -*- coding: utf-8 -*-

import wave
import numpy as np
from scipy import fromstring, int16
import struct
# import matplotlib.pyplot as plt


class wave_extruct():

    def extruct(self, infname, outfname, start_time, length):
        wf = wave.open(infname, 'r')
        ch = wf.getnchannels()
        width = wf.getsampwidth()
        fr = wf.getframerate()
        fn = wf.getnframes()
        print("input file: ", infname, "Channel: ", ch, "Sample width: ", width, "Frame Rate: ", fr, "Frame num: ", fn)

        data_in = wf.readframes(wf.getnframes())
        wf.close()

        X = np.frombuffer(data_in, dtype=int16)

        start_frame = int(start_time * fr * ch)
        out_frames = int(length * fr * ch)
        end_frame = int(start_frame + out_frames)

        Y = X[start_frame: end_frame]
        data_out = struct.pack("h" * len(Y), *Y)

        print("start frame: ", start_frame, "end frame: ", end_frame)

        ww = wave.open(outfname, 'w')
        ww.setnchannels(ch)
        ww.setsampwidth(width)
        ww.setframerate(fr)
        ww.writeframes(data_out)
        ww.close()


def main():
    ext = wave_extruct()

    infname = 'ref_speach.wav'
    outfname = 'extruct.wav'
    start_time = 12.0
    length = 12.0

    ext.extruct(infname, outfname, start_time, length)


if __name__ == '__main__':
    main()
