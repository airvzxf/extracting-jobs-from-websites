#!/usr/bin/python



# Python modules
import sys, os, re
import pycurl
import subprocess
import collections
import urllib
from shutil import copyfile
from datetime import date




# Personal modules
import html_ca




if __name__ == "__main__":


	print ''


	# Execute pwt to get current path
	p = subprocess.Popen("pwd", stdout=subprocess.PIPE, shell=True)
	(output, err_p) = p.communicate()



	# If get some error exit the program
	if err_p:
		print "Error execute pwd: ", err_p
		exit()



	if len(sys.argv) == 1:
		params_search_query = 'default'
		print 'Error: You need to send some parameter for example: python run.py iOS'
		exit()
	else:
		params_search_query = str(sys.argv[1]).lower()
		params_search_query_path = s = re.sub('[^0-9a-zA-Z]+', '', str(sys.argv[1]).decode('utf-8').lower())

	date_today = date.today()

	filw_web_ext = ".html"



	# Save current path
	path_main = '"' + output.strip() + '/"'

	path_main_web_pages = './web_pages'
	if not os.path.exists( path_main_web_pages ):
		os.makedirs( path_main_web_pages )

	if not os.path.isfile( path_main_web_pages + '/index.php' ):
		copyfile( 'index_template.php', path_main_web_pages + '/index.php' )


	path_main_web_pages = './web_pages/' + params_search_query_path
	if not os.path.exists( path_main_web_pages ):
		os.makedirs( path_main_web_pages )

	if not os.path.isfile( path_main_web_pages + '/index.php' ):
		copyfile( 'index_template.php', path_main_web_pages + '/index.php' )


	path_main_web_pages = './web_pages/' + params_search_query_path + '/' + date_today.strftime("%Y_%m_%d")
	if not os.path.exists( path_main_web_pages ):
		os.makedirs( path_main_web_pages )

	path_main_web_pages = './web_pages/' + params_search_query_path + '/' + date_today.strftime("%Y_%m_%d") + '/'

	if os.path.isfile( path_main_web_pages + 'index' + filw_web_ext ):
		print "Sorry, This search exit in: " + path_main_web_pages + 'index' + filw_web_ext
		exit()



	# Get Main Web Page and save in file

	url_http = 'https:'
	url = url_http + "//www.craigslist.org/about/sites#CA"

	file_web_main = path_main_web_pages + "web_page_main"

	print "Get web page: ", url
	print ""
	c = pycurl.Curl()
	c.setopt( c.URL, url)
	with open( file_web_main + filw_web_ext, 'w' ) as f:
		c.setopt( c.WRITEFUNCTION, f.write )
		c.perform()
	c.close()



	# Open file and search all .ca web pages


	# Search all href="****.ca"

	print "Get all links with .ca extension"
	print ""

	get_link_pattern = re.compile('href="(.*\.ca\/)"')

	f = open( file_web_main + filw_web_ext, 'r' )
	text_web_main = f.read()
	f.close()
	findall_web_main = re.findall( get_link_pattern, text_web_main )



	# Get states or subdomain in previous link

	print "Get all Web pages founded with search: " + params_search_query
	print ""

	#url_query = "search/jjj?lang=en&cc=us&query=software+develop"
	url_query = "search/jjj?query=" + urllib.quote_plus( params_search_query )

	get_states_pattern = re.compile('\/\/(.*?)\.')

	states_array = {}


	for states_link in findall_web_main:

		#~ url_states = url_http + states_link + url_query
		url_states = states_link + url_query

		state = re.search( get_states_pattern, states_link )

		file_web_main_state = file_web_main + '_' + state.group(1)

		states_array[state.group(1)] = file_web_main_state + filw_web_ext

		c = pycurl.Curl()
		c.setopt( c.URL, url_states)
		with open( file_web_main_state + filw_web_ext, 'w' ) as f:
			c.setopt( c.WRITEFUNCTION, f.write )
			c.perform()
		c.close()

	states_array = collections.OrderedDict(sorted(states_array.items()))



	# Create Results files

	print "Create Results files"
	print ""


	#~ CARRIS_REGEX = u'<a href="(\S+)" data-id="(\d+)" class="hdrlnk"><span id="titletextonly">([[\u0020-\u007E\u00A1-\u00FF]*?)<\/span><\/a>'
	CARRIS_REGEX = u'<a href="(\S+)" data-id="(\d+)" class="result-title hdrlnk">([[\u0020-\u007E\u00A1-\u00FF]*?)<\/a>'
	get_job_pattern = re.compile(CARRIS_REGEX, re.UNICODE)


	file_web_results = "index"
	f = open( path_main_web_pages + file_web_results + filw_web_ext, 'w' )

	f.write( html_ca.get_HtmlHead() )


	for k in states_array:

		f2 = open( states_array[k], 'r' )
		text_file = f2.read()
		f2.close()

		job_array = []
		for match in get_job_pattern.findall( text_file ):

			url_match = match[0]

			if not match[0].startswith("http"):
				if not match[0].startswith("//"):
					url_match = url_http + "//" + k + ".craigslist.ca" + str(match[0])
					job_array.append( [match[2], url_match] )


		job_count = len(job_array)

		state_url = url_http + "//" + k + ".craigslist.ca/" + url_query

		f.write( html_ca.get_HtmlState ( k, state_url, job_count ) )

		for l in job_array:
			f.write( html_ca.get_HtmlJob ( l[0], l[1] ) )

	f.write( html_ca.get_HtmlFooter() )

	f.close()

	print ""
