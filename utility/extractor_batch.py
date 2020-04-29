print('load extractor_batch')

import pandas as pd
import os
import sys
import glob
from tqdm.auto import tqdm 
from queue import Queue
from threading import Thread 
import datetime
import time
import logging


# thread class
class ExtractorDiagramThread(Thread):

    def __init__(self, queue,extdia ,wn):
        Thread.__init__(self)
        self.queue = queue
        self.wn = wn
        self.extdia = extdia
        self.stop = False

    def run(self):
        while not self.stop:
            # Get the work from the queue and expand the tuple
            file_path, target_class = self.queue.get()  
            # execute diagaram
            self.extdia.execute_diagram(file_path,target_class)
            self.queue.task_done()


def IfStrReturnList(s):
    if type(s) == str:
        return [s]
    else:
        return s

def time_stemp_str():
    now = datetime.datetime.now()
    return (now.strftime("%Y-%m-%d %H:%M:%S"))
    
class LoggerWrap():
    def __init__(self):
        self.logger = logging.getLogger('feature_extraction_batch')
        if (self.logger.hasHandlers()):
            self.logger.handlers.clear()
        self.logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        self.fh = logging.FileHandler('feature_extraction_batch.log')
        self.fh.setLevel(logging.DEBUG)
        self.logger.addHandler(self.fh)
    def close(self):
        print('close log file')
        #print(self.fh)
        self.fh.close()
        logging.shutdown()
    def log(self,s):
        m = time_stemp_str() + ': ' +  s
        self.logger.info(m)
        
        print(m)

def get_file_list(machine, snr, id, target_class_map, 
                  FileCountLimit, 
                  datset_folder_from_base, 
                  base_folder):
    flist = []
    tlsit = []
    tn = {}
    fn = {}
    for tc in target_class_map:
        fn[tc] = sorted( \
                 glob.glob( \
                 os.path.abspath( "{base}/{SNR}/{machine}/id_{ID}/{n}/*.{ext}".format(
                base=base_folder+datset_folder_from_base,
                SNR=snr,
                machine=machine,ID=id, 
                n=tc,
                ext='wav' ))))
        
        if FileCountLimit:
            if FileCountLimit < len(fn[tc]):
                    fn[tc] = fn[tc][:FileCountLimit]
        
        tn[tc] = np.ones(len(fn[tc]), dtype='int')*target_class_map[tc]
                
    for tc in target_class_map:
        flist+= fn[tc] 
        tlsit+=(list((tn[tc])))
        
    return flist, tlsit

def multithreadpolltracker(queue, total):
    last = total
    done_l = 0
    pbar = tqdm(total=total)
    while not queue.empty():
        time.sleep(0.05)
        if last > queue.qsize():
            done = total-int(queue.qsize())
            #print(done, end ="--")
            pbar.update(done-done_l)
            done_l = done
        last = queue.qsize()
    queue.join()
    done = total
    pbar.update(done)

def extractor_batch(base_folder, target_folder, extdia, 
                    FileFindDict = {'SNR': '6dB',
                                    'machine': 'pump', 
                                     'ID': ['00']},
                    n_jobs = 1,
                    target_class_map = {'abnormal':1, 'normal': 0},
                    FileCountLimit = None,
                    datset_folder_from_base = 'dataset'):
    lw = LoggerWrap()
    base_folder_full = os.path.abspath(base_folder)
    target_folder_full = os.path.abspath(base_folder+target_folder)
    os.makedirs(target_folder_full, exist_ok=True)
    lw.log('Target folder will be: ' + target_folder_full)
    lw.log('Extractor diagram is fof type: ' + str(extdia))
    
    for m in IfStrReturnList(FileFindDict['machine']):
        for snr in IfStrReturnList(FileFindDict['SNR']):
            for id in IfStrReturnList(FileFindDict['ID']):
                lw.log('Working on machinepart:' + m + ' SNR:' + snr + ' ID:' + id )
                ts = time.time()
                # create file list for ID batch
                filelist, targetlist = get_file_list(m, snr, id, 
                                         target_class_map, 
                                         FileCountLimit, 
                                         datset_folder_from_base, 
                                         base_folder)
                lw.log('Files to process: ' + str(len(filelist)) )
                # start processing
                
                if n_jobs == 1: # in the notebook
                    ed = extdia(base_folder,0)
                    pbar= tqdm(total = len(filelist))
                    for f,tc in (zip(filelist, targetlist)):
                        ed.execute_diagram(f,tc)
                        pbar.update()
                    outport_akkulist_tofile(base_folder,target_folder,ed,m,snr,id)
                    lw.log('list for the id pickled' ) 
                else: # to threads
                    # create the threads and akku diagram
                    edl = []
                    wl = []
                    queue = Queue()
                    for w in range(n_jobs):
                        edl.append(extdia(base_folder,w))
                        worker = ExtractorDiagramThread(queue,edl[w],w)
                        worker.daemon = True
                        worker.start()
                        wl.append(worker)
                    # fill the Queue
                    lw.log('multithread mode filling the queue' )
                    for f,tc in (zip(filelist, targetlist)):
                        queue.put((f, tc))
                    
                    multithreadpolltracker(queue, len(filelist))
                    
                    for w in wl:
                        w.stop = True
                    lw.log('multithread mode all threads done' ) 
                    joinlist = outport_akkulist_join(exdia_list=edl) 
                    outport_akkulist_tofile(base_folder, target_folder, joinlist, m, snr, id)
                    lw.log('multithread mode list joined and pickled for the id' ) 
                tneeded_sec = np.round(time.time()- ts,2)
                tneeded_min = np.round(tneeded_sec/60,2)
                lw.log('total time needed for the ID: ' + str(tneeded_sec) + 'sec' + ' = ' + str(tneeded_min) + 'min') 
                        
                    
    lw.close()