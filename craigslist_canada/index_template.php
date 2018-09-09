<?php

	$dirs = array_filter(glob('*'), 'is_dir');
	
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
		</style>
	</head>

	<body>
		<h1 align="center">Hacking Employes in craigslist.org</h1>
		<br>
		<h3>
			<a href="../" target="_self">Back</a><br>
			<br>
			<br>
			Select the folder, click the link below:
		</h3>
<?php foreach ($dirs AS $dir){ ?>
			<h3>
				<a href="<?php echo $dir; ?>" target="_self"><?php echo $dir; ?></a>
			</h3>
<?php } ?>
	</body>

</html>
