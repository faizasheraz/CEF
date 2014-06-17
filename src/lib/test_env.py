'''
@author: faiza
'''

import json
import sys
import time

from lib import vpc
from boto import ec2

class TestEnvir(object):
    '''
    classdocs
    '''


    def __init__(self, config_file):
        '''
        Constructor
        '''
        try:
            json_data = open(config_file)
            self.data = json.load(json_data)
            print self.data
           
            json_data.close()
        except:
            print "TestEnvir: __init__"
            raise
        
        #VPC objects created will go in this list
        self.vpc_list = []
        
    #loads the test environment
    # deal with None
    def setup(self):
        
        # list of VPCs to be created
        VPCs = self.data["VPCs"]
         
        for a_vpc in VPCs:
            my_vpc = vpc.VPC(a_vpc["vpc-name"], a_vpc["cidr"])
            security_groups = a_vpc["security-groups"]
            for security_group in security_groups:
                my_vpc.create_security_group(security_group["name"],
                                             security_group["description"],
                                             security_group["region"],
                                             security_group["rules"])
            
            vm_groups = a_vpc["vm_groups"]
            for vm_group in vm_groups:
                if (vm_group["key-name"] == None):
                    #  Create a key pair
                    conn = ec2.connect_to_region(vm_group["region"])
                    key = conn.create_key_pair(str(vm_group["group-name"]))
                    key.save('/home/faiza/') # xxxx change path
                    self._launch_vms_in_group(my_vpc, vm_group)
                    conn.delete_key_pair(str(vm_group["group-name"]))
                    
                else:
                    self._launch_vms_in_group(my_vpc, vm_group)
                # xxx add or check for ssh rule in security group
            time.sleep(50)
            
    def _launch_vms_in_group(self, my_vpc, vm_group):
        number_of_vms = int(vm_group["number-of-vms"])
        for i in range(0, number_of_vms):          
            my_vpc.create_aws_instance(str(i), vm_group["ami"],
                                       vm_group["type"],
                                       vm_group["region"],
                                       vm_group["key-name"],
                                       vm_group["placement"],
                                       vm_group["security-group"],
                                       vm_group["user_data"],
                                       vm_group["private-ip"],
                                       vm_group["subnet-id"],
                                       vm_group["instance-profile-name"])
            #xxx launch vms as well
                    
        
    def load(self):
        pass
    
    def cleanup(self):
        pass