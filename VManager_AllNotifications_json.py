#!/usr/bin/python
# -*- coding: cp1252 -*-
'''
This script takes all notifications from motes and network...

'''

#============================ adjust path =====================================

import sys
import os
if __name__ == "__main__":
    here = sys.path[0]
    sys.path.insert(0, os.path.join(here, '..', 'libs'))
    sys.path.insert(0, os.path.join(here, '..', 'external_libs'))

#============================ imports =========================================

import urllib3
import traceback
import base64
import certifi
import json
import datetime
from datetime import datetime
import time, threading

# generic SmartMeshSDK imports
from SmartMeshSDK                      import sdk_version
# VManager-specific imports
from VManagerSDK.vmanager              import Configuration
from VManagerSDK.vmgrapi               import VManagerApi
from VManagerSDK.vmanager.rest         import ApiException
from VManagerSDK.vmanager              import SystemWriteConfig

#============================ defines =========================================

DFLT_VMGR_HOST           = "128.93.102.105"
urllib3.disable_warnings() # disable warnings that show up about self-signed certificates

#============================ variables =======================================

line_counter = 1         
global_counter = [0]*25     # counts the number of packetsfor each notification
period_call_counter = 1
fileLock = threading.RLock()

#============================ helpers =========================================
def process_alarmClosed(mydata):
    '''Process data notifications from dataPacketReceived'''
    global line_counter, global_counter, fileLock

    with fileLock:    
        print 'Writting Line {0} -- Data Notification : {1}\n'.format(line_counter, mydata.type)
        line_counter += 1
        global_counter[0] += 1
        time = datetime.now()
        time_str = time.strftime('%H:%M:%S')
        
        data = {
            mydata.type: {
                "Time": time_str,
                "sysTime": mydata.sys_time,
                "alarmType": mydata.alarm_type,
                "type": mydata.type
                }
            }
        # Function to handle with datetime
        def myconverter(o):
            if isinstance(o, datetime):
                return o.__str__()
        
        json.dump(data, file, default = myconverter)
        file.write("\n")

def process_alarmOpened(mydata):
    '''Process data notifications from dataPacketReceived'''
    global line_counter, global_counter, fileLock

    with fileLock:
        print 'Writting Line {0} -- Data Notification : {1}\n'.format(line_counter, mydata.type)
        line_counter += 1
        global_counter[1] += 1
        time = datetime.now()
        time_str = time.strftime('%H:%M:%S') 

        data = {
            mydata.type: {
                "Time": time_str,
                "sysTime": mydata.sys_time,
                "alarmType": mydata.alarm_type,
                "type": mydata.type
                }
            }
        # Function to handle with datetime
        def myconverter(o):
            if isinstance(o, datetime):
                return o.__str__()
        
        json.dump(data, file, default = myconverter)
        file.write("\n")

def process_apStateChanged(mydata):
    '''Process data notifications from dataPacketReceived'''
    global line_counter, global_counter, fileLock

    with fileLock:
        print 'Writting Line {0} -- Data Notification : {1}\n'.format(line_counter, mydata.type)
        line_counter += 1
        global_counter[2] += 1
        time = datetime.now()
        time_str = time.strftime('%H:%M:%S') 

        data = {
            mydata.type: {
                "Time": time_str,
                "sysTime": mydata.sys_time,
                "reason": mydata.reason,
                "state": mydata.state,
                "macAddress": mydata.mac_address,
                "type": mydata.type
                }
            }
        # Function to handle with datetime
        def myconverter(o):
            if isinstance(o, datetime):
                return o.__str__()
        
        json.dump(data, file, default = myconverter)
        file.write("\n")

