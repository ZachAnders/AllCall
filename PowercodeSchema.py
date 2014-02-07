from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class AccessPoint(Base):
	__tablename__ = "AccessPoint"

	EquipmentID = Column(Integer, ForeignKey("Equipment.ID"), primary_key=True)
	equipment = relationship("Equipment", foreign_keys='AccessPoint.EquipmentID')

class Equipment(Base):
	__tablename__ = "Equipment"

	ID = Column(Integer, primary_key=True)
	Name = Column(String)
	MACAddress = Column(String)
	IPAddress = Column(Integer)
	DeviceType = Column(String)
	equipment_ex = relationship("EquipmentEx", uselist=False, backref="Equipment")

	def decodedIPAddress(self):
		return ".".join([str((self.IPAddress >> ((3-i)*8))&0xFF) for i in range(4)])

class EquipmentEx(Base):
	__tablename__ = "EquipmentEx"

	EquipmentID = Column(Integer, ForeignKey('Equipment.ID'), primary_key=True)
	NetworkLocationID = Column(Integer, ForeignKey('NetworkLocation.NetworkLocationID'))
	network_location = relationship("NetworkLocation", foreign_keys='EquipmentEx.NetworkLocationID')

class NetworkLocation(Base):
	__tablename__ = "NetworkLocation"
	NetworkLocationID = Column(Integer, primary_key=True)
	AddressID = Column(Integer, ForeignKey("Address.AddressID"))
	Name = Column(String)
	Notes = Column(String)
	TypeOfSite = Column(String)
	address = relationship("Address", foreign_keys='NetworkLocation.AddressID')

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
