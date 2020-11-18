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

 
	
from logging.handlers import BaseRotatingHandler
import codecs

def MultiProcessLogger(loggerName, filename):
    logger = logging.getLogger(loggerName)
    
    path = os.path.join(cwd,'log')
    if not os.path.exists(path):
        os.makedirs(path)
    
    level = logging.DEBUG
    logfilename = os.path.join(path, filename)
    format = '%(asctime)s %(levelname)-8s %(message)s'
    hdlr = MultiProcessSafeDailyRotatingFileHandler(logfilename,encoding='utf-8')
    fmt = logging.Formatter(format)
    hdlr.setFormatter(fmt)
    logger.addHandler(hdlr)
    logger.setLevel(level)
	

# https://my.oschina.net/lionets/blog/796438
class MultiProcessSafeDailyRotatingFileHandler(BaseRotatingHandler):
    """Similar with `logging.TimedRotatingFileHandler`, while this one is
    - Multi process safe
    - Rotate at midnight only
    - Utc not supported
    """
    def __init__(self, filename, encoding=None, delay=False, utc=False, **kwargs):
        self.utc = utc
        self.suffix = "%Y-%m-%d_%H-%M.log"
        self.baseFilename = filename
        self.currentFileName = self._compute_fn()
        BaseRotatingHandler.__init__(self, filename, 'a', encoding, delay)

    def shouldRollover(self, record):
        if self.currentFileName != self._compute_fn():
            return True
        return False

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        self.currentFileName = self._compute_fn()

    def _compute_fn(self):
        return self.baseFilename + "." + time.strftime(self.suffix, time.localtime())

    def _open(self):
        if self.encoding is None:
            stream = open(self.currentFileName, self.mode)
        else:
            stream = codecs.open(self.currentFileName, self.mode, self.encoding)
        # simulate file name structure of `logging.TimedRotatingFileHandler`
        if os.path.exists(self.baseFilename):
            try:
                os.remove(self.baseFilename)
            except OSError:
                pass
        try:
            os.symlink(self.currentFileName, self.baseFilename)
        except OSError:
            pass
        return stream


 
    
def some_function():
    normalLogger.debug('this is somethimg want to record')
    

if __name__ == '__main__':
    #SetupLogger('normalLogger', "%Y-%m-%d.log")
    MultiProcessLogger('normalLogger','server')
    some_function()
    