def process_cmdFinished(mydata):
    '''Process data notifications from dataPacketReceived'''
    global line_counter, global_counter, fileLock

    with fileLock:
        print 'Writting Line {0} -- Data Notification : {1}\n'.format(line_counter, mydata.type)
        line_counter += 1
        global_counter[3] += 1
        time = datetime.now()
        time_str = time.strftime('%H:%M:%S') 

        data = {
            mydata.type: {
                "Time": time_str,
                "sysTime": mydata.sys_time,
                "callbackId": mydata.callback_id,
                "resultCode": mydata.result_code,
                "type": mydata.type
                }
            }
        # Function to handle with datetime
        def myconverter(o):
            if isinstance(o, datetime):
                return o.__str__()
        
        json.dump(data, file, default = myconverter)
        file.write("\n")

def process_configChanged(mydata):
    '''Process data notifications from dataPacketReceived'''
    global line_counter, global_counter, fileLock

    with fileLock:
        print 'Writting Line {0} -- Data Notification : {1}\n'.format(line_counter, mydata.type)
        line_counter += 1
        global_counter[4] += 1
        time = datetime.now()
        time_str = time.strftime('%H:%M:%S')  

        data = {
            mydata.type: {
                "Time": time_str,
                "sysTime": mydata.sys_time,
                "module": mydata.module,
                "type": mydata.type
                }
            }
        # Function to handle with datetime
        def myconverter(o):
            if isinstance(o, datetime):
                return o.__str__()
        
        json.dump(data, file, default = myconverter)
        file.write("\n")

def process_configDeleted(mydata):
    '''Process data notifications from dataPacketReceived'''
    global line_counter, global_counter, fileLock

    with fileLock:
        print 'Writting Line {0} -- Data Notification : {1}\n'.format(line_counter, mydata.type)
        line_counter += 1
        global_counter[5] += 1
        time = datetime.now()
        time_str = time.strftime('%H:%M:%S') 

        data = {
            mydata.type: {
                "Time": time_str,
                "sysTime": mydata.sys_time,
                "module": mydata.module,
                "type": mydata.type
                }
            }
        # Function to handle with datetime
        def myconverter(o):
            if isinstance(o, datetime):
                return o.__str__()
        
        json.dump(data, file, default = myconverter)
        file.write("\n")

def process_configLoaded(mydata):
    '''Process data notifications from dataPacketReceived'''
    global line_counter, global_counter, fileLock

    with fileLock:
        print 'Writting Line {0} -- Data Notification : {1}\n'.format(line_counter, mydata.type)
        line_counter += 1
        global_counter[6] += 1
        time = datetime.now()
        time_str = time.strftime('%H:%M:%S')  

        data = {
            mydata.type: {
                "Time": time_str,
                "sysTime": mydata.sys_time,
                "module": mydata.module,
                "type": mydata.type
                }
            }
        # Function to handle with datetime
        def myconverter(o):
            if isinstance(o, datetime):
                return o.__str__()
        
        json.dump(data, file, default = myconverter)
        file.write("\n")

def process_configRestored(mydata):
    '''Process data notifications from dataPacketReceived'''
    global line_counter, global_counter, fileLock

    with fileLock:
        print 'Writting Line {0} -- Data Notification : {1}\n'.format(line_counter, mydata.type)
        line_counter += 1
        global_counter[7] += 1
        time = datetime.now()
        time_str = time.strftime('%H:%M:%S')
        
        data = {
            mydata.type: {
                "Time": time_str,
                "sysTime": mydata.sys_time,
                "module": mydata.module,
                "type": mydata.type
                }
            }
        # Function to handle with datetime
        def myconverter(o):
            if isinstance(o, datetime):
                return o.__str__()
        
        json.dump(data, file, default = myconverter)
        file.write("\n")
                
def process_dataPacketReceived(mydata):
    '''Process data notifications from dataPacketReceived'''
    global line_counter, global_counter, time, time_str, fileLock

    with fileLock:    
        print 'Writting Line {0} -- Data Notification : {1}\n'.format(line_counter, mydata.type)
        line_counter += 1
        global_counter[8] += 1   
        time = datetime.now()
        time_str = time.strftime('%H:%M:%S')
        
        data = {
            mydata.type: {
                "Time": time_str,
                "sysTime": mydata.sys_time,
                "macAddress": mydata.mac_address,
                "Latency": mydata.latency,
                "payload": mydata.payload,
                "genNetTime": mydata.gen_net_time,
                "macAddress": mydata.mac_address,
                "destPort": mydata.dest_port,
                "type": mydata.type,
                "hops": mydata.hops
                }
            }
        # Function to handle with datetime
        def myconverter(o):
            if isinstance(o, datetime):
                return o.__str__()
        
        json.dump(data, file, default = myconverter)
        file.write("\n")
    
