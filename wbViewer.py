#!/usr/bin/python3
import json
import argparse
from collections import defaultdict

class libwb_parser():
    def __init__(self,json_file_path):
        self.raw = []
        self.timers = []
        self.traces = defaultdict(list)
        for line in open(json_file_path):
            parsed = json.loads(line)
            self.raw.append(parsed)
            data = parsed['data']
            if 'level' in data.keys() and data['level'] == 'Trace':
                self.traces[data['file']].append(data['message'])
            if 'start_time' in data.keys():
                elapsed = (data['message'],(data['end_time']-data['start_time'])/1.e6)
                self.timers.append(elapsed)
    def display_timers(self):
        print("Timer Output:")
        for timer in self.timers:
            print (timer)
    def display_logger(self):
        print("Logger Output:")
        for key in self.traces.keys():
            print (" "+key+": ")
            for log in self.traces[key]:
                print ("   "+log)



if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input", type=str,help="input file",default=None,required=True)
    args = parser.parse_args()

    wb = libwb_parser(args.input)
    wb.display_timers()
    wb.display_logger()
