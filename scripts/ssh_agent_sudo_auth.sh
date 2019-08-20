#!/bin/sh

# On Debian you need to compile the code and make your own .deb package you can later on distribute.
# 
# Anyway pam_ssh_agent_auth is good way how you can elevate your account using sudo, it's not asking for
# password, but rather for the ssh-key which can be pushed via ssh-agent on remote machine.
#
# Centos 7 has this as a package and configuration is fairly easy.

aptitude install build-essential checkinstall libssl-dev libpam0g-dev 
wget http://sourceforge.net/projects/pamsshagentauth/files/pam_ssh_agent_auth/v0.9.5/pam_ssh_agent_auth-0.9.5.tar.bz2
tar -xvzf pam_ssh_agent_auth-0.9.5.tar.bz2
cd pam_ssh_agent_auth_0.9.5
./configure --libexecdir=/lib/security --with-mantype=man
make
make install
checkinstall
