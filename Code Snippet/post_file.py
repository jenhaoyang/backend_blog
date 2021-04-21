f = open(".../file.txt", 'rb')
files = {"file": (f.name, f, "multipart/form-data")}
requests.post(url="SERVER_URL/create_file", files=files)
