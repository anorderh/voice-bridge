import pyaudio

p = pyaudio.PyAudio()

# Printing all connected devices info
for i in range(p.get_device_count()):
    print(p.get_device_info_by_index(i))

# P Audio connection
p.terminate()

