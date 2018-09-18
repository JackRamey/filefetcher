#! /usr/bin/env python3

import os, sys, time
from urllib.request import unquote, urlopen

hostname = '<hostname_here>'

hrefs = []

def sizeof_fmt(num, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)

def download_rate(bytes, total_duration):
    return bytes/total_duration

def read_csv_file(filename):
    with open(filename, "r") as inf:
        for line in [line.strip().split(',') for line in inf]:
            hrefs.extend(line)
        #print(hrefs)

def fetch_files():
    for count, href in enumerate(hrefs):
        href_slice = unquote(href).split("/")
        dir = os.path.join(*href_slice[1:-1])
        filename = href_slice[-1]
        os.makedirs(dir, exist_ok=True)
        # print(dir)
        # print(filename)
        download(hostname + href, os.path.join(dir, filename), count)

def download(url, filename, count):
    start_time = time.time()
    u = urlopen(url)
    f = open(filename, 'wb')
    meta = u.info()
    file_size = int(u.getheader("Content-Length"))
    print("Downloading: {0} Bytes: {1}".format(filename, sizeof_fmt(file_size)))
    print("File #{0} of {1}".format(count+1, len(hrefs)))

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        buf_size = len(buffer) # in bytes
        file_size_dl += buf_size
        f.write(buffer)
        curr_time = time.time()
        duration = curr_time - start_time# in milliseconds
        dl_speed_fmt = sizeof_fmt(file_size_dl/ duration) + "/s"
        status = r"%10s  [%3.2f%%] %1.10f %10s" % (sizeof_fmt(file_size_dl), file_size_dl * 100. / file_size, duration, dl_speed_fmt)
        status = status + chr(8) * (len(status) + 1)
        print(status, end='\r')

    f.close()



if __name__ == "__main__":
    os.chdir('out')
    hostname = sys.argv[1]
    read_csv_file(sys.argv[2])
    fetch_files()
