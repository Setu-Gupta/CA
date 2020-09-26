#!/bin/bash
echo "Hi"
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
./susan input_small.pgm output_small.smoothing.pgm -s
./susan input_small.pgm output_small.edges.pgm -e
./susan input_small.pgm output_small.corners.pgm -c

