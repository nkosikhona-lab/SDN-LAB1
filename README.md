Project Overview

The project uses:

Mininet to create a 5-switch network topology

Ryu Controller to install flow rules and collect link statistics

OpenFlow 1.3 as the protocol between controller and switches

A Python script (dynamic_lb.py) for dynamic load balancing

iperf3 and ping for network testing

The controller checks the traffic load on each switch port and tries to route packets through the least busy path. The goal is to improve network performance, especially under heavy traffic.

Files in This Repository
File	Description
dynamic_lb.py	Ryu controller load-balancing script
topo.py	Custom Mininet topology (5 switches + 10 hosts)
/screenshots/	Contains screenshots from tests and results
/results/	RTT and throughput graphs
/report/	Final project report in PDF/DOCX format
How to Run the Project
1. Start the Ryu Controller
ryu-manager dynamic_lb.py

2. Start Mininet
sudo mn --custom topo.py --topo fiveswitchtopo --controller=remote --switch ovsk --mac

3. Test Latency (Ping)

Inside Mininet:

pingall
h1 ping h2

4. Test Throughput (iperf3)

On one host:

iperf3 -s


On the other:

iperf3 -c <serverIP> -t 20

Results

Average Latency: ~0.63 ms

Throughput: Up to 24 Gbps

The load balancer successfully reduced congestion and improved performance.

Graphs and screenshots are included in the /results and /screenshots folders.

Purpose of the Project

The goal was to show how SDN can improve network performance by using dynamic routing instead of static paths. This helps avoid congestion and makes better use of available links.

Future Improvements

Test a larger network topology

Deploy the setup on AWS EC2

Add machine learning for smarter routing decisions

Add security features (e.g., firewall rules)

Author

N. Mbatha
Student Number: 231014805# SDN-LAB1
