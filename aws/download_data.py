import sys
import os
import urllib  
import urllib2  
import webbrowser

from mechanize import ParseResponse, urlopen, urljoin, Browser

url = 'https://archive.nrao.edu/archive/advquery.jsp'


def download_with_mech(email, destination, file):
	'''
	download data from nrao archive. Now it only works for filling the form. It cannot 
	submit by clicking "Get my data" buttom
	'''
	br = Browser()
	br.set_handle_robots(False) # ignore robots
	br.open(url)
	br.select_form(nr=0)
	br["PROJECT_CODE"] = "14A-425"
	submit_response = br.submit(name = "SUBMIT", label = "Submit Query")
	content = submit_response.read()
	#print br.read()

	'''redirect to the download page'''
	br.select_form(name = "Form1")
	br["EMAILADDR"] = "jtan0325@berkeley.edu" #replace by email
	br["COPYFILEROOT"] = "/lustre/aoc/projects/fasttransients/moving" #replace by destination
	br["CONVERT2FORMAT"] = ["SDM"]
	achive_files = br.form.find_control(name = "FTPCHECKED")

	for v in range(0, len(achive_files.items)):
		# file name should be replaced by FILE
	    if "14A-425_sb29260830_1_000.56825.290659375" in str(achive_files.items[v]):
	        achive_files.items[v].selected = True
	        break
	print str(br.read())
	#submit_response = br.submit(name = "DOWNLOADFTPCHK")
	#submit_content = submit_response.read()
	#print submit_response

