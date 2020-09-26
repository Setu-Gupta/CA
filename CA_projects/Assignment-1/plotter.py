"""
Author: Setu Gupta
Roll number: 2018190
Date: 26/9/20

Usage:
	python3 path/to/this/file path/to/stats/dir
"""

from matplotlib import pyplot as plt
from matplotlib.ticker import ScalarFormatter
import sys
import os

"""
Plots the data using pyplot
Args:
	data	: {assoc:[[x_vals], [y_vals]], ...}
	where:
		assoc is associativity
		x_vals is cache size
		y_vals demand miss rate of data
Rets:
	None
"""
def plot(data):

	plt.title("L2 Cache data demand base rate")
	plt.grid(True)
	plt.xscale('log', basex=2)	# Log base 2 scale for size
	plt.gca().xaxis.set_major_formatter(ScalarFormatter())
	plt.xlabel("Size in Kb of L2 cache")
	plt.ylabel("Data demand miss rate")

	for assoc in data:	# Plot for all assoc values
		label = "Associativity = " + str(assoc)
		x = data[assoc][0]
		y = data[assoc][1]
		plt.plot(x, y, label=label)
		plt.plot(x, y, 'ko')
		plt.xticks(x)

	plt.autoscale(enable=True, axis='x', tight=True)
	plt.legend()
	plt.show()



"""
Parses files in stats_dir
Files are searched as stats_dir/*/stats.txt
Args:
	stats_dir
Rets:
	None
"""
def get_data(stats_dir):
	
	data = {}

	# Iterate over files and parse data
	temp_data = {}	# Not fully parsed data. {assoc:[(size, rate), ...]}
	for subdir, dirs, files in os.walk(stats_dir):

		if(len(dirs) == 0):	# At base of directory tree

			base_dir = subdir.split("/")[-1]
			size = int(base_dir.split("_")[0][:-2])	# Remove the last "KB" form size
			assoc = int(base_dir.split("_")[1])
			
			if assoc not in temp_data:	# Add entry for associativity
				temp_data[assoc] = []

			stats_file = subdir + "/stats.txt"
			with open(stats_file, 'r') as stats:	# Start going through stats
				for line in stats:
					if(".l2cache.demand_miss_rate::.cpu.data" in line):	# Find the required stat
						rate = float(line.split()[1])	# Parse the value
						temp_data[assoc].append((size, rate))	# Store the data

	
	for assoc in temp_data:
		vals = temp_data[assoc]
		vals.sort(key = lambda x:x[0])	# Sort based on size

		data[assoc] = [[], []]
		for v in vals:
			data[assoc][0].append(v[0])
			data[assoc][1].append(v[1])
	return data

def main():
	if(len(sys.argv) < 2):
		print("Usage: python3 path/to/this/file path/to/stats/dir")
		return

	data = get_data(sys.argv[1])
	plot(data)

if __name__ == '__main__':
	main()