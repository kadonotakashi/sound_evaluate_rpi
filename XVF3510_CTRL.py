# -*- coding: utf-8 -*-

# This code is modified from
# https://github.com/respeaker/usb_4_mic_array
# Code licensed under the Apache License v2.0.
# For details, see http://www.apache.org/licenses/LICENSE-2.0.
# Modifications copyright (C) 2019 Yukai Engineering Inc.
# 
# add -r option Glory T.KDN 2020/01/17


import sys
import struct
import usb.core
import usb.util
import subprocess


# parameter list
XVF_COMMAND = [
    # device control
    'GET_VERSION',
    'GET_MIC_SHIFT_SATURATE', 'SET_MIC_SHIFT_SATURATE',
    # automatic delay estimator control
    'GET_ADEC_ENABLED', 'SET_ADEC_ENABLED',
    'SET_MANUAL_ADEC_CYCLE_TRIGGER',
    'GET_ADEC_MODE',
    'GET_DELAY_SAMPLES', 'SET_DELAY_SAMPLES',
    'GET_DELAY_DIRECTION', 'SET_DELAY_DIRECTION',
    # addaptive echo canceller
    'GET_BYPASS_AEC', 'SET_BYPASS_AEC',
    # 'GET_ADAPTATION_CONFIG_AEC', 'SET_ADAPTATION_CONFIG_AEC',
    # 'GET_FILTER_COEFFICIENTS_AEC',
    'GET_FORCED_MU_VALUE_AEC', 'SET_FORCED_MU_VALUE_AEC',
    'GET_MU_SCALAR_AEC', 'SET_MU_SCALAR_AEC',
    'GET_MU_LIMITS_AEC', 'SET_MU_LIMITS_AEC',
    'GET_ERLE_CH0_AEC', 'GET_ERLE_CH1_AEC',
    'RESET_FILTER_AEC',
    # interference canceller
    'GET_BYPASS_IC', 'SET_BYPASS_IC',
    # 'GET_ADAPTATION_CONFIG_IC',
    'SET_ADAPTATION_CONFIG_IC',
    'RESET_FILTER_IC',
    # 'GET_FILTER_COEFFICIENTS_IC',
    # noise suppression
    'GET_BYPASS_SUP', 'SET_BYPASS_SUP',
    'GET_ENABLED_NS', 'SET_ENABLED_NS',
    'GET_ASR_ALL_CHANNELS', 'SET_ASR_ALL_CHANNELS',
    # automatic gain control'
    'GET_GAIN_CH0_AGC', 'SET_GAIN_CH0_AGC',
    'GET_GAIN_CH1_AGC', 'SET_GAIN_CH1_AGC',
    'GET_ADAPT_CH0_AGC', 'SET_ADAPT_CH0_AGC',
    'GET_ADAPT_CH1_AGC', 'SET_ADAPT_CH1_AGC'
]


class XVF3510_CTRL:
    TIMEOUT = 100000

#    def __init__(self,dev):
#        self.dev = dev

    def write(self, cmnd, value):
        if cmnd not in XVF_COMMAND:
            return False
        if cmnd[0:3] != 'SET':
            return False
        result = subprocess.check_output(['./vfctrl_usb.exe ', cmnd, str(value)])
        return result.decode().strip()

    def read(self, cmnd):
        if cmnd not in XVF_COMMAND:
            return False
        if cmnd[0:3] != 'GET':
            return False

        result = subprocess.check_output(['./vfctrl_usb.exe ', cmnd])
        return result.decode().strip()

    def dumpReg(self, logfile):
        for cmnd in XVF_COMMAND:
            if cmnd[0:3] == 'GET':
                result = subprocess.check_output(['./vfctrl_usb.exe ', cmnd])
                result = result.decode().strip()+'\n'
                logfile.write(result)
        return


def main():
    dev = XVF3510_CTRL()

    logfile = open('test.txt', 'w')
    dev.dumpReg(logfile)
    logfile.close()

    dev.write('SET_ADAPT_CH0_AGC', 0)
    result = dev.write('SET_ADAPT_CH1_AGC', 0)
    print(result)

    result = dev.read('GET_GAIN_CH0_AGC')
    print(result)
    dev.read('GET_GAIN_CH1_AGC')
    dev.write('SET_GAIN_CH0_AGC', 100)
    dev.write('SET_GAIN_CH1_AGC', 100)
    result = dev.read('GET_GAIN_CH0_AGC')
    print(result)
    result = dev.read('GET_GAIN_CH1_AGC')
    print(result)


if __name__ == '__main__':
    main()
