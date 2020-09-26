import m5
from m5.objects import *
from caches import *
from optparse import OptionParser

# Parser for args
parser = OptionParser()
parser.add_option('--l2_assoc', help="Unified L2 cache associativity")
parser.add_option('--l2_size', help="Unified L2 cache size")
parser.add_option('--cmd', help="Command to run")
parser.add_option('--args', help="Arguments to command")

# Get the arguments
(options, args) = parser.parse_args()

# Print the arguments
print("Got the following arguments")
print("Command: " + str(options.cmd))
print("Arguments: " + str(options.args))
print("L2 size: " + str(options.l2_size))
print("L2 Associativity: " + str(options.l2_assoc))

system = System()

# Create clock domains. Running at 1Ghz
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Declare 512MB RAM
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

# Create a CPU
system.cpu = TimingSimpleCPU()

# Create a memory bus
system.membus = SystemXBar()

# Create L1 caches
system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()

# Connect L1 caches to CPU
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

# Create bus to connect L1 and L2
system.l2bus = L2XBar()

# Connect L1 to l2bus
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

# Instantiate L2 and connect to l2bus and membus
system.l2cache = L2Cache(options)
system.l2cache.connectCPUSideBus(system.l2bus)
system.l2cache.connectMemSideBus(system.membus)

# Connect system port to membus to load data
system.system_port = system.membus.slave

# Set up RAM
system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master

# Set up interrupts
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.master
system.cpu.interrupts[0].int_master = system.membus.slave
system.cpu.interrupts[0].int_slave = system.membus.master

# Create a process
process = Process()
process.cmd = [options.cmd] + options.args.split()
system.cpu.workload = process
system.cpu.createThreads()

# Create root system
root = Root(full_system = False, system = system)
m5.instantiate()

# Start simulation
print("Beginning simulation!")
exit_event = m5.simulate()

print('Exiting @ tick {} because {}'.format(m5.curTick(), exit_event.getCause()))
