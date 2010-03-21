#!/usr/bin/python

# args are: uid, local_part

import sys, os, tempfile, email, commands

import logging
LOG_FILENAME = '/tmp/mail2.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

DEBUG = True

if __name__ == '__main__':
	if sys.argv[2] == "" :
		print "usage: ", sys.argv[0], " uid local_part"
		exit(1)
	uid = sys.argv[1]
	local_part = sys.argv[2]
	home = os.path.expanduser('~' + uid)
	logging.debug("home: " + home)
	wd = os.path.join(home, '.mail2')
	logging.debug("started: " + uid + " " + local_part + " " + wd)
	if not os.path.exists(wd) : os.mkdir(wd)
	tmpd = os.path.join(wd, 'tmp')
	if not os.path.exists(tmpd) : os.mkdir(tmpd)
	(tmpfd, tmpname) = tempfile.mkstemp(dir=tmpd, prefix="spool_")
	tmpf = os.fdopen(tmpfd, "r+w", 4096)
	logging.debug("spool name: " + tmpname)
	while True :
		buf = sys.stdin.read(4096)
		if buf == "": break
		tmpf.write(buf)
	tmpf.seek(0)
	msg = email.message_from_file(tmpf)
	logging.debug(msg.get("to"))
	logging.debug(msg.get("subject"))
	# change later to popen or similar to spool modified data
	cmd = "/usr/bin/maildrop -d " + uid + " mail2 " + local_part + " <" + tmpname
	(status, retm) = commands.getstatusoutput(cmd)
	logging.debug("exec:" + cmd + ": " + str(status) + retm)
	tmpf.close
	os.remove(tmpname)
