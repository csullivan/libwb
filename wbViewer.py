 # MIT License (MIT)
 #
 # Copyright (c) 2016-  Chris Sullivan
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documentation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to whom the Software is furnished
 # to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in all
 # copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 # INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 # PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 # HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 # OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 # SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


#!/usr/bin/python3
import json
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str,help="Input libwb json file.",default=None)
    args = parser.parse_args()

    if not args.input:
        parser.error("No input file specified.")

    wb = libwb_parser(args.input)
    wb.display_timers()
    wb.display_logger()


class libwb_parser():
    def __init__(self,json_file_path):
        self.raw = []
        self.timers = []
        self.timer_widths = [0,0,0,0]
        self.log_widths = [0,0,0,0]
        self.log = []
        for line in open(json_file_path):
            parsed = json.loads(line)
            self.raw.append(parsed)
            data = parsed['data']
            if 'level' in data.keys() and data['level'] == 'Trace':
                level = data['level']
                location = data['file']+":"+str(data['line'])
                message = data['message']
                log = [level,location,message]
                self.log_widths = [max(len(x),self.log_widths[i]) for i,x in enumerate(log)]
                self.log.append(log)
            if 'start_time' in data.keys():
                timer_data = []
                kind = data['kind']
                location = data['start_file']+":"+str(data['start_line'])
                message = data['message']
                elapsed = str((data['end_time']-data['start_time'])/1.e6)
                timer = [kind,location,elapsed,message]
                self.timer_widths = [max(len(x),self.timer_widths[i]) for i,x in enumerate(timer)]
                self.timers.append(timer)

    def display_timers(self):
        print("\nTimer Output\n")
        width = [str(max(x+10,20)) for x in self.timer_widths]
        aggregate = "{0:<"+width[0]+"}{1:<"+width[1]+"}{2:<"+width[2]+"}{3:<"+width[3]+"}"
        print(aggregate.format("Kind","Location","Time (ms)","Message"))
        for timer in self.timers:
            print(aggregate.format(timer[0],timer[1],timer[2],timer[3]))
    def display_logger(self):
        print("\nLogger Output:\n")
        width = [str(max(x+10,20)) for x in self.log_widths]
        aggregate = "{0:<"+width[0]+"}{1:<"+width[1]+"}{2:<"+width[2]+"}"
        print(aggregate.format("Level","Location","Message"))
        for trace in self.log:
            print(aggregate.format(trace[0],trace[1],trace[2]))

if __name__=="__main__":
    main()
