#============================ adjust path =====================================

import sys
import os
if __name__ == "__main__":
    here = sys.path[0]
    sys.path.insert(0, os.path.join(here, '..', '..','libs'))
    sys.path.insert(0, os.path.join(here, '..', '..','external_libs'))

#============================ import =====================================

# Python
import json
import copy
import pprint

# third-party
from matplotlib import pyplot as plt
import statistics as sta

#============================ defines =========================================

FILENAME                   = 'experiment_data.txt'

#============================ variables =======================================

#============================ helpers =========================================

def get_list_type(file_name, msg_type):
    list_type              = []

    with open(FILENAME,'r') as data_file:
        for line in data_file:
            line_dict = json.loads(line)
            if line_dict['type'] == msg_type:
                list_type.append(line_dict)
    data_file.close() 
    return list_type
    
def get_data(type_info, parameter):
    list_data              = []
    element_data           = []
    n                      = len(parameter)
    counter_parameter      = 0
    
    for x in type_info:
        position = x['data']
        for i in parameter:
            if type(position)   == dict and counter_parameter == n-1:
                list_data.append(position[i])
            elif type(position) == dict:
                position = position[i]
            elif type(position) == list:
                for j in position:
                    try:
                        element_data.append(j[i][parameter[-1]])
                    except:
                        pass
                break
            else:
				print 'fedbhfbdhfbdh'
				break
            counter_parameter     += 1
	    list_data.append(element_data)
	    element_data              = []
	    counter_parameter         = 0
        
    return list_data

def get_timestamp(list):
    list_timestamp       = []
    counter              = 0
    for i in list:
        list_timestamp.append(list[counter]['timestamp'])
        counter          = counter + 1
    return list_timestamp

#moteInfo_charge    = get_data(snapShotList, ['motes','mote_info','charge'])
#connectionInfo    = get_data(snapShotList, ['motes','connections','mac_address'])

#======================= clearing and processing data =========================


#======================= Plotting for all network size ========================

#============================ main ============================================
def main():

	#=== Some debugs tests

	# Filtering Lines per type
	notif_list            = get_list_type(FILENAME, 'notif')    
	snapShotList          = get_list_type(FILENAME, 'snapshot')

	#=== Getting data

	# Time 
	time_stamp_snapshot   = get_timestamp(snapShotList)
	time_stamp            = [] 
	for i  in time_stamp_snapshot:
		time_stamp.append(i - time_stamp_snapshot[0])
		
	#=== Notification 
	notifInfo          = get_data(notif_list, ['sys_time']) 
					   
	#=== Network  
	# Number of Packets        
	network_rx         = get_data(snapShotList, ['network_info','rx_packet_count'])   
	network_lost_pck   = get_data(snapShotList, ['network_info','lost_packet_count'])  

	# Total Number of packets 
	network_pckTotal   = []
	for network_rx, network_lost_pck in zip(network_rx, network_lost_pck):
		network_pckTotal.append(network_rx + network_lost_pck) 

	'''
	# Packets per second
	packets_per_second = []
	for i in range(1, len(network_pckTotal)):
		packets_per_second.append(network_pckTotal[i][-1]/time_stamp[i])
    '''
		
	# Latency
	network_latency   = get_data(snapShotList, ['network_info','latency'])

	# Time System
	network_latency   = get_data(snapShotList, ['network_info','latency'])    
					   
	# Mote Info        
	moteInfo_charge   = get_data(snapShotList, ['motes','mote_info','charge']) 

	# Charge Max list
	charge_max        = []
	for i in range(1, len(moteInfo_charge)):
		charge_max.append(max(moteInfo_charge[i]))

	#avg_charge = sum(moteInfo_charge)/len(moteInfo_charge)

	# Connections 
	#connectionInfo    = get_data(snapShotList, ['motes','connections','mac_address']) # Nao Funciona

	#=== Print to test
	
	print len(snapShotList)
	#print moteInfo_charge[1]
	#print len(moteInfo_charge)	
	#print charge_max
	#print len(charge_max)

	#print connectionInfo #-- Nao Funciona
	#print len(connectionInfo)

	#======================= Plotting for all network size ========================
	'''
	print ('Plotting Graphs ...')
	current_dir = os.getcwd()
	new_dir = current_dir + '\Experiment_Figures'
	if not os.path.exists(new_dir):
		os.makedirs(new_dir)

	#1 - Numbers of Packet per AP Mote
	plt.suptitle('Numbers of Packet per AP Mote', fontsize = 12)
	plt.xlabel  ('Number of AP Motes ', fontsize = 10)
	plt.ylabel  ('Number of Packets', fontsize = 10)

	x_axis_packets = range(len(packets_per_second))

	plt.plot(x_axis_packets, packets_per_second, marker = 'o')
	plt.savefig('Experiment_Figures/number_pck_per_total.png')
	plt.show()
	'''
	
	#2 - Charge consommed per mote and per AP Mote
	plt.suptitle('Charge Consommed', fontsize = 12)
	plt.xlabel  ('Number of AP Motes ', fontsize = 10)
	plt.ylabel  ('Charge Consumed [mC]', fontsize = 10)

	x_axis_charge = range(len(moteInfo_charge[-1]))

	#plt.boxplot([moteInfo_charge, moteInfo_charge, moteInfo_charge])
	plt.plot(x_axis_charge, moteInfo_charge[-1], marker = 'o')
	plt.savefig('Experiment_Figures/charge_per_total.png')
	plt.grid()
	plt.show()

	'''
	#3 - Latency per AP Mote
	plt.suptitle('Latency per AP Mote', fontsize = 12)
	plt.xlabel('Number of AP Motes ', fontsize = 10)
	plt.ylabel('Time [ms]', fontsize = 10)

	x_axis_latency = range(len(network_latency))

	plt.plot(x_axis_latency, network_latency, marker = 'o')
	plt.savefig('Experiment_Figures/latency_per_total.png')
	plt.show()
	'''
	raw_input('Press any key to finish')

if __name__=="__main__":
    main()

