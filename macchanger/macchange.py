import subprocess
import optparse
import re

def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="interface to change MAC of")
    parser.add_option("-m", "--new_mac", dest="new_mac", help="new MAC")
    return parser.parse_args()


def change_mac(interface,new_mac):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


(options,arguments)=get_args()
#change_mac(options.interface,options.new_mac)

ifconfig_result=subprocess.check_output(["ifconfig",options.interface])
mac_address_search_result=re.search("\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",str(ifconfig_result))
print(mac_address_search_result[0])
