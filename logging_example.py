import logging
import os
import datetime


normalLogger = logging.getLogger('normalLogger')

def SetupLogger(loggerName, filename):
    path = 'C:\\my_project\\logs'
    if not os.path.exists(path):
        os.makedirs(path)

    logger = logging.getLogger(loggerName)

    logfilename = datetime.datetime.now().strftime(filename)
    logfilename = os.path.join(path, logfilename)
    
    logformatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    fileHandler = logging.FileHandler(logfilename, 'a', 'utf-8')
    fileHandler.setFormatter(logformatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(logformatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)

    
    

def get_logger(loggerName, level, filename):
    levels = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }
    level = levels[level]

    logger = logging.getLogger(loggerName)
    logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s :: %(levelname).8s :: %(message)s')
    file_handler = logging.FileHandler(filename)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger

    
    
def some_function():
    normalLogger.debug('this is somethimg want to record')
    

if __name__ == '__main__':
    SetupLogger('normalLogger', "%Y-%m-%d.log")
    some_function()
    
