import math
import requests
from scapy.all import sniff
from scapy.layers.inet import TCP
from scapy.packet import Raw

from Payload import Payload
from Stream import Stream
from scapy.config import conf
conf.debug_dissector = 2

# A dictionary to store packets by their TCP sequence number
tcp_streams = {}
server_ip = ''

def packet_callback(packet):
    global server_ip
    ip_src = packet["IP"].src
    ip_dst = packet["IP"].dst

    if packet.haslayer(TCP) and packet.haslayer(Raw):
        p = Payload(packet[Raw].load)
        try:
            d = p.read_string_to_end().decode("utf-8", errors="ignore")
            if "s123456" in d:
                server_ip = ip_dst
                print("Hooking successful " + server_ip)
        except ValueError:
            print("Something went wrong")

    if ip_src != server_ip:
        return

    if packet.haslayer(TCP) and packet.haslayer(Raw):  # Check if the packet contains TCP and raw data
        p = Payload(packet[Raw].load)
        ack = packet[TCP].ack
        if p.size() < 44+1+4+4:
            return

        try:
            if tcp_streams.get(ack) is not None:
                data = p.read_string_to_end().decode("utf-8", errors="ignore")
                tcp_streams[ack].append_data(data.split("TOZ")[0])
                if "AuctionInventory" in data:
                    json_data = tcp_streams[ack].get_data()
                    json_data = json_data[0:json_data.rfind("}")+1]
                    print(json_data)
                    requests.post("http://localhost:8080/item", data=json_data)
            else:
                data = p.read_string_to_end().decode("utf-8", errors="ignore")
                if "data" in data:
                    tcp_streams[ack] = Stream(1)
                    tcp_streams[ack].append_data(data[data.index("{"):])
        except ValueError:
                print("Failed to convert something:")
                print(p.payload.hex())
                return

def main():
    # Your main code here
    sniff(filter="tcp", prn=packet_callback, store=False)
    print("Hello, World!")

if __name__ == "__main__":
    main()