def process_deviceHealthReport(mydata):
    '''Process data notifications from HealthReport'''
    global line_counter, global_counter, fileLock

    with fileLock:
        print 'Writting Line {0} -- Data Notification : {1}\n'.format(line_counter, mydata.type)
        line_counter += 1
        global_counter[9] =+ 1
        time = datetime.now()
        time_str = time.strftime('%H:%M:%S')

        data = {
            mydata.type: {
                "Time": time_str,
                "badLinkFailures": mydata.bad_link_failures,
                "badLinkFrameId": mydata.bad_link_frame_id,
                "badLinkOffset": mydata.bad_link_offset,
                "numRxDrop": mydata.num_rx_drop,
                "macAddress": mydata.mac_address,
                "numTxFail": mydata.num_tx_fail,
                "avgQueue": mydata.avg_queue,
                "type": mydata.type,
                "numRxOk": mydata.num_rx_ok,
                "temperature": mydata.temperature,
                "sysTime": mydata.sys_time,
                "numTxOk": mydata.num_tx_ok,
                "charge": mydata.charge,
                "voltage": mydata.voltage,
                "badLinkSlot": mydata.bad_link_slot,
                "numMacDrop": mydata.num_mac_drop,
                "maxQueue": mydata.max_queue
                }
            }
        # Function to handle with datetime
        def myconverter(o):
            if isinstance(o, datetime):
                return o.__str__()
        
        json.dump(data, file, default = myconverter)
        file.write("\n")

def process_discoveryHealthReport(mydata):
    '''Process data notifications from HealthReport'''
    global line_counter, global_counter, fileLock

    with fileLock:   
        print 'Writting Line {0} -- Data Notification : {1}\n'.format(line_counter, mydata.type)
        line_counter += 1
        global_counter[10] += 1
        time = datetime.now()
        time_str = time.strftime('%H:%M:%S') 

        data = {
            mydata.type: {
                "Time": time_str,
                "sysTime": mydata.sys_time,
                "discoveredNeighbors": mydata.discovered_neighbors,
                "macAddress": mydata.mac_address,
                "type": mydata.type,
                #"heardCount": mydata.heard_count,
                #"macAddress": mydata.mac_address,
                #"rssi": mydata.rssi
                }
            }
        # Function to handle with datetime
        def myconverter(o):
            if isinstance(o, datetime):
                return o.__str__()
        
        json.dump(data, file, default = myconverter)
        file.write("\n")

def process_invalidMIC(mydata):
    '''Process data notifications from HealthReport'''
    global line_counter, global_counter, fileLock

    with fileLock: 
        print 'Writting Line {0} -- Data Notification : {1}\n'.format(line_counter, mydata.type)
        line_counter += 1
        global_counter[11] += 1
        time = datetime.now()
        time_str = time.strftime('%H:%M:%S')

        data = {
            mydata.type: {
                "Time": time_str,
                "sysTime": mydata.sys_time,
                "macAddress": mydata.mac_address,
                "type": mydata.type
                }
            }
        # Function to handle with datetime
        def myconverter(o):
            if isinstance(o, datetime):
                return o.__str__()
        
        json.dump(data, file, default = myconverter)
        file.write("\n")

