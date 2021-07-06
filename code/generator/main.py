'''
Author: Lee Chun Hao
GitHub: https://github.com/0x4F776C
LinkedIn: https://sg.linkedin.com/in/lee-chun-hao
'''

from template import *

def main():
    for i in range(10):
        flag = createFlag()
        exec_list = [tcpTraffic, fuzzDataTCP, icmpTraffic, fuzzDataICMP, dnsTraffic, fuzzDataDNS, httpTraffic, fuzzDataHTTP]
        exec_me = random.randint(0, 7)
        if (exec_me == 1) or (exec_me == 3) or (exec_me == 5) or (exec_me == 7):
            exec_list[exec_me]()
            sleepTimer()
        else:
            exec_list[exec_me](flag)
            addFlagToDB(flag)
            sleepTimer()
    return None

if __name__ == "__main__":
    main()