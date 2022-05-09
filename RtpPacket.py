import sys
from time import time
HEADER_SIZE = 12

class RtpPacket:	
	header = bytearray(HEADER_SIZE)
	
	def __init__(self):
		pass
		
	def encode(self, version, padding, extension, cc, seqnum, marker, pt, ssrc, payload):
		"""Encode the RTP packet with header fields and payload."""
		timestamp = int(time())
		header = bytearray(HEADER_SIZE)

		# Fill the header bytearray with RTP header fields
		# We used https://www.geeksforgeeks.org/real-time-transport-protocol-rtp/
		# to figure out the proper lengths for each field in tandem with 
		# page six of the assignment sheet
		
		#byte 1: version, padding, extension, cc
		header[0] = (version << 6 | padding << 5 | extension << 4 | cc)
		
		#byte 2: marker, payload type
		header[1] = (marker << 7 | pt)
		
		#byte 3: sequence number (1)
		header[2] = seqnum >> 8
		#byte 4: sequence number (2)
		header[3] =  seqnum
		
		# Bitwise AND used below to filter out unwanted leading 1's

		# byte 5: timestamp (1)
		header[4] =  timestamp >> 24
		# byte 6: timestamp (2)
		header[5] =  (timestamp >> 16) & 0b11111111
		# byte 7: timestamp (3)
		header[6] =  (timestamp >> 8) & 0b11111111
		# byte 8: timestamp (4)
		header[7] =  timestamp & 0b11111111
		
		# byte 9: ssrc (1)
		header[8] =  ssrc >> 24
		# byte 10: ssrc (2)
		header[9] =  (ssrc >> 16) & 0b11111111
		# byte 11: ssrc (3)
		header[10] =  (ssrc >> 8) & 0b11111111
		# byte 12: ssrc (4)
		header[11] = ssrc & 0b11111111

		# Get the payload from the argument
		self.payload = payload
		
		self.header = header
		
	def decode(self, byteStream):
		"""Decode the RTP packet."""
		self.header = bytearray(byteStream[:HEADER_SIZE])
		self.payload = byteStream[HEADER_SIZE:]
	
	def version(self):
		"""Return RTP version."""
		return int(self.header[0] >> 6)
	
	def seqNum(self):
		"""Return sequence (frame) number."""
		seqNum = self.header[2] << 8 | self.header[3]
		return int(seqNum)
	
	def timestamp(self):
		"""Return timestamp."""
		timestamp = self.header[4] << 24 | self.header[5] << 16 | self.header[6] << 8 | self.header[7]
		return int(timestamp)
	
	def payloadType(self):
		"""Return payload type."""
		pt = self.header[1] & 127
		return int(pt)
	
	def getPayload(self):
		"""Return payload."""
		return self.payload
		
	def getPacket(self):
		"""Return RTP packet."""
		return self.header + self.payload