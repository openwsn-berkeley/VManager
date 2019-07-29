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
from   matplotlib import pyplot as plt
import pylab
import statistics as sta

#============================ defines =========================================

FILENAME                    = 'experiment_data.txt'     # Whole Script
FILENAME_1                  = 'experiment_data_1AP.txt' # Script from the first day
FILENAME_2                  = 'experiment_data_2AP.txt' # Script from the second day
FILENAME_3                  = 'experiment_data_3AP.txt' # Script from the third day


#============================ variables =======================================

#============================ helpers =========================================

def get_list_type(file_name, msg_type):
    list_type              = []

    with open(file_name,'r') as data_file:
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
    temp				   = []					
    counter_parameter      = 0
    
    for x in type_info:
        lista = False 
        position = x['data']
        for i in parameter:
            if type(position)   == dict and counter_parameter == n-1:
                list_data.append(position[i])
            elif type(position) == dict:
                position = position[i]
            elif type(position) == list:
                lista = True
                for j in position:
                    try:
						if counter_parameter == n-1:              # caso connectionInfo = get_data(snapShotList, ['motes','mac_address'])
							element_data.append(j[parameter[-1]])
						else:
							element_data.append(j[i][parameter[-1]])
                    except:
                        for k in position:
                            if i in k:
                                for l in k[i]:
                                    temp.append(l[parameter[-1]]) #parameter[-1] = mac_address
                                element_data.append(temp[:])	
                                temp = []
                            else:
                                element_data.append(temp[:]) #Adiciona um lista vazia 
                        break
                break
            else:
                break
            counter_parameter     += 1
        if lista == True:
            list_data.append(element_data[:])
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
	
#======================= clearing and processing data =========================


#======================= Plotting for all network size ========================

