import csv
from re import M
import time
import datetime
import pandas as pd
import netmiko
import nmap3


def getData():
    # reader = csv.DictReader(open('app/switches.csv', 'r'))
    # iparp = "show ip arp"
    # connection_core = netmiko.ConnectHandler(ip="10.100.10.254", \
    #         device_type="cisco_ios", username="boohoomlr",\
    #             password="*sJ8r*JwQd")
    # raw_output = connection_core.send_command(iparp, use_textfsm=True)
    # arp_data = {'ip':  [entry['address'] for entry in raw_output],\
    #         'mac': [entry['mac'] for entry in raw_output],\
    #         'vlan': [entry['interface'] for entry in raw_output]}
    # df1 = pd.DataFrame(arp_data, columns=list(arp_data.keys()))
    # now = datetime.datetime.now()
    # writer2 = pd.ExcelWriter(f'/app/data/iparp-{now.day}-{now.month}-{now.year}-{now.hour}:{now.minute}.xlsx', engine='xlsxwriter')
    # df1.to_excel(writer2, "iparp")
    # writer2.save()
    # connection_core.disconnect()
    for row in reader:
        hostname = row['hostname']
        print(hostname)
        username = row['username']
        print(username)
        ipaddress = row['ip']
        print(ipaddress)
        device_type = "cisco_ios"
        success = False
        password = row['password']
        try:
            command = "show mac address-table | ex STATIC"
            connection = netmiko.ConnectHandler(ip=ipaddress, \
            device_type=device_type, username=username,\
                password=password)
            mac_table = connection.send_command(command, use_textfsm=True)
            mac_data = {'mac':  [entry['destination_address'] for entry in mac_table],\
            'interface': [entry['destination_port'] for entry in mac_table],\
            'vlan': [entry['vlan'] for entry in mac_table]}
            connection.disconnect()
            print(connection.is_alive())
            df = pd.DataFrame(mac_data, columns=list(mac_data.keys()))
            now = datetime.datetime.now()
            writer = pd.ExcelWriter(f'/app/data/{hostname}-{now.day}-{now.month}-{now.year}-{now.hour}:{now.minute}.xlsx', engine='xlsxwriter')
            df.to_excel(writer, hostname)
            writer.save()
            success = True
            print('success')

            time.sleep(10)
            continue
        except:
            success = False
            print('error')
            time.sleep(20)
            continue

while True:
    getData()
    time.sleep(28800)


