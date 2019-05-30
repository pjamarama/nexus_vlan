# v1.7
# Cloud SQL ports added
# v1.7.1 4th cloudsql added
# v1.8 hh, kk
# v1.9 ci_addrs module added, vCloud renamed, structural changes

#!/usr/bin/env python3


rrom netmiko import ConnectHandler
import ci_addrs

dc_choice = input ("Which DC (rr1/rr2/hh/kk)? ")
while dc_choice not in ('rr1', 'rr2', 'hh', 'kk'):
    print ("Please try once again")
    dc_choice = input ("Which DC (rr1/rr2/hh/kk)? ")

vlan_number = input('Enter a VLAN number to create: ')
vlan_name = input('Enter a VLAN name: ')

#Checking if the VLAN exists in rr DC
def vlan_check():
    global vlan_number
    global vlan_name
    net_connect = ConnectHandler(ip='172.25.200.146', device_type='cisco_nxos', username='python', password='Ht7Wuvsj4H')
    vl = net_connect.send_config_set(['show vlan id ' + vlan_number + ' | grep ' + vlan_number])
    print (vl + '\n')

    while 'active' in vl:
        print('*******   VLAN ' + vlan_number + ' exists. Please choose another VLAN number')
        vlan_number = input('Enter a VLAN number to create: ')
        vlan_name = input('Enter a VLAN name: ')
        net_connect = ConnectHandler(ip='172.25.200.146', device_type='cisco_nxos', username='python', password='Ht7Wuvsj4H')
        vl = net_connect.send_config_set(['show vlan id ' + vlan_number + ' | grep ' + vlan_number])
        print (vl + '\n')
    print('*******   Horray! Proceeding with creation VLAN ' + vlan_number)

#Checking if the VLAN exists in hh DC
def hh_vlan_check():
    global vlan_number
    global vlan_name
    net_connect = ConnectHandler(ip='172.23.0.5', device_type='cisco_nxos', username='python', password='Ht7Wuvsj4H')
    vl = net_connect.send_config_set(['show vlan id ' + vlan_number + ' | grep ' + vlan_number])
    print (vl + '\n')

    while 'active' in vl:
        print('*******   VLAN ' + vlan_number + ' exists. Please choose another VLAN number')
        vlan_number = input('Enter a VLAN number to create: ')
        vlan_name = input('Enter a VLAN name: ')
        net_connect = ConnectHandler(ip='172.23.0.5', device_type='cisco_nxos', username='python', password='Ht7Wuvsj4H')
        vl = net_connect.send_config_set(['show vlan id ' + vlan_number + ' | grep ' + vlan_number])
        print (vl + '\n')
    print('*******   Horray! Proceeding with creation VLAN ' + vlan_number)

#Checking if the VLAN exists in kk DC
def kk_vlan_check():
    global vlan_number
    global vlan_name
    net_connect = ConnectHandler(ip='172.28.8.4', device_type='cisco_nxos', username='python', password='Ht7Wuvsj4H')
    vl = net_connect.send_config_set(['show vlan id ' + vlan_number + ' | grep ' + vlan_number])
    print (vl + '\n')

    while 'active' in vl:
        print('*******   VLAN ' + vlan_number + ' exists. Please choose another VLAN number')
        vlan_number = input('Enter a VLAN number to create: ')
        vlan_name = input('Enter a VLAN name: ')
        net_connect = ConnectHandler(ip='172.28.8.4', device_type='cisco_nxos', username='python', password='Ht7Wuvsj4H')
        vl = net_connect.send_config_set(['show vlan id ' + vlan_number + ' | grep ' + vlan_number])
        print (vl + '\n')
    print('*******   Horray! Proceeding with creation VLAN ' + vlan_number)



#Creating a VLAN on all rr switches
def rr_vlan_creation():
    print ('*******   Checking if the VLAN exists')
    vlan_check()
    print('*******   Creating a VLAN on all core switches in', dc_choice)
    for device in ci_addrs.switches_rr_all:
        print ('*******   Connecting to ', device.get('ip'))
        print ('Creating VLAN' + vlan_number)
        net_connect = ConnectHandler(**device)
        vlan_config_commands = ['vlan ' + vlan_number, 'name ' + vlan_name, 'mode fabricpath']
        output_vlan = net_connect.send_config_set(vlan_config_commands)
        print (output_vlan + '\n')

def hh_vlan_creation():
    print ('*******   Checking if the VLAN exists')
    hh_vlan_check()
    print('*******   Creating a VLAN on all core switches in', dc_choice)
    for device in ci_addrs.switches_hh_all:
        print ('*******   Connecting to ', device.get('ip'))
        print ('Creating VLAN' + vlan_number)
        net_connect = ConnectHandler(**device)
        vlan_config_commands = ['vlan ' + vlan_number, 'name ' + vlan_name]
        output_vlan = net_connect.send_config_set(vlan_config_commands)
        print (output_vlan + '\n')

def kk_vlan_creation():
    print ('*******   Checking if the VLAN exists')
    kk_vlan_check()
    print('*******   Creating a VLAN on all core switches in', dc_choice)
    for device in ci_addrs.switches_kk_all:
        print ('*******   Connecting to ', device.get('ip'))
        print ('Creating VLAN' + vlan_number)
        net_connect = ConnectHandler(**device)
        vlan_config_commands = ['vlan ' + vlan_number, 'name ' + vlan_name]
        output_vlan = net_connect.send_config_set(vlan_config_commands)
        print (output_vlan + '\n')

#Adding a VLAN to ports on rr1n5k1|2
def rr1_assign_ports():
    """Adding a VLAN to ports on rr1n5k1|2"""
    print('*******   Assigning ports')
    for device in ci_addrs.switches_rr1_12:
        print ('*******   Connecting to ', device.get('ip'))
        net_connect = ConnectHandler(**device)
        output_vlan_cp = net_connect.send_config_set(cp_rr1_config_commands)
        print (output_vlan_cp)
        output_vlan_cloud =  net_connect.send_config_set(cloud_rr1_config_commands)
        print (output_vlan_cloud)
        output_vlan_f5 = net_connect.send_config_set(f5_config_commands)
        print (output_vlan_f5)
        net_connect.send_config_set('wr')
    for device in ci_addrs.switches_rr2_12:
        print ('*******   Connecting to ', device.get('ip'))
        net_connect = ConnectHandler(**device)
        output_vlan_cp = net_connect.send_config_set(cp_rr1_config_commands)
        print (output_vlan_cp)
        output_vlan_cloud = net_connect.send_config_set(cloud_rr2_config_commands)
        print (output_vlan_cloud)
        output_vlan_f5 = net_connect.send_config_set(f5_config_commands)
        print (output_vlan_f5)
        net_connect.send_config_set('wr')    
    assign_ports_n5k34()

  
def rr2_assign_ports():
    """Adding a VLAN to ports on rr2n5k1|2"""
    print('*******   Assigning ports')
    for device in ci_addrs.switches_rr1_12:
        print ('*******   Connecting to ', device.get('ip'))
        net_connect = ConnectHandler(**device)
        output_vlan_cp = net_connect.send_config_set(cp_rr2_config_commands)
        print (output_vlan_cp)
        output_vlan_cloud = net_connect.send_config_set(cloud_rr1_config_commands)
        print (output_vlan_cloud)
        output_vlan_f5 = net_connect.send_config_set(f5_config_commands)
        print (output_vlan_f5)
        net_connect.send_config_set('wr')
    for device in ci_addrs.switches_rr2_12:
        print ('*******   Connecting to ', device.get('ip'))
        net_connect = ConnectHandler(**device)
        output_vlan_cp = net_connect.send_config_set(cp_rr2_config_commands)
        print (output_vlan_cp)
        output_vlan_cloud = net_connect.send_config_set(cloud_rr2_config_commands)
        print (output_vlan_cloud)
        output_vlan_f5 = net_connect.send_config_set(f5_config_commands)
        print (output_vlan_f5)
        net_connect.send_config_set('wr')
    assign_ports_n5k34()


def assign_ports_n5k34():
    for device in ci_addrs.switches_rr1_34:
        print ('*******   Connecting to ', device.get('ip'))
        net_connect = ConnectHandler(**device)
        output_cloudsql = net_connect.send_config_set(cloudsql_rr1_config_commands)
        print (output_cloudsql)
    for device in ci_addrs.switches_rr2_34:
        print ('*******   Connecting to ', device.get('ip'))
        net_connect = ConnectHandler(**device)
        output_cloudsql = net_connect.send_config_set(cloudsql_rr2_config_commands)
        print (output_cloudsql)


def hh_assign_ports():
    """Adding a VLAN to ports on hh1n5k1|2 and hh2n5k1|2"""
    print('*******   Assigning ports')
    for device in ci_addrs.switches_hh1:
        print ('*******   Connecting to ', device.get('ip'))
        net_connect = ConnectHandler(**device)
        output_vlan_cp = net_connect.send_config_set(cp_hh1_config_commands)
        print (output_vlan_cp)
        output_vlan_cloud =  net_connect.send_config_set(cloud_hh1_config_commands)
        print (output_vlan_cloud)
        output_vlan_f5 = net_connect.send_config_set(f5_hh_config_commands)
        print (output_vlan_f5)
        net_connect.send_config_set('wr')

    for device in ci_addrs.switches_hh2:
        print ('*******   Connecting to ', device.get('ip'))
        net_connect = ConnectHandler(**device)
        output_vlan_cp = net_connect.send_config_set(cp_hh2_config_commands)
        print (output_vlan_cp)
        output_vlan_cloud =  net_connect.send_config_set(cloud_hh2_config_commands)
        print (output_vlan_cloud)
        output_vlan_f5 = net_connect.send_config_set(f5_hh_config_commands)
        print (output_vlan_f5)
        net_connect.send_config_set('wr')