#============================ main ============================================
def main():

	#=== Some debugs tests

	# Filtering Lines per type
	# Notif
	notif_list            = get_list_type(FILENAME, 'notif')    
	
	# SnapShot
	snapShotList          = get_list_type(FILENAME, 'snapshot')
	snapShotList_1        = get_list_type(FILENAME_1, 'snapshot')
	snapShotList_2        = get_list_type(FILENAME_2, 'snapshot')
	snapShotList_3        = get_list_type(FILENAME_3, 'snapshot')
	
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

	# Packets per second
	packets_per_second = []
	for i in range(1, len(network_pckTotal)):
		packets_per_second.append(network_pckTotal[i]/time_stamp[i])
	
	# Latency
	network_latency   = get_data(snapShotList, ['network_info','latency'])

	# Time System
	network_latency   = get_data(snapShotList, ['network_info','latency'])    
		
		
	# Mote Info       
	# Charge
	moteInfo_charge       = get_data(snapShotList,   ['motes','mote_info','charge']) 
	moteInfo_charge_1AP   = get_data(snapShotList_1, ['motes','mote_info','charge']) 
	moteInfo_charge_2AP   = get_data(snapShotList_2, ['motes','mote_info','charge']) 
	moteInfo_charge_3AP   = get_data(snapShotList_3, ['motes','mote_info','charge'])  
	                                                                                 
	# Net Charge - 2
	moteInfo_charge_net_1AP   = moteInfo_charge_1AP
	moteInfo_charge_net_2AP   = []
	moteInfo_charge_net_3AP   = []
	charge_temp_2             = []
	charge_temp_3             = []
	
	for i in range(len(moteInfo_charge_1AP)):
		for j in range(len(moteInfo_charge_1AP[i])):
			charge_temp_2.append(moteInfo_charge_2AP[i][j] - moteInfo_charge_1AP[i][j])
			charge_temp_3.append(moteInfo_charge_3AP[i][j] - moteInfo_charge_2AP[i][j])
		moteInfo_charge_net_2AP.append(charge_temp_2)
		moteInfo_charge_net_3AP.append(charge_temp_3)
		charge_temp_2     = []
		charge_temp_3     = []
	
	'''
	# Charge Max list
	charge_max        = []
	for i in range(1, len(moteInfo_charge)):
		charge_max.append(max(moteInfo_charge[i]))
	'''
	
	#avg_charge_1 = sum(moteInfo_charge_net_1AP)/len(moteInfo_charge_net_1AP)
	#avg_charge_2 = sum(moteInfo_charge_net_2AP)/len(moteInfo_charge_net_2AP)
	#avg_charge_3 = sum(moteInfo_charge_net_3AP)/len(moteInfo_charge_net_3AP)

	# Connections 
	connectionInfo        = get_data(snapShotList, ['motes','connections','mac_address'])
	connectionInfo_mac    = get_data(snapShotList, ['motes','mac_address'])

	#=== Print to test

	#print connectionInfo_mac 
	#print len(connectionInfo_mac[0])
	
	#print connectionInfo 
	#print len(connectionInfo[0])

	#======================= Plotting for all network size ========================
	
	print ('Plotting Graphs ...')
	current_dir = os.getcwd()
	new_dir = current_dir + '\Experiment_Figures'
	if not os.path.exists(new_dir):
		os.makedirs(new_dir)
	'''
	#=== 1 - Numbers of Packet per AP Mote
	#plt.suptitle('Numbers of Packet per AP Mote', fontsize = 14)
	plt.xlabel  ('Time [h] ', fontsize = 10)
	plt.ylabel  ('Number of Packets per Second', fontsize = 10)

	# Axis Configuration 
	range_packets    = range(len(packets_per_second))
	x__time_packets  = map(lambda x:x*1/12, range_packets)  # Convert in hours
	
	x_1          = len(snapShotList_1)/12
	x_2          = (len(snapShotList_1) + len(snapShotList_2))/12
	
	x_1_line     = [x_1, x_1]
	y_1_line     = [min(packets_per_second), max(packets_per_second)]
	             
	y_2_line     = [min(packets_per_second), max(packets_per_second)]
	x_2_line     = [x_2, x_2]

	plt.plot(x__time_packets, packets_per_second, 'k-')
	pylab.plot(x_1_line, y_1_line, 'b--', label = "2 AP Motes")
	pylab.plot(x_2_line, y_2_line, 'r--', label = "3 AP Motes")
	pylab.legend(loc='upper right')
	plt.grid()
	plt.savefig('Experiment_Figures/number_pck_per_total_line.png')
	plt.show()
	'''

	# Fazer um grafico de barras (histograma)
	# -------- converter mC em mV -------- 
	#=== 2 - Charge Consumed per mote and per AP Mote
	
	#plt.suptitle('Charge Consommed', fontsize = 14)
	plt.xlabel  ('Mote Id ', fontsize = 10)
	plt.ylabel  ('Charge Consumed [mC]', fontsize = 10)

	# Axis Configuration 
	x_axis_charge_1 = range(len(moteInfo_charge_1AP[-1]))
	x_axis_charge_2 = range(len(moteInfo_charge_net_2AP[-1]))
	x_axis_charge_3 = range(len(moteInfo_charge_net_3AP[-1]))\
	
	print moteInfo_charge_net_1AP[-1]
	print moteInfo_charge_net_2AP[-1]
	
	plt.hist(moteInfo_charge_net_1AP[-1], x_axis_charge_1, moteInfo_charge_net_1AP[-1]
	#plt.hist(moteInfo_charge_net_2AP[-1], x_axis_charge_2)
	
	#plt.boxplot([moteInfo_charge, moteInfo_charge, moteInfo_charge])
	#pylab.plot(x_axis_charge_1, moteInfo_charge_net_1AP[-1],  'b--', label = "First day")
	#pylab.plot(x_axis_charge_2, moteInfo_charge_net_2AP[-1], 'r--', label = "Second day")
	#pylab.plot(x_axis_charge_3, moteInfo_charge_net_3AP[-1], 'k--', label = "Third day")
	pylab.legend(loc='upper right')
	plt.grid()
	plt.savefig('Experiment_Figures/charge_per_total.png')
	plt.show()

	'''
	#=== 3 - Latency per AP Mote
	#plt.suptitle('Latency per AP Mote', fontsize = 14)
	plt.xlabel  ('Time [h] ', fontsize = 10)
	plt.ylabel  ('Latency [ms]', fontsize = 10)
	
	# Axis Configuration 
	range_latency   = range(len(network_latency))
	x__time         = map(lambda x:x*1/12, range_latency)  # Convert in hours
	
	x_1_line        = [x_1, x_1]
	y_1_line        = [min(network_latency), max(network_latency)]
	               
	y_2_line        = [min(network_latency), max(network_latency)]
	x_2_line        = [x_2, x_2]

	plt.plot(x__time, network_latency, 'k-')
	pylab.plot(x_1_line, y_1_line, 'b--', label = "2 AP Motes")
	pylab.plot(x_2_line, y_2_line, 'r--', label = "3 AP Motes")
	pylab.legend(loc='upper right')
	plt.grid()
	plt.savefig('Experiment_Figures/latency_per_total_line.png')
	plt.show()
	'''
	
	raw_input('Press any key to finish')

if __name__=="__main__":
    main()

