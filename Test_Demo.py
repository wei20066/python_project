# coding:utf-8
import serial
import serial.tools.list_ports
import binascii
import struct

start_byte =0xAA
end_byte=0xBB

beep_word = [0xAA, 0x30, 0x05, 0x05, 0xDC, 0x05, 0xDC, 0x01, 0xA2, 0xBB]
find_card = [0xAA, 0x3B, 0x01, 0x00, 0xE6, 0xBB]
halt_word = [0xAA, 0x35, 0x01, 0x00, 0xE0, 0xBB]
key_word = [0xAA, 0x38, 0x08, 0x01, 0x01, 0xDF, 0xA6, 0x40, 0xE3, 0x15, 0x49, 0xF2, 0xBB]
#key_word = [0xAA, 0x38, 0x08, 0x00, 0x01, 0xAD, 0x18, 0xB9, 0xAC, 0xE5, 0xC0, 0xBA, 0xBB]
auth_sector1 = [0xAA, 0x34, 0x02, 0x01, 0x01, 0xE2, 0xBB]
#auth_word_sector1 = [0xAA, 0x34, 0x02, 0x00, 0x01, 0xE1, 0xBB]
secter1_block4 = [0xAA, 0x36, 0x01, 0x04, 0xE5, 0xBB]
secter1_block5 = [0xAA, 0x36, 0x01, 0x05, 0xE6, 0xBB]
secter1_block6 = [0xAA, 0x36, 0x01, 0x06, 0xE7, 0xBB]
auth_sector4 = [0xAA, 0x34, 0x02, 0x01, 0x04, 0xE5, 0xBB]
secter4_block10 = [0xAA, 0x36, 0x01, 0x10, 0xF1, 0xBB]
secter4_block11 = [0xAA, 0x36, 0x01, 0x11, 0xF2, 0xBB]
secter4_block12 = [0xAA, 0x36, 0x01, 0x012, 0xF3, 0xBB]
auth_sector5 = [0xAA, 0x34, 0x02, 0x01, 0x05, 0xE6, 0xBB]
secter5_block14 = [0xAA, 0x36, 0x01, 0x14, 0xF5, 0xBB]
secter5_block15 = [0xAA, 0x36, 0x01, 0x15, 0xF6, 0xBB]
secter5_block16 = [0xAA, 0x36, 0x01, 0x16, 0xF7, 0xBB]
rats_card = [0xAA, 0x39, 0x01, 0x00, 0xE4, 0xBB]
dict={}

def open_serial():
    plist = list(serial.tools.list_ports.comports())
    if len(plist) <= 0:
        print("the serial port can't find")
    else:
        plist_0 = list(plist[0])
        serial_name = plist_0[0]
        return serial.Serial(serial_name, 115200, timeout=60)
        # print serialFd.portstr
        #print("check which[%s] port was really used>" % serialFd.name)
        # strInput = raw_input('enter some words:')


def pack_cmd(comannd_str):
    return struct.pack("%dB" % len(comannd_str), *comannd_str)


def beep(serialfd,beep_word):
    dat=pack_cmd(beep_word)
    serialfd.write(dat)
    serialFd.read(7)


def search_card(serialfd,find_card):
    list = []
    dat = pack_cmd(find_card)
    serialfd.write(dat)
    rcv=serialFd.read(10)
    back_data = rcv[3:7][::-1].encode('hex').upper() # 十位卡号
    if back_data == '00000000':
        return False
    else:
        list.append(int("0x"+rcv[3:7][::-1].encode('hex').upper(),16)) #10位卡号
        list.append(int("0x" + rcv[3:6][::-1].encode('hex').upper(), 16)) #8位卡号
        #print("10位物理卡号："+list[0])
        #print("8位物理卡号：" + list[1])
        return list


def halt_read(serialfd,halt_word):
    dat = pack_cmd(halt_word)
    serialfd.write(dat)
    serialFd.read(7)


def load_key(serialfd,key_word):
    dat = pack_cmd(key_word)
    serialfd.write(dat)
    rcv = serialFd.read(7)
    back_data = rcv[3:5].encode('hex').upper()
    #print (back_data)
    if back_data == '0000':
        return True
    else:
        print("load_key failed")
        exit(10001)


def auth_key(serialfd,auth_word_sector):
    dat = pack_cmd(auth_word_sector)
    serialfd.write(dat)
    rcv = serialFd.read(7)
    back_data = rcv[3:5].encode('hex').upper()
    if back_data == '0000':
        return True
    else:
        print("auth_key failed")
        exit(10002)


def read_sector(serialfd,auth_word_sector):
    load_key(serialfd,key_word)
    auth_key(serialfd,auth_word_sector)



def read_block(serialfd, block):
    dat = pack_cmd(block)
    serialfd.write(dat)
    data = serialFd.read(22)
    return data


def read1_block(serialfd,block):
    dat = pack_cmd(block)
    serialfd.write(dat)
    rcv = serialFd.read(22)
    reback_data = rcv[3:6][::-1].encode('hex').upper()
    print ("卡流水号：" + str(int("0x" + reback_data, 16)))
    back_data = rcv[3:19].encode('hex').upper()
    print ("卡类："+str(back_data[-1]))
    print ("有效期：" + "20" + str(back_data[6:8]) + "年" + str(back_data[9:10]) + "月" + str(back_data[10:11]) + "日")
    if (int(back_data[12:14]) ==41):
        print("男")
    else:
        print(back_data[12:14])
        print("女")
    print ("身份证号码：" + str(back_data[14:36]))
    print(back_data)