def process_ipPacketReceived(mydata):
    '''Process data notifications from dataPacketReceived'''
    global line_counter, global_counter, fileLock

    with fileLock:  
        print 'Writting Line {0} -- Data Notification : {1}\n'.format(line_counter, mydata.type)
        line_counter += 1
        global_counter[12] += 1
        time = datetime.now()
        time_str = time.strftime('%H:%M:%S')

        data = {
            mydata.type: {
                "Time": time_str,
                "sysTime": mydata.sys_time,
                "Latency": mydata.latency,
                "macAddress": mydata.mac_address,
                "payload": mydata.payload,
                "genNetTime": mydata.gen_net_time,
                "macAddress": mydata.mac_address,
                "type": mydata.type,
                "hops": mydata.hops
                }
            }
        # Function to handle with datetime
        def myconverter(o):
            if isinstance(o, datetime):
                return o.__str__()
        
        json.dump(data, file, default = myconverter)
        file.write("\n")

def process_joinFailed(mydata):
    '''Process data notifications from dataPacketReceived'''
    global line_counter, global_counter, fileLock

    with fileLock:   
        print 'Writting Line {0} -- Data Notification : {1}\n'.format(line_counter, mydata.type)
        line_counter += 1
        global_counter[13] += 1
        time = datetime.now()
        time_str = time.strftime('%H:%M:%S')

        data = {
            mydata.type: {
                "Time": time_str,
                "sysTime": mydata.sys_time,
                "reason": mydata.reason,
                "macAddress": mydata.mac_address,
                "type": mydata.type
                }
            }
        # Function to handle with datetime
        def myconverter(o):
            if isinstance(o, datetime):
                return o.__str__()
        
        json.dump(data, file, default = myconverter)
        file.write("\n")

def process_managerStarted(mydata):
    '''Process data notifications from dataPacketReceived'''
    global line_counter, global_counter, fileLock

    with fileLock:  
        print 'Writting Line {0} -- Data Notification : {1}\n'.format(line_counter, mydata.type)
        line_counter += 1
        global_counter[14] += 1
        time = datetime.now()
        time_str = time.strftime('%H:%M:%S')

        data = {
            mydata.type: {
                "Time": time_str,
                "sysTime": mydata.sys_time,
                "type": mydata.type
                }
            }
        # Function to handle with datetime
        def myconverter(o):
            if isinstance(o, datetime):
                return o.__str__()
        
        json.dump(data, file, default = myconverter)
        file.write("\n")

def process_managerStopping(mydata):
    '''Process data notifications from dataPacketReceived'''
    global line_counter, global_counter, fileLock

    with fileLock:    
        print 'Writting Line {0} -- Data Notification : {1}\n'.format(line_counter, mydata.type)
        line_counter += 1
        global_counter[15] += 1
        time = datetime.now()
        time_str = time.strftime('%H:%M:%S')

        data = {
            mydata.type: {
                "Time": time_str,
                "sysTime": mydata.sys_time,
                "type": mydata.type
                }
            }
        # Function to handle with datetime
        def myconverter(o):
            if isinstance(o, datetime):
                return o.__str__()
        
        json.dump(data, file, default = myconverter)
        file.write("\n")

def process_moteStateChanged(mydata):
    '''Process data notifications from dataPacketReceived'''
    global line_counter, global_counter, fileLock

    with fileLock:    
        print 'Writting Line {0} -- Data Notification : {1}\n'.format(line_counter, mydata.type)
        line_counter += 1
        global_counter[16] += 1
        time = datetime.now()
        time_str = time.strftime('%H:%M:%S')

        data = {
            mydata.type: {
                "Time": time_str,
                "sysTime": mydata.sys_time,
                "reason": mydata.reason,
                "state": mydata.state,
                "macAddress": mydata.mac_address,
                "type": mydata.type
                }
            }
        # Function to handle with datetime
        def myconverter(o):
            if isinstance(o, datetime):
                return o.__str__()
        
        json.dump(data, file, default = myconverter)
        file.write("\n")

