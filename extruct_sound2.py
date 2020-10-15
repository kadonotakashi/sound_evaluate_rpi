# -*- coding: utf-8 -*-
import wave_extruct as extruct
import sys
import os
import pandas as pd


def extruct_sound(winfo, srcfile, offset_time):
    ex = extruct.wave_extruct()
    wave_info = pd.read_csv(winfo)
    row = wave_info.shape[0]

    record_path = srcfile.split('.')
    distpath = '.' + record_path[1]
    os.makedirs(distpath, exist_ok=True)

    for i in range(row):
        outfname = str(i)+".wav"
        length = float(wave_info.length_time[i])
        start_time = float(wave_info.start_time[i])
        start_time += offset_time
        if start_time < 0.0:
            start_time = 0.0

        print(srcfile, distpath + '/' + outfname, start_time, length)
        ex.extruct(srcfile, distpath + '/' + outfname, start_time, length)


def main():
    if (len(sys.argv) >= 2):
        offset_time = int(sys.argv[1])
    else:
        offset_time = -2

    if (len(sys.argv) >= 3):
        rinfName = sys.argv[2]
    else:
        rinfName = './record/rec_setting.csv'

    if (len(sys.argv) >= 4):
        winfName = sys.argv[3]
    else:
        winfName = './record/wave_info.csv'

    rec_info = pd.read_csv(rinfName)  # 録音シーケンス
#    wave_info = pd.read_csv(winfName)  # wavファイルの内容

    row = rec_info.shape[0]
    rec_cnt = 0
    for i in range(row):
        if (rec_info.key[i]).lower() == 'start':
            rec_cnt += 1
        if (rec_info.key[i]).lower() == 'end':
            break

    print(rec_cnt, "words record")

#    mic_flag = 'codama'
    envfile = ''
    envlevel = 0
    reffile = ''
    reflevel = 0
    rec_path = './record'
    rec_file = 'auto'
    rec_cnt = 0

    for i in range(row):
        if (rec_info.key[i]).lower() == 'end':
            print("END keyword detect in record setting file")
            break
#        elif (rec_info.key[i]).lower() == 'mic':
#            if (rec_info.augment0[i]).lower() == 'xvf3510':
#                mic_flag = 'xvf3510'
#            else:
#                mic_flag = 'codama'
        elif (rec_info.key[i]).lower() == 'envfile':
            envfile = rec_info.augment0[i]
            print("env sound file is ", envfile)

        elif (rec_info.key[i]).lower() == 'envlevel':
            envlevel = rec_info.augment0[i]
            print("env sound level is ", envlevel)

        elif (rec_info.key[i]).lower() == 'reffile':
            reffile = rec_info.augment0[i]
            print("reference sound file is ", reffile)

        elif (rec_info.key[i]).lower() == 'reflevel':
            reflevel = rec_info.augment0[i]
            print("reference sound level is ", reflevel)

        elif (rec_info.key[i]).lower() == 'rec_path':
            rec_path = rec_info.augment0[i]
            print("recording path is ", rec_path)

        elif (rec_info.key[i]).lower() == 'rec_file':
            rec_file = rec_info.augment0[i]
            print("recording file is ", rec_file)

        elif (rec_info.key[i]).lower() == 'prm':
            prm_reg = rec_info.augment0[i]
            prm_val = rec_info.augment1[i]
            print(prm_reg, ' <= ', prm_val)

        elif (rec_info.key[i]).lower() == 'start':
            if rec_file.lower() == 'auto':
                rec_filename = rec_path + 'rec' + str(rec_cnt) + '.wav'
            else:
                rec_filename = rec_path + rec_file

            extruct_sound(winfName, rec_filename, offset_time)
            rec_cnt += 1


if __name__ == '__main__':
    main()
