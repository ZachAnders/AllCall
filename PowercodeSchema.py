from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

def unravel_ip(ip):
	ip = recurse_ip(ip)
	return ".".join([str(octet) for octet in ip])
	
def recurse_ip(ip):
	if ip <= 0:
		return []
	return recurse_ip(ip>>8) + [ip&0xFF,]

class AccessPoint(Base):
	__tablename__ = "AccessPoint"

	EquipmentID = Column(Integer, primary_key=True)

	@staticmethod
	def get_all_equipment(session):
		ap_equipment = []
		for ap in session.query(AccessPoint):
			current_id = ap.EquipmentID
			current_equipment = session.query(Equipment).filter(Equipment.ID == current_id).all()
			if len(current_equipment) != 1:
				print("Retrieved more than one piece of equipment for id " + str(current_id) + ", this is unexpected behaviour!")
			ap_equipment += current_equipment	
		return ap_equipment

class Equipment(Base):
	__tablename__ = "Equipment"

	ID = Column(Integer, primary_key=True)
	Name = Column(String)
	MACAddress = Column(String)
	IPAddress = Column(Integer)
	DeviceType = Column(String)
	equipment_address = None
	network_location = None
	def decodedIPAddress(self):
		return unravel_ip(self.IPAddress)
	def populate(self, session):
		eq_ex = EquipmentEx.get_equipment_ex(session, self.ID)
		self.network_location = NetworkLocation.get_network_location(session, eq_ex.NetworkLocationID)
		self.equipment_address = Address.get_address(session, self.network_location.AddressID)

class EquipmentEx(Base):
	__tablename__ = "EquipmentEx"

	EquipmentID = Column(Integer, primary_key=True)
	NetworkLocationID = Column(Integer)
	
	@staticmethod
	def get_equipment_ex(session, eq_id):
		eq_exs = session.query(EquipmentEx).filter(EquipmentEx.EquipmentID == eq_id).all()
		if len(eq_exs) != 1:
			print("Retrieved more than one EquipEx for id " + str(eq_id) + ", this is unexpected behaviour!")
		return eq_exs[0]


class NetworkLocation(Base):
	__tablename__ = "NetworkLocation"
	NetworkLocationID = Column(Integer, primary_key=True)
	AddressID = Column(String)
	Name = Column(String)
	Notes = Column(String)
	TypeOfSite = Column(String)

	@staticmethod
	def get_network_location(session, network_location_id):
		net_locs = session.query(NetworkLocation).filter(NetworkLocation.NetworkLocationID == network_location_id).all()
		if len(net_locs) != 1:
			print("Retrieved more than one EquipEx for id " + str(network_location_id) + ", this is unexpected behaviour!")
		return net_locs[0]


class Address(Base):
	__tablename__ = "Address"
	AddressID = Column(Integer, primary_key=True)
	Address1 = Column(String)
	Address2 = Column(String)
	City = Column(String)
	State = Column(String)
	Zipcode = Column(String)
	Latitude = Column(Float)
	Longitude = Column(Float)

	@staticmethod
	def get_address(session, addr_id):
		addrs = session.query(Address).filter(Address.AddressID == addr_id).all()
		if len(addrs) != 1:
			print("Retrieved more than one address for id " + str(addr_id) + ", this is unexpected behaviour!")
		return addrs[0]