def process_neighborHealthReport(mydata):
    '''Process data notifications from dataPacketReceived'''
    global line_counter, global_counter, fileLock

    with fileLock:   
        print 'Writting Line {0} -- Data Notification : {1}\n'.format(line_counter, mydata.type)
        line_counter += 1
        global_counter[17] += 1
        time = datetime.now()
        time_str = time.strftime('%H:%M:%S')

        data = {
            mydata.type: {
                "Time": time_str,
                "sysTime": mydata.sys_time,
                "connectedNeighbors": mydata.connected_neighbors,
                "macAddress": mydata.mac_address,
                "type": mydata.type,
                "macAddress": mydata.mac_address,
                #"numRx": mydata.num_rx,
                #"numtx": mydata.num_tx,
                #"numTxFail": mydata.num_tx_fail,
                #"rssi": mydata.rssi
                }
            }
        # Function to handle with datetime
        def myconverter(o):
            if isinstance(o, datetime):
                return o.__str__()
        
        json.dump(data, file, default = myconverter)
        file.write("\n")

def process_optPhase(mydata):
    '''Process data notifications from dataPacketReceived'''
    global line_counter, global_counter, fileLock

    with fileLock:  
        print 'Writting Line {0} -- Data Notification : {1}\n'.format(line_counter, mydata.type)
        line_counter += 1
        global_counter[18] += 1
        time = datetime.now()
        time_str = time.strftime('%H:%M:%S')

        data = {
            mydata.type: {
                "Time": time_str,
                "sysTime": mydata.sys_time,
                "type": mydata.type,
                "phase": mydata.phase
                }
            }
        # Function to handle with datetime
        def myconverter(o):
            if isinstance(o, datetime):
                return o.__str__()
        
        json.dump(data, file, default = myconverter)
        file.write("\n")

def process_packetSent(mydata):
    '''Process data notifications from dataPacketReceived'''
    global line_counter, global_counter, fileLock

    with fileLock:   
        print 'Writting Line {0} -- Data Notification : {1}\n'.format(line_counter, mydata.type)
        line_counter += 1
        global_counter[19] += 1
        time = datetime.now()
        time_str = time.strftime('%H:%M:%S')

        data = {
            mydata.type: {
                "Time": time_str,
                "sysTime": mydata.sys_time,
                "callbackId": mydata.callback_id,
                "type": mydata.type
                }
            }
        # Function to handle with datetime
        def myconverter(o):
            if isinstance(o, datetime):
                return o.__str__()
        
        json.dump(data, file, default = myconverter)
        file.write("\n")
        
def process_pathAlert(mydata):
    '''Process data notifications from dataPacketReceived'''
    global line_counter, global_counter, fileLock

    with fileLock:    
        print 'Writting Line {0} -- Data Notification : {1}\n'.format(line_counter, mydata.type)
        line_counter += 1
        global_counter[20] += 1
        time = datetime.now()
        time_str = time.strftime('%H:%M:%S')

        data = {
            mydata.type: {
                "Time": time_str,
                "sysTime": mydata.sys_time,
                "endpointA": mydata.endpoint_a,
                "endpointB": mydata.endpoint_b,
                "type": mydata.type
                }
            }
        # Function to handle with datetime
        def myconverter(o):
            if isinstance(o, datetime):
                return o.__str__()
        
        json.dump(data, file, default = myconverter)
        file.write("\n")

def process_pathStateChanged(mydata):
    '''Process data notifications from dataPacketReceived'''
    global line_counter, global_counter, fileLock

    with fileLock:   
        print 'Writting Line {0} -- Data Notification : {1}\n'.format(line_counter, mydata.type)
        line_counter += 1
        global_counter[21] += 1
        time = datetime.now()
        time_str = time.strftime('%H:%M:%S')

        data = {
            mydata.type: {
                "Time": time_str,
                "sysTime": mydata.sys_time,
                "endpointA": mydata.endpoint_a,
                "endpointB": mydata.endpoint_b,
                "state": mydata.state,
                "parent": mydata.parent,
                "type": mydata.type
                }
            }
        # Function to handle with datetime
        def myconverter(o):
            if isinstance(o, datetime):
                return o.__str__()
        
        json.dump(data, file, default = myconverter)
        file.write("\n")

