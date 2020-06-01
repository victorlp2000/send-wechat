import psutil
import time

def hasHandle(fpath):
    for proc in psutil.process_iter():
        try:
            for item in proc.open_files():
                if fpath == item.path:
                    return True
        except Exception:
            pass

    return False

# return if the file has no access
def waitFile(fpath, maxSeconds=0):
    while hasHandle(fpath):
        time.sleep(1)
        if maxSeconds == 0:
            break
        maxSeconds -= 1
    return maxSeconds       # 0 for timeout

if __name__ == '__main__':
    import sys
    fpath = sys.argv[1]
    print (fpath, hasHandle(fpath))
