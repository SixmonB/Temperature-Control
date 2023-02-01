import matplotlib.pyplot as plt

temperature = []
time = []
constant = []

f = open("D:\Programs (x86)\PuTTY\putty.txt")
i = 0

for row in f:
    print(row)
    row = row.split(';')
    if(i%2 != 0):
        temperature.append(float(row[1]))
        time.append(i*0.5)
        constant.append(40)
    i += 1

max_time = int(time[-1]) 
seconds = int(time[-1]/2)
plt.xlim(0,time[-1])
# each element of list time is half a second, so we get a second every two elements
# That's why we label each tick with half its value

# check the math so as to always get the same amount of ticks and labels
# maybe try with numpy library and operate with floats instead of ints

#plt.xticks(range(0, max_time, 2), range(0, seconds, 1))   
plt.xlabel('Time [s]')
plt.ylabel('Temperature [C]')
plt.title('Temperature with PI Controller')
plt.ylim(0,50)
plt.yticks(range(0, 70, 5))
plt.plot(time, constant)
plt.plot(time, temperature, label = 'Temperature = f(Time)')


#plt.plot(time, constant)




plt.show()