def process_pingResponse(mydata):
    '''Process data notifications from dataPacketReceived'''
    global line_counter, global_counter, fileLock

    with fileLock:    
        print 'Writting Line {0} -- Data Notification : {1}\n'.format(line_counter, mydata.type)
        line_counter += 1
        global_counter[22] += 1
        time = datetime.now()
        time_str = time.strftime('%H:%M:%S') 

        data = {
            mydata.type: {
                "Time": time_str,
                "sysTime": mydata.sys_time,
                "result": mydata.result,
                "latency": mydata.latency,
                "hopCount": mydata.hop_count,
                "voltage": mydata.voltage,
                "callbackId": mydata.callback_id,
                "macAddress": mydata.mac_address,
                "type": mydata.type,
                "temperature": mydata.temperature
                }
            }
        # Function to handle with datetime
        def myconverter(o):
            if isinstance(o, datetime):
                return o.__str__()
        
        json.dump(data, file, default = myconverter)
        file.write("\n")

def process_rawMoteNotification(mydata):
    '''Process data notifications from dataPacketReceived'''
    global line_counter, global_counter, fileLock

    with fileLock:    
        print 'Writting Line {0} -- Data Notification : {1}\n'.format(line_counter, mydata.type)
        line_counter += 1
        global_counter[23] += 1
        time = datetime.now()
        time_str = time.strftime('%H:%M:%S') 

        data = {
            mydata.type: {
                "Time": time_str,
                "sysTime": mydata.sys_time,
                "payload": mydata.payload,
                "macAddress": mydata.mac_address,
                "type": mydata.type
                }
            }
        # Function to handle with datetime
        def myconverter(o):
            if isinstance(o, datetime):
                return o.__str__()
        
        json.dump(data, file, default = myconverter)
        file.write("\n")

def process_serviceChanged(mydata):
    '''Process data notifications from dataPacketReceived'''
    global line_counter, global_counter, fileLock

    with fileLock:    
        print 'Writting Line {0} -- Data Notification : {1}\n'.format(line_counter, mydata.type)
        line_counter += 1
        global_counter[24] += 1
        time = datetime.now()
        time_str = time.strftime('%H:%M:%S')

        data = {
            mydata.type: {
                "Time": time_str,
                "sysTime": mydata.sys_time,
                "destMacAddress": mydata.dest_mac_address,
                "allocatedPkPeriod": mydata.allocated_pk_period,
                "sourceMacAddress": mydata.source_mac_address,
                "type": mydata.type
                }
            }
        # Function to handle with datetime
        def myconverter(o):
            if isinstance(o, datetime):
                return o.__str__()
        
        json.dump(data, file, default = myconverter)
        file.write("\n")

# This function will be called in a specific period of time  
def period_call():
    '''Make a Description ...'''
    global line_counter, global_counter, period_call_counter, fileLock

    with fileLock:
        print 'Writting Line {0} -- Period Call: {1}\n'.format(line_counter, period_call_counter)
        line_counter += 1
        period_call_counter += 1
        time = datetime.now()
        time_str = time.strftime('%H:%M:%S')
            
        # Get the whole list of motes 
        mote_list = voyager.motesApi.get_motes()

        # Convert "mote_list" to a dictionary
        list_of_mote = mote_list.to_dict()

        # Function to handle with datetime
        def myconverter(o):
            if isinstance(o, datetime):
                return o.__str__()

        # Command to write only this file 
        
        print 'Writting Period Call ...'
        # ======================= Motes Information =======================
        file.write('Time :' + time_str + '\n')
            # This loop takes the information concernning each mote
        for motes in list_of_mote.values():
           for mac in motes:
               file.write(mac['mac_address'])
               mote_info = voyager.motesApi.get_mote_info(mac['mac_address']).to_str()
               mote_info = mote_info.replace("\n","")
               file.write(mote_info)
               file.write("\n")
                       
        # ========================== Motes Paths ==========================
        file.write('Time :' + time_str + '\n')

        # Get Mote Paths
        # This loop takes the paths concernning each mote
        for motes in list_of_mote.values():
           for mac in motes:
               file.write(mac['mac_address'])
               mote_path = voyager.pathsApi.get_connections(mac['mac_address']).to_str()
               mote_path = mote_path.replace("\n             ","")
               json.dump(mote_path, file, indent=-8, default = myconverter)
               #file.write(mote_path) # param str mac: MAC Address (required)
               file.write("\n")

        # ======================== NetWork Statistics ========================
        file.write('Time :' + time_str + '\n')
        
        # Get Network Statistics
        file.write("network_statistics")
        network_info = voyager.networkApi.get_network_info().to_str()
        network_info = network_info.replace("\n","")
        json.dump(network_info, file, indent=-4)
        file.write("\n")
        
        threading.Timer(60, period_call).start() # The first parameter is in seconds Ex: 600 = 10 minutes
        print 'Period Call Finished ...'
        # =================================================================
    
