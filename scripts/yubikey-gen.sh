#!/bin/bash

# Code sample how to deal with gpg keys when you want them to store on your Yubikey,

# It's only concept and there are few headaches but you can use it with
# pam_ssh_auth script. Just be careful, you can end up with SPOF.

export GNUPGHOME=$(mktemp -d) ; echo $GNUPGHOME


install_deps() {
    sudo apt install libpam-yubico
}

add_udev() {
sudo touch /etc/udev/rules.d/70-yubikey.rules
# @TODO: fix permissions
sudo chown root:root /etc/udev/rules.d/70-yubikey.rules
sudo chmod 0777 /etc/udev/rules.d/70-yubikey.rules

sudo cat << EOF > /etc/udev/rules.d/70-yubikey.rules
ACTION=="add|change", SUBSYSTEM=="usb", ATTR{idVendor}=="1050", ATTR{idProduct}=="0010|0110|0111|0114|0116|0401|0403|0405|0407|0410", OWNER="${USERNAME}", TAG+="uaccess"
EOF

sudo chmod 0644 /etc/udev/rules.d/70-yubikey.rules
sudo udevadm control --reload-rules
}

gpg_card_status() {
    gpg --version
    gpg --card-status
    echo "\n"
    gpg2 --version
    gpg2 --card-status
}

# How to yubikey
#https://blog.liw.fi/posts/2017/05/29/using_a_yubikey_4_for_ensafening_one_s_encryption/


gpg_conf_encryption() {
# https://www.gnupg.org/documentation/manuals/gnupg/Unattended-GPG-key-generation.html
# https://gnupg.org/documentation/manuals/gnupg-2.0/Unattended-GPG-key-generation.html (check example)
# https://serverfault.com/questions/691120/how-to-generate-gpg-key-without-user-interaction (use haveged)
# cat << EOF > $GNUPGHOME/jtester
cat << EOF > jtester
     %echo Generating a basic OpenPGP key
     Key-Type: RSA
     Key-Length: 1024
     Subkey-Type: ELG-E
     Subkey-Length: 1024
     Name-Real: Joe Tester
     Name-Comment: with stupid passphrase
     Name-Email: joe@foo.bar
     Expire-Date: 0
     Passphrase: abckineo
     %pubring jtester.pub
     %secring jtester.sec
     # Do a commit here, so that we can later print "done" :-)
     %commit
     %echo done
EOF
}

#gpg_conf_signing() {}


gpg_conf_authentication() {
#cat << EOF > $GNUPGHOME/gpg.conf
cat << EOF > gpg.conf
use-agent
personal-cipher-preferences AES256 AES192 AES CAST5
personal-digest-preferences SHA512 SHA384 SHA256 SHA224
default-preference-list SHA512 SHA384 SHA256 SHA224 AES256 AES192 AES CAST5 ZLIB BZIP2 ZIP Uncompressed
cert-digest-algo SHA512
s2k-digest-algo SHA512
s2k-cipher-algo AES256
charset utf-8
fixed-list-mode
no-comments
no-emit-version
keyid-format 0xlong
list-options show-uid-validity
verify-options show-uid-validity
with-fingerprint
EOF

gpg --full-generate-key

}


init_install() {
#    install_deps
#    add_udev
#    gpg_card_status
    gpg_conf_encryption
}

init_install
