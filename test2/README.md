-- if N >= 1000, check your ulimit settings in the following commands:
	ulimit -n
	ulimit -s
	cat /etc/security/limits.conf
	sysctl -n fs.nr_open
