import multiprocessing.pool
import sys, pillowcase_api, getopt, os
import multiprocessing

def main():
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "f:d:a:", ["file=", "directory=","api-key="])
    except getopt.GetoptError as err:
        print(err)
        return
    
    if len(opts) == 0:
        print("use plwcse-cli -h for info on how to use")
        return

    for opt, val in opts:

        if opt in ("-f", "--file"):
            file = val
        elif opt in ("-a", "-api-key"):
            api_key = val
        elif opt in ("-d", "--directory"):
            dir = val
        else:
            print("use plwcse-cli -h for info on how to use")

    
    if 'file' in locals():
        upload_file(file, api_key)

    elif "dir" in locals():
        global pool
        pool = multiprocessing.pool.ThreadPool(3)
        upload_dir(dir, api_key)
        pool.close()
        pool.join()
    

def upload_file(file, api_key):
    print("started")
    try:
        url = pillowcase_api.upload_request(file, api_key)
        print("["+os.path.basename(file)+"] -", url)
    except Exception as err:
        print("["+os.path.basename(file)+"] -", err)


def upload_dir(dir, api_key):
    list = os.listdir(dir)

    for elt in list:
        elt = os.path.join(dir,elt)
        if os.path.isdir(elt):
            upload_dir(elt, api_key)
        else:
            pool.apply_async(upload_file, args=(elt, api_key))

if __name__ == "__main__":
    main()