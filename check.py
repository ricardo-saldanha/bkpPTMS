#!/usr/bin/python
# -*- coding: UTF8 -*-
'''
Created on 24/01/2011

@author: rosaldanha
'''
from ping import *
import config,os
import alert
msg = "Teste de backup\n"
try:
    # check if dest is up
    if do_one(config.CP_DESTINO,100):
        msg += "Computador destino ok\n"
    else:
        msg += "Computador destino não pode ser localizado, VERIFIQUE!\n"
        raise Exception( "Computador destino não pode ser localizado, VERIFIQUE!")
# check if drive can be mapped
    if os.system(config.MAP_COMMAND) == 0:
        msg += "Drive de backup mapeado com sucesso\n"
    else:
        msg += "Drive de backup não pode ser mapeado\n"
        raise Exception( "Drive de backup não pode ser mapeado, VERIFIQUE!")
# check if can write to drive
    f = open (os.path.join(config.TARGET_BKP_DIR,'teste.txt'),'w')
    f.write('teste')
    f.close()
    os.remove(os.path.join(config.TARGET_BKP_DIR,'teste.txt'))
    msg += "Teste de escrita no drive de backup OK!\n"    
    alert.Alert().mail("Verificado OK ! Backup PTM:"+config.PTM_NAME, msg,None)
    
except Exception as e:
    print e
    msg += "\n Erro do sistema:\n"+str(e)
    alert.Alert().mail("Falha ! Verifique ! Backup PTM:"+config.PTM_NAME, msg,None)
finally:
    os.system(config.UNMAP_COMMAND)
    