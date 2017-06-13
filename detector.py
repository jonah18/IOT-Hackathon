import json

with open('metrics.json') as json_data:
	metrics = json.load(json_data)

blacklist = []
index_translate = {}

packet = sys.argv[1]
metric = sys.argv[2]
std_devs = sys.argv[3]

src_ip = packet['source']['layers']['eth']['eth.src']

# Check source address is already blacklisted
if src_ip in blacklist:
	print ("Blacklisted packet")
	return

# TODO: Determine packet type
index = index_translate['metric']
val = packet['index']

mean = metrics['packet_type']['metric']['mean']
values = metrics['packet_type']['metric']['values']
stdev = metrics['packet_type']['metric']['stdev']

# Compute number of stdevs datapoint is from mean
num_devs = abs(val - mean)/stdev

if num_devs > std_devs:

	# Blacklist IP address
	print("Packet rejected")
	blacklist.append(src_ip)

else:
	print("Packet passed")