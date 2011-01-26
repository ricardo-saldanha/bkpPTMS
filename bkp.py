#!/usr/bin/python
# -*- coding: UTF8 -*-
import os,config, alert,utils
import sys 
import tarfile,zipfile
from datetime import datetime
from string import Template
import os,codecs

ok_files = []
os.system(config.MAP_COMMAND)
 
LOG_FILE_NAME = 'bkp.log'
ZIP_LOG_FILE_NAME = 'bkp_log.zip'
inicio = datetime.now()
total_size_bytes = 0L
num_files_ok = 0L
num_files_total = 0L
num_files_fail = 0L
if os.path.exists(utils.get_zip_file_name()):
    os.remove(utils.get_zip_file_name())    
#zip = zipfile.ZipFile(utils.get_zip_file_name(), 'w', zipfile.ZIP_DEFLATED, True)
zip = tarfile.open(utils.get_zip_file_name().encode('utf-8'),'w:gz')
zip.format = tarfile.PAX_FORMAT
log = codecs.open(filename=LOG_FILE_NAME, mode='w',encoding='utf-8')
log.write("Lista De Arquivos Copiados:\n")
fail_files = []
# incluido a nova forma
for root,dirs,files in  os.walk(config.BASE_BKP_DIR):
    for f in files:
        try:
            fname = os.path.join(root,f) 
            print fname
            zip.add(os.path.join(root,f))
            total_size_bytes += os.path.getsize(fname)
            num_files_ok += 1
            log.write(fname+'\n')
        except:
            print "Error :"+fname
            num_files_fail += 1
            fail_files.append(fname)
        num_files_total += 1

        
print 'end backup'
zip.close()
print 'close tar'
log.close()

## apenas ordenando o arquivo para melhor entendimento, Resumo, arquivos com falha e arq. ok.
l = codecs.open(filename=LOG_FILE_NAME, mode='r',encoding='utf-8')
txt = l.read()
l.close() 

log = codecs.open(filename=LOG_FILE_NAME, mode='w',encoding='utf-8')

fim = datetime.now()

#Tmsg = Template("""
#        PTM: $ptm
#        Data: $data
#        Hora de Início: $inicio
#        Hora de Término: $fim
#        Tempo do Backup: $tempo
#        Número Total de arquivos: $tfiles 
#        Número de arquivos copiados: $tfcopied
#        Número de arquivos com falha: $tfail
#        Tamanho Total da origem: $tori
#        Tamanho do arquivo compactado: $tcompact
#        Espaço disponível na unidade de backup: $tavail
#        Nome do arquivo de backup: $fbkp_name
#        Computador de origem: $cpori
#        Computador de destino: $cpdest \n""")



#msg = Tmsg.substitute(ptm=config.PTM_NAME,
#                      data=inicio.date().strftime("%d/%m/%Y"),
#                      inicio=inicio.time().strftime("%H:%M:%S"),
#                      fim=fim.time().strftime("%H:%M:%S"),
#                      tempo=str(fim-inicio),
#                      tfiles=num_files_total,
#                      tfcopied=num_files_ok,
#                      tfail=num_files_fail,
#                      tori=utils.convert_bytes(total_size_bytes),
#                     tcompact=utils.convert_bytes(os.path.getsize(utils.get_zip_file_name())),
#                      tavail=utils.get_free_space(config.TARGET_BKP_DIR),
#                      fbkp_name=utils.get_zip_file_name().,
#                      cpori=config.CP_ORIGEM,
#                      cpdest=config.CP_DESTINO)
print 'ptm='+config.PTM_NAME
print 'data='+inicio.date().strftime("%d/%m/%Y")
print 'inicio='+inicio.time().strftime("%H:%M:%S")
print 'fim='+fim.time().strftime("%H:%M:%S")
print 'tempo='+str(fim-inicio)
print 'tfiles='+str(num_files_total)
print 'tfcopied='+str(num_files_ok)
print 'tfail='+str(num_files_fail)
print 'tori='+str(utils.convert_bytes(total_size_bytes))
print 'tcompact='+str(utils.convert_bytes(os.path.getsize(utils.get_zip_file_name() ) ) )
print 'tavail='+str(utils.get_free_space(config.TARGET_BKP_DIR))
print 'fbkp_name='+utils.get_zip_file_name()
print 'cpori='+config.CP_ORIGEM
print 'cpdest='+config.CP_DESTINO

         
msg = []
msg.append('PTM:'+config.PTM_NAME)

msg.append(u'Data:'+inicio.date().strftime("%d/%m/%Y"))
msg.append(u'Hora de Início:'+inicio.time().strftime("%H:%M:%S"))
msg.append(u'Hora de Término:'+fim.time().strftime("%H:%M:%S"))
msg.append(u'Tempo do Backup:'+str(fim-inicio))
msg.append(u'Número Total de arquivos:'+str(num_files_total))
msg.append(u'Número de arquivos copiados:'+str(num_files_ok))
msg.append(u'Número de arquivos com falha:'+str(num_files_fail))
msg.append(u'Tamanho Total da origem:'+str(utils.convert_bytes(total_size_bytes)))
msg.append(u'Tamanho do arquivo compactado:'+str(utils.convert_bytes(os.path.getsize(utils.get_zip_file_name() ) ) ))
msg.append(u'Espaço disponível na unidade de backup:'+str(utils.get_free_space(config.TARGET_BKP_DIR)))
msg.append(u'Nome do arquivo de backup:'+utils.get_zip_file_name())
msg.append(u'Computador de origem:'+config.CP_ORIGEM)
msg.append(u'Computador de destino:'+config.CP_DESTINO)                      
  
log.write(u'Resumo do Backup:\n'+u'\n'.join(msg))
log.write('\nArquivos com falhas:\n')
if len(fail_files) == 0:
    log.write(u"\n   Não existem arquivos com falhas!  \n\n")
else:
    for fname in fail_files:
        log.write(fname+'\n')

log.write(txt)
log.close()

zlog = zipfile.ZipFile(ZIP_LOG_FILE_NAME, 'w', zipfile.ZIP_DEFLATED, True)
zlog.write(LOG_FILE_NAME)
zlog.close()
alert.Alert().mail("Backup PTM:"+config.PTM_NAME, u'\n'.join(msg), ZIP_LOG_FILE_NAME)