########## Process Notif ##########
def process_notif(notif):
    '''
    Dispatch notifications to specific processing functions
    '''
    if   notif.type in (
            'alarmClosed'
        ):
        # handle data notifications
        process_alarmClosed(notif)
        pass
        
    elif   notif.type in (
            'alarmOpened'
        ):
        # handle data notifications
        process_alarmOpened(notif)
        pass
        
    elif   notif.type in (
            'apStateChanged'
        ):
        # handle data notifications
        process_apStateChanged(notif)
        pass
        
    elif   notif.type in (
            'configChanged'
        ):
        # handle data notifications
        process_configChanged(notif)
        pass
        
    elif   notif.type in (
            'configDeleted'
        ):
        # handle data notifications
        process_configDeleted(notif)
        pass
        
    elif   notif.type in (
            'configChanged'
        ):
        # handle data notifications
        process_configChanged(notif)
        pass
        
    elif   notif.type in (
            'configLoaded'
        ):
        # handle data notifications
        process_configLoaded(notif)
        pass
        
    elif   notif.type in (
            'configRestored'
        ):
        # handle data notifications
        process_configRestored(notif)
        pass
        
    elif   notif.type in (
            'dataPacketReceived'
        ):
        # handle data notifications
        process_dataPacketReceived(notif)        
        pass
        
    elif notif.type in (
            'deviceHealthReport'
        ):
        # handle health reports
        process_deviceHealthReport(notif)
        pass
        
    elif   notif.type in (
            'discoveryHealthReport'
        ):
        # handle data notifications
        process_discoveryHealthReport(notif)
        pass
        
    elif   notif.type in (
            'invalidMIC'
        ):
        # handle data notifications
        process_invalidMIC(notif)
        pass
        
    elif   notif.type in (
            'ipPacketReceived'
        ):
        # handle data notifications
        process_ipPacketReceived(notif)
        pass
        
    elif   notif.type in (
            'joinFailed'
        ):
        # handle data notifications
        process_joinFailed(notif)
        pass
        
    elif   notif.type in (
            'managerStarted'
        ):
        # handle data notifications
        process_managerStarted(notif)
        pass
        
    elif   notif.type in (
            'managerStopping'
        ):
        # handle data notifications
        process_managerStopping(notif)
        pass
        
    elif   notif.type in (
            'moteStateChanged'
        ):
        # handle data notifications
        process_moteStateChanged(notif)
        pass
        
    elif   notif.type in (
            'neighborHealthReport'
        ):
        # handle data notifications
        process_neighborHealthReport(notif)        
        pass
        
    elif notif.type in (
            'optPhase'
        ):
        # handle health reports
        process_optPhase(notif)
        pass
        
    elif   notif.type in (
            'packetSent'
        ):
        # handle data notifications
        process_packetSent(notif)
        pass
        
    elif   notif.type in (
            'pathAlert'
        ):
        # handle data notifications
        process_pathAlert(notif)
        pass
        
    elif   notif.type in (
            'pathStateChanged'
        ):
        # handle data notifications
        process_pathStateChanged(notif)        
        pass
        
    elif notif.type in (
            'pingResponse'
        ):
        # handle health reports
        process_pingResponse(notif)
        pass
        
    elif   notif.type in (
            'rawMoteNotification'
        ):
        # handle data notifications
        process_rawMoteNotification(notif)
        pass
        
    elif   notif.type in (
            'serviceChanged'
        ):
        # handle other event notifications
        process_serviceChanged(notif)
        pass
        
    else:
        # handle other event notifications
        pass

