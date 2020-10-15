# -*- coding: utf-8 -*-

import wave
import numpy as np
import matplotlib.pyplot as plt


class wave_att():

    def att(self, infname, outfname, level, plot):
        wf = wave.open(infname, 'r')
        ch = wf.getnchannels()
        width = wf.getsampwidth()
        fr = wf.getframerate()
        fn = wf.getnframes()

        print("Channel: ", ch, "Sample width: ", width, "Frame Rate: ", fr, "Frame num: ", fn)
        print("Total time: ", 1.0 * fn / fr)

        data = wf.readframes(wf.getnframes())
        wf.close()

        X = np.frombuffer(data, dtype=np.int16)/32768   # float -1.0 ~1.0
        X = X * level * 32768                           # 減衰しながら-32768.0 ~32767.0に
        X = X.astype(np.int16)                          # int16に戻す
        data = X

        if plot != 0:
            if ch == 2:
                Rch = X[1::2]
                Lch = X[::2]
                plt.plot(Rch[:3*fr])
                plt.plot(Lch[:3*fr])
            else:
                plt.plot(X[:3*fr])
            plt.show()

        ww = wave.open(outfname, 'w')
        ww.setnchannels(ch)
        ww.setsampwidth(width)
        ww.setframerate(fr)
        ww.writeframes(data)
        ww.close()


def main():
    infname = './test.wav'

    att = wave_att()
    att.att(infname, 'att09.wav', 0.9, 0)
    att.att(infname, 'att08.wav', 0.8, 0)
    att.att(infname, 'att07.wav', 0.7, 0)
    att.att(infname, 'att06.wav', 0.6, 0)
    att.att(infname, 'att05.wav', 0.5, 0)
    att.att(infname, 'att04.wav', 0.4, 0)
    att.att(infname, 'att03.wav', 0.3, 0)
    att.att(infname, 'att02.wav', 0.2, 0)
    att.att(infname, 'att01.wav', 0.1, 0)


if __name__ == '__main__':
    main()