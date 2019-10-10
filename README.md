# google_traces_parser

This a preprocessor that parses the Google traces [1] and produces files compatible for CloudSim. It consists of two Python files:
gtraces_parser.py
gtraces_produce.py

The gtraces_parser.py file parses the files under the task_event and task_usage folders. These folders contain the information for the VM requirements and usage. First, you have to define the path of these folders in the gtraces_parser.py. Then, you have to unzip the files in these folders. (For testing reasons, you only have to unzip a few files and not the entire content of the folders, as it may take time.) Then, our parser creates a new folder (output) which contains two files for each VM. The VM_name_load file contains the maximum requirements of a VM as following:
[timestamp], [VM_name], [priority], [max CPU requirements], [max RAM requirements]

The VM_name_usage file contains the load (CPU requirements) of a VM for each scheduling period:
[timestamp], [VM_name], [CPU requirements]

Then we use the gtraces_produce.py in order to create the input files for CloudSim. These are created under the normalized folder. The format of these files is similar to the format of the planetlab traces, in order to avoid extensive changes in the CloudSim code. Each file contains information for one VM. The first line indicates the maximum requirements and characteristics of the VM:
[max CPU requirements] [max RAM requirements] [priority]

The following lines indicate the load of the VMs in relation to their maximum requirements for each scheduling period, similarly to planetlab traces, and the number of these lines is equal to the number of the scheduling periods. For periods when the VM was not live, we use a very small number to initialize the load values. This is to account for the fact that VMs in google traces are not necessarily live during all scheduling periods (at a given point in time they may have left the system or they may have not arrived yet). For periods when the VM is live, the values in the respective lines correspond to the load specified in the trace. In contrast with planetlab traces, we represent the VM load using doubles rather than integers in the traces.

 [1] C. Reiss, J. Wilkes, and J. L. Hellerstein, [“Google cluster-usage traces: format + schema,” Google Inc.](https://github.com/google/cluster-data), Mountain View, CA, USA, Technical Report, Nov. 2011, revised 2014-11-17 for version 2.1.
