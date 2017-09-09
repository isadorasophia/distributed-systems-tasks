-- if N >= 1000, check your ulimit settings in the following commands:
	ulimit -n
	cat /etc/security/limits.conf
	sysctl -n fs.nr_open
