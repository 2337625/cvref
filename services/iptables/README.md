Iptables
========

Mostly repalced by nftables and firewalld, but anyway, this sample is just a basic fw configuration. Yes it's bit nasty as it doesn't like you to communicate with the internet and drops everything
except the incoming connections to opened ports. Why? Because you don't trust internet at all. On server you usally need to communicate only with your repo servers, yes backups make sense too.

Simple sample, quite old one as well.
