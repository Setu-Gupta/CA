###################################################
####      Install tools for development.       ####
###################################################

apt-get update && apt-get install -y python python-pip git tmux vim cmake wget ack-grep
pip install --upgrade pip

###########################################
####      Environment variables        ####
###########################################

mkdir -p /workspace
export ALADDIN_HOME=/workspace/gem5-aladdin/src/aladdin
export TRACER_HOME=/workspace/LLVM-Tracer
export LLVM_HOME=/usr/local
export BOOST_ROOT=/usr/include

export SHELL=/bin/bash

# So we can link gem5 against libprotobuf when installed from apt.
export FORCE_CXX11_ABI=1

#######################################################
####      Install gem5-Aladdin dependencies.       ####
#######################################################

# Install gem5 dependencies.
apt-get update -qq
apt-get install -y m4 libprotobuf-dev protobuf-compiler libsqlite3-dev libtcmalloc-minimal4 scons zlib1g zlib1g-dev python3 python3-pip libgoogle-perftools-dev
# Change the default Python version to 3.6.
update-alternatives --install /usr/bin/pip pip /usr/bin/pip2 1
update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 2
pip3 install --user --upgrade pip
update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
update-alternatives --install /usr/bin/python python /usr/bin/python3.6 2

pip install numpy six configparser pyparsing pytest pytest-xdist

# Install Aladdin dependencies.
apt-get install -y libboost-graph-dev libpthread-stubs0-dev libreadline-dev libncurses5-dev

# Build LLVM and Clang 6.0 from source.
cd /tmp
RUN wget -q http://releases.llvm.org/6.0.0/llvm-6.0.0.src.tar.xz && tar -xf llvm-6.0.0.src.tar.xz && wget -q http://releases.llvm.org/6.0.0/cfe-6.0.0.src.tar.xz && tar -xf cfe-6.0.0.src.tar.xz && mkdir -p llvm-6.0.0.src/tools/clang && mv cfe-6.0.0.src/* llvm-6.0.0.src/tools/clang && cd llvm-6.0.0.src && mkdir build && cd build && cmake -DCMAKE_INSTALL_PREFIX=/usr/local -DCMAKE_BUILD_TYPE=Release .. && make -j24 && make install && rm -rf /tmp/llvm-6.0.0* && rm -rf /tmp/cfe-6.0.0*

# Build and install LLVM-Tracer
cd /workspace
git clone https://github.com/ysshao/LLVM-Tracer && cd LLVM-Tracer && git fetch --all && mkdir bin && mkdir lib && mkdir build && cd build && cmake .. && make && make install

# Clone gem5-aladdin, but don't build. We'll assume the developer will build.
git clone https://github.com/harvard-acc/gem5-aladdin && cd gem5-aladdin && git submodule init && git submodule update
