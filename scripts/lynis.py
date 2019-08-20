#!/usr/bin/env python3

def lynis_report():
	"""
	Simple security report with Lynis - PoC sample test

	Poor man's basic security report using Lynis

	Function should be shoved into Fabric i.e.
	
	Run report on remote system and copy the output to local system, no more magic. Requries sudo to perform this task,
	always delete security report on server as it's very sensitive information.
	
	"""

	sudo_run('apt install lynis kbtin')
	sudo_run('lynis audit system --auditor="Poor Auditor" | ansi2html -la > /tmp/secreport.html')
	get('/tmp/secreport.html', 'secreport.html')
	sudo_run('rm /tmp/secreport.html')
	sudo_run('apt remove lynis kbtin')
	sudo_run('dpkg --purge lynis')
