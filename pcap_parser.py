import json
import numpy as np

data = None
with open('json-data/zigbee-data-2.json') as json_data:
    data = json.load(json_data)

list_of_frame_lens = []
list_of_data_lens = []

for packet in data:
    # get frame_type of packet for parsing
    frame_type = packet["_source"]["layers"]["wpan"]["wpan.fcf_tree"][
        "wpan.frame_type"]
    frame_type = int(frame_type, 0)

    # getting length of packet frame
    frame_len = packet["_source"]["layers"]["frame"]["frame.len"]
    list_of_frame_lens.append(int(frame_len))

    try:
        data_len = packet["_source"]["layers"]["zbee_aps"]["data"]["data.len"]
        list_of_data_lens.append(int(data_len))
    except KeyError:
        pass

    try:
        data_len = packet["_source"]["layers"]["zbee_nwk"]["data"]["data.len"]
        list_of_data_lens.append(int(data_len))
# only adding if the data field is there
# so we dont keep track of which packet right now
    except KeyError:
        pass

# change lists to numpy arrays
np_frame_lens = np.asarray(list_of_frame_lens)
np_data_lens = np.asarray(list_of_data_lens)

# get average values for lengths
mean_frame_lens = np.mean(np_frame_lens)
mean_data_lens = np.mean(np_data_lens)

# get standard deviation
std_dev_frame_lens = np.std(np_frame_lens)
std_dev_data_lens = np.std(np_data_lens)
print std_dev_frame_lens, std_dev_data_lens

# check if any packets' length are greater than twice the stdev
for i in xrange(0, len(list_of_frame_lens)):
    diff_mean_value = abs(list_of_frame_lens[i] - mean_frame_lens)
    if (diff_mean_value / std_dev_frame_lens) > 2:
        print 'bad!'

for i in xrange(0, len(list_of_data_lens)):
    diff_mean_value = abs(list_of_data_lens[i] - mean_data_lens)
    if (diff_mean_value / std_dev_data_lens) > 2:
        print 'bad!'
