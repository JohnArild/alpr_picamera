#!/usr/bin/env python3

# BSD 3-Clause License

# Copyright (c) 2020, John Arild Lolland
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import picamera
import time
import subprocess
import json
import re

temp1 = True
camera = picamera.PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()
time.sleep(2)

def read_json(text):
    ret = []
    try:
        alpr_json = json.loads(text)
        for result in alpr_json["results"]:
            candidates = result["candidates"]
            for plates in candidates:
                regex = re.search("\D{2}\d{5}", plates["plate"])
                if regex:
                    ret.append(regex.group())
        return ret
    except:
        return

def print_numbers(text):
    result = read_json(text)
    if result:
        for plate in result:
            print(plate)

def pic_update(temp1):
    if temp1:
        print("\r\\", end="")
    else:
        print("\r/", end="")

while True:
    imagepath="test.jpg"
    camera.capture(imagepath)
    proc=subprocess.Popen(["alpr", imagepath, "-c eu", "-j"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    readchar = "must initialize as not empty"
    readline = ""
    while readchar:
        pic_update(temp1)
        temp1 = not temp1
        readchar = proc.stdout.read(1).decode()
        readline += readchar
        if readchar == "\r" or readchar == "\n" or readchar == "":
            print_numbers(readline)
            readline = ""