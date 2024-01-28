import json
import subprocess
import time

def run_and_handle_script(script_path, data_path, output_path, flag):
    while True:
        process = subprocess.Popen(["python", script_path])
        while True:
            if process.poll() is not None:  
                if process.returncode == 0:  
                    return  
                else:  
                    data = read_json_file(data_path)
                    last_id = read_output_file(output_path)[-1]["id"]
                    if flag == 1:
                        for i, item in enumerate(data):
                            if item["id"] == last_id:
                                data = data[i+1:]
                                break
                    elif flag == 0:
                        for i, item in enumerate(data):
                            if item["id"] == last_id:
                                data = data[:i]
                                break
                    write_json_file(data_path, data)
                break
            time.sleep(1)  

def read_json_file(file_path):
    with open(file_path, "r") as f:
        return json.load(f)



def read_output_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()
        last_comma = content.rfind(',')
        content = '[\n' + content[:last_comma]  + '\n]'
        data = json.loads(content)
    return data


def write_json_file(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

def main():
    run_and_handle_script("api.py", "input.json", "output.json", 1)
    #run_and_handle_script("apicopy.py", "input.json", "output.json", 0)
if __name__ == "__main__":
    main()
