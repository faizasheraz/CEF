import time
import base64

from boto import ec2

from lib import aws_vm
from lib import security_group
from lib import vpc
from lib import test_base
from lib import traffic

# properties ("ami-358c955c", "t1.micro", "us-east-1", None, None)

def create_topology():
    """
    vpc1 = vpc.VPC("vpc-1", "10.0.0.0/16")
    vpc2 = vpc.VPC("vpc-2", "20.0.0.0/16")
    
    rules = [ {"protocol":"tcp", "from_src_port":"0", "to_src_port":"80",
               "src_ip_address":"0.0.0.0/0", "src_group":None},
             
              {"protocol":"udp", "from_src_port":"0", "to_src_port":"80",
               "src_ip_address":"0.0.0.0/0", "src_group":None},
             
              {"protocol":"icmp", "from_src_port":"0", "to_src_port":"10",
               "src_ip_address":"0.0.0.0/0", "src_group":None}
            ]
    
    vpc1.create_security_group("test", "sec group for vpc1", "us-east-1", rules)
    vpc1.create_security_group("sec2_vpc1", "sec group for vpc1", "us-east-1", rules)  
    vpc1.delete_security_group("sec2_vpc1")
    
    vpc2.create_security_group("test", "sec group for vpc1", "us-east-1", rules)
    vpc2.create_security_group("sec_vpc2", "sec group for vpc1", "us-east-1", rules)
    #("ami-358c955c", "t1.micro", "us-east-1", None, None)
    time.sleep(50)
    """
    vpc1 = vpc.VPC("vpc-1", "10.0.0.0/16")
    
    #  Create a key pair
    # conn = ec2.connect_to_region("us-east-1")
    # key = conn.create_key_pair("faiza_key")
    # key.save('/home/faiza/.ssh/') # xxxx change path
    rules = [ {"protocol":"tcp", "from_src_port":"0", "to_src_port":"65535",
               "src_ip_address":"0.0.0.0/0", "src_group":None},
             
              {"protocol":"udp", "from_src_port":"0", "to_src_port":"65535",
               "src_ip_address":"0.0.0.0/0", "src_group":None},
             
              {"protocol":"icmp", "from_src_port":"-1", "to_src_port":"-1",
               "src_ip_address":"0.0.0.0/0", "src_group":None}
            ]
    
    #initialization_script_encoded = None
    with open("/home/faiza/workspace/CEF/config/initialization_script.sh") as fd:
        initialization_script = fd.read()
        
        
    vpc1.create_security_group("test", "sec group for vpc1", "us-east-1", rules)
    sec_id1 = vpc1.get_security_group_id("test")
    print sec_id1
    #vpc1.create_aws_instance("vm1", "ami-358c955c", "t1.micro", "us-east-1",
    #                         "faiza_key", security_groups=[sec_id1],
    #                         user_data=initialization_script)
   # 
    #vpc1.create_aws_instance("vm2", "ami-358c955c", "t1.micro", "us-east-1",
    #                         "faiza_key", security_groups=[sec_id1],
    #                         user_data=initialization_script)
    
   # vm1 = vpc1.aws_instances[0]
    #vm2 = vpc1.aws_instances[1]
    
    #vm2_private_ip = vm2.get_private_ip()
    
    #test = traffic.Traffic()
    #test.ping([vm1], [vm2_private_ip], "/home/faiza/workspace/CEF/results/output_log.txt")
    #time.sleep(50)
    
    #env = test_env.TestEnvir("/home/faiza/workspace/CEF/config/test_config.json")
    #env.setup()
    print "instance created"
    try:
        eval(input("press enter to continue"))
    except:
        print "Test Ended - waiting for clean-up"
    

if __name__ == "__main__":
    create_topology()
