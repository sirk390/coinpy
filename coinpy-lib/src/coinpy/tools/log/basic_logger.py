import logging
import sys

def stdout_logger(name="coinpy", level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    #Stdout
    stdout = logging.StreamHandler(sys.stdout)
    stdout.setFormatter(fmt)
    logger.addHandler(stdout)
    return logger

