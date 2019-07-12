#============================ adjust path =====================================

import sys
import os
if __name__ == "__main__":
    here = sys.path[0]
    sys.path.insert(0, os.path.join(here, '..', 'libs'))
    sys.path.insert(0, os.path.join(here, '..', 'external_libs'))

#============================ imports =========================================

# Python
import traceback
import json
import time
import threading
import datetime
# third-party
import urllib3
import certifi
# local
from SmartMeshSDK                      import sdk_version
from VManagerSDK.vmanager              import Configuration
from VManagerSDK.vmgrapi               import VManagerApi
from VManagerSDK.vmanager.rest         import ApiException
from VManagerSDK.vmanager              import SystemWriteConfig

urllib3.disable_warnings() # disable warnings that show up about self-signed certificates

#============================ defines =========================================

FILENAME_OUT             = 'poipoi.txt'
DFLT_VMGR_HOST           = "128.93.102.105"

#============================ variables =======================================

fileLock                 = threading.RLock()

#============================ helpers =========================================

def writeToFile(intype,indata,firstline=False):
    try:
        assert type(indata)==dict
    except:
        raise
    if firstline:
        openmode = 'w'
    else:
        openmode = 'a'
    
    output = {
        'timestamp': time.time(),
        'type':      intype,
        'data':      indata,
    }
    
    with fileLock:
        with open(FILENAME_OUT, openmode) as f:
            f.write(json.dumps(output)+'\n')

def remove_datetime(data):
    for (k,v) in data.items():
        if type(v)==datetime.datetime:
            data[k] = str(v)
    return data

def _handle_notifications(notif):
    writeToFile(
        intype     = 'notif' ,
        indata     = remove_datetime(notif.to_dict()),
    )

#============================ main ============================================

def main():

    writeToFile(
        intype     = 'admin' ,
        indata     = {'msg': 'starting'},
        firstline  = True
    )

    try:
        #=== connect
        
        # banner
        print '\nVMgr_LogFileSnapshot (c) Dust Networks'
        print 'SmartMesh SDK {0}\n'.format('.'.join([str(i) for i in sdk_version.VERSION]))

        # log-in as user "dust"
        config                    = Configuration()
        config.username           = 'dust'
        config.password           = 'dust'
        config.verify_ssl         = False
        
        if os.path.isfile(certifi.where()):
            config.ssl_ca_cert    = certifi.where()
        else:
            config.ssl_ca_cert    = os.path.join(os.path.dirname(sys.executable), "cacert.pem")

        # initialize the VManager Python library
        voyager   = VManagerApi(host=DFLT_VMGR_HOST)

        fileLock  = threading.RLock()
        
        voyager.get_notifications(notif_callback=_handle_notifications)
        
        #=== collect
        
        snapshot = {}
        
        while True:

            motes         = voyager.motesApi.get_motes().to_dict()
            assert motes.keys()==['motes']
            motes         = motes['motes']
            '''
            motes = [
                {   'mac_address': '00-17-0D-00-00-31-CA-03', 'state': 'operational'},
                {   'mac_address': '00-17-0D-00-00-38-06-D5', 'state': 'operational'},
                ...
            ]
            '''
            snapshot['motes'] = motes

            for (i,mote) in enumerate(motes):
               
                mote_info    = voyager.motesApi.get_mote_info(mote['mac_address']).to_dict()
                mote_info    = remove_datetime(mote_info)
                
                '''
                mote_info = {
                    'app_id': 1,
                    'app_sw_rev': '1.4.1.8',
                    'avg_hops': 1.0,
                    ...
                }
                '''
                snapshot['motes'][i]['mote_info'] = mote_info
                
                connections  = voyager.pathsApi.get_connections(mote['mac_address']).to_dict()
                assert connections.keys()==['devices']
                connections  = connections['devices']
                for (i,c) in enumerate(connections):
                    connections[i] = remove_datetime(c)
                '''
                connections = [
                    {
                        'mac_address': '00-17-0D-00-00-58-2B-4F',
                        'num_links': None,
                        'quality': None,
                        'rssi_ato_b': None,
                        'rssi_bto_a': None,
                    },
                    ...
                ]
                '''
                snapshot['motes'][i]['connections'] = connections

            network_info = voyager.networkApi.get_network_info().to_dict()
            network_info = remove_datetime(network_info)
            '''
            network_info = {
                'adv_state': 'on',
                'cur_down_frame_size': 512,
                ...
            }
            '''
            snapshot['network_info'] = network_info
            
            #==== write
            
            writeToFile(
                intype     = 'snapshot' ,
                indata     = snapshot,
            )
            
            #=== wait a bit
            
            time.sleep(5*60)
            
    except:
        traceback.print_exc()
    
if __name__=="__main__":
    main()
