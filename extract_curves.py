from lakeshore import Model224
from sys import argv
'''
jonathan St-Antoine, jonathan@astro.umontreal.ca
This script must be runned on the same network as the lakeshore.
This could easily be modified to read lakeshore 336 as well.
Good luck!
'''
def extract_curve(IP):
    ls = Model224(ip_address=IP)
    channels = ['A','B','C1','C2','C3','C4','C5','D1','D2','D3','D4','D5']
    d = {}
    for chan in channels:
        ch = int(ls.query('INCRV? %s'%chan))
        sensor = ls.query('CRVHDR? %d'%ch).split(',')[0].strip()
        d[sensor] = [];
        for i in range(1,53):
            out = ls.query('CRVPT? %d,%d'%(ch,i))
            d[sensor].append(out)
    for sens in d:
        with open('%s.csv.out'%sens,'w') as f:
            f.write('resistance,temperature\n')
            for s in d[sens]:
                f.write(s.replace('+','')+"\n")

if '__main__' in __name__:
    if '--help' in argv:
        print("Example:\npython extract_curves.py --ip=192.168.1.1 --ip=192.168.1.2\npython extract_curves.py 192.168.1.1 192.168.1.2")
        exit(0)
    if len(argv)<2:
        ips = ['192.168.62.50','192.168.62.192']
    else:
        ips = [arg.replace('--ip=','') for arg in argv if '--ip' in arg]
        if len(ips)<1:
            ips = argv[1:]
    for ip in ips:
        extract_curve(ip)