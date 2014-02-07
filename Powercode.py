import sqlalchemy
from PowercodeSchema import AccessPoint, Equipment, EquipmentEx

class DbSession():
	def __init__(self):
		self.eng = sqlalchemy.create_engine("mysql://root:usemysql@localhost/powernoc")
		self.session_maker = sqlalchemy.orm.sessionmaker(bind=self.eng)
		self.current_session = self.session_maker()
	def get_session(self):
		return self.current_session

#
class AccessPoint():
	def __init__(self):
		pass

if __name__ == "__main__":
	print "Testing"
	import sqlalchemy

