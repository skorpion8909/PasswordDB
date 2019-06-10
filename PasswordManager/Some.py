import os
import sys
from socket import inet_aton
from subprocess import getoutput
import telnetlib

port = 53 # dns port

if __name__ == "__main__":

    tracertCommand = "tracert -d -h 1 8.8.8.8"

    trace = getoutput(tracertCommand.split(" "))

    # get line with modem ip should be first in trace
    trace = [x for x in trace.split("\n")][3]

    ip = None

    #get ip
    for x in trace.split(" "):
        try:
            inet_aton(x)
            if len(x.split(".")) == 4:
                ip = x
        except Exception:
            pass
    if ip == None:
        print("Ip could not be found")
        print("Check cabels and PC LAN interface")
        sys.exit(0)

    pingOk = False

    if os.system(f"ping {ip} -n 2") == 0:
        print("Modem pinged")
    else:
        print("Not in network")
        sys.exit(0)
    # turn on telnet from your command prompt dism /online /Enable-Feature /FeatureName:TelnetClient

    try:
        telnet = telnetlib.Telnet(f"{ip}", port)
        print("Connection allowed")
    except Exception:
        print("Connection refused")
