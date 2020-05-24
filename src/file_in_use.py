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
def waitFile(fpath):
    while hasHandle(fpath):
        time.sleep(1)

if __name__ == '__main__':
    import sys
    fpath = sys.argv[1]
    print (fpath, hasHandle(fpath))
