import pyshark

def capture_dns_traffic(domain):
    capture = pyshark.LiveCapture(
        interface='Ethernet',
        bpf_filter='udp port 53',
        tshark_path='C:\\Program Files\\Wireshark\\tshark.exe'  # Укажите путь к TShark
    )
    for packet in capture.sniff_continuously(packet_count=10):
        if 'DNS' in packet:
            try:
                if domain in packet.dns.qry_name:
                    print(f"Размер пакета: {packet.length} байт")
                    print(f"IP-адреса: {packet.dns.a}")
                    break
            except AttributeError:
                continue

capture_dns_traffic("wireshark.org")