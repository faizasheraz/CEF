"""
Unit test for cloud experimentation framework
"""


from lib import test_base
from lib import traffic

config_file_path = "/home/faiza/workspace/CEF/config/test_config.json"
log_file = "/home/faiza/workspace/CEF/results/output_log.txt"

#Test to ping vms in a mesh
class Test1(test_base.TestBase):
    
    # xxx check what super does
    def __init__(self, config_file):
        test_base.TestBase.__init__(self, config_file)
    
    # xxx check if name of a method of base and derived class can be same
    def setup(self):
        test_base.TestBase.setup(self)
        
    def execute(self):
        src_vms = []
        dest_ips = []
        
        for vpc in self.vpc_list:
            for instance in vpc.aws_instances:
                src_vms.append(instance)
                dest_ips.append(instance.get_private_ip())
            traffic_test = traffic.Traffic()
            traffic_test.ping(src_vms, dest_ips, log_file)
                
        
            
            
    def cleanup(self):
        test_base.TestBase.cleanup(self)
        
        
if __name__ == "__main__":
    test = Test1(config_file_path)
    test.setup()
    test.execute()
    test.cleanup()
    
