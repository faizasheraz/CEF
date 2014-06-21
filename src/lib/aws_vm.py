import sys
import time

import boto
from boto import ec2
from boto import exception
from sets import Set

import VM


#EC2 VMs state constants
class Ec2State():
    RUNNING = "running"
    SHUTTING_DOWN = "shutting-down"
    TERMINATED = "terminated"
    STOPPED = "stopped"
    STOPPING = "stopping"
    

class AWSVm():
                    
    def __init__(self, vm_name, image_id, vmtype="t1.micro", region="us-east-1",
                 key_name=None, placement=None, security_groups=None,
                 user_data=None, private_ip_address=None, subnet_id=None,
                 instance_profile_name=None):
        self.vm_name = vm_name
        self.__vmtype = vmtype
        self.__region = region
        self.__image_id = image_id
        self.__key_name = key_name
        self.__placement = placement
        self.__security_groups = security_groups
        self.__user_data = user_data
        self.__private_ip_address = private_ip_address
        self.__subnet_id = subnet_id
        self.__instance_profile_name = instance_profile_name
        
        self.__reservation = None
        self.__instance = None
        self.__state = None
        self.__private_ip = None
        self.__public_ip = None
        self.__start_time = ""
        self.__earlier_run_duration = ""
    
        self.ec2_conn = ec2.connect_to_region(self.__region)
        
        self.elastic_ip_address = self.ec2_conn.allocate_address("vpc")
        
        

# TODO: Handle other possible exceptions
    def launch(self):

        try:
            self.__reservation = self.ec2_conn.run_instances(self.__image_id,
                                                             instance_type = self.__vmtype,
                                                             key_name = self.__key_name,
                                                             placement = self.__placement,
                                                             security_groups = None,
                                                             user_data = self.__user_data,
                                                             private_ip_address = self.__private_ip_address,
                                                             subnet_id = self.__subnet_id,
                                                             instance_profile_name = self.__instance_profile_name,
                                                             dry_run = False)
            #for r in self.ec2_conn.get_all_instances():
            #    #print "waiting for reservation id"
            #    if r.id == self.__reservation.id:
            #        break

            self.__instance = self.__reservation.instances[0]
            while (self.__instance.state != Ec2State.RUNNING):
                self.__instance.update()
            self.__state = Ec2State.RUNNING
            
            print "state of instance" , self.__instance.state
            
            self.__increment_usage()
            print "Instance Launched"
            
            self.ec2_conn.associate_address(self.__instance.id, None,
                                            self.elastic_ip_address.allocation_id)
            
            # wait for the ip to be assigned
            time.sleep(60)            
            self.__public_ip = self.elastic_ip_address.public_ip
            self.__private_ip = self.__instance.private_ip_address
            print "private_ip", self.__private_ip
            print "public ip", self.__public_ip
            
            print "security groups to be assigned are: \n" , self.__security_groups
            if self.__security_groups is not None:
                self.ec2_conn.modify_instance_attribute(self.__instance.id,
                                                        "groupSet",
                                                        Set(self.__security_groups))
        except exception.BotoServerError as e:
            print "Boto Server Error - AWSVM: launch", e
        except:
            print "An exception has occurred" 
            raise
        
        

    def terminate(self):
        if (self.__state != None) and (self.__state != Ec2State.TERMINATED):
            try:
                
                # clean-up associated public ip addresses
                self.elastic_ip_address.disassociate()
                self.elastic_ip_address.delete()
                
                self.ec2_conn.terminate_instances(self.__instance.id,
                                                  dry_run = False)
                while (self.__instance.state != Ec2State.TERMINATED):
                    self.__instance.update()
                self.__state = Ec2State.TERMINATED
                
                self.__private_ip = None
                self.__public_ip = None
            except exception.BotoServerError as e:
                print "Exception occurred" , e
            except AttributeError as e:
                print e
            except:
                print "Unhandled Exception"
                raise
        
    # make this func sophisticated or make another class    
    def __increment_usage(self):
        with open("/home/faiza/workspace/CEF/results/usage.txt") as inputFile:
            instance_hours = int(inputFile.readline())
            print "instance_hours", instance_hours
            instance_hours = instance_hours + 1
                
            with open ("/home/faiza/workspace/CEF/results/usage.txt", "w") as outputFile:
                outputFile.write(str(instance_hours))
    
    #todo: check if ips updated after restart or not
    def start(self):
        if self.__state == Ec2State.STOPPED:
            try:
                self.ec2_conn.start_instances(self.__instance.id, dry_run = True)
                while (self.__instance.state != Ec2State.RUNNING):
                    self.__instance.update()
                self.__state = Ec2State.RUNNING
            except exception.BotoServerError as e:
                print e
            except:
                print "Unhandled exception occurred"
                raise
        

    def stop(self):
        if self.__state == Ec2State.RUNNING:
            try:
                self.ec2_conn.stop_instances(self.__instance.id, dry_run = True)
                while (self.__instance.state != Ec2State.STOPPED):
                    self.__instance.update()
                self.__state = Ec2State.STOPPED
            except exception.BotoServerError as e:
                print e
            except:
                print "Unhandled exception has occurred"
                raise
        
    def get_state(self):
        return self.__state
    
    def get_private_ip(self):
        return self.__private_ip
    
    def get_public_ip(self):
        return self.__public_ip
        
    def execute_code(self):    
        pass
