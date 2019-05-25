# coding:utf-8
import time
import binascii
import serial
import serial.tools.list_ports
import urllib


def little2big_endian(hex_string):
    big_endian_str = '' #定义一个空字符串
    for i in range(len(hex_string)/4):#因为Unicode是4个字符表示一个汉字，每四个一组
        little_endian_char = hex_string[i*4: i*4+4] #取的是四位连续的数字
        big_endian_char = little_endian_char[2:4] + little_endian_char[0:2] #逆字节序
        big_endian_str = big_endian_str + big_endian_char
    return big_endian_str

def HextoHanzi(hex_string):
    unicode_Hanzi = '' #定义一个空字符串
    for i in range(len(hex_string)/4): #因为Unicode是4个字符表示一个汉字，每四个一组
        Hex_char = hex_string[i*4: i*4+4]
        unicode_char = "\\u" + Hex_char
        unicode_Hanzi = unicode_Hanzi + unicode_char
    return unicode_Hanzi.decode('unicode_escape')


def hex_to_han_zi(data):
    emp_name = ''
    for i in range(0, len(data2), 4):
        # print(data2[i:i + 4])
        if data2[i:i + 4] != '0000':
            hw = hex(int(str(int("0x" + data2[i:i + 4], 16))[0:2]) + int("0xA0", 16))[2:4]
            lw = hex(int(str(int("0x" + data2[i:i + 4], 16))[2:4]) + int("0xA0", 16))[2:4]
            # print(r'\x'+h+r'\x'+l)
            emp_name = emp_name + (r'\x' + hw + r'\x' + lw)
            continue
        else:
            break
    name = emp_name.decode('gbk', 'ignore').encode('utf-8')
    return name

if __name__ == '__main__':
    #hex_string = '1162B07328572857005F1A4F62546153A16C265EAB8EB98F'
    #big_endian_str = little2big_endian(hex_string)
    #print HextoHanzi(big_endian_str)
#
   #data='202020202020202020203130303033'
   #empno = ''
   #for i in range(0, len(data), 2):
   #    print(data[i:i + 2])
   #    if data[i:i + 2] != '20':
   #        empno = empno + binascii.a2b_hex(data[i:i + 2])
   #        continue
   #    else:
   #        continue
   #print(empno)
   #print(int(binascii.a2b_hex(data)))
    data2='0CC80E03000000000000000000000000'
    user_name=hex_to_han_zi(data2)
    print(user_name)






