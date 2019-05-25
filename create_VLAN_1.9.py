# v1.7
# Cloud SQL ports added
# v1.7.1 4th cloudsql added
# v1.8 ch, hk
# v1.9 ci_addrs module added, vCloud renamed, structural changes

#!/usr/bin/env python3


from netmiko import ConnectHandler
import ci_addrs

dc_choice = input ("Which DC (fr1/fr2/ch/hk)? ")
while dc_choice not in ('fr1', 'fr2', 'ch', 'hk'):
    print ("Please try once again")
    dc_choice = input ("Which DC (fr1/fr2/ch/hk)? ")

vlan_number = input('Enter a VLAN number to create: ')
vlan_name = input('Enter a VLAN name: ')

#Checking if the VLAN exists in FR DC
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

#Checking if the VLAN exists in CH DC
def ch_vlan_check():
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

#Checking if the VLAN exists in HK DC
def hk_vlan_check():
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



#Creating a VLAN on all FR switches
def fr_vlan_creation():
    print ('*******   Checking if the VLAN exists')
    vlan_check()
    print('*******   Creating a VLAN on all core switches in', dc_choice)
    for device in ci_addrs.switches_fr_all:
        print ('*******   Connecting to ', device.get('ip'))
        print ('Creating VLAN' + vlan_number)
        net_connect = ConnectHandler(**device)
        vlan_config_commands = ['vlan ' + vlan_number, 'name ' + vlan_name, 'mode fabricpath']
        output_vlan = net_connect.send_config_set(vlan_config_commands)
        print (output_vlan + '\n')

def ch_vlan_creation():
    print ('*******   Checking if the VLAN exists')
    ch_vlan_check()
    print('*******   Creating a VLAN on all core switches in', dc_choice)
    for device in ci_addrs.switches_ch_all:
        print ('*******   Connecting to ', device.get('ip'))
        print ('Creating VLAN' + vlan_number)
        net_connect = ConnectHandler(**device)
        vlan_config_commands = ['vlan ' + vlan_number, 'name ' + vlan_name]
        output_vlan = net_connect.send_config_set(vlan_config_commands)
        print (output_vlan + '\n')

def hk_vlan_creation():
    print ('*******   Checking if the VLAN exists')
    hk_vlan_check()
    print('*******   Creating a VLAN on all core switches in', dc_choice)
    for device in ci_addrs.switches_hk_all:
        print ('*******   Connecting to ', device.get('ip'))
        print ('Creating VLAN' + vlan_number)
        net_connect = ConnectHandler(**device)
        vlan_config_commands = ['vlan ' + vlan_number, 'name ' + vlan_name]
        output_vlan = net_connect.send_config_set(vlan_config_commands)
        print (output_vlan + '\n')

#Adding a VLAN to ports on fr1n5k1|2
def fr1_assign_ports():
    """Adding a VLAN to ports on fr1n5k1|2"""
    print('*******   Assigning ports')
    for device in ci_addrs.switches_fr1_12:
        print ('*******   Connecting to ', device.get('ip'))
        net_connect = ConnectHandler(**device)
        output_vlan_cp = net_connect.send_config_set(cp_fr1_config_commands)
        print (output_vlan_cp)
        output_vlan_cloud =  net_connect.send_config_set(cloud_fr1_config_commands)
        print (output_vlan_cloud)
        output_vlan_f5 = net_connect.send_config_set(f5_config_commands)
        print (output_vlan_f5)
        net_connect.send_config_set('wr')
    for device in ci_addrs.switches_fr2_12:
        print ('*******   Connecting to ', device.get('ip'))
        net_connect = ConnectHandler(**device)
        output_vlan_cp = net_connect.send_config_set(cp_fr1_config_commands)
        print (output_vlan_cp)
        output_vlan_cloud = net_connect.send_config_set(cloud_fr2_config_commands)
        print (output_vlan_cloud)
        output_vlan_f5 = net_connect.send_config_set(f5_config_commands)
        print (output_vlan_f5)
        net_connect.send_config_set('wr')    
    assign_ports_n5k34()

  
