import pyActigraphy
import os
import fld
# retrieve path to example files
fpath = os.path.join(os.path.dirname(fld.__file__),'data/')

import plotly.graph_objs as go

#Read files by batch
# Read test files
raw = pyActigraphy.io.read_raw(fpath+'example*.AWD', reader_type='AWD')

# Check how many files have been read
len(raw.readers)

raw.names()

# Check the duration of the recording
raw.duration()

raw.IS()

raw.kAR(0)

for iread in raw.readers:
    print("Object type: {}. Name: {}. Duration of the recording: {}. Number of acquisition points: {}".format(type(iread),iread.name,iread.duration(),len(iread.data)))
