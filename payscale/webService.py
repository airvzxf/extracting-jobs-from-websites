#!/home4/rovisof1/python/bin/python2.7
# -*- coding: utf-8 -*-
#/usr/bin/python
print "Content-type: application/json; charset=utf-8"
#~ print "Content-Encoding: none"
print

#-- python __init__.py Software Engineer, iOS Developer



#-- Python modules

import os
import sys
import ast
import re
import socket
import pycurl
import json
import cgi

from collections import defaultdict

from io import BytesIO

from datetime import datetime, timedelta
from time import gmtime, strftime
from pytz import timezone

import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

#-- DEBUG: This option show system errors in web pages.
import traceback
sys.stderr = sys.stdout







def getDataFromURL(urlStr):
	mainWebPage = BytesIO()

	c = pycurl.Curl()
	c.setopt( pycurl.FOLLOWLOCATION, True )
	c.setopt(pycurl.MAXREDIRS, 1)
	c.setopt( pycurl.URL, urlStr )
	c.setopt( pycurl.USERAGENT, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36' )
	c.setopt( pycurl.ENCODING, "gzip,deflate" )
	c.setopt(c.WRITEFUNCTION, mainWebPage.write)

	try:
		c.perform()
	except pycurl.error, error:
		#-- Comment: More than one redirect.
		if error[0] == 47:
			return False
		else:
			print 'error: ', error
			exit()
	finally:
		c.close()

	return mainWebPage.getvalue()







def convertJsonToDataTables(dataJobs):
	recordsTotal = 0
	jsonResponse = {
		'draw': 1,
		'recordsTotal': 0,
		'recordsFiltered': 0,
		'data': []
	}


	for country in dataJobs:
		#~ print 'country: ', country
		#~ print '\n'

		for word in dataJobs[country]:
			#~ print 'word: ', word
			#~ print 'dataJobs: ', dataJobs[word][country]

			job = dataJobs[country][word]

			jobUrl = None
			if job['jobUrl'] != '':
				jobUrl = '<a href="'+job['jobUrl']+'" target="_blank">PayScale</a>'

			exchangeRateURL = None
			if job['exchangeRateURL'] != '':
				exchangeRateURL = '<a href="'+job['exchangeRateURL']+'" target="_blank">Google finances</a>'

			jobArray = []
			jobArray.append(job['countryName'] + ' (' + job['countryAbbr'] + ')')
			jobArray.append(word)
			jobArray.append(jobUrl)
			jobArray.append(locale.currency( (job['salaryToUSD']['median'] / 12), grouping=True) )
			jobArray.append(locale.currency( job['salaryToUSD']['median'], grouping=True) )
			jobArray.append(locale.currency( job['salaryToUSD']['salaryMin'], grouping=True) )
			jobArray.append(locale.currency( job['salaryToUSD']['salaryMax'], grouping=True) )
			jobArray.append(locale.currency( job['salaryToUSD']['totalPayMin'], grouping=True) )
			jobArray.append(locale.currency( job['salaryToUSD']['totalPayMax'], grouping=True) )
			jobArray.append(job['salaryToUSD']['exchangeRate'])
			jobArray.append(exchangeRateURL)
			jobArray.append(job['salary']['currency'])
			jobArray.append(locale.currency( (job['salary']['median'] / 12), grouping=True) )
			jobArray.append(locale.currency( job['salary']['median'], grouping=True) )
			jobArray.append(locale.currency( job['salary']['salaryMin'], grouping=True) )
			jobArray.append(locale.currency( job['salary']['salaryMax'], grouping=True) )
			jobArray.append(locale.currency( job['salary']['totalPayMin'], grouping=True) )
			jobArray.append(locale.currency( job['salary']['totalPayMax'], grouping=True) )

			#~ jsonResponse['recordsFiltered']['data'] += jobArray
			jsonResponse['data'].append(jobArray)

			#~ jsonResponse['recordsTotal'] = jobArray
			recordsTotal += 1
			#~ print '\n'
		#~ print '\n\n'
	#~ print '\n'

	jsonResponse['recordsTotal'] = recordsTotal
	jsonResponse['recordsFiltered'] = recordsTotal

	#~ r = {'is_claimed': 'True', 'rating': 3.5}
	#~ r = json.dumps(r)
	#~ loaded_r = json.loads(r)
	#~ print '\n'

	#~ print 'jsonResponse: ', jsonResponse
	#~ print '\n\n'
	#~ print 'jsonResponse: ', json.dumps(jsonResponse)

	return json.dumps(jsonResponse)







if __name__ == '__main__':
	#~ print '\n\n'
	#~ print 'PAYSCALE :: GET SALARY RATE'
	#~ print '--------------------------------------------------------'


	urlStr = 'http://www.payscale.com/rccountries.aspx'
	#~ dirPath = os.path.dirname( os.path.abspath( __file__ ) )

	argsCgi = cgi.FieldStorage()

	if argsCgi.has_key('jobsWords'):
		searchingWordsJob = argsCgi.getvalue('jobsWords')

		if searchingWordsJob.find('@') >= 0 :
			searchingWordsJob = searchingWordsJob.split('@')
			searchingWordsJob = filter(None, searchingWordsJob)
		else:
			searchingWordsJob = [searchingWordsJob]
	elif len(sys.argv) > 1:
		searchingWordsJob = sys.argv[1:]
	else:
		print 'Error: You need to send some parameter.'
		print 'Console example: python webService.py "iOS Developer" "Senior Software Architect"'
		print 'Web example: https://project.rovisoft.net/hck/payscale/webService.py?jobsWords=iOS Developer;Senior Software Architect'
		exit()

	#~ print 'searchingWordsJob: ', searchingWordsJob
	searchingWordsJob = [w.strip().lower().replace(' ', '_') for w in searchingWordsJob]
	#~ print 'searchingWordsJob: ', searchingWordsJob

	#~ print '{"draw": 1,"recordsTotal": 57,"recordsFiltered": 57,"data": [["Airi","Satou","$1","$2","$3","$4","$5","MXN","$6","$7","$8","$9","$10","$11"]]}'
	#~ exit()







	#~ print ""
	#~ print ""
	#~ print "Get countries in web page: ", urlStr
	#~ print ""

	webPageContentSting = getDataFromURL(urlStr)
	countryInfoPattern = re.compile( '<div.*title=".* flag"></div><a href="/research/(.*)/Country=.*".*>(.*)</a>' )
	countriesList = re.findall( countryInfoPattern, webPageContentSting )
	#~ print 'countriesList: ', countriesList

	#~ countriesList = [('US', 'United States')]
	#~ print 'countriesList: ', countriesList

	#~ exit()







	#~ print ""
	#~ print ""
	#~ print ""
	#~ print " Get salary per country and word."
	#~ print ""

	resultWordsAndCountries = {}
	countWebPages = 0

	for countryAbbr, countryName in countriesList:
		resultWordsAndCountries[countryAbbr] = {}
		#~ if countWebPages == 6:
			#~ break
			#~ exit()

		for word in searchingWordsJob:
			#-- TODO: Create multi threading to get the web page info and exchange currency.
			urlStr = 'http://www.payscale.com/research/'+countryAbbr+'/Job='+word+'/Salary'
			#~ print 'urlStr: ', urlStr


			salaryDictionary = {
				'currency':None,
				'median':0,
				'salaryMin':0,
				'salaryMax':0,
				'totalPayMin':0,
				'totalPayMax':0
			}
			salaryToUSDDictionary = {
				'currency':'USD',
				'exchangeRate':'1',
				'median':0,
				'salaryMin':0,
				'salaryMax':0,
				'totalPayMin':0,
				'totalPayMax':0
			}


			webPageContentSting = getDataFromURL(urlStr)

			if False == webPageContentSting:
				#~ print 'This country has any job.'
				#~ print '\n'
				continue


			isYearlyPattern = re.compile( '<div class="yearly">' )
			isYearlyString = re.findall( isYearlyPattern, webPageContentSting )
			if not isYearlyString:
				#~ print 'This country has any salary per year.'
				#~ print '\n'
				continue


			resultWordsAndCountries[countryAbbr][word] = {
				'countryAbbr':countryAbbr,
				'countryName':countryName,
				'jobUrl':urlStr,
				'salary':salaryDictionary,
				'salaryToUSD':salaryToUSDDictionary,
				'exchangeRateURL':''
			}

			countWebPages += 1
			#~ print 'countWebPages: ', countWebPages
			#~ if countWebPages == 6:
				#~ break
				#~ exit()


			try:
				currencyPattern = re.compile( 'Currency: (\w{3})' )
				currencyString = re.findall( currencyPattern, webPageContentSting )[0]
			except IndexError:
				try:
					currencyPattern = re.compile( 'MEDIAN:&nbsp;\s*(\w{3})' )
					currencyString = re.findall( currencyPattern, webPageContentSting )[0]
				except IndexError:
					try:
						currencyPattern = re.compile( 'MEDIAN:&nbsp;\s*(&euro;)' )
						currencyString = re.findall( currencyPattern, webPageContentSting )[0]
						currencyString = 'EUR'
					except IndexError:
						try:
							currencyPattern = re.compile( 'MEDIAN:&nbsp;\s*(Rp)' )
							currencyString = re.findall( currencyPattern, webPageContentSting )[0]
							currencyString = 'IDR'
						except IndexError:
							if countryAbbr == 'PE':
								currencyString = 'PEN'
							elif countryAbbr == 'VN':
								currencyString = 'USD'
							else:
								#~ print 'Warning: something is wrong when it gets the currencyString.'
								#~ print '\n'
								continue
			#~ print 'currencyString: ', currencyString

			try:
				#~ medianPattern = re.compile( 'MEDIAN:&nbsp;\D*(\d+(?:[\.\,]\d*)?)' )
				medianPattern = re.compile( 'MEDIAN:&nbsp;\D*(\d{1,3}[,\d{3}]*[.\d]*)?' )
				medianFloat = locale.atof(re.findall( medianPattern, webPageContentSting )[0])
			except IndexError:
				#~ print 'Warning: something is wrong when it gets the medianFloat.'
				medianFloat = 0.0
			#~ print "medianFloat: ", medianFloat

			try:
				#~ salaryPattern = re.compile( '<strong>Salary</strong>.*vm">\D*(\d+(?:[\.\,]\d*)?) - \D*(\d+(?:[\.\,]\d*)?)</td>' )
				salaryPattern = re.compile( '<strong>Salary</strong>.*vm">\D*(\d{1,3}[,\d{3}]*[.\d]*)? - \D*(\d{1,3}[,\d{3}]*[.\d]*)?</td>' )
				salaryList = re.findall( salaryPattern, webPageContentSting )[0]
				salaryMinFloat = locale.atof(salaryList[0])
				salaryMaxFloat = locale.atof(salaryList[1])
				#~ print "salaryList: ", salaryList
			except IndexError:
				try:
					salaryPattern = re.compile( 'class="payRange".*\D*(\d{1,3}[,\d{3}]*[.\d]*)? - \D*(\d{1,3}[,\d{3}]*[.\d]*)?\s*</div>' )
					salaryList = re.findall( salaryPattern, webPageContentSting )[0]
					salaryMinFloat = locale.atof(salaryList[0])
					salaryMaxFloat = locale.atof(salaryList[1])
					#~ print "salaryList: ", salaryList
				except IndexError:
					#~ print 'Warning: something is wrong when it gets the salaryList.'
					salaryMinFloat = 0.0
					salaryMaxFloat = 0.0

			try:
				#~ totalPayPattern = re.compile( '<strong>Total Pay.*vm">\D*(\d+(?:[\.\,]\d*)?) - \D*(\d+(?:[\.\,]\d*)?)</td>' )
				totalPayPattern = re.compile( '<strong>Total Pay.*vm">\D*(\d{1,3}[,\d{3}]*[.\d]*)? - \D*(\d{1,3}[,\d{3}]*[.\d]*)?</td>' )
				totalPayList = re.findall( totalPayPattern, webPageContentSting )[0]
				totalPayMinFloat = locale.atof(totalPayList[0])
				totalPayMaxFloat = locale.atof(totalPayList[1])
				#~ print "totalPayList: ", totalPayList
			except IndexError:
				try:
					totalPayPattern = re.compile( 'class="payRange".*\D*(\d{1,3}[,\d{3}]*[.\d]*)? - \D*(\d{1,3}[,\d{3}]*[.\d]*)?\s*</div>' )
					totalPayList = re.findall( totalPayPattern, webPageContentSting )[0]
					totalPayMinFloat = locale.atof(totalPayList[0])
					totalPayMaxFloat = locale.atof(totalPayList[1])
					#~ print "totalPayList: ", totalPayList
				except IndexError:
					#~ print 'Warning: something is wrong when it gets the totalPayList.'
					totalPayMinFloat = 0.0
					totalPayMaxFloat = 0.0

			salaryDictionary['currency'] = currencyString
			salaryDictionary['median'] = medianFloat
			salaryDictionary['salaryMin'] = salaryMinFloat
			salaryDictionary['salaryMax'] = salaryMaxFloat
			salaryDictionary['totalPayMin'] = totalPayMinFloat
			salaryDictionary['totalPayMax'] = totalPayMaxFloat

			if currencyString == 'USD':
				salaryToUSDDictionary['median'] = medianFloat
				salaryToUSDDictionary['salaryMin'] = salaryMinFloat
				salaryToUSDDictionary['salaryMax'] = salaryMaxFloat
				salaryToUSDDictionary['totalPayMin'] = totalPayMinFloat
				salaryToUSDDictionary['totalPayMax'] = totalPayMaxFloat

				resultWordsAndCountries[countryAbbr][word]['salary'] = salaryDictionary
				resultWordsAndCountries[countryAbbr][word]['salaryToUSD'] = salaryToUSDDictionary

				#~ print '\n'
				continue


			#-- Comment: Another option https://www.google.com/search?q=convert+43171540+cop+to+usd
			urlUSDStr = 'https://www.google.com/finance/converter?a=1&from='+currencyString+'&to=USD'
			webPageContentSting = getDataFromURL(urlUSDStr)
			#~ print 'urlUSDStr: ', urlUSDStr

			#~ exchangeRateUSDPattern = re.compile( '<span class=bld>\D*(\d+(?:[\.\,]\d*)?) USD</span>' )
			exchangeRateUSDPattern = re.compile( '<span class=bld>\D*(\d{1,3}[,\d{3}]*[.\d]*)? USD</span>' )
			exchangeRateUSDFloat = locale.atof(re.findall( exchangeRateUSDPattern, webPageContentSting )[0])
			#~ print "exchangeRateUSDFloat: ", exchangeRateUSDFloat

			medianUSDFloat = round((exchangeRateUSDFloat*medianFloat), 2)
			salaryMinUSDFloat = round((exchangeRateUSDFloat*salaryMinFloat), 2)
			salaryMaxUSDFloat = round((exchangeRateUSDFloat*salaryMaxFloat), 2)
			totalPayMinUSDFloat = round((exchangeRateUSDFloat*totalPayMinFloat), 2)
			totalPayMaxUSDFloat = round((exchangeRateUSDFloat*totalPayMaxFloat), 2)

			#~ print "medianUSDFloat:       ", medianUSDFloat
			#~ print "salaryMinUSDFloat:    ", salaryMinUSDFloat
			#~ print "salaryMaxUSDFloat:    ", salaryMaxUSDFloat
			#~ print "totalPayMinUSDFloat:  ", totalPayMinUSDFloat
			#~ print "totalPayMaxUSDFloat:  ", totalPayMaxUSDFloat

			salaryToUSDDictionary['median'] = medianUSDFloat
			salaryToUSDDictionary['exchangeRate'] = exchangeRateUSDFloat
			salaryToUSDDictionary['salaryMin'] = salaryMinUSDFloat
			salaryToUSDDictionary['salaryMax'] = salaryMaxUSDFloat
			salaryToUSDDictionary['totalPayMin'] = totalPayMinUSDFloat
			salaryToUSDDictionary['totalPayMax'] = totalPayMaxUSDFloat

			resultWordsAndCountries[countryAbbr][word]['salary'] = salaryDictionary
			resultWordsAndCountries[countryAbbr][word]['salaryToUSD'] = salaryToUSDDictionary
			resultWordsAndCountries[countryAbbr][word]['exchangeRateURL'] = urlUSDStr

			#~ print '\n'
		#~ break


	#~ print 'resultWordsAndCountries: ', resultWordsAndCountries
	#~ print 'countWebPages: ', countWebPages







	#~ print ""
	#~ print ""
	#~ print "Convert data to JSON"
	#~ print ""

	jsonResponse = convertJsonToDataTables(resultWordsAndCountries)
	print jsonResponse







	#~ print ""
	#~ print ""
	#~ print ""
	#~ print "--------------------------------------------------------"
	#~ print "PAYSCALE :: JUST FINISHED"
	#~ print '\n\n\n'






