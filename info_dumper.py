# -*- coding: utf-8 -*-
import sys
from os import listdir
from os.path import isdir, isfile, join, splitext, basename
import pefile
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, create_engine, func
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json


Base = declarative_base()
engine = create_engine('sqlite:///db_test.db')


class Test(Base):
	__tablename__ = 'tests'
	id = Column(Integer, primary_key=True)
	datetime = Column(DateTime)
	testfile = relationship('TestFile')


class TestFile(Base):
	__tablename__ = 'testfiles'
	test_id = Column(Integer, ForeignKey('tests.id'))
	filename = Column(String(100))
	extension = Column(String(4))
	filepath = Column(String)
	result = Column(String(7))
	dump_result = Column(String)
	id = Column(Integer, primary_key=True)

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

pe_extensions = (".acm", ".ax", ".cpl", ".dll", ".drv", ".efi", ".exe",
				".mui", ".ocx", ".scr", ".sys", ".tsp")

try:
	pe_dir = sys.argv[1]
except IndexError:
	print("Please specify path. For example: python info_dumper.py c:\\users")
	sys.exit()

if not isdir(pe_dir):
	print("Directory doesn't exist.")
	sys.exit()


only_files = [f for f in listdir(pe_dir) if isfile(join(pe_dir, f))]

new_test = Test(datetime=func.now())
session.add(new_test)
session.commit()

def printo(text):
	print(text)

report = {"Test ": new_test.id, "File": {}}

for f in only_files:

	filename, file_extension = splitext(join(pe_dir, f))
	filename = basename(filename)

	if file_extension in pe_extensions:
		text = ""
		bool_dump_res = ""
		try:
			pe = pefile.PE(join(pe_dir, f))
			text = pe.dump_info()
			bool_dump_res = "Success"
		except pefile.PEFormatError as err:
			pass
			text = str(err)
			bool_dump_res = "Fail"

		new_testfile = TestFile(filename=filename, 
								extension=file_extension, filepath=join(pe_dir, f), 
								result=bool_dump_res, dump_result=text, test_id=new_test.id)
		session.add(new_testfile)
		session.commit()

		report["File"][f] = {'Path': join(pe_dir, f), 'Result': bool_dump_res}
		print('Result: ' + bool_dump_res + ' for ' + join(pe_dir, f))

with open('Report test ' + str(new_test.id) + '.txt', 'a') as outfile:
	json.dump(report, outfile)
outfile.close()