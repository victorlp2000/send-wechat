import subprocess
import time
from collections import namedtuple

# try to synchroze with crantab event
#
def getCrontabSetting(key):
    output = subprocess.check_output(['crontab', '-l'])
    s = output.decode('utf-8')
    for line in s.splitlines():
        if line.startswith('#'):
            continue
        if not key in line:
            continue
        return line
    return None

def matchHour(t, tItems):
    if tItems[1] == '*':
        return True
    if int(tItems[1]) == t.tm_hour:
        return True
    return False

def matchMinute(t, tItems):
    if tItems[0] == '*':
        return True
    if tItems[0].startswith('*/'):
        if t.tm_min % int(tItems[0][2:]) == 0:
            return True
    elif int(tItems[0]) == t.tm_min:
        return True
    return False

def timeMatch(t, tItems):
    if t.tm_sec != 0:
        return False
    if matchHour(t, tItems) and matchMinute(t, tItems):
        return True
    return False

def checkCrontab():
    cmd = getCrontabSetting('scan_websites.sh')
    t = time.localtime()
    if cmd != None:
        s = cmd.split()
        return timeMatch(t, s)
    print('did not find crontab command')
    return False

def nextMatchSeconds(t, tItems):
    Time = namedtuple('Time', 'tm_hour tm_min tm_sec')
    h = t.tm_hour
    m = t.tm_min
    s = t.tm_sec
    count = 0
    while not timeMatch(Time(h, m, s), tItems):
        s += 1
        if s == 60:
            s = 0
            m += 1
        if m == 60:
            m = 0
            h += 1
        count += 1
    return (count, h, m)

if __name__ == '__main__':

    waitTime = ()
    cmd = getCrontabSetting('scan_websites.sh')
    t = time.localtime()
    if cmd != None:
        print(cmd)
        s = cmd.split()
        waitTime = nextMatchSeconds(t, s)
    else:
        print('did not find crontab command')
    print(waitTime)

    # Time = namedtuple('Time', 'tm_hour tm_min tm_sec')
    # t = Time(10, 10, 1)
    # s = ['*/10', '*']
    # print(nextMatchSeconds(t, s))

    # h = 0
    # m = 0
    # s = 0
    # for i in range(0, 24*60*60):
    #     s = i % 60
    #     m = int(i / 60) % 60
    #     h = int(i / (60*60))
    #     # print(h, m, s)
    #     if timeMatch(Time(h, m, s), ['*/30', '*']) == True:
    #         print(h,m,s)
