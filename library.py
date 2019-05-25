#encoding=utf8
from socket import*
import socket
import threading
import array
import binascii
from binascii import hexlify
import sys
import time
from datetime import datetime,date
import csv


def get_dev_ipstrhex(ipstr):
    packed_ip_addr = socket.inet_aton(ipstr)
    hexStr = hexlify(packed_ip_addr)
    return hexStr


def get_dev_portstrhex(port):
    strport=str(hex(port))
    hexport=strport[4:6]+strport[2:4]
    return hexport
def ask_info(strmac):
    'BA55000000'+strmac+'02220000C600000000000005B2BBCFD4CABEB7B5BBD8D0C5CFA2202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202000ED'

def set_network_parameter(strmac,newip,newgateway,newnetmask,newacquip,newacquport,newrealtimeip,newrealtimeport):
    cmd="BA3F000000"+ strmac +"01020000"+get_dev_ipstrhex(newip) +get_dev_ipstrhex(newgateway)+\
        get_dev_ipstrhex(newnetmask)+get_dev_ipstrhex(newacquip)+get_dev_portstrhex(newacquport)+\
        get_dev_ipstrhex(newrealtimeip)+get_dev_portstrhex(newrealtimeport)+"00ED"
    return binascii.a2b_hex(cmd)


def set_dev_time(strmac):
    time_str=str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))+'0'+str(datetime.today().weekday())
    return binascii.a2b_hex('BA0E000000'+strmac+'01030000'+time_str[2:] +'00ED')


def get_dev_time(strmac):
    return binascii.a2b_hex('BA0E000000'+ strmac +'010A00000000ED')


def set_fire_alarm(strmac):
    return binascii.a2b_hex('BA0E000000' + strmac + '024D000001ED')


def cancel_fire_alarm(strmac):
    return binascii.a2b_hex('BA0E000000' + strmac + '024D000002ED')


def test_dev_online(strmac):
    return binascii.a2b_hex('BA0E000000'+strmac +'010100000000ED')

def get_search_dev_cmd_str():
    return binascii.a2b_hex("BA0E000000FFFFFFFFFFFF020100000000ED")


def send_get_dev_time(localip,localport,remoteip,remoteport,cmd_str):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.setblocking(False)
    s.settimeout(20)
    try:
      s.bind((localip,localport))
    except:
        print '端口被占用'
    s.sendto(cmd_str,(remoteip, remoteport))
    try:
        data, addr = s.recvfrom(2048)
    except:
        print'设备没有回应'
        return Fales
    if str(data[12:13].encode('hex')) == '0a':
        return True
    else: return False
    s.close()


def send_set_fire_alarm(localip,localport,remoteip,remoteport,cmd_str):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.setblocking(False)
    s.settimeout(20)
    try:
      s.bind((localip,localport))
    except:
        print '端口被占用'
    s.sendto(cmd_str,(remoteip, remoteport))
    try:
        data, addr = s.recvfrom(2048)
    except:
        print'设备没有回应'
        return Fales
    if str(data[12:13].encode('hex')) == '4d':
        return True
    else:
        return False
    s.close()


def send_cancel_fire_alarm(localip,localport,remoteip,remoteport,cmd_str):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.setblocking(False)
    s.settimeout(10)
    try:
      s.bind((localip,localport))
    except:
        print '端口被占用'
    s.sendto(cmd_str,(remoteip, remoteport))
    try:
        data, addr = s.recvfrom(2048)
    except:
        print'设备没有回应'
        return Fales
    if str(data[12:13].encode('hex')) == '4d':
        return True
    else:
        return False
    s.close()


def send_test_dev_online(localip,localport,remoteip,remoteport,cmd_str):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.setblocking(False)
    s.settimeout(20)
    try:
      s.bind((localip,localport))
    except:
        print '端口被占用'
    s.sendto(cmd_str,(remoteip, remoteport))
    try:
        data, addr = s.recvfrom(2048)
    except:
        print'设备没有回应'
        return False
    if str(data[12:13].encode('hex')) == '01':
        return True
    else:
        return False
    s.close()


def send_set_dev_time(localip,localport,remoteip,remoteport,cmd_str):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.setblocking(False)
    s.settimeout(20)
    try:
      s.bind((localip,localport))
    except:
        print '端口被占用'
    s.sendto(cmd_str,(remoteip, remoteport))
    try:
        data, addr = s.recvfrom(2048)
    except:
        print'设备没有回应'
        return False
    if str(data[12:13].encode('hex')) == '03':
        return True
    else:
        return False
    s.close()


