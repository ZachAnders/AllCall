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
	EndUserID = Column(Integer, ForeignKey('Customer.CustomerID'))
	equipment_ex = relationship("EquipmentEx", uselist=False, backref="Equipment")
	children = relationship("EquipmentParent", foreign_keys="EquipmentParent.ParentID")
	end_user = relationship("Customer", uselist=False, foreign_keys="Equipment.EndUserID")

	def decodedIPAddress(self):
		return ".".join([str((self.IPAddress >> ((3-i)*8))&0xFF) for i in range(4)])

	def __repr__(self):
		return "{ID: %s Name: %s MAC: %s IP: %s DevType: %s}" % (repr(self.ID), repr(self.Name),\
				repr(self.MACAddress), repr(self.IPAddress), repr(self.DeviceType))
	
	def get_children(self):
		return [child.child for child in self.children]

	def get_enduser(self):
		return 

class EquipmentEx(Base):
	__tablename__ = "EquipmentEx"

	EquipmentID = Column(Integer, ForeignKey('Equipment.ID'), primary_key=True)
	NetworkLocationID = Column(Integer, ForeignKey('NetworkLocation.NetworkLocationID'))
	network_location = relationship("NetworkLocation", foreign_keys='EquipmentEx.NetworkLocationID')

class EquipmentParent(Base):
	__tablename__ = "EquipmentParent"
	
	EquipmentID = Column(Integer, ForeignKey('Equipment.ID'), primary_key=True)
	ParentID = Column(Integer, ForeignKey('Equipment.ID'))

	parent = relationship("Equipment", foreign_keys='EquipmentParent.ParentID')
	child = relationship("Equipment", foreign_keys='EquipmentParent.EquipmentID')

	def __repr__(self):
		return "{Parent: %s, Child: %s}" % (repr(self.parent), repr(self.child))

class NetworkLocation(Base):
	__tablename__ = "NetworkLocation"
	NetworkLocationID = Column(Integer, primary_key=True)
	AddressID = Column(Integer, ForeignKey("Address.AddressID"))
	Name = Column(String)
	Notes = Column(String)
	TypeOfSite = Column(String)
	address = relationship("Address", foreign_keys='NetworkLocation.AddressID')

class Customer(Base):
	__tablename__ = "Customer"
	CustomerID = Column(Integer, primary_key=True)
	FirstName = Column(String)
	LastName = Column(String)
	CompanyName = Column(String)

	phone_numbers = relationship("Phone", foreign_keys="Phone.CustomerID")
	_first_number = None

	def get_first_number(self, default_type="Home"):
		if not self._first_number and len(self.phone_numbers) > 0:
			# Default to the first number
			self._first_number = self.phone_numbers[0]
			# Check for other more preferable numbers
			for num in self.phone_numbers:
				if num.Type == default_type:
					self._first_number = num
		return self._first_number

	def __repr__(self):
		return "{CustomerID: %d, FirstName: %s, LastName: %s, Company: %s}" % (self.CustomerID, self.FirstName, self.LastName, self.CompanyName)
	
class Phone(Base):
	__tablename__ = "Phone"
	ID = Column(Integer, primary_key=True)
	CustomerID = Column(Integer, ForeignKey("Customer.CustomerID"))
	Number = Column(String)
	Type = Column(String)

	def __repr__(self):
		return "{PhoneID: %d, CustomerID: %d, Number: %s, Type: %s}" % (self.ID, self.CustomerID, self.Number, self.Type)

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
