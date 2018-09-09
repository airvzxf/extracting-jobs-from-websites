#!/usr/bin/python

import datetime



# Get HTML Header

def get_HtmlHead ():
	d = datetime.date.today()
	t = datetime.datetime.now().time()

	html = """<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1">
		<title>Hacking Employes in craigslist.org</title>
		<style>
			body
			{
				word-break: break-word;
			}
			small
			{
				font-size: medium;
			}
		</style>
	</head>
	<body>
		<h1 align="center">Hacking Employes in craigslist.org</h1>
		<h2 align="center">%s</h2>
		<h2 align="center">%s</h2>
""" % ( d.strftime("%A, %d %B %Y"), t.strftime("%H:%M:%S.%f") )
	return html


# Get HTML Footer

def get_HtmlFooter ():
	html = """
	</body>
</html>
"""
	return html



# Get HTML State

def get_HtmlState ( name, url, total ):
	html = """
		<br>
		<br>
		<br>
		<h2>
			=== %s (%s) ===<br>
			<small><a href="%s" target="_blank">%s</a></small>
		</h2>
		<hr align="left" width="300">
""" % ( name.upper(), total, url, url )
	return html



# Get HTML Job

def get_HtmlJob ( name, link ):
	html = """
		<h3>
			%s<br>
			<small>
				<a href="%s" target="_blank">%s</a>
			</small>
		</h3>
""" % ( name, link, link )
	return html
