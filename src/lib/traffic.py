'''
@author: faiza
'''
import rpyc

from lib import aws_vm

class traffic():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def ping(self, src_vms, dest_addresses, log_file):
        remote_ping_text = ''' 
def remote_ping(address):
    import subprocess
    cmd = ["ping", "-c4", address]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    output, error = process.communicate()

    if error is not "":
        return error        
    if output is not "":
        pings, text, result = output.split("---")
        return result
        '''
        for vm in src_vms:
            ip_address = vm.get_public_ip()
            rpyc_conn = rpyc.classic.connect(ip_address)
            rpyc_conn.execute(remote_ping_text)
            remote_ping = rpyc_conn.namespace['remote_ping']
            for dest_address in dest_addresses:
                output_text = remote_ping(dest_address)
                print output_text
                with open(log_file, "a") as fd:
                    text = "\nping from " + vm.vm_name + " to " + dest_address + "\n"
                    fd.write(text)
                    fd.write(output_text)
                    
    def trace_route(self):
        pass
        
        
    def ping_old(self, src_vms, dest_addresses):
        rpyc_conn = None
        output_log = "/home/faiza/workspace/CEF/results/test_output"
        remote_log_file = "/tmp/result.txt"
        local_log_file = "/tmp/results.txt"
        chunk_size = 16000
        for vm in src_vms:
            ip_address = vm.get_public_ip()
            rpyc_conn = rpyc.classic.connect(ip_address)
            for dest_address in dest_addresses:
                cmd = "ping -c 10 " + dest_address + " > " + remote_log_file
                rpyc_conn.modules.os.system(cmd)
                
                # download output file
                rpyc.classic.download_file(rpyc_conn, remote_log_file,
                                           local_log_file,
                                           chunk_size)
                with open(local_log_file) as fd:
                    output_string = fd.read()
                    with open("output_log", "a") as fdw:
                        fdw.write(output_string)
        pass
        