def kk_assign_ports():
    """Adding a VLAN to ports on kk1n5k1|2"""
    print('*******   Assigning ports')
    for device in ci_addrs.switches_kk_all:
        print ('*******   Connecting to ', device.get('ip'))
        net_connect = ConnectHandler(**device)
        output_vlan_cp = net_connect.send_config_set(cp_kk_config_commands)
        print (output_vlan_cp)
        output_vlan_cloud =  net_connect.send_config_set(cloud_kk_config_commands)
        print (output_vlan_cloud)
        output_vlan_f5 = net_connect.send_config_set(f5_kk_config_commands)
        print (output_vlan_f5)
        net_connect.send_config_set('wr')

# VLAN to Checkpoint
cp = input("Add vlan to Checkpoint? (y/n): ")
while cp not in ('y', 'n'):
    print ("Please try once again")
    cp = input("Add vlan to Checkpoint? (y/n): ")
if cp == 'y':
    cp_rr1_config_commands = ['int po4', 'switchport trunk allowed vlan add ' + vlan_number]
    cp_rr2_config_commands = ['int po5', 'switchport trunk allowed vlan add ' + vlan_number]
    cp_hh1_config_commands = ['int po8', 'switchport trunk allowed vlan add ' + vlan_number]
    cp_hh2_config_commands = ['int po8', 'switchport trunk allowed vlan add ' + vlan_number]
    cp_kk_config_commands = ['int po14', 'int po15', 'switchport trunk allowed vlan add ' + vlan_number]
else:
    cp_rr1_config_commands = []
    cp_rr2_config_commands = []
    cp_hh1_config_commands = []
    cp_hh2_config_commands = []
    cp_kk_config_commands = []


# VLAN to  Nutanix   
cloud = input("Add vlan to  Nutanix   ? (y/n): ")
while cloud not in ('y', 'n'):
    print ("Please try once again")
    cloud = input("Add vlan to  Nutanix   ? (y/n): ")
if cloud == 'y':
    cloud_rr1_config_commands = ['int Po202-209, Po230, Po232, Po236, Po242-245, Po251-252', 'switchport trunk allowed vlan add ' + vlan_number]
    cloud_rr2_config_commands = ['int Po202-209, Po220-221, Po223-224, Po263-266, Po281-288, Po297-300', 'switchport trunk allowed vlan add ' + vlan_number]
    cloud_hh1_config_commands = ['int Po325, Po326, Po327, Po328, Po329, Po330, Po331, Po332, Po515, Po516, Po517, Po518, Po519, Po520, Po521', 'switchport trunk allowed vlan add ' + vlan_number]
    cloud_hh2_config_commands = ['int Po325, Po326, Po327, Po328, Po329, Po330, Po331, Po332, Po343, Po344, Po345, Po346, Po347, Po348, Po349', 'switchport trunk allowed vlan add ' + vlan_number]
    cloud_kk_config_commands = ['int Eth2/1, Eth2/2, Eth2/3, Eth2/4, Eth2/5, Eth2/6, Eth2/7, Eth2/8', 'switchport trunk allowed vlan add ' + vlan_number]

else:
    cloud_rr1_config_commands = []
    cloud_rr2_config_commands = []
    cloud_hh1_config_commands = []
    cloud_hh2_config_commands = []
    cloud_kk_config_commands = []

# rr VLAN to Cloudsql
cloudsql = input("Add vlan to Cloud SQL? (y/n): ")
while cloudsql not in ('y', 'n'):
    print ("Please try once again")
    cloud = input("Add vlan to Cloud SQL? (y/n): ")
if cloud == 'y':
    cloudsql_rr1_config_commands = ['int Eth120/1/11, Eth123/1/6, Eth140/1/13, Eth141/1/8', 'switchport trunk allowed vlan add ' + vlan_number]
    cloudsql_rr2_config_commands = ['int Eth123/1/13, Eth124/1/9, Eth129/1/16, Eth141/1/8', 'switchport trunk allowed vlan add ' + vlan_number]
else:
    cloudsql_rr1_config_commands = []
    cloudsql_rr2_config_commands = []

# rr VLAN to F5
f5 = input("Add vlan to F5? (y/n): ")
while f5 not in ('y', 'n'):
    print ("Please try once again")
    f5 = input("Add vlan to F5? (y/n): ")
if f5 == 'y':
    f5_config_commands = ['int Po7', 'switchport trunk allowed vlan add ' + vlan_number]
    f5_hh_config_commands = ['int Po6', 'switchport trunk allowed vlan add ' + vlan_number]
    f5_kk_config_commands = ['int Po10, Po11, Po12, Po13', 'switchport trunk allowed vlan add ' + vlan_number]
else:
    f5_config_commands = []
    f5_hh_config_commands = []
    f5_kk_config_commands = []


if dc_choice == 'rr1':
    rr_vlan_creation()
    rr1_assign_ports()
elif dc_choice == 'rr2':
    rr_vlan_creation()
    rr2_assign_ports()
elif dc_choice == 'hh':
    hh_vlan_creation()
    hh_assign_ports()
else:
    kk_vlan_creation()
    kk_assign_ports()