def fr2_assign_ports():
    """Adding a VLAN to ports on fr2n5k1|2"""
    print('*******   Assigning ports')
    for device in ci_addrs.switches_fr1_12:
        print ('*******   Connecting to ', device.get('ip'))
        net_connect = ConnectHandler(**device)
        output_vlan_cp = net_connect.send_config_set(cp_fr2_config_commands)
        print (output_vlan_cp)
        output_vlan_cloud = net_connect.send_config_set(cloud_fr1_config_commands)
        print (output_vlan_cloud)
        output_vlan_f5 = net_connect.send_config_set(f5_config_commands)
        print (output_vlan_f5)
        net_connect.send_config_set('wr')
    for device in ci_addrs.switches_fr2_12:
        print ('*******   Connecting to ', device.get('ip'))
        net_connect = ConnectHandler(**device)
        output_vlan_cp = net_connect.send_config_set(cp_fr2_config_commands)
        print (output_vlan_cp)
        output_vlan_cloud = net_connect.send_config_set(cloud_fr2_config_commands)
        print (output_vlan_cloud)
        output_vlan_f5 = net_connect.send_config_set(f5_config_commands)
        print (output_vlan_f5)
        net_connect.send_config_set('wr')
    assign_ports_n5k34()


def assign_ports_n5k34():
    for device in ci_addrs.switches_fr1_34:
        print ('*******   Connecting to ', device.get('ip'))
        net_connect = ConnectHandler(**device)
        output_cloudsql = net_connect.send_config_set(cloudsql_fr1_config_commands)
        print (output_cloudsql)
    for device in ci_addrs.switches_fr2_34:
        print ('*******   Connecting to ', device.get('ip'))
        net_connect = ConnectHandler(**device)
        output_cloudsql = net_connect.send_config_set(cloudsql_fr2_config_commands)
        print (output_cloudsql)


def ch_assign_ports():
    """Adding a VLAN to ports on ch1n5k1|2 and ch2n5k1|2"""
    print('*******   Assigning ports')
    for device in ci_addrs.switches_ch1:
        print ('*******   Connecting to ', device.get('ip'))
        net_connect = ConnectHandler(**device)
        output_vlan_cp = net_connect.send_config_set(cp_ch1_config_commands)
        print (output_vlan_cp)
        output_vlan_cloud =  net_connect.send_config_set(cloud_ch1_config_commands)
        print (output_vlan_cloud)
        output_vlan_f5 = net_connect.send_config_set(f5_ch_config_commands)
        print (output_vlan_f5)
        net_connect.send_config_set('wr')

    for device in ci_addrs.switches_ch2:
        print ('*******   Connecting to ', device.get('ip'))
        net_connect = ConnectHandler(**device)
        output_vlan_cp = net_connect.send_config_set(cp_ch2_config_commands)
        print (output_vlan_cp)
        output_vlan_cloud =  net_connect.send_config_set(cloud_ch2_config_commands)
        print (output_vlan_cloud)
        output_vlan_f5 = net_connect.send_config_set(f5_ch_config_commands)
        print (output_vlan_f5)
        net_connect.send_config_set('wr')

def hk_assign_ports():
    """Adding a VLAN to ports on hk1n5k1|2"""
    print('*******   Assigning ports')
    for device in ci_addrs.switches_hk_all:
        print ('*******   Connecting to ', device.get('ip'))
        net_connect = ConnectHandler(**device)
        output_vlan_cp = net_connect.send_config_set(cp_hk_config_commands)
        print (output_vlan_cp)
        output_vlan_cloud =  net_connect.send_config_set(cloud_hk_config_commands)
        print (output_vlan_cloud)
        output_vlan_f5 = net_connect.send_config_set(f5_hk_config_commands)
        print (output_vlan_f5)
        net_connect.send_config_set('wr')

# VLAN to Checkpoint
cp = input("Add vlan to Checkpoint? (y/n): ")
while cp not in ('y', 'n'):
    print ("Please try once again")
    cp = input("Add vlan to Checkpoint? (y/n): ")
