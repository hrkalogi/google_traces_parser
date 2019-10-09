# Copyright (c) 2019 Christos Kalogirou and Panos Koutsovasilis, University of Thessaly, Greece
# Contact: hrkalogi@inf.uth.gr, pkoutsovasilis@uth.gr
#
# This software is licensed for research and non-commercial use only.
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

import os
import glob
import shutil
from operator import itemgetter
import re

#define the number of the VMs you want to produce
VMS_NUMBER = 100

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

input_folder = "/home/chris/traces/output"
output_folder = "/home/chris/traces/normalized"


if not os.path.exists(output_folder):
    os.mkdir(output_folder)
else:
    for the_file in os.listdir(output_folder):
        file_path = os.path.join(output_folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path): 
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)

time_series = {}

#define the number of scheduling periods
#by default the number of the scheduling periods is 290
for i in range(6,870,3):
    time_series[i] = 10e-9

#extract information for vms from files in output folder
#create the final files for cloudsim which contain the maximum vm requirements and resource usage per scheduling period
vms=0
for idx, ufile in enumerate(natural_sort(glob.glob(input_folder+"/*_usage"))):

    tokens = ufile.split("/")[-1].split("_")
    vm_name = tokens[-3]+"_"+tokens[-2]

    load_file = input_folder+os.sep+vm_name+"_load"

    if not os.path.exists(load_file):
        print "VM incomplete"
        continue

    if vms == VMS_NUMBER:
        break
    
    vms += 1
    
    load_lines = [ float(y) for idx, y in enumerate([x.split(",") for x in open(load_file,"r")][0]) if idx != 1]
    
    usage_lines = [x.replace("\n","").split(",") for x in open(ufile,"r")]
    
    usage_lines = [[float(x[0])/100000000,float(x[2])/load_lines[2]] for x in usage_lines]

    usage_lines = sorted(usage_lines, key=itemgetter(0))
    
    temp_time_series = time_series.copy()

    for x in usage_lines:
        temp_time_series[x[0]] = x[1]
        
#if cpu usage is more than the maximum throttle the VM
        if temp_time_series[x[0]] > 1.0 :
                temp_time_series[x[0]] = 1.0
    
    usage_output_file =open(output_folder+os.sep+str(vm_name),"w")
    usage_output_file.write(str(load_lines[2])+" "+str(load_lines[3])+" "+str(load_lines[1])+"\n")
    for x in temp_time_series:
        usage_output_file.write("{:20.10f}".format(temp_time_series[x]).strip()+"\n")
    usage_output_file.close()


    
    

    


