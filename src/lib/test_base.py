'''
@author: faiza
'''

import json
import sys
import time

from lib import vpc
from boto import ec2

class TestBase():
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
                self._launch_vms_in_group(my_vpc, vm_group)
            self.vpc_list.append(my_vpc)    
        time.sleep(50)
            
            
    def _launch_vms_in_group(self, my_vpc, vm_group):
        number_of_vms = int(vm_group["number-of-vms"])
        
        # get ids of security groups and add rule for rpyc
        rule = {"protocol":"tcp", "from_src_port":"18812", "to_src_port":"18812",
                    "src_ip_address":"0.0.0.0/0", "src_group":None}
        sec_id = my_vpc.get_security_group_id(vm_group["security-group"])
        if sec_id != None:
            security_group_id_list = []
            security_group_id_list.append(sec_id)
            my_vpc.add_rule_in_security_group(vm_group["security-group"], rule)
        else:
            security_group_id_list = None
            my_vpc.add_rule_in_security_group("default", rule)
            
        with open(vm_group["user_data_file"]) as fd:
            startup_script = fd.read()
            
        for i in range(0, number_of_vms):
            my_vpc.create_aws_instance(str(i), vm_group["ami"],
                                       vm_group["type"],
                                       vm_group["region"],
                                       vm_group["key_name"],
                                       placement = None,
                                       security_groups = security_group_id_list,
                                       user_data = startup_script)
            
            
    def __create_key_pair(self, region, key_name, key_path):
        #  Create a key pair
        conn = ec2.connect_to_region(region)
        key = conn.create_key_pair(key_name)
        key.save(key_path)
        
        
    def __delete_key_pair(self, region, key_name):
        conn = ec2.connect_to_region(region)
        conn.delete_key_pair(key_name)
                    
        
    def cleanup(self):
        del self.vpc_list[:]
        pass