if cp == 'y':
    cp_fr1_config_commands = ['int po4', 'switchport trunk allowed vlan add ' + vlan_number]
    cp_fr2_config_commands = ['int po5', 'switchport trunk allowed vlan add ' + vlan_number]
    cp_ch1_config_commands = ['int po8', 'switchport trunk allowed vlan add ' + vlan_number]
    cp_ch2_config_commands = ['int po8', 'switchport trunk allowed vlan add ' + vlan_number]
    cp_hk_config_commands = ['int po14', 'int po15', 'switchport trunk allowed vlan add ' + vlan_number]
else:
    cp_fr1_config_commands = []
    cp_fr2_config_commands = []
    cp_ch1_config_commands = []
    cp_ch2_config_commands = []
    cp_hk_config_commands = []


# VLAN to  Nutanix   
cloud = input("Add vlan to  Nutanix   ? (y/n): ")
while cloud not in ('y', 'n'):
    print ("Please try once again")
    cloud = input("Add vlan to  Nutanix   ? (y/n): ")
if cloud == 'y':
    cloud_fr1_config_commands = ['int Po202-209, Po230, Po232, Po236, Po242-245, Po251-252', 'switchport trunk allowed vlan add ' + vlan_number]
    cloud_fr2_config_commands = ['int Po202-209, Po220-221, Po223-224, Po263-266, Po281-288, Po297-300', 'switchport trunk allowed vlan add ' + vlan_number]
    cloud_ch1_config_commands = ['int Po325, Po326, Po327, Po328, Po329, Po330, Po331, Po332, Po515, Po516, Po517, Po518, Po519, Po520, Po521', 'switchport trunk allowed vlan add ' + vlan_number]
    cloud_ch2_config_commands = ['int Po325, Po326, Po327, Po328, Po329, Po330, Po331, Po332, Po343, Po344, Po345, Po346, Po347, Po348, Po349', 'switchport trunk allowed vlan add ' + vlan_number]
    cloud_hk_config_commands = ['int Eth2/1, Eth2/2, Eth2/3, Eth2/4, Eth2/5, Eth2/6, Eth2/7, Eth2/8', 'switchport trunk allowed vlan add ' + vlan_number]

else:
    cloud_fr1_config_commands = []
    cloud_fr2_config_commands = []
    cloud_ch1_config_commands = []
    cloud_ch2_config_commands = []
    cloud_hk_config_commands = []

# FR VLAN to Cloudsql
cloudsql = input("Add vlan to Cloud SQL? (y/n): ")
while cloudsql not in ('y', 'n'):
    print ("Please try once again")
    cloud = input("Add vlan to Cloud SQL? (y/n): ")
if cloud == 'y':
    cloudsql_fr1_config_commands = ['int Eth120/1/11, Eth123/1/6, Eth140/1/13, Eth141/1/8', 'switchport trunk allowed vlan add ' + vlan_number]
    cloudsql_fr2_config_commands = ['int Eth123/1/13, Eth124/1/9, Eth129/1/16, Eth141/1/8', 'switchport trunk allowed vlan add ' + vlan_number]
else:
    cloudsql_fr1_config_commands = []
    cloudsql_fr2_config_commands = []

# FR VLAN to F5
f5 = input("Add vlan to F5? (y/n): ")
while f5 not in ('y', 'n'):
    print ("Please try once again")
    f5 = input("Add vlan to F5? (y/n): ")
if f5 == 'y':
    f5_config_commands = ['int Po7', 'switchport trunk allowed vlan add ' + vlan_number]
    f5_ch_config_commands = ['int Po6', 'switchport trunk allowed vlan add ' + vlan_number]
    f5_hk_config_commands = ['int Po10, Po11, Po12, Po13', 'switchport trunk allowed vlan add ' + vlan_number]
else:
    f5_config_commands = []
    f5_ch_config_commands = []
    f5_hk_config_commands = []


if dc_choice == 'fr1':
    fr_vlan_creation()
    fr1_assign_ports()
elif dc_choice == 'fr2':
    fr_vlan_creation()
    fr2_assign_ports()
elif dc_choice == 'ch':
    ch_vlan_creation()
    ch_assign_ports()
else:
    hk_vlan_creation()
    hk_assign_ports()

