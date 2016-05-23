from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, create_engine, func
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///db_test.db')


class Test(Base):
	__tablename__ = 'tests'
	id = Column(Integer, primary_key=True)
	testfile = relationship('TestFile')


class TestFile(Base):
	__tablename__ = 'testfiles'
	test_id = Column(Integer, ForeignKey('tests.id'))
	datetime = Column(DateTime, )
	filename = Column(String(100))
	extension = Column(String(4))
	filepath = Column(String)
	result = Column(String(7))
	dump_result = Column(String)
	id = Column(Integer, primary_key=True)

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

new_test = Test()
session.add(new_test)
session.commit()

dump_res = "Success"

new_testfile = TestFile(datetime=func.now(), filename='sdf', extension='exe', filepath='C:\\games\\', 
						result=dump_res, dump_result="sometext", test_id=new_test.id)
session.add(new_testfile)
session.commit()

print(new_testfile.id)


#if __name__ == "__main__":
	