# -*- coding: utf-8 -*-
import sys
import pandas as pd
import time
import codama_ctrl
import UMC404_PLAY as SoundOut
import CODAMA_PLAY as GuideOut

import CODAMA_REC as SoundInCodama
import MCU03_REC as SoundInMCU03
import wave_att as att

DeviceGuideOut = GuideOut.CODAMA_PLAY()     # 音声ガイダンス出力
DeviceOut = SoundOut.UMC404_PLAY()          # 評価音、環境音出力
DeviceCodama = SoundInCodama.CODAMA_REC()       # 録音
DeviceMCU03 = SoundInMCU03.MCU03_REC()    # 録音
att = att.wave_att()

# 録音
#   引数    outfile1,level1:    評価音声ファイル名,評価音声レベル
#           outfile2,level2:    環境音声ファイル名,環境音声レベル
#           outfile3,level3:    音声ガイダンスファイル名,音声ガイダンスレベル
#           recfile:            録音ファイル名
#           mic:                マイク種類


def record(outfile1, level1, outfile2, level2, outfile3, level3, recfile, mic):
    print("recording ........")
    att.att(outfile1, 'temp0.wav', level1, 0)   # temp0.wav -- 評価音声
    att.att(outfile2, 'temp1.wav', level2, 0)   # temp1.wav -- 環境音
    att.att(outfile3, 'temp2.wav', level3, 0)   # temp2.wav -- 音声ガイダンス

    DeviceOut.SetFileName('temp0.wav', 'temp1.wav')
    DeviceGuideOut.SetFileName('temp2.wav')

    if mic == 'codama':
        DeviceCodama.SetFileName(recfile)
        DeviceCodama.START()
    else:
        DeviceMCU03.SetFileName(recfile)
        DeviceMCU03.START()

    DeviceOut.START()       # 評価音、環境音　出力開始
    DeviceGuideOut.START()  # 音声ガイダンス　出力開始

    while DeviceOut.chek_active():
        time.sleep(0.1)
    DeviceOut.STOP()
    DeviceGuideOut.STOP()

    if mic == 'codama':
        DeviceCodama.STOP()
    else:
        DeviceMCU03.STOP()

    return


def main():
    codama_flag = 1
    cdm_ctrl = codama_ctrl

    if (len(sys.argv) >= 3):
        logfName = sys.argv[3]
    else:
        logfName = './record/rec_log.txt'

    logfile = open(logfName, 'w')

    if (len(sys.argv) >= 2):
        rinfName = sys.argv[2]
    else:
        rinfName = './record/rec_setting.csv'

    rec_info = pd.read_csv(rinfName)  # 録音シーケンス

    row = rec_info.shape[0]
    rec_cnt = 0
    for i in range(row):
        if (rec_info.key[i]).lower() == 'start':
            rec_cnt += 1
        if (rec_info.key[i]).lower() == 'end':
            break

    mic_flag = 'codama'
    envfile = ''
    envlevel = 0
    reffile = ''
    reflevel = 0
    guifile = ''
    guilevel = 0
    rec_path = './record'
    rec_file = 'auto'
    rec_cnt = 0

    for i in range(row):
        if (rec_info.key[i]).lower() == 'end':
            print("END keyword detect in record setting file")
            break
        elif (rec_info.key[i]).lower() == 'mic':
            if (rec_info.augment0[i]).lower() == 'codama':
                mic_flag = 'codama'
                dev_codama_ctrl = cdm_ctrl.find()
                if not dev_codama_ctrl:
                    print("can't control codama")
                    codama_flag = 0
                else:
                    codama_flag = 1
            else:
                micflag = 'mcu03'

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

        elif (rec_info.key[i]).lower() == 'guifile':
            guifile = rec_info.augment0[i]
            print("guidance sound file is ", reffile)

        elif (rec_info.key[i]).lower() == 'guilevel':
            guilevel = rec_info.augment0[i]
            print("guidance sound level is ", reflevel)

        elif (rec_info.key[i]).lower() == 'rec_path':
            rec_path = rec_info.augment0[i]
            print("recording path is ", rec_path)

        elif (rec_info.key[i]).lower() == 'rec_file':
            rec_file = rec_info.augment0[i]
            print("recording file is ", rec_file)

        elif (rec_info.key[i]).lower() == 'prm':
            prm_reg = rec_info.augment0[i]
            prm_val = rec_info.augment1[i]

            if mic_flag == 'codama':
                if codama_flag == 0:
                    print("can't control codama")
                else:
                    dev_codama_ctrl.write(prm_reg, prm_val)
                    ParamValue = dev_codama_ctrl.read(prm_reg)
                    print("codama's param", prm_reg, "is set to ", ParamValue)

        elif(rec_info.key[i]).lower() == 'start':
            if rec_file.lower() == 'auto':
                rec_filename = rec_path + 'rec' + str(rec_cnt) + '.wav'
            else:
                rec_filename = rec_path + rec_file

            logfile.write("#######  recording start  #######" + '\n')
            logfile.write("MIC is:" + mic_flag + '\n')
            logfile.write("envelop sound:" + envfile + "   level:" + str(envlevel)+'\n')
            logfile.write("reference sound:" + reffile + "   level:" + str(reflevel)+'\n')
            logfile.write("guidance sound:" + guifile + "   level:" + str(guilevel)+'\n')
            logfile.write("recording to : " + rec_filename + '\n')

            if mic_flag == 'codama':
                dev_codama_ctrl.dump_reg(logfile)

            record(reffile, float(reflevel), envfile, float(envlevel), guifile, float(guilevel), rec_filename, mic_flag)
            rec_cnt = rec_cnt + 1


if __name__ == '__main__':
    main()
