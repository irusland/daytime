from socket import socket, AF_INET, SOCK_DGRAM
import struct
import time

FORMAT = "!12I"
EPOCH = 2208988800
HOST = 'pool.ntp.org'
PORT = 123

#    0                   1                   2                   3
#  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |LI | VN  |Mode |    Stratum     |     Poll      |  Precision   |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# +-------+--------------------------+
# | Value |          Meaning         |
# +-------+--------------------------+
# |   0   | reserved                 |
# |   1   | symmetric active         |
# |   2   | symmetric passive        |
# |   3   | client                   |
# |   4   | server                   |
# |   5   | broadcast                |
# |   6   | NTP control message      |
# |   7   | reserved for private use |
# +-------+--------------------------+


def bitstring_to_bytes(s):
    return int(s, 2).to_bytes(len(s) // 8, byteorder='big')


def build_packet(leap_indicator, version_number, mode):
    bin_str = f'{leap_indicator:02b}{version_number:03b}{mode:03b}'
    bts = bitstring_to_bytes(bin_str)
    b = bts + 47 * b'\0'
    return b


def request_time(packet):
    with socket(AF_INET, SOCK_DGRAM) as s:
        s.connect((HOST, PORT))
        s.sendall(packet)
        data = s.recv(1024)

    size = struct.calcsize(FORMAT)
    unpacked = struct.unpack(FORMAT, data[0:size])
    r = unpacked[10] + float(unpacked[11]) / 2 ** 32 - EPOCH
    return time.ctime(r).replace("  ", " ")


def main():
    li = 0
    vn = 3
    mode = 3
    packet = build_packet(li, vn, mode)

    print(request_time(packet))


if __name__ == '__main__':
    main()
