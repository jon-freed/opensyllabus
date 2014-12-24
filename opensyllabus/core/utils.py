# -*- coding:utf8 -*-
"""
Author: Maxim Kosinov
Specialization: Python, HighLoad Crawlers, Data Mining, Scraping
E-Mail: astrey.labs@gmail.com
Skype: geminiozz
O-Desk: Astrey
"""

import os
import re
import logging
import zipfile
import subprocess
from magic import Magic
from logging.handlers import RotatingFileHandler
from logging import StreamHandler, FileHandler, Formatter

from opensyllabus.config import DATA_DIR


log_levels = {
    'debug': logging.DEBUG, 
    'info': logging.INFO, 
    'warning': logging.WARNING, 
    'error': logging.ERROR
}

file_types = {
    'application/pdf': 'pdf',
    'application/msword': 'word',
    'text/html': 'html',
}

def configure_loggers(log, verbosity, log_file, log_verbosity):
    LOGFMT_CONSOLE = ('[%(asctime)s] %(name)-10s %(levelname)-7s in %(module)s.%(funcName)s(),'
                      ' line %(lineno)d\n\t%(message)s')
    
    LOGFMT_FILE = ('[%(asctime)s] [%(process)d]%(name)-10s %(levelname)-7s in %(module)s.%(funcName)s(),'
                   ' line %(lineno)d\n\t%(message)s')

    # Configure root logger to log to stdout
    logging.basicConfig(level=verbosity, datefmt='%H:%M:%S', format=LOGFMT_CONSOLE)
    
    # Configure main logger to rotate log files
    rh = RotatingFileHandler(log_file, maxBytes=100000, backupCount=25)
    log.addHandler(rh)

    # Configure main logger to log to a file
    if log_file:
        fh = FileHandler(log_file, 'w')
        fh.setFormatter(Formatter(LOGFMT_FILE, '%Y-%m-%d %H:%M:%S'))
        fh.setLevel(log_verbosity)
        log.addHandler(fh)
        
    return log


def clean_list(in_list):
    """
    Remove special symbols on each elemnt in the list
    Input: list
    Output: list with cleaned elements
    """
    return [re.sub('[\r\n\t ]+', ' ', el.strip()) for el in in_list if re.sub('[\r\n\t ]+', '', el)]


def get_data_files_2():
    """
    Walking over data directories and return data files
    Input: None
    Output: iterator with pathes to data files
    """
    for i in range(1):
        for top_dir in os.listdir(DATA_DIR):
            for r, dirs, files in os.walk(os.path.join(DATA_DIR, top_dir)):
                for data_file in files:
                    yield os.path.join(r, data_file)
                    
def get_data_files():
    """
    Walking over data directories and return data files
    Input: None
    Output: iterator with pathes to data files
    """
    for top_dir in os.listdir(DATA_DIR):
        if not ('cohen-archive' in top_dir):
            for r, dirs, files in os.walk(os.path.join(DATA_DIR, top_dir)):
                for data_file in files:
                    yield os.path.join(r, data_file)
        else:
            # trick for walk over big directories
            archive_path = os.path.join(DATA_DIR, top_dir, 'web.archive.org', 'web')
            p = subprocess.Popen(['ls', '-f', archive_path], stdout=subprocess.PIPE)
            for dir in p.communicate()[0].split('\n'):
                if dir not in ['.', '..']:
                    for r, dirs, files in os.walk(os.path.join(archive_path, dir)):
                        for data_file in files:
                            yield os.path.join(r, data_file)                
                

def get_file_dir(filepath):
    """
    Return root directory for the file
    Input: full path to file
    Output: root directory
    """
    data_dir = os.path.split(DATA_DIR)[1]
    dirs = filepath.split('/')
    return dirs[dirs.index(data_dir) + 1] 
    
            
def get_file_ext(filename):
    """
    Return file extension
    Input: filename
    Output: file extension
    """
    ext = os.path.splitext(filename)[1].lower()
    if 7 > len(ext) > 1:
        return ext[1:]

    return None
    
    
def get_file_type(filename):
    """
    Return file mime type
    Input: filename
    Output: file mime type
    """
    try:
        mime_type = Magic(mime=True).from_file(filename)
    except:
        pass
    else:
        file_type = file_types.get(mime_type, None)
        
        if file_type == 'word':
            if zipfile.is_zipfile(filename):
                return 'docx'
            else:
                return 'doc'
    
        return file_type
