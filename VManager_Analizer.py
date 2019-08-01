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
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import	

#============================ defines =========================================

FILENAME                    = 'experiment_data_31_07.txt'     # Whole Script
FILENAME_1                  = 'experiment_data_31_07_1AP.txt' # Script from the first day
FILENAME_2                  = 'experiment_data_31_07_2AP.txt' # Script from the second day
FILENAME_3                  = 'experiment_data_31_07_3AP.txt' # Script from the third day


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
    snapShotList          = get_list_type(FILENAME,   'snapshot')
    snapShotList_1        = get_list_type(FILENAME_1, 'snapshot')
    snapShotList_2        = get_list_type(FILENAME_2, 'snapshot')
    snapShotList_3        = get_list_type(FILENAME_3, 'snapshot')
		
    #=== Getting data

    # Time 
    time_stamp_snapshot        = get_timestamp(snapShotList)
    time_stamp_snapshot_1      = get_timestamp(snapShotList_1)
    time_stamp_snapshot_2      = get_timestamp(snapShotList_2)
    time_stamp_snapshot_3      = get_timestamp(snapShotList_3)
    time_stamp                 = [] 
    time_stamp_1               = [] 
    time_stamp_2               = [] 
    time_stamp_3               = [] 
	
    for i  in time_stamp_snapshot:
        time_stamp.append(i - time_stamp_snapshot[0])
	
    for i  in time_stamp_snapshot_1:
	time_stamp_1.append(i - time_stamp_snapshot_1[0])
	
    for i  in time_stamp_snapshot_2:
	time_stamp_2.append(i - time_stamp_snapshot_2[0])
		
    for i  in time_stamp_snapshot_3:
	time_stamp_3.append(i - time_stamp_snapshot_3[0])
	
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
    network_latency     = get_data(snapShotList, ['network_info','latency'])

    # Network_Reliability
    network_reliability = get_data(snapShotList, ['network_info','reliability'])  
	
    # Mote Info       
    # Charge
    moteInfo_charge       = get_data(snapShotList,   ['motes','mote_info','charge']) 
    moteInfo_charge_1AP   = get_data(snapShotList_1, ['motes','mote_info','charge']) 
    moteInfo_charge_2AP   = get_data(snapShotList_2, ['motes','mote_info','charge']) 
    moteInfo_charge_3AP   = get_data(snapShotList_3, ['motes','mote_info','charge'])  
	                                                                                 
    # Net Charge - 2
    moteInfo_charge_net_1AP   = moteInfo_charge_1AP[:]
    moteInfo_charge_net_2AP   = []
    moteInfo_charge_net_3AP   = []
    charge_temp_2             = []
    charge_temp_3             = []
	
    for i in range(len(moteInfo_charge_3AP)):
	for j in range(len(moteInfo_charge_3AP[i])):
	    charge_temp_2.append(moteInfo_charge_2AP[i][j] - moteInfo_charge_1AP[i][j])
	moteInfo_charge_net_2AP.append(charge_temp_2)
	charge_temp_2   = []
    
    # Net Charge - 2
    for j in range(len(moteInfo_charge_1AP[i])):
	    charge_temp_3.append(moteInfo_charge_3AP[-1][j] - moteInfo_charge_3AP[0][j])
    moteInfo_charge_net_3AP.append(charge_temp_3)
    charge_temp_3   = []
  
    # Charge Max list
    charge_max        = []
    for i in range(1, len(moteInfo_charge)):
	    charge_max.append(max(moteInfo_charge[i]))
        
    # Average Charge list
    avg_charge   = []
    avg_charge.append(sum(moteInfo_charge_net_1AP[-1])/len(moteInfo_charge_net_1AP[-1]))
    avg_charge.append(sum(moteInfo_charge_net_2AP[-1])/len(moteInfo_charge_net_2AP[-1]))
    avg_charge.append(sum(moteInfo_charge_net_3AP[-1])/len(moteInfo_charge_net_3AP[-1]))
        
    # Average charge per second
    avg_consommed_charge = []
    print avg_charge
	
    avg_consommed_charge.append(avg_charge[0]/(time_stamp_1[-1] - time_stamp_1[0]))
    avg_consommed_charge.append(avg_charge[1]/(time_stamp_2[-1] - time_stamp_2[0]))
    avg_consommed_charge.append(avg_charge[2]/(time_stamp_3[-1] - time_stamp_3[0]))
	    
    print avg_consommed_charge
    
    '''
    # Life Time 
    battery_capacity    = 2900 # [mAh]
    battery_charge      = battery_capacity * 3.6 # [C]
	
    charge_per_second   = []
    charge_per_second_1 = []
    charge_per_second_2 = []
    charge_per_second_3 = []    
	
    life_time           = []
    life_time_1         = []
    life_time_2         = []
    life_time_3         = []
	
    for i in range(len(moteInfo_charge_net_1AP[-1])):
	charge_per_second.append(moteInfo_charge[-1][i]/time_stamp[-1])
	charge_per_second_1.append(moteInfo_charge_net_1AP[-1][i]/time_stamp_1[-1])
	charge_per_second_2.append(moteInfo_charge_net_2AP[-1][i]/time_stamp_2[-1])
	charge_per_second_3.append(moteInfo_charge_net_3AP[-1][i]/time_stamp_3[-1])
	life_time.append((battery_charge/charge_per_second[i]))     # [s]
	life_time_1.append((battery_charge/charge_per_second_1[i])) # [s]
	life_time_2.append((battery_charge/charge_per_second_2[i])) # [s]
	life_time_3.append((battery_charge/charge_per_second_3[i])) # [s] 

    life_time_avg_1  = battery_charge/(avg_charge[0]/time_stamp_1[-1])
    life_time_avg_2  = battery_charge/(avg_charge[1]/time_stamp_2[-1])
    life_time_avg_3  = battery_charge/(avg_charge[2]/time_stamp_3[-1])
    
    

    
    # Convert seconds in years
    for i in range(len(life_time_1)):
	    life_time[i]   = life_time[i]  *1000/(24*3600*365)
	    life_time_1[i] = life_time_1[i]*1000/(24*3600*365)
	    life_time_2[i] = life_time_2[i]*1000/(24*3600*365)
	    life_time_3[i] = life_time_3[i]*1000/(24*3600*365)
    
    life_time_avg_1    = life_time_avg_1*1000/(24*3600*365)
    life_time_avg_2    = life_time_avg_2*1000/(24*3600*365)
    life_time_avg_3    = life_time_avg_3*1000/(24*3600*365)
    '''
    
    # Connections 
    connectionInfo        = get_data(snapShotList, ['motes','connections','mac_address'])
    connectionInfo_mac    = get_data(snapShotList, ['motes','mac_address'])

    #=== Print to test
   

    #======================= Plotting for all network size ========================
	
    print ('Plotting Graphs ...')
    current_dir = os.getcwd()
    new_dir = current_dir + '\Experiment_Figures'
    if not os.path.exists(new_dir):
    	os.makedirs(new_dir)
	
    #=== 1 - Numbers of Packet per AP Mote
    #plt.suptitle('Numbers of Packet per AP Mote', fontsize = 14)
    plt.xlabel  ('Time [h] ', fontsize = 10)
    plt.ylabel  ('Number of Packets per Second', fontsize = 10)

    # Axis Configuration 
    range_packets    = range(len(packets_per_second))
    x__time_packets  = map(lambda x:x*0.08333, range_packets)  # Convert in hours
		
    x_1          = len(snapShotList_1)/12                      # Convert in hours
    x_2          = (len(snapShotList_1) + len(snapShotList_2))/12
    #x_1          = len(snapShotList_1)
    #x_2          = (len(snapShotList_1) + len(snapShotList_2))
	
    x_1_line     = [x_1, x_1]
    y_1_line     = [min(packets_per_second), max(packets_per_second)]
	             
    y_2_line     = [min(packets_per_second), max(packets_per_second)]
    x_2_line     = [x_2, x_2]

    plt.plot(x__time_packets, packets_per_second, marker = 'o')
    pylab.plot(x_1_line, y_1_line, 'b--', label = "2 AP Motes")
    pylab.plot(x_2_line, y_2_line, 'r--', label = "3 AP Motes")
    pylab.legend(loc='upper right')
    plt.grid()
    plt.savefig('Experiment_Figures/number_pck_per_total_line.png')
    plt.show()
    
	
    # Fazer um grafico de barras (histograma)
    #=== 2 - Charge Consumed per mote and per AP Mote
	
    #plt.suptitle('Charge Consommed', fontsize = 14)
    plt.xlabel  ('Number of APs ', fontsize = 10)
    plt.ylabel  ('[mC/s]', fontsize = 10)

    # Axis Configuration 
    x_axis_charge_1       = range(len(moteInfo_charge_1AP[-1]))
    x_axis_charge_2       = range(len(moteInfo_charge_net_2AP[-1]))
    x_axis_charge_3       = range(len(moteInfo_charge_net_3AP[-1]))   
    x_axis_avg_charge     = [1,2,3]   
    avg_charge_list_1     = []
    avg_charge_list_2     = []
    avg_charge_list_3     = []

    pylab.plot(x_axis_avg_charge, avg_consommed_charge, marker = 'o')
     
    plt.grid()
    plt.savefig('Experiment_Figures/average_charge.png')
    plt.show()
        
    '''
    for i in range(len(x_axis_charge_1)):
        avg_charge_list_1.append(life_time_avg_1)
        avg_charge_list_2.append(life_time_avg_2)
        avg_charge_list_3.append(life_time_avg_3)
   
    pylab.bar(x_axis_charge_1, life_time_1, color="blue", label = "First day")
    pylab.plot(x_axis_charge_1, avg_charge_list_1,'k-', label = "Average Charge")

    pylab.bar(x_axis_charge_1, life_time_2, color="red", label = "Second day")
    pylab.plot(x_axis_charge_1, avg_charge_list_2,'k-', label = "Average Charge")

    pylab.bar(x_axis_charge_1, life_time_3, color="green", label = "Third day")
    pylab.plot(x_axis_charge_1, avg_charge_list_3,'k-', label = "Average Charge")
	'''
    '''    
    data_to_plot = [life_time_1, life_time_2, life_time_3]
	
    # Create a figure instance
    fig = plt.figure(1, figsize=(9, 6))

    # Create an axes instance
    ax = fig.add_subplot(111)
    	
    # Create the boxplot
    bp = ax.boxplot(data_to_plot)
		
    ax.set_xticklabels(['1 AP', '2 AP', '3 AP'])

    # Save the figure
    plt.savefig('Experiment_Figures/boxplot.png')
    fig.savefig('boxplot.png', bbox_inches='tight')
    '''
	
    #pylab.plot(x_axis_charge_1, life_time_1, 'b--', label = "First day")
    #pylab.plot(x_axis_charge_2, life_time_2, 'r--', label = "Second day")
    #pylab.plot(x_axis_charge_3, life_time_3, 'k--', label = "Third day")
	
    '''
    pylab.legend(loc='upper left')
    plt.savefig('Experiment_Figures/charge_per_total.png')
    plt.show()
    '''
	
   
    '''
    #=== 3 - Latency per AP Mote
    plt.xlabel  ('Time [h] ', fontsize = 10)
    plt.ylabel  ('Latency [ms]', fontsize = 10)
	
    # Axis Configuration 
    range_latency   = range(len(network_latency))
    x__time         = map(lambda x:x*0.08333, range_latency)  # Convert in hours
	
    x_1_line        = [x_1, x_1]
    y_1_line        = [min(network_latency), max(network_latency)]
	               
    y_2_line        = [min(network_latency), max(network_latency)]
    x_2_line        = [x_2, x_2]

    plt.plot(x__time, network_latency, marker = 'o')
    pylab.plot(x_1_line, y_1_line, 'b--', label = "2 AP Motes")
    pylab.plot(x_2_line, y_2_line, 'r--', label = "3 AP Motes")
    pylab.legend(loc='upper right')
    plt.grid()
    plt.savefig('Experiment_Figures/latency_per_total_line.png')
    plt.show()
    '''
    
    '''
    #=== 4 - Network Reliability
	# Axis Configuration
    plt.xlabel  ('Time [h] ', fontsize = 10)
    plt.ylabel  ('Network Reliability [%]', fontsize = 10)
	
    range_reliability   = range(len(network_reliability))
    x__time_reliability = map(lambda x:x*0.08333, range_reliability)  # Convert in hours
	    
    plt.plot(x__time_reliability, network_reliability, marker = 'o')
    pylab.legend(loc='upper right')
    plt.grid()
    plt.savefig('Experiment_Figures/reliability_per_total_line.png')
    plt.show()
    '''
    
    raw_input('Press any key to finish')

if __name__=="__main__":
    main()

