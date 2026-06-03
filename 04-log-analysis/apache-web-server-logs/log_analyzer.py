import re
import sys

LOG_PATTERN = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+)'             # Capture the IP Address
    r'.+?'                                    # Skip the ident and user fields
    r'\[(?P<timestamp>[^\]]+)\]'              # Capture the timestamp inside [ ]
    r'\s"(?P<method>\w+)\s(?P<path>\S+)'      # Capture HTTP method and URL path
    r'.+?"'                                   # Skip HTTP version
    r'\s(?P<status>\d{3})'                    # Capture the 3-digit status code
    r'\s(?P<size>\d+)'                        # Capture response size
)

global c
d=dict()
suspicious_timestamp=[]
suspicious_ip=[]
suspicious_path=[]
suspicious_status=[]
suspicious_method=[]
failed_attempts=dict()
failed_paths = dict() 

def apache_web_server_log_analyzer(log_file):
    c=0
    for line in log_file:
        match = LOG_PATTERN.search(line)
        if match:
            c=c+1
            d[match.group("ip")]=d.get(match.group("ip"),0)+1
            if match.group("status") == "401" or match.group("status") == "403":
                suspicious_timestamp.append(match.group("timestamp"))
                suspicious_ip.append(match.group("ip"))
                failed_attempts[match.group("ip")] = failed_attempts.get(match.group("ip"), 0) + 1
                failed_paths[match.group("ip")] = match.group("path")
                suspicious_path.append(match.group("path"))
                suspicious_status.append(match.group("status"))
                suspicious_method.append(match.group("method"))
    
    print("="*60)
    print("FORENSIC LOG ANALYSIS REPORT")
    print("="*60)
    
    print("\n[*] Total log entries parsed : ", c)
    
    c1 = len(d)    
    print("\n[*] Unique IP addresses found : ",c1)
    
    print("\n--- REQUEST COUNT PER IP ---\n")
    for ip in list(d):
        print(ip + " -> " + str(d[ip]) + " requests")
    
    print("\n--- SUSPICIOUS EVENTS (401 / 403) ---\n")
    for i in range(len(suspicious_timestamp)):
        print(suspicious_timestamp[i]+"\t"+suspicious_ip[i]+" -> "+suspicious_method[i]+"\t"+suspicious_path[i]+"\t"+suspicious_status[i])
        
    print("\n--- BRUTE FORCE DETECTION (Threshold : 5 failed attempts) ---\n")
    
    for ip in list(d):
        if ip in suspicious_ip:
            no_of_failed_attempts=failed_attempts[ip]
            if no_of_failed_attempts>5:
                print("[!!] BRUTE FORCE DETECTED : " + ip + " -> " + str(no_of_failed_attempts) + " failed attempts on " + failed_paths[ip])
    
    print("="*60)
    
if __name__ == "__main__":
# This block allows us to run the script from the command line
# e.g., python log_analyzer.py basic-access.log
    if len(sys.argv) < 2:
        print("Usage: python log_analyzer.py <path_to_file>")
    else:
        target_file = sys.argv[1]
        with open(target_file, "r") as f:
            apache_web_server_log_analyzer(f)
                
                
            
        
            