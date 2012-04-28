#!/usr/bin/env python
# @author : garfee

import sys
import os
import time

class Catcher:
	def __init__(self):
		self.date=time.strftime('%Y%m%d')
		self.file=open(self.date+'.sty','a')
		self.head=[
			'time','cpu:%user', 'cpu:%nice', 'cpu:%system', 'cpu:%iowait', 'cpu:%idle',
			'mem:total', 'mem:free', 'mem:used', 'mem:free+cache+buffer', 'mem:used-cache-buffer',
			'disk:tps', 'disk:read(MB/s)', 'disk:write(MB/s)', 'disk:avgrq-sz', 'disk:await', 'disk:svctm', 'disk:%util',
			'net:lo:in(MB/s)', 'net:lo:out(MB/s)', 'net:lo:indrop(packet/s)', 'net:lo:outdrop(packet/s)',
			'net:eth0:in(MB/s)', 'net:eth0:out(MB/s)', 'net:eth0:indrop(packet/s)', 'net:eth0:outdrop(packet/s)',
			'net:eth1:in(MB/s)', 'net:eth1:out(MB/s)', 'net:eth1:indrop(packet/s)', 'net:eth1:outdrop(packet/s)',
			]
		if self.file.tell()==0:
			self.file.write('\t'.join(self.head)+'\n')
			self.file.flush()
			

	def __del__(self):
		self.file.close()
	
	def daycheck(self):
		cur_date=time.strftime('%Y%m%d')
		if self.date!=cur_date:
			self.file.close()
			self.date=cur_date
			self.file=open(self.date+'.sty','a')
			self.file.write('\t'.join(self.head)+'\n')
			self.file.flush()

	def cpustat(self,cpu):
		cells=cpu.split()
		return '\t'.join(cells[2:6])+'\t'+cells[7]

	def memstat(self,mem):
		cells=[0]
		mem=mem.split()
		cells.append(str(float(mem[1])/1000))
		cells.append(str(float(mem[2])/1000))
		cells[0]=str(float(mem[1])/1000+float(mem[2])/1000)
		cached=float(mem[4])/1000+float(mem[5])/1000
		cells.append(str(float(cells[1])+cached))
		cells.append(str(float(cells[2])-cached))
		return '\t'.join(cells)

	def diskstat(self,disk):
		cells=[]
		disk=disk.split()
		#print disk
		cells.append(disk[2])
		cells.append(str(float(disk[3])*512/1024/1024))
		cells.append(str(float(disk[4])*512/1024/1024))
		cells.append(str(float(disk[5])*512/1024/1024))
		cells.append(str(float(disk[7])*512/1024/1024))
		cells.append(str(float(disk[8])*512/1024/1024))
		cells.append(str(float(disk[9])*512/1024/1024))
		return '\t'.join(cells)

	def netstat(self,net,enet):
		cells=[]
		net=net.split()
		enet=enet.split()
		cells.append(str(float(net[4])/1000))
		cells.append(str(float(net[5])/1000))
		cells.append(enet[5])
		cells.append(enet[6])
		return '\t'.join(cells)
		
		
	def catch(self):
		f=os.popen('sar -n DEV -n EDEV -u -d -r -p 10 1')
		raw=f.readlines()[2:26]
		#print len(raw)
		stat=[time.strftime('%Y-%m-%d %H:%M')]
		#print self.cpustat(raw[1])
		stat.append(self.cpustat(raw[1]))
		stat.append(self.memstat(raw[23]))
		stat.append(self.diskstat(raw[19]))
		stat.append(self.netstat(raw[10],raw[4]))
		stat.append(self.netstat(raw[11],raw[5]))
		stat.append(self.netstat(raw[12],raw[6]))
		self.file.write('\t'.join(stat)+'\n')
		self.file.flush()
		self.daycheck()

	def loop(self):
		while True:
			self.catch()
			time.sleep(50)
			
if __name__=='__main__':
	catcher=Catcher()
	catcher.loop()
