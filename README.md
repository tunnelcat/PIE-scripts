# PIE-scripts
PIE ("Pentesting is Easy") scripts to make parsing misc. data and pentesting easier.

## extract-fqdns.py
Takes a list of in-scope "top-level" domains (one per line) and extracts all subdomains related to them out of a text file: 
Example in-scope domain: example.org
Output: 
```
example.org
test.example.org
weather.elements.example.org
[etc...]
```

## nmap-observed-hosts-ports.py
Parses multiple .gnmap files to generate 3 files:
- all_hosts.txt (all hosts seen thus far)
- all_tcp_ports.txt (all open tcp ports seen thus far)
- all_udp_ports.txt (all open udp ports seen thus far)

Note: this script also supports Nmap ping sweeps as well as (obviously) standard udp/tcp port scans.
