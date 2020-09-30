import pandas as pd
import numpy as np
from Streams import stream

# Import data table for stream data
Data = pd.read_excel('test values.xlsx', index_col=0)

# Extract data from table
InletT = Data.loc[:, "Inlet"]
OutletT = Data.loc[:, 'Outlet']
CP = Data.loc[:, 'cp']

# Create and add streams
streams_container = []  # list that contains stream objects
for i in range(1, len(InletT)+1):
    name = 'Stream_{}'.format(i)
    stream_add = stream(name, InletT[i], OutletT[i], CP[i])
    streams_container.append(stream_add)

# Set DTmin
dtmin = float(input('What is the DTmin?'))

for s in streams_container:
    s.intervalT(dtmin)

# Find interval cascade temperatures
IntervalT = np.zeros(len(streams_container) * 2)  # create array for interval temperatures which will be sorted

i = 0  # set counter for indexing into IntervalT
for g in streams_container:
    IntervalT[i] = g.intervalTinlet
    IntervalT[i+1] = g.intervalToutlet
    i = i + 2
# remove values that are the same so that there is only one of each value in IntervalT
ToDel = np.zeros(len(IntervalT))
for i in range(len(IntervalT)):
    ValueSelect = IntervalT[i]
    index = i
    for g in range(len(IntervalT)):
        if index == g:
            ToDel[g] = 0
        elif ValueSelect == IntervalT[g]:
            ToDel[g] = 1

IntervalT = np.delete(IntervalT, ToDel > 0)
IntervalT[::-1].sort()

# Find out if stream is in interval
noStreams = int(len(streams_container))
IntervalMatrix = np.zeros((len(IntervalT) - 1, int(noStreams)))  # rows are intervals, colums are stream
for r in range(len(IntervalT) - 1):
    streamnumber = 0
    for d in streams_container:
        d.inInterval(IntervalT[r], IntervalT[r+1], r, streamnumber, IntervalMatrix)
        streamnumber += 1

# Calculate change in enthalpy
H_Change = np.zeros(len(IntervalT) - 1)  # store enthalpy values

for i in range(len(IntervalT) - 1):  # Calculate enthalpies
    index = np.where(IntervalMatrix[i, :] == 1) # creates tuple of length 2
    index = index[0] # access array of index values from the tuple
    deltaT = IntervalT[i] - IntervalT[i + 1]
    sumCpCold = 0
    sumCpHot = 0

    for g in range(len(index)):  # select Cp for stream then add to either hot or cold Cp total
        streamSelected = streams_container[index[g]]
        streamCp = streamSelected.CP
        if streamSelected.classification == 'Hot':
            sumCpHot += streamCp
        else:
            sumCpCold += streamCp

    H_Change[i] = (sumCpCold - sumCpHot) * deltaT

# Calculate r1 values
r1 = np.zeros(len(IntervalT))
for i in range(len(r1) - 1):
    r1[i + 1] = r1[i] - H_Change[i]

# Calculate r2 values to find pinch point
minr1 = min(r1)
r2 = r1 + abs(minr1)

# display max heat and cooling requirement as well as pinch point temperatures
print('Max heat requirement', r2[0])
print('Max cooling load', r2[-1])
pinchPointIndex = np.where(r2 == 0)
print('Pinch point temperature', IntervalT[pinchPointIndex])
pinchpoint = IntervalT[pinchPointIndex]
hotPinchPointT = pinchpoint + (dtmin / 2)
coldPincPointT = pinchpoint - (dtmin / 2)
print('Hot stream pinch temperature', hotPinchPointT)
print('Cold stream pinch temperature', coldPincPointT)