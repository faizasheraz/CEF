'''
@author: faiza
'''

from boto import ec2

class SecurityGroup():
    '''
    classdocs
    '''

    def __init__(self, name, description, region, vpc_id=None):
        '''
        Constructor
        '''
        # xxx Do we need this bookkeeping?
        self.name = name
        self.rules = []
        self.__region = region
        
        try:
            self.ec2_conn = ec2.connect_to_region(self.__region)
            all_sec_groups = self.ec2_conn.get_all_security_groups(filters={"vpc-id":vpc_id})
            #all_sec_groups = self.ec2_conn.get_all_security_groups()
            print "All security groups in vpc"
            for i in range(0, len(all_sec_groups)):
                print all_sec_groups[i].name
                if (all_sec_groups[i].name == self.name):
                    self.sec_group = all_sec_groups[i]
                    break
            else:
                self.sec_group = self.ec2_conn.create_security_group(name,
                                                                    description,
                                                                    vpc_id)
            while (1):
                if self.__group_created(vpc_id) == 1:
                    break
        except:
            print "Exception: SecurityGroup __init__"
            raise
       
    # xxx wait for sec group to be created
    def __group_created(self, vpc_id):    
        groups = self.ec2_conn.get_all_security_groups(filters={"vpc-id":vpc_id})
        print "__group_created: groups are: " , groups
        for group in groups:
            if self.sec_group.name == group.name:
                return 1
        return 0
                    
    # {"protocol":"tcp", from_src_port:"0", to_src_port:"80",
    #   src_ip_address:"0.0.0.0/0", src_group="None"} 
    def add_inbound_rule(self, rule):
        
        try:
            print "creating rule in group:",self.sec_group.id
            self.sec_group.authorize(rule["protocol"], rule["from_src_port"],
                                     rule["to_src_port"],
                                     rule["src_ip_address"],
                                     rule["src_group"])
        except:
            print "Exception occurred"
            raise
    
    def del_inbound_rule(self, protocol=None, from_port=None, to_port=None,
                 src_ip_address=None, src_group=None):
        try:
            self.sec_group.revoke(protocol, from_port, to_port, src_ip_address,
                                  src_group)
        except:
            print "Exception occurred"
            raise
    
    def get_inbound_rules(self):
        return self.sec_group.rules
    
    def delete_security_group(self):
        self.sec_group.delete()
    
    def __del__(self):
        
        #try:
        #    self.sec_group.delete()
        #except:
        #    print "SecurityGroup: __del__"
        #    raise
        pass