# from __future__ import (
#     absolute_import,
#     division,
#     print_function,
#     unicode_literals,
# )
# from builtins import *


import csv
import time
import pandas as pd
import netmiko


# netmiko_excpetions = (netmiko.ssh_exception.NetMikoTimeoutException,
#                       netmiko.ssh_exception.NetMikoAuthenticationException,
#                       netmiko.ssh_exception.SSHException)


reader = csv.DictReader(open('app/switches.csv', 'r'))
for row in reader:
    hostname = row['hostname']
    print(hostname)
    username = row['username']
    print(username)
    ipaddress = row['IP']
    print(ipaddress)
    device_type = "cisco_ios"
    success = False
    password = row['password']
    try:
        command = "show mac address-table"
        connection = netmiko.ConnectHandler(ip=ipaddress, \
        device_type=device_type, username=username,\
            password=password)
        mac_table = connection.send_command(command, use_textfsm=True)
        mac_data = {'device hostname': hostname,'mac':  [entry['mac'] for entry in mac_table],\
        'interface': [entry['ports'] for entry in mac_table],\
        'vlan': [entry['vlan'] for entry in mac_table]}
        print(mac_data)
        connection.disconnect()
        df = pd.DataFrame(mac_data, columns=list(mac_data.keys()))
        writer = pd.ExcelWriter('mac_table.xlsx', engine='xlsxwriter')
        df.to_excel(writer, hostname)
        writer.save()
        success = True

    except netmiko_excpetions as e:
        print('Failed to', ipaddress, e)
        success = False
        time.sleep(2)

