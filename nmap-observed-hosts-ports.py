import re

def parse_gnmap_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    hosts = set()
    tcp_ports = set()
    udp_ports = set()

    # Parses ping sweep file - Check the second line for the "Ports scanned" information
    if len(lines) > 1 and re.match(r'# Ports scanned: TCP\(0;\) UDP\(0;\) SCTP\(0;\) PROTOCOLS\(0;\)', lines[1]):
        # Add hosts by checking for "Status: Up"
        for line in lines:
            if line.startswith('Host:') and 'Status: Up' in line:
                # Extract IP address
                host = re.search(r'Host: (\S+)', line).group(1)
                hosts.add(host)

    # Parses port scan file
    else:
        # Add hosts by checking if they have at least one port open
        for line in lines:
            if line.startswith('Host:'):
                # Extract IP address
                host = re.search(r'Host: (\S+)', line).group(1)
                ports_info = re.findall(r'(\d+)\/open\/(tcp|udp)', line)
                if ports_info:
                    hosts.add(host)
                    for port, protocol in ports_info:
                        if protocol == 'tcp':
                            tcp_ports.add(port)
                        elif protocol == 'udp':
                            udp_ports.add(port)

    return hosts, tcp_ports, udp_ports

def write_to_file(file_path, data):
    with open(file_path, 'w') as file:
        for item in sorted(data):
            file.write(f'{item}\n')

def main(gnmap_files):
    all_hosts = set()
    all_tcp_ports = set()
    all_udp_ports = set()

    for gnmap_file in gnmap_files:
        hosts, tcp_ports, udp_ports = parse_gnmap_file(gnmap_file)
        all_hosts.update(hosts)
        all_tcp_ports.update(tcp_ports)
        all_udp_ports.update(udp_ports)

    write_to_file('all_hosts.txt', all_hosts)
    write_to_file('all_tcp_ports.txt', all_tcp_ports)
    write_to_file('all_udp_ports.txt', all_udp_ports)

if __name__ == '__main__':
    import sys
    gnmap_files = sys.argv[1:]
    if not gnmap_files:
        print("Usage: python script.py <gnmap_file1> <gnmap_file2> ...")
    else:
        main(gnmap_files)

