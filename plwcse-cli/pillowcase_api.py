import os, requests

def upload_request(file, api_key):
    with open(file, "rb") as f:
        total_size = os.stat(file).st_size
        offset = 0
        part_size = 10 * 1024 * 1024 # 10 MB
        part_number = 0
        file_name = os.path.basename(file)

        file_info = {"fileSize": total_size, "fileName": file_name}
        header = {"content-type": "application/json", "x-api-key": api_key}
        
        init_request = requests.post("https://api-upload.plwcse.top/api/upload/init", headers=header, json=file_info)

        if init_request.status_code != (200 or 201):
            try:
                error = init_request.json()["message"]["error"]
            except Exception:
                error = "No error message provided"
            raise Exception("Error during upload : "+error)
        
        upload_id = init_request.json()["message"]["id"]

        while offset < total_size :
            if total_size - offset < part_size:
                part_size = total_size - offset

            f.seek(offset)
            
            r = requests.put("https://api-upload.plwcse.top/api/upload/"+upload_id+"/part" , data={"part": part_number}, files={"file": (file_name,f.read(part_size), "text/plain")})

            if r.status_code != (200 or 201):
                raise Exception("Error during upload of file part "+part_number)
            
            offset += part_size
            part_number += 1

        final_req = requests.get("https://api-upload.plwcse.top/api/upload/"+upload_id+"/done")

        if final_req.status_code != 200:
            raise Exception("Error when retrieving file url.")

        return "https://plwcse.top/f/"+final_req.json()["message"]["id"]

