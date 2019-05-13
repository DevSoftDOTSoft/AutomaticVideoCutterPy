#	Copyright (C) 2018  Ricardo Boavida
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import time,subprocess,sys,os

# WINDOWS BASED PS
def process_exists(process_name,pid):
    call = 'TASKLIST', '/FI', 'PID eq %s' % pid
    # use buildin check_output right away
    output = subprocess.check_output(call)
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.startswith(process_name)

def analyse(file):
    read = open(file, 'r')
    for line in read.readlines():
        if "[Parsed_blackframe_1" in line:
            for i in range(len(line.split("\r"))):
                if "[Parsed_blackframe_1" in line.split("\r")[i]:
                    TimeLine = float(line.split("\r")[i].split(":")[4].split(" ")[0])
                    return TimeLine
            break
    return None

# INIT VARS ############################
args = sys.argv

Pic_Begin = args[3]
Pic_End = args[4]
Video = args[2]
ffmpeg = args[1] # BINARY
New_Video = args[5]
VialPercent = args[6]
#########################################

print("\nParsing Begin...\n")

with open('outputBeg.txt', 'w') as output_f:
    p = subprocess.Popen('"' + ffmpeg + '" -i "' + Video + '" -loop 1 -i "' + Pic_Begin + '" -an -filter_complex "blend=difference:shortest=1,blackframe=' + VialPercent + ':32" -f null -',
                         stdout=output_f,
                         stderr=output_f)

    # Stop as Soon as you can find it on Begin, since you want the very 1's Frame compatible
    # MultiOS Fix needed
    while process_exists("ffmpeg.exe",p.pid):
        TOF = analyse('outputBeg.txt')
        if TOF != None:
            Begin_TimeLine = TOF
            p.kill()
            break


print("Begin Found : " + str(float(Begin_TimeLine)) + "\n")
print("Parsing End...\n")

with open('outputEnd.txt', 'w') as output_f:
    p = subprocess.Popen('"' + ffmpeg + '" -i "' + Video + '" -loop 1 -i "' + Pic_End + '" -an -filter_complex "blend=difference:shortest=1,blackframe=' + VialPercent + ':32" -f null -',
                         stdout=output_f,
                         stderr=output_f)
    p.wait()
    End_TimeLine = analyse('outputEnd.txt')

End_TimeLine -= Begin_TimeLine
print("End Found : " + str(float(End_TimeLine)) + "\n")

print("Cutting...\n")
p = subprocess.Popen('"' + ffmpeg + '" -v quiet -y -i "' + Video + '" -vcodec copy -acodec copy -ss ' + str(Begin_TimeLine)  + ' -t ' + str(End_TimeLine) + ' -sn "' + New_Video + '"')

print("All Done...")
time.sleep(5)
exit()