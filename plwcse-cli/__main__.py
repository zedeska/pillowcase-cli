import multiprocessing.pool
import sys, pillowcase_api, getopt, os
import multiprocessing

def main():
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "hf:d:a:", ["--help" ,"file=", "directory=","api-key="])
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
        elif opt in ("-h", "--help"):
            help()
            return
        else:
            print("use plwcse-cli -h for info on how to use")

    if 'file' in locals() and "dir" in locals():
        print("can't use --file and --directory in the same line/command.")
        return

    elif 'api_key' not in locals():
        print("It is mendatory to provide an API key to upload to pillowcase. If you don't have one, please create an account on https://plwcse.top")
    
    elif 'file' in locals():
        upload_file(file, api_key)

    elif "dir" in locals():
        global pool
        pool = multiprocessing.pool.ThreadPool(3)
        upload_dir(dir, api_key)
        pool.close()
        pool.join()
    

def upload_file(file, api_key):
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

def help():
    print("""
    Welcome to pillowcase-cli, a simple programm to upload files to the https://plwcse.top file host.
          
    Here are the general options :
          
    -h , --help              display this menu.
    -a , --api_key           Provide your pillowcase API key, which is mendatory.
    -f , --file              Path to a file (in quotes) you want to upload.
    -d , --directory         Path to a directory (in quotes), will try to upload everything that is inside this directory, even the files that are inside an other folder.
          
    Please note that you can't use --file and --directory in the same line/command.

    """)

if __name__ == "__main__":
    main()