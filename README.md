# vpn_mon

## Prerequisites

- Python 3
- MySQL 
- Windows (for Linux you'll have to adapt the code)

## How to use it

Create a .bat file with the contents:

```
python vpn_mon.py 192.168.xxx.yyy
```
Where `192.168.xxx.yyy` is the IP in the VPN you want o monitor.

In the Task Scheduler, configure a new task (not "basic task") where the action is this .bat file. Choose the desired frequency.

Mark the option "Run whether the user is logged on or not".

That's all. The data will be saved in the database `vpn_mon`.
