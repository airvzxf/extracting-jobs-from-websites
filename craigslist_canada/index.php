<?php

$output = null;


if ( isset($_GET['processing']) && $_GET['processing'] == 'true' )
{
	$searching = '';

	if ( isset($_GET['searching']) && trim($_GET['searching']) != '' ) $searching = ' "' . trim(str_replace('"', '', $_GET['searching'])) . '"';

	shell_exec('chmod +x ./run.py');

	$output = shell_exec('./run.py' . $searching);
}

$searching = 'Software Develop';
if ( isset($_GET['searching']) ) $searching = $_GET['searching'];

?><!DOCTYPE html>
<html>

	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1">
		<title>Hacking Employes in craigslist.org</title>
		<style>
			body
			{
				word-wrap: break-word;
			}
			pre
			{
				word-wrap: break-word;
			}
		</style>
	</head>

	<body>
		<h1 align="center">Hacking Employes in craigslist.org</h1>
		<h2 align="center"><?php echo date("l, d F Y"); ?></h2>
		<h2 align="center"><?php echo date("H:i:s.u"); ?></h2>
		<br>
		<br>
		<form action="./" method="GET">
			<input type="hidden" name="processing" value="true">
			<label for="searching">searching:</label> <input type="text" id="searching" name="searching" value="<?php echo $searching; ?>" autofocus ><br>
			<br>
			<input type="submit">
		</form>
		<br>
		<br>
		<a href="./web_pages/" target="_self">See the results</a><br>
		<pre><?php echo $output; ?></pre>
	</body>

</html>
