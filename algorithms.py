#!/usr/bin/env python3

from loguru import logger 

from time import monotonic
from os.path import exists
from argparse import ArgumentParser
from configparser import ConfigParser

CONFIG_FILE = "config.ini"

class Tasks: # Tasks namespace

    class test:
        def __init__ (self, data):
            self.data = data['hello'] + data['world']
        def start(self):

            return self.data


if __name__ == '__main__':
    ArgParser = ArgumentParser()
    ArgParser.add_argument("--task", "-t", required = True)
    args = ArgParser.parse_args()

    tasklist = dir(Tasks)
    IsTask = args.task in tasklist

    if IsTask:
        taskInit = getattr(Tasks, args.task)
        
        if exists(CONFIG_FILE):
            data_parse = ConfigParser()
            data_parse.read(CONFIG_FILE)

            try:
                data = data_parse[args.task]
            except KeyError:
                logger.error(f"not found settings for '{args.task}' in config.ini")
                exit()

            start_time = monotonic() 

            result = taskInit(data).start()

            logger.info(f"[{args.task}] time: {monotonic() - start_time}")
            logger.info(f"[{args.task}] output -> {result}")

        else:
            logger.error(f"config file '{CONFIG_FILE}' is not exists *_*")

    elif args.task == "list":
        for x in tasklist:
            if x[0] != "_":
                print(x)
    else:
        logger.error(f"task '{args.task}' is not found *_*")