#============================ main ============================================

try:
    # print banner
    print '\nVMgr_LifeTime (c) Dust Networks'
    print 'SmartMesh SDK {0}\n'.format('.'.join([str(i) for i in sdk_version.VERSION]))

    # ask the user for VManager host
    mgrhost = raw_input('Enter the IP address of the manager (e.g. {0} ): '.format(DFLT_VMGR_HOST))
    if mgrhost == "":
        mgrhost = DFLT_VMGR_HOST

    # log-in as user "dust"
    config = Configuration()
    config.username     = 'dust'
    config.password     = 'dust'
    config.verify_ssl   = False
    
    if os.path.isfile(certifi.where()):
        config.ssl_ca_cert  = certifi.where()
    else:
        config.ssl_ca_cert = os.path.join(os.path.dirname(sys.executable), "cacert.pem")

    # initialize the VManager Python library
    voyager = VManagerApi(host=mgrhost)

    fileLock = threading.RLock()
    
    # Get the whole list of motes 
    mote_list = voyager.motesApi.get_motes()

    # Create a script in the VManager_Data folder
    file = open(os.path.join('C:\INRIA-Victor\VManager\Scripts\smartmeshsdk\VManager_Data',"teste.txt"), "w")

    print 'Script Created Successfully !'

    # Start listening for data notifications
    voyager.get_notifications(notif_callback=process_notif)
    period_call()

    print '\n==== Subscribing to data notifications'
    reply = raw_input ('\n Waiting for notifications from mote, Press any key to stop\n')

    file.close
    print 'Script Closed'
   
    voyager.stop_notifications()
    print 'Script ended normally'

    print '================================================================================'
    print 'alarmClosed Packets: {0}\n'.format(global_counter[0])
    print 'alarmOpened Packets: {0}\n'.format(global_counter[1])
    print 'apStateChanged Packets: {0}\n'.format(global_counter[2])
    print 'cmdFinished Packets: {0}\n'.format(global_counter[3])
    print 'configChanged Packets: {0}\n'.format(global_counter[4])
    print 'configDeleted Packets: {0}\n'.format(global_counter[5])
    print 'configLoaded Packets: {0}\n'.format(global_counter[6])
    print 'configRestored Packets: {0}\n'.format(global_counter[7])
    print 'dataPacketReceived Packets: {0}\n'.format(global_counter[8])
    print 'deviceHealthReport Packets: {0}\n'.format(global_counter[9])
    print 'discoveryHealthReport Packets: {0}\n'.format(global_counter[10])
    print 'invalidMIC Packets: {0}\n'.format(global_counter[11])
    print 'ipPacketReceived Packets: {0}\n'.format(global_counter[12])
    print 'joinFailed Packets: {0}\n'.format(global_counter[13])
    print 'managerStarted Packets: {0}\n'.format(global_counter[14])
    print 'managerStopping Packets: {0}\n'.format(global_counter[15])
    print 'moteStateChanged Packets: {0}\n'.format(global_counter[16])
    print 'neighborHealthReport Packets: {0}\n'.format(global_counter[17])
    print 'optPhase Packets: {0}\n'.format(global_counter[18])
    print 'packetSent Packets: {0}\n'.format(global_counter[19])
    print 'pathAlert Packets: {0}\n'.format(global_counter[20])
    print 'pathStateChanged Packets: {0}\n'.format(global_counter[21])
    print 'pingResponse Packets: {0}\n'.format(global_counter[22])
    print 'rawMoteNotification Packets: {0}\n'.format(global_counter[23])
    print 'serviceChanged Packets: {0}\n'.format(global_counter[24])
    print 'Period Calls : {0}\n'.format(period_call_counter)
    print '================================================================================'
    print 'Total Packets: {0}\n'.format(line_counter)
 
except:
    traceback.print_exc()
    print ('Script ended with an error.')
    sys.exit()
