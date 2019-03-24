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

import time,subprocess,sys

args = sys.argv

Pic_Begin = args[3]
Pic_End = args[4]
Video = args[2]
ffmpeg = args[1] # BINARY
New_Video = args[5]
VialPercent = args[6]



print("\nParsing Begin...")

with open('output.txt', 'w') as output_f:
    p = subprocess.Popen('"' + ffmpeg + '" -i "' + Video + '" -loop 1 -i "' + Pic_Begin + '" -an -filter_complex "blend=difference:shortest=1,blackframe=' + VialPercent + ':32" -f null -',
                         stdout=output_f,
                         stderr=output_f)
    while p.wait():
        print()

Begin_TimeLine = ""
doc = ""
read = open('output.txt', 'r')
for line in read.readlines():
    if "[Parsed_blackframe_1" in line:
        for i in range(len(line.split("\r"))):
            if "[Parsed_blackframe_1" in line.split("\r")[i]:
                Begin_TimeLine = float(line.split("\r")[i].split(":")[4].split(" ")[0])
        break
read.close()


print("Begin Found : " + str(float(Begin_TimeLine)) + "\n")

print("Parsing End...")


with open('output2.txt', 'w') as output_f:
    p = subprocess.Popen('"' + ffmpeg + '" -i "' + Video + '" -loop 1 -i "' + Pic_End + '" -an -filter_complex "blend=difference:shortest=1,blackframe=' + VialPercent + ':32" -f null -',
                         stdout=output_f,
                         stderr=output_f)
    while p.wait():
      print()


End_TimeLine = ""
read = open('output2.txt', 'r')
for line in read.readlines():
    if "[Parsed_blackframe_1" in line:
        for i in range(len(line.split("\r"))):
            if "[Parsed_blackframe_1" in line.split("\r")[i]:
                End_TimeLine = float(line.split("\r")[i].split(":")[4].split(" ")[0])
read.close()

End_TimeLine = End_TimeLine - Begin_TimeLine

print("End Found : " + str(float(End_TimeLine)) + "\n")


print("Cutting...\n")

p = subprocess.Popen('"' + ffmpeg + '" -v quiet -y -i "' + Video + '" -vcodec copy -acodec copy -ss ' + str(Begin_TimeLine)  + ' -t ' + str(End_TimeLine) + ' -sn "' + New_Video + '"')


print("All Done...")
time.sleep(5)
exit()