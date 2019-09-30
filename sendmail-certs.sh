#!/bin/sh
openssl genrsa -out CAkey.pem 4096
openssl genrsa -out MYkey.pem 4096
openssl req -new -x509 -days 730 -key CAkey.pem -out CAcert.pem << EOF
--
SomeState
SomeCity
SomeOrganization
SomeOrganizationalUnit
localhost.localdomain
root@localhost.localdomain
EOF

openssl req -new -key MYkey.pem -out MYreq.pem << EOF
--
SomeState
SomeCity
SomeOrganization
SomeOrganizationalUnit
localhost.localdomain
root@localhost.localdomain


EOF
mkdir demoCA
cp /dev/null demoCA/index.txt
echo '01' > demoCA/serial
openssl ca -name CA_default -cert CAcert.pem -keyfile CAkey.pem -in MYreq.pem -out MYcert.pem -outdir ./ << EOF
y
y
EOF
rm -fr demoCA
rm -f 01.pem
rm -f MYreq.pem
chmod 0600 *.pem

