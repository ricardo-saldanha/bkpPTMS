# -*- coding: UTF8 -*-
'''
Created on 20/01/2011

@author: rosaldanha
'''
import os
import platform
import ctypes
import datetime
import config

WEEKDAYS = [ 
            u'SEGUNDA',
            u'TERÇA',
            u'QUARTA',
            u'QUINTA',
            u'SEXTA',
            u'SABADO',
            u'DOMINGO',
          ]

def convert_bytes(bytes):
    bytes = float(bytes)
    if bytes >= 1099511627776:
        terabytes = bytes / 1099511627776
        size = '%.2fT' % terabytes
    elif bytes >= 1073741824:
        gigabytes = bytes / 1073741824
        size = '%.2fG' % gigabytes
    elif bytes >= 1048576:
        megabytes = bytes / 1048576
        size = '%.2fM' % megabytes
    elif bytes >= 1024:
        kilobytes = bytes / 1024
        size = '%.2fK' % kilobytes
    else:
        size = '%.2fb' % bytes
    return size


def get_free_space(folder):
    """ Return folder/drive free space (in bytes)
    """
    ufolder = folder.encode('utf-8', 'ignore')
    try:
        if platform.system() == 'Windows':
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(ufolder), None, None, ctypes.pointer(free_bytes))
            return convert_bytes(free_bytes.value)
        else:        
            return convert_bytes(os.statvfs(ufolder).f_bsize * os.statvfs(ufolder).f_bfree)
    except:
        return -1

def get_zip_file_name():    
    return os.path.join(config.TARGET_BKP_DIR,"bkp_"+WEEKDAYS[datetime.datetime.now().weekday()]+".zip") 