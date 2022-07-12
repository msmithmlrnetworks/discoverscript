import csv
from re import M
import time
import pandas as pd
import netmiko

reader = csv.DictReader(open('app/switches.csv', 'r'))
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
        command = "show mac address-table"
        connection = netmiko.ConnectHandler(ip=ipaddress, \
        device_type=device_type, username=username,\
            password=password)
        mac_table = connection.send_command(command, use_textfsm=True)
        mac_data = {'mac':  [entry['destination_address'] for entry in mac_table],\
        'interface': [entry['destination_port'] for entry in mac_table],\
        'vlan': [entry['vlan'] for entry in mac_table]}
        connection.disconnect()
        df = pd.DataFrame(mac_data, columns=list(mac_data.keys()))
        writer = pd.ExcelWriter('/app/app/data/mac_table.xlsx', engine='xlsxwriter')
        df.to_excel(writer, hostname)
        writer.save()
        success = True

        time.sleep(102)
    except:
        success = False
        time.sleep(2)