def find_m1_card(serialfd,show_card_num=0):
    data = search_card(serialfd)
    if (data != 0):
        if(show_card_num==1):
            print("卡物理号："+str(data))
    else:
        halt_read(serialfd)
        flag = 1
        while flag < 3:
            data = search_card(serialfd)
            if (search_card(serialfd) !=False ):
                print(data)
                beep(serialfd)
                break
            else:
                flag = flag + 1
                halt_read(serialfd)
        print("find card is null")
        beep(serialfd, 4)
        exit(2)
        return False

    # load keyword on RAM ,for M1 card
    if load_key(serialFd) != 0:
        print("load key fialed")
        beep(serialFd, 4)
        exit(3)
        return False
    return True


def read_card_sector(serial_handle, sector,block1,block2,block3):
    dic = {}
    if sector == 1:
        if find_m1_card(serial_handle,1) == True:
            if auth_key(serial_handle, auth_sector1)==True:
                data_block1 = read_block(serial_handle, block1)
                cardid_hex =  data_block1[3:6][::-1].encode('hex').upper()
                dic["cardID"]=str(int("0x" + cardid_hex, 16))
                print ("卡流水号：" + str(int("0x" + cardid_hex, 16)))
                data_sub =  data_block1[3:19].encode('hex').upper()
                print ("有效期："+ "20"+str(data_sub[6:8])+"年"+str(data_sub[9:10])+"月"+str(data_sub[10:11])+"日")
                if(data_sub[11:12]=="41"):
                    print("男")
                else:
                    print("女")
                print ("身份证号码：" + str(data_sub[14:36]))
                data_block2=read_block(serial_handle, block2)
                data_sub2 = data_block2[3:19].encode('hex').upper()
                print ("卡类：" + str(data_sub2[-1]))
                data_block3=read_block(serial_handle, block3)
                data_sub3 = data_block3[3:19].encode('hex').upper()









def strhextohanzi(code):
    h='\\x'+hex(int(str(int("0x"+code,16))[0:2])+int("0xA0",16))[2:4]
    l='\\x'+hex(int(str(int("0x"+code,16))[2:4])+int("0xA0",16))[2:4]
    return h+l


if __name__ == '__main__':
    serialFd = serial.Serial('COM6', 115200, timeout=60)
    dic={}
    secter_data = []
    ls=search_card(serialFd,find_card)
    dic['wg34']=ls[0]
    dic['wg26']=ls[1]
    #print(ls[0])
    #print(ls[1])
    read_sector(serialFd, auth_sector1)
    secter_data.append( read_block(serialFd, secter1_block4))
    dic['cardid']=int(secter_data[0][3:6][::-1].encode('hex').upper())
    #print(dic['cardid'])
    data = secter_data[0][3:19].encode('hex').upper()
    dic['end_date']='20'+str(data[6:8])+'-'+str(data[8:10])+'-'+str(data[10:12])
    #print(dic['end_date'])
    dic['id']=str(data[14:36])
    #print (dic['id'])
    if (data[12:14] == "41"):
        dic['sex']='男'
    else:
        dic['sex']='女'
    #print(dic['sex'])
    del secter_data[0]
    secter_data.append(read_block(serialFd, secter1_block5))
    data = str(secter_data[0][4:19].encode('hex').upper())
    dic['empno']=int(binascii.a2b_hex(data))
    #print(dic['empno'])
    del secter_data[0]
    secter_data.append(read_block(serialFd, secter1_block6))
    data = str(secter_data[0][3:19].encode('hex').upper())
    empname = ''
    for i in range(0, len(data), 4):
        # print(data2[i:i + 4])
        if data[i:i + 4] != '0000':
            h = hex(int(str(int("0x" + data[i:i + 4], 16))[0:2]) + int("0xA0", 16))[2:4]
            l = hex(int(str(int("0x" + data[i:i + 4], 16))[2:4]) + int("0xA0", 16))[2:4]
            # print(r'\x'+h+r'\x'+l)
            empname = empname + (r'\x' + h + r'\x' + l)
            continue
        else:
            break
    name = empname.decode('gbk', 'ignore').encode('gb2312')
    print(name)
    #b='\xd5\xc5\xd1\xa7\xd3\xd1'.decode('gbk', 'ignore').encode('utf-8')
    #print(b)
    #bytes([0x01, 0x02, 0x31, 0x32])

    beep(serialFd, beep_word)
    #read_sector(serialFd, auth_sector4)
    #find_m1_card(serialFd,1)
    #auth_key(serialFd,auth_word_sector1)
    #read1_block(serialFd,read_block4)
    #read1_block(serialFd,read_block5)
    #read1_block(serialFd, read_block6)
    #halt_read(serialFd)
    #beep(serialFd)

    #b = "\xc0\xe8\xc3\xf7".decode('gbk','ignore').encode('utf-8')
    #print(b)
    #find_m1_card(serialFd)
    #auth_key(serialFd, auth_word_sector4)
    #read_block(serialFd, read_block10)
    #r#ead_block(serialFd, read_block11)
    #read_block(serialFd, read_block12)
    #halt_read(serialFd)
    #beep(serialFd)
    #find_m1_card(serialFd)
    #auth_key(serialFd, auth_word_sector5)
    #read_block(serialFd, read_block14)
    #read_block(serialFd, read_block15)
    #read_block(serialFd, read_block16)
    #beep(serialFd)
#










