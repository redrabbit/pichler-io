"""
Module for accessing Pichler ventilation / heat-pump unit
"""

import sys
import os
import nabto
import json
from collections import namedtuple
try:
	import configparser
except:
	# python2 compatibility
	import ConfigParser
	configparser = ConfigParser

class Pichler:
	"""
	A class for accessing Pichler ventilation / heat-pump unit.
	
	It allows to read runtime parameters (datapoints) as well as to read/write unit's settings (setpoints).
	"""
	
	def __init__(self, device=None, user=None, passwd=None):
		"""
		Initialize communication with Pichler unit.

		Creates underlying Nabto communication client and establishes session to device.
		
		Parameters
		----------
		device : str, optional
			Device ID, by default None
		user : str, optional
			Name of account that should be used to access unit's data, by default None
		passwd : str, optional
			Password for given account, by default None

		If any of these parameters is not provided, value from `pichler.ini` file is used instead.
		"""
		package_dir = os.path.dirname(os.path.abspath(__file__))

		if not device or not user or not passwd:
			config = configparser.ConfigParser()
			config.read(os.path.join(package_dir, 'pichler.ini'))

			if not device:
				device = config.get('pichler', 'device')
			if not user:
				user = config.get('pichler', 'user')
			if not passwd:
				passwd = config.get('pichler', 'pass')

		if not '.' in device:
			device += '.remote.lscontrol.dk'

		self.device = device
		self.client = nabto.Client(os.path.join(package_dir, '.home'))
		self.session = self.client.open_session(user, passwd)

		with open(os.path.join(package_dir, 'unabto_queries.xml'), 'r') as file:
		    rpc_xml = file.read()

		self.session.rpc_set_default_interface(rpc_xml)

	def rpc_invoke(self, command, params):
		"""
		Invoke RPC command to device
		
		Parameters and response data are defined in RPC interface file (`unabto_queries.xml` by default).

		Parameters
		----------
		command : str
			Command name
		params : str
			Request parameters (JSON)
		
		Returns
		-------
		dict
			Response from device
		"""
		r = self.session.rpc_invoke('nabto://%s/%s.json?%s' % (self.device, command, params))
		if r:
			return r['response']
		return []

	def ping(self):
		"""
		Ping device and return its reponse
		
		Returns
		-------
		dict
			Device's response to ping
		"""
		return self.rpc_invoke('ping', 'ping=1885957735')

	def datapoint_read_values(self, address, obj, length):
		"""
		Read raw values from one or more (neighboring) datapoints
		
		Parameters
		----------
		address : int
			Address to read from
		obj : int
			Object to read from
		length : int
			Number of subsequent datapoints to read
		
		Returns
		-------
		list
			List of raw values read from given address
		"""
		response = self.rpc_invoke('datapointReadValue', 'address=%d&obj=%d&length=%d' % (address, obj, length))
		if response:
			return [i['value'] for i in response['data']]
		return []

	def datapoint_read_value(self, address, obj=0):
		"""
		Read raw value from single datapoint
		
		Parameters
		----------
		address : int
			Address to read from
		obj : int, optional
			Object to read from, by default 0
		
		Returns
		-------
		int
			Raw value read from given address
		"""
		return self.datapoint_read_values(address, obj, 1)[0]

	def datapoint_read_list_values(self, lst):
		"""
		Read raw values from multiple datapoints
		
		Parameters
		----------
		lst : list
			List of (address, object) pairs of datapoints to read
		
		Returns
		-------
		list
			Raw values for each pair in original order
		"""
		l = [{'address': i[0], 'obj': i[1]} if type(i) is tuple else {'address': i, 'obj': 0} for i in lst]
		request = {'request': {'list': l}}
		response = self.rpc_invoke('datapointReadListValue', 'json=%s' % json.dumps(request))
		if response:
			return [i['value'] for i in response['data']]
		return []

	def setpoint_read_values(self, address, obj, length):
		"""
		Read raw values from one or more (neighboring) setpoints
		
		Parameters
		----------
		address : int
			Address to read from
		obj : int
			Object to read from
		length : int
			Number of subsequent setpoints to read
		
		Returns
		-------
		list
			List of raw values read from given address
		"""
		response = self.rpc_invoke('setpointReadValue', 'address=%d&obj=%d&length=%d' % (address, obj, length))
		if response:
			return [i['value'] for i in response['data']]
		return []

	def setpoint_read_value(self, address, obj=0):
		"""
		Read raw value from single setpoint
		
		Parameters
		----------
		address : int
			Address to read from
		obj : int, optional
			Object to read from, by default 0
		
		Returns
		-------
		int
			Raw value read from given address
		"""
		return self.setpoint_read_values(address, obj, 1)[0]

	def setpoint_read_list_values(self, lst):
		"""
		Read raw values from multiple setpoints
		
		Parameters
		----------
		lst : list
			List of (address, object) pairs of setpoints to read
		
		Returns
		-------
		list
			Raw values for each pair in original order
		"""
		l = [{'address': i[0], 'obj': i[1]} if type(i) is tuple else {'address': i, 'obj': 0} for i in lst]
		request = {'request': {'list': l}}
		response = self.rpc_invoke('setpointReadListValue', 'json=%s' % json.dumps(request))
		if response:
			return [i['value'] for i in response['data']]
		return []
