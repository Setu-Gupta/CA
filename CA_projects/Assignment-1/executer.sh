#!/bin/bash

# Store current directory
cur_dir=$(pwd)

# Jump to gem5 directory
gem5_dir="./../../."
cd $gem5_dir
echo "Entered $(pwd)"

# Start executing gem5
run_dir=$cur_dir/run_dir
out_dir=$run_dir/stats
log_dir=$run_dir/logs

base_cmd="build/X86/gem5.opt"
config_path="CA_projects/Assignment-1/configs/two_level.py"
benchmark='--cmd=CA_projects/Assignment-1/automotive/susan/susan --args="CA_projects/Assignment-1/automotive/susan/input_small.pgm CA_projects/Assignment-1/automotive/susan/output_small_t.smoothing.pgm -s"'

for size in 4KB 8KB 16KB 32KB 64KB 128KB 256KB 512KB 1024KB;
do
	for assoc in 1 2 4 8;
	do
		name="${size}_${assoc}"
		stat_arg="-d $out_dir/$name"
		size_arg="--l2_size=$size"
		assoc_arg="--l2_assoc=$assoc"
		log_path="$log_dir/$name"
		cmd="$base_cmd $stat_arg $config_path $benchmark $size_arg $assoc_arg > $log_path"
		eval $cmd
	done
done
