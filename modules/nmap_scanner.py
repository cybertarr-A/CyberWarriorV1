import nmap
import pprint

class AdvancedNmapScanner:
    def __init__(self):
        self.nm = nmap.PortScanner()
        print("AdvancedNmapScanner initialized")

    def run_advanced_scan(self, target, ports="1-65535"):
        """
        Run an advanced Nmap scan with:
        - Service/version detection (-sV)
        - OS detection (-O)
        - Aggressive scan (-A)
        - All ports or specified ports
        - Default scripts and vulnerability scripts (--script vuln)
        """
        try:
            print(f"[*] Starting advanced Nmap scan on {target}, ports: {ports} ...")
            args = '-p {} -sS -sV -O -A --script vuln'.format(ports)
            self.nm.scan(target, arguments=args)

            if target not in self.nm.all_hosts():
                print("[!] No hosts found in scan results.")
                return None

            host_info = self.nm[target]

            # Basic host info
            scan_result = {
                'hostname': host_info.hostname(),
                'state': host_info.state(),
                'os': host_info.get('osmatch', []),
                'protocols': {},
                'scripts': {},
            }

            # Parse protocols and ports
            for proto in host_info.all_protocols():
                ports_list = []
                for port in host_info[proto]:
                    port_data = host_info[proto][port]
                    ports_list.append({
                        'port': port,
                        'state': port_data['state'],
                        'name': port_data.get('name', ''),
                        'product': port_data.get('product', ''),
                        'version': port_data.get('version', ''),
                        'extrainfo': port_data.get('extrainfo', ''),
                        'reason': port_data.get('reason', ''),
                        'conf': port_data.get('conf', ''),
                    })
                scan_result['protocols'][proto] = ports_list

            # Parse scripts output (like vuln scripts)
            if 'hostscript' in host_info:
                for script in host_info['hostscript']:
                    scan_result['scripts'][script['id']] = script['output']

            # Parse scripts output on ports (if any)
            for proto in scan_result['protocols']:
                for port_info in scan_result['protocols'][proto]:
                    p = port_info['port']
                    scripts = host_info[proto][p].get('scripts', {})
                    port_info['scripts'] = scripts

            print(f"[+] Advanced Nmap scan completed on {target}")
            return scan_result

        except Exception as e:
            print(f"[!] Error during advanced Nmap scan: {e}")
            return None

    def pretty_print(self, scan_result):
        pprint.pprint(scan_result)
