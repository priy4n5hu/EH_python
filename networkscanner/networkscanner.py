from asyncio import timeout
from tabnanny import verbose

import scapy.all as scapy
import optparse

def get_args():
    parser=optparse.OptionParser()
    parser.add_option("-i","--ip address",dest="ip",help="enter ip address or ip range")
    options=parser.parse_args()[0]
    return options.ip

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast=broadcast/arp_request
    answered_list=scapy.srp(arp_request_broadcast, timeout=1,verbose=False)[0]

    #print("IP\t\t\tMAC ADDRESS\n-----------------------------------------------------")
    clients_lists=[]
    for elements in answered_list:
        client_dict = {"ip":elements[1].psrc,"mac":elements[1]. hwsrc}
        clients_lists.append(client_dict)
        #print(elements[1].psrc+"\t\t"+elements[1]. hwsrc)
    #print(clients_lists)
    return clients_lists

def output(clients_lists):
    print("IP\t\t\tMAC ADDRESS\n-----------------------------------------------------")
    element=0
    for element in clients_lists:
        print(element["ip"]+"\t\t"+element["mac"])


ip=get_args()
scan_result = scan(ip)
output(scan_result)