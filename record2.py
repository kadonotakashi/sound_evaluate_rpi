# -*- coding: utf-8 -*-
import sys
import os
import pandas as pd
import time
import XVF3510_CTRL as xvf_ctrl
import codama_ctrl
import UMC404_PLAY as SoundOut
import CODAMA_REC as SoundInCodama
import XVF3510_REC as SoundInXVF3510
import wave_att as att
DeviceOut = SoundOut.UMC404_PLAY()
DeviceCodama = SoundInCodama.CODAMA_REC()
DeviceXVF3510 = SoundInXVF3510.XVF3510_REC()
att = att.wave_att()
xvf_ctrl = xvf_ctrl.XVF3510_CTRL()

def record(outfile1, level1, outfile2, level2, recfile, mic):
    print("recording ........")
    att.att(outfile1, 'temp0.wav', level1, 0)
    att.att(outfile2, 'temp1.wav', level2, 0)

    DeviceOut.SetFileName('temp0.wav', 'temp1.wav')

    if mic == 'codama':
        DeviceCodama.SetFileName(recfile)
        DeviceCodama.START()
    else:
        DeviceXVF3510.SetFileName(recfile)
        DeviceXVF3510.START()

    DeviceOut.START()

    while DeviceOut.chek_active():
        time.sleep(0.1)
    DeviceOut.STOP()

    if mic == 'codama':
        DeviceCodama.STOP()
    else:
        DeviceXVF3510.STOP()
    return


def main():
    xvf3510_flag = 1
    codama_flag = 1
    cdm_ctrl = codama_ctrl

    if (len(sys.argv) >= 3):
        logfName = sys.argv[3]
    else:
        logfName = './record/rec_log.txt'
    
    logfile = open(logfName,'w')


    if (len(sys.argv) >= 2):
        rinfName = sys.argv[2]
    else:
        rinfName = './record/rec_setting.csv'

    rec_info = pd.read_csv(rinfName) #録音シーケンス

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
    rec_path = './record'
    rec_file = 'auto'
    rec_cnt = 0

    for i in range(row):
        if (rec_info.key[i]).lower() == 'end':
            print("END keyword detect in record setting file")
            break
        elif (rec_info.key[i]).lower() == 'mic':
            if (rec_info.augment0[i]).lower() == 'xvf3510':
                mic_flag = 'xvf3510'
                readvalue = xvf_ctrl.read('GET_VERSION')
                if not readvalue:
                    print("can't control XVF3510")
                    xvf3510_flag = 0
                else:
                    xvf3510_flag = 1
                    print("XVF3510",readvalue)
                
            else:
                mic_flag = 'codama'
                dev_codama_ctrl = cdm_ctrl.find()
                if not dev_codama_ctrl:
                    print("can't control codama")
                    codama_flag = 0
                else:
                    codama_flag = 1

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

            if mic_flag == 'codama':
                if codama_flag == 0:
                    print ("can't control codama")
                else:
                    dev_codama_ctrl.write(prm_reg, prm_val)
                    ParamValue = dev_codama_ctrl.read(prm_reg)
                    print("codama's parameter", prm_reg, "is set to ", ParamValue)
            elif mic_flag == 'xvf3510':
                if xvf3510_flag == 0:
                    print ("can't control XVF3510")
                else:
                    retval = xvf_ctrl.write(prm_reg,prm_val)
                    print(retval)

        elif(rec_info.key[i]).lower() == 'start':
            if rec_file.lower() == 'auto':
                rec_filename = rec_path + 'rec' + str(rec_cnt) + '.wav'
            else:
                rec_filename = rec_path + rec_file

            logfile.write("#####################  recording start  #####################" + '\n')    
            logfile.write("MIC is:" + mic_flag + '\n')    
            logfile.write("envelop sound:" + envfile + "   level:" + str(envlevel)+'\n')   
            logfile.write("reference sound:" + reffile + "   level:" + str(reflevel)+'\n')   
            logfile.write("recording to : " + rec_filename + '\n')   

            if mic_flag == 'xvf3510':
                xvf_ctrl.dumpReg(logfile)
            if mic_flag ==  'codama':
                dev_codama_ctrl.dump_reg(logfile)

            record(reffile, float(reflevel), envfile, float(envlevel), rec_filename, mic_flag)
            rec_cnt = rec_cnt + 1

if __name__ == '__main__':
    main()