class MessageSender:
    remote_ip = None
    remote_port = None

    def __init__(self,local_ip,local_port=20105):
        self.local_ip=local_ip
        self.local_port=local_port
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)
        self.sock.settimeout(20)
        try:
            self.sock.bind((self.local_ip, self.local_port))
        except Exception,e:
            print 'ip or port error:',str(e)
            self.sock.close()



    def send_message(self,message):
        global data
        try:
            self.sock.sendto(message,(self.remote_ip, self.remote_port))
            data, address = self.sock.recvfrom(2048)
        except Exception, e:
            print 'send/recv message fail:',str(e)
            self.sock.close()

    def run_comm_sever(self):
        global data
        count = 0
        while count<10:
        #while True:
            try:
                data,address = self.sock.recvfrom(2048)
            except Exception,e:
                print '等待数据上报',str(e)
                continue
                # break
            self.check_data()
            count+=1

    def check_data(self):
        global data
        print data.encode('hex')
        data=None

    def __delete__(self, instance):
        self.sock.close()

    def display_info(self):
        print self.local_ip
        print self.local_port
        print self.remote_ip
        print self.remote_port


class DeviceSearcher(MessageSender):
    cmm='BA0E000000FFFFFFFFFFFF020100000000ED'
    filename = 'D:/devices_list.csv'

    def set_broadcast(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.remote_ip='<broadcast>'
        self.remote_port=20105

    def get_command(self):
        return binascii.a2b_hex(self.cmm)

    def send_message(self):
        try:
            self.sock.sendto(self.get_command(), (self.remote_ip, self.remote_port))
            data, address = self.sock.recvfrom(2048)
        except Exception, e:
               print 'send/recv message fail:', str(e)
        count=0
        #while True:
        old=''
        dev=[]
        while count < 10:
            try:
                data, addr = self.sock.recvfrom(2048)
            except:
                sys.exit(0)
            if data[5:11].encode('hex') == 'ffffffffffff'or data.encode('hex') == old.encode('hex'):
                continue
            count += 1
            old = data
            dev.append(data)
        print dev
        return dev
        self.sock.close()

    def writer_info(self,datas):
        device=[]
        devices = [['StatusCode', 'AgentNumber', 'DevClass', 'DevNo', 'DevMAC', \
                    'DevIP', 'DevGateway', 'DevSubnetMask', 'DevLocalPort', \
                    'DatAcquisitionIP', 'DataAcquisitionPort', 'RealTimeIP', \
                    'RealTimePort', 'HardwareVersion']]
        for data in datas():
            device.append(data[13:15].encode('hex'))
            device.append(data[3:5].encode('hex'))
            device.append(data[17:18].encode('hex'))
            device.append(data[18:20].encode('hex'))
            device.append(data[20:26].encode('hex'))
            device.append(data[26:30].encode('hex'))
            device.append(data[30:34].encode('hex'))
            device.append(data[34:38].encode('hex'))
            device.append(data[38:40].encode('hex'))
            device.append(data[40:44].encode('hex'))
            device.append(data[44:46].encode('hex'))
            device.append(data[46:50].encode('hex'))
            device.append(data[50:52].encode('hex'))
            device.append(data[52:60].encode('hex'))
        devices.append(device)
        with open(self.filename,'wb') as f:
            writer = csv.writer(f)
            writer.writerows(devices)
        f.close()
        with open(self.filename) as f:
            reader = csv.reader(f)
            print(list(reader))
        f.close()

    def reade_info(self):
        with open(self.filename) as f:
            reader = csv.reader(f)
            print(list(reader))
        return list(reader)

        #with open(self.filename) as f:
            #reader = csv.reader(f)
            #head_row = next(reader)
            #for row in reader:
                #print(reader.line_num, row)
                #print(row)
                #print(list(reader))




if __name__ == "__main__":
    #ms=MessageSender('192.168.2.200',20106)
    #ms.run_comm_sever()
    ds=DeviceSearcher('192.168.2.200')
    ds.set_broadcast()
    ds.send_message()
    ds.reade_info()
    #ms2=MessageSender('192.168.2.200')
    #ms2.set_broadcast()
    #cmd_str=get_search_dev_cmd_str()
    #ms2.send_message(cmd_str)
    #ms2.check_data()
    #result = send_test_dev_online('192.168.2.200',20105,'192.168.2.42',20105,cmd_str)
    #print result
