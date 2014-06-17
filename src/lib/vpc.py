'''
@author: faiza
'''
import time

from boto import vpc

from lib import aws_vm
from lib import security_group


class VPC(object):
    '''
    classdocs
    '''


    def __init__(self, name, cidr_block):
        '''
        Constructor
        '''
        self.name = name
        self.cidr_block = cidr_block
        self.aws_instances = []
        self.subnets = []
        self.security_groups = []
        self.routing_tables = []
        self.cidr_block = cidr_block
        self.subnet = None
        
        try:
            self.vpc_conn = vpc.VPCConnection()
            self.vpc = self.vpc_conn.create_vpc(self.cidr_block)
        except:
            print "Exception occurred"
            raise
        
    def create_aws_instance(self, vm_name, ami_name, instance_type, region,
                            key_name=None, placement=None,
                            security_groups=None, user_data=None,
                            private_ip_address=None,
                            subnet_id=None, instance_profile_name=None):
        try:
            self.subnet = self.vpc_conn.create_subnet(self.vpc.id, self.cidr_block)
            print "subnet id is: " , self.subnet.id
            vm = aws_vm.AWSVm(vm_name, ami_name, instance_type, region,
                              key_name, placement, security_groups,
                              user_data, private_ip_address, self.subnet.id,
                              instance_profile_name)
            vm.launch()
            self.aws_instances.append(vm)
        except:
            print "Exception occurred"
            raise
        
    def terminate_aws_instance(self, vm_name):
        try:
            for instance in self.aws_instances:
                if instance.vm_name == vm_name:
                    self.aws_instances.remove(instance)
                    instance.terminate()
                    
        except:
            print "Exception occurred"
            raise
    
    
    def create_security_group(self, name, description, region, rules):
        try:
            print self.vpc.id
            sec_group = security_group.SecurityGroup(name, description, region,
                                                     self.vpc.id)
            self.security_groups.append(sec_group)
            #time.sleep(10)
            for rule in rules:
                sec_group.add_inbound_rule(rule)
                
        except:
            print "Exception VPC: create_security_group"
            raise
        
    def delete_security_group(self, group_name):
        try:
            for sec_group in self.security_groups:
                if sec_group.name == group_name:
                    self.security_groups.remove(sec_group)
                    sec_group.delete_security_group() #xxx two funcs __del__ and delete
        except:
            print "Exception"
            raise
        
    def get_security_group_id(self, name):
        for group in self.security_groups:
            if group.name == name:
                return group.sec_group.id
        return 
        
    # pop a vm from list based on a criteria e.g. region, type, ami etc
    def pop_vm(self, criteria):
        pass
        
     
    # xxx disassociate elastic ip subnets etc
    def __del__(self):
        try:
            for group in self.security_groups:
                group.delete_security_group()
                
            for vm in self.aws_instances:
                vm.terminate()
                
            if self.subnet is not None: 
                self.vpc_conn.delete_subnet(self.subnet.id)
            #self.security_groups = []
            #self.aws_instances = []
            self.vpc_conn.delete_vpc(self.vpc.id)
        except:
            print "VPC: __del__"
            raise