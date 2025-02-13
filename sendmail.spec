%define	alternatives	1
%define sendmaildir	%{_prefix}/lib

%define miltersomajor 1.0
%define libname %mklibname milter %{miltersomajor}
%define devname %mklibname milter -d

Summary:	A widely used Mail Transport Agent (MTA)
Name:		sendmail
Version: 	8.15.2
Release: 	12
License:	Sendmail
Group:		System/Servers
Provides:	mail-server sendmail-command
Conflicts:	vacation postfix
URL:		https://www.sendmail.com/sm/open_source/

Source0:	ftp://ftp.sendmail.org/pub/sendmail/%{name}.%{version}.tar.gz
Source2:	ftp://ftp.sendmail.org/pub/sendmail/%{name}.%{version}.tar.gz.sig
Source3:	aliases
Source4:	sendmail.sysconfig
Source5:	sendmail-etc-mail-Makefile
Source6:	sendmail-mandrake.mc
Source7:	Sendmail.conf
Source8:	sendmail.pam
Source9:	sendmail-real-time.mc
Source10:	README.mdk
Source13:	sendmail-certs.sh
Source14:	sendmail.service
Source15:	sm-client.service

Patch1:		sendmail-8.10.0-makemapman.patch
Patch3:		sendmail-8.8.7-rmail.patch
Patch5:		sendmail-8.12.10-movefiles.patch
# build configuration
Patch9:		sendmail-8.14.0-mdk.patch
# (cjw) set .pid file for queue runner and set some other Mageia defaults
#       adapted from fedora sendmail package, originally applied in mdv
Patch12:	sendmail-submit.mc-mandriva.patch
# (cjw) fix cyrus-imapd path, from fedora pkg
Patch13:	sendmail-8.13.0-cyrus.patch
# (ngompa) make sendmail dynamic with pie, from fedora
Patch14:	sendmail-8.15.2-dynamic.patch
Patch15:	sendmail-8.14.8-link.patch
# From debian: allow fd:N socket address specifications for sendmail socket activation
# http://anonscm.debian.org/cgit/collab-maint/sendmail.git/plain/debian/patches/socket_activation.patch
Patch16:	socket_activation.patch
# (cjw) fix build
Patch17:	sendmail-8.15.1-format-security.patch
# from fedora: fix build with openssl 1.1
# https://bugzilla.redhat.com/show_bug.cgi?id=1400239
Patch18:	sendmail-8.15.2-openssl-1.1.0-fix.patch
# from fedora: another openssl 1.1 fix
# https://bugzilla.redhat.com/show_bug.cgi?id=1473971
Patch19:	sendmail-8.15.2-openssl-1.1.0-ecdhe-fix.patch
# (ngompa) make sendmail make a shared library
Patch20:	sendmail-8.14.3-sharedmilter.patch
# from fedora: fix build with glibc 2.30
Patch21:	sendmail-8.15.2-gethostbyname2.patch

Patch50:	sendmail-8.11.1-up-limit.patch

Requires(pre):	rpm-helper
Requires(pre):	update-alternatives
Requires:	procmail
Requires:	bash >= 2.0
Requires:	cyrus-sasl
Requires:	openssl
Requires: 	setup
BuildRequires:  db-devel
BuildRequires:  pkgconfig(libnsl)
BuildRequires:  cyrus-sasl
BuildRequires:  groff-for-man
BuildRequires:  gdbm-devel
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(libsasl2)
BuildRequires:  tcp_wrappers-devel
BuildRequires:  openldap-devel
BuildRequires:	openssl

%description
The Sendmail program is a widely used Mail Transport Agent (MTA).
MTAs send mail from one machine to another.

Sendmail is not a client program, which you use to read your e-mail.
Sendmail is a behind-the-scenes program which moves your
e-mail over networks or the Internet to where you want it to go.

If you ever need to reconfigure Sendmail, you'll also need to have the
sendmail.cf package installed.  If you need documentation on Sendmail, you can
install the sendmail-doc package.

%package doc
Summary:	Documentation about the Sendmail Mail Transport Agent program
Group:		System/Servers 

%description doc
The sendmail-doc package contains documentation about the Sendmail
Mail Transport Agent (MTA) program, including release notes, the
Sendmail FAQ and a few papers written about Sendmail.  The papers are
provided in PostScript(TM) and troff formats.

Install the sendmail-doc package if you need documentation about
Sendmail.

%package cf
Summary:	The files needed to reconfigure Sendmail
Group:		System/Servers
Requires:	make
Requires:	m4

%description cf
This package includes the configuration files which you'd need to generate the
sendmail.cf file distributed with the sendmail package.

You'll need the sendmail-cf package if you ever need to reconfigure and rebuild
your sendmail.cf file. For example, the default sendmail.cf file is not
configured for UUCP. If someday you needed to send and receive mail over UUCP,
you'd need to install the sendmail-cf package to help you reconfigure Sendmail.

Install the sendmail-cf package if you need to reconfigure your
sendmail.cf file.

%package -n %{libname}
Summary:        Sendmail milter library
Group:		System/Libraries

%description -n %{libname}
This package provides the Sendmail milter shared library.

%package -n %{devname}
Summary:	Sendmail milter development libraries and headers
Group:		Development/C
Conflicts:	%{name}-devel < 8.15.2-5
Obsoletes:	%{name}-devel < 8.15.2-5
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{name}-milter-devel = %{version}-%{release}
Provides:	libmilter-devel = %{version}-%{release}
Requires:	%{libname}%{?_isa} = %{version}-%{release}

%description -n %{devname}
This package includes the libraries and header files
to build applications using sendmail libmilter.

%prep
%setup -q
cp devtools/M4/UNIX/{,shared}library.m4
%autopatch -p1

# XXX REVERTING
sed -e 's|@@PATH@@|\.\.|' < %{SOURCE6} > cf/cf/mandrake.mc
sed -e 's|@@PATH@@|\.\.|' < %{SOURCE9} > cf/cf/real-time.mc
# (sb) smrsh path fixes in docs
perl -pi -e 's|\/usr\/libexec|\/usr\/sbin|g' smrsh/README
perl -pi -e 's|\/usr\/adm\/sm.bin|\/etc\/smrsh|g' smrsh/README
perl -pi -e 's|\/usr\/lib\/sendmail|\/usr\/sbin\/sendmail|g' smrsh/README
echo 'Paths modified for Mageia.' >> smrsh/README

perl -pi -e 's|\/usr\/adm\/sm.bin|\/etc\/smrsh|g' smrsh/smrsh.8
perl -pi -e 's|sm.bin|\/etc\/smrsh|g' smrsh/smrsh.8
head -n -17 smrsh/smrsh.8 > smrsh/smrsh.8.mdk
cat << EOF >> smrsh/smrsh.8.mdk
.SH FILES
/etc/smrsh \- directory for restricted programs
.SH SEE ALSO
sendmail(8)
EOF
mv smrsh/smrsh.8.mdk smrsh/smrsh.8

# (sb) m4 path
perl -pi -e 's|\`sh \$BUILDTOOLS\/bin\/find_m4.sh\`|\/usr\/bin\/m4|g' cf/cf/Build

%build

%serverbuild
export RPM_OPT_FLAGS="%optflags -DNETINET6 -DHAS_GETHOSTBYNAME2"

export confLIBDIR=%{_libdir}

%make_build LDOPTS="%ldflags -fPIC"

%install
mkdir -p %buildroot/{%_sysconfdir/sysconfig,%{_unitdir},%_sysconfdir/pam.d}
mkdir -p %buildroot/{%_bindir,%_libdir,%{sendmaildir},%{_mandir}/man{1,5,8},%_sbindir}
mkdir -p %buildroot/{var/log,var/spool,%_datadir/sendmail-cf,%_includedir/libmilter}
mkdir -p %buildroot/%_docdir/sendmail

OBJDIR=obj.$(uname -s).$(uname -r).$(arch)

# fix default id and gid during install steps

nameuser=`id -nu`
namegroup=`id -ng`

export confLIBDIR=%{_libdir}
export ID="SBINOWN=${nameuser} SBINGRP=${namegroup} UBINOWN=${nameuser} UBINGRP=${namegroup} MANOWN=${nameuser} MANGRP=${namegroup} MSPQOWN=${nameuser} GBINGRP=${namegroup} GBINOWN=${nameuser} GBINGRP=${namegroup} MSPQOWN=${nameuser} MBINOWN=${nameuser} MBINGRP=${namegroup} LIBOWN=${nameuser} LIBGRP=${namegroup} CFOWN=${nameuser} CFGRP=${namegroup} INCOWN=${nameuser} INCGRP=${namegroup} CFMODE=0644"

# (sb) fix example perl script interpreter paths
sed -i 's|/usr/local/bin/perl|/usr/bin/perl|' contrib/*.pl
sed -i 's|/usr/perl5/bin/perl|/usr/bin/perl|' contrib/*.pl
sed -i 's|/bin/perl|/usr/bin/perl|' contrib/passwd-to-alias.pl

# see https://bugzilla.mandriva.com/show_bug.cgi?id=34050
cat cf/cf/mandrake.mc | \
        sed -e "s,%{_datadir}/sendmail-cf/m4/cf\.m4,../../cf/m4/cf.m4," \
        > cf/cf/mandrake-build.mc
cat cf/cf/submit.mc | \
        sed -e "s,%{_datadir}/sendmail-cf/m4/cf\.m4,../../cf/m4/cf.m4," \
        > cf/cf/submit-build.mc
%make_install MANROOT=%{_mandir}/man CF=mandrake-build SUBMIT=submit-build $ID

%make_install MANROOT=%{_mandir}/man $ID force-install -C $OBJDIR/rmail
%make_install MANROOT=%{_mandir}/man $ID force-install -C $OBJDIR/mail.local

%make_install MANROOT=%{_mandir}/man $ID install -C $OBJDIR/smrsh

ln -sf ../sbin/makemap %{buildroot}/usr/bin/makemap

# install docs by hand - do it in builddir instead of RPM_BUILD_ROOT
rm -fr sendmail-docs
mkdir -p sendmail-docs%{_docdir}/sendmail
cp -ar FAQ LICENSE KNOWNBUGS README RELEASE_NOTES doc sendmail-docs%{_docdir}/sendmail
cp smrsh/README sendmail-docs%{_docdir}/sendmail/README.smrsh
cp sendmail/README sendmail-docs%{_docdir}/sendmail/README.sendmail
cp sendmail/SECURITY sendmail-docs%{_docdir}/sendmail/SECURITY.sendmail
cp sendmail/TUNING sendmail-docs%{_docdir}/sendmail/TUNING.sendmail
cp mail.local/README sendmail-docs%{_docdir}/sendmail/README.mail.local
cp cf/README sendmail-docs%{_docdir}/sendmail/README.cf
cp cf/cf/README sendmail-docs%{_docdir}/sendmail/README.install-cf
cp %{SOURCE10} sendmail-docs%{_docdir}/sendmail/README.mga
cp libmilter/README sendmail-docs%{_docdir}/sendmail/README.libmilter
cp -ar libmilter/docs/ sendmail-docs%{_docdir}/sendmail/libmilter

# install the cf files
make DESTDIR=%{buildroot} MANROOT=%{_mandir}/man $ID CF=mandrake-build SUBMIT=submit-build install-cf -C cf/cf
# restore include path
sed -i -e "s,\.\./\.\./cf/m4/cf\.m4,%{_datadir}/sendmail-cf/m4/cf.m4,g" \
        %{buildroot}%{_sysconfdir}/mail/sendmail.cf
rm -f cf/cf/mandrake-build.mc
rm -f cf/cf/submit-build.mc
pushd cf
cp -ar * %{buildroot}/usr/share/sendmail-cf
install -m 644 %{SOURCE9} %{buildroot}/usr/share/sendmail-cf/cf
rm -f %{buildroot}/usr/share/sendmail-cf/*/*.m4path
make -C cf mandrake-build.cf
popd

rm -f %{buildroot}%{_datadir}/sendmail-cf/cf/mandrake-build.cf

mkdir -p %{buildroot}/%_sysconfdir/mail
sed -e 's|@@PATH@@|/usr/share/sendmail-cf|' < %{SOURCE6} > %{buildroot}/%_sysconfdir/mail/sendmail.mc
cp cf/cf/submit.mc %{buildroot}/%_sysconfdir/mail/

echo "# local-host-names - include all aliases for your machine here." > %{buildroot}/%_sysconfdir/mail/local-host-names
( echo "# trusted-users - users that can send mail as others without a warning"
echo "# apache, mailman, majordomo, uucp, are good candidates" ) \
	> %{buildroot}/%_sysconfdir/mail/trusted-users


install -d -m755 %buildroot/var/spool/mqueue
install -d -m755 %buildroot/var/spool/clientmqueue

# dangling symlinks
ln -sf ../sbin/sendmail.sendmail %buildroot/%{sendmaildir}/sendmail
for f in hoststat mailq newaliases purgestat
  do
    ln -sf ../sbin/sendmail.sendmail %buildroot/%_bindir/${f}
  done

mkdir -p %buildroot/%_sysconfdir/smrsh

cat <<EOF > %{buildroot}/%_sysconfdir/mail/access
# Check the /usr/share/doc/sendmail-%{version}/README.cf file for a description
# of the format of this file. (search for access_db in that file)
# The /usr/share/doc/sendmail-%{version}/README.cf is part of the sendmail-doc
# package.
#
# by default we allow relaying from localhost...
localhost.localdomain		RELAY
localhost			RELAY
127.0.0.1			RELAY

EOF

for map in virtusertable access domaintable mailertable
  do
    touch %{buildroot}/%_sysconfdir/mail/${map}
    chmod 0644 %{buildroot}/%_sysconfdir/mail/${map}
    %{buildroot}/usr/sbin/makemap -C %{buildroot}/%_sysconfdir/mail/sendmail.cf hash %{buildroot}/%_sysconfdir/mail/${map}.db < %{buildroot}/%_sysconfdir/mail/${map}
    chmod 0644 %{buildroot}/%_sysconfdir/mail/${map}.db
  done
install -m644 %{SOURCE3} %{buildroot}/%_sysconfdir/aliases
%{buildroot}/usr/sbin/makemap -C %{buildroot}/%_sysconfdir/mail/sendmail.cf hash %{buildroot}/%_sysconfdir/aliases.db < %{SOURCE3}

install -m644 %SOURCE4 %{buildroot}/%_sysconfdir/sysconfig/sendmail
install -d -m 755 %{buildroot}%{_unitdir}
install -m644 %SOURCE14 %{buildroot}%{_unitdir}
install -m644 %SOURCE15 %{buildroot}%{_unitdir}

install -m 644 %{SOURCE5} %{buildroot}/%_sysconfdir/mail/Makefile

chmod u+w %{buildroot}/usr/sbin/{mailstats,praliases}
chmod u+w %{buildroot}/usr/bin/rmail

install -m755 -d %{buildroot}%{_libdir}/sasl2
install -m 644 %{SOURCE7} %{buildroot}%{_libdir}/sasl2/Sendmail.conf
install -m 644 %{SOURCE8} %{buildroot}/%_sysconfdir/pam.d/smtp

# add certs directory for STARTTLS
mkdir -p %{buildroot}/%_sysconfdir/ssl/%{name}
# create placeholder certs
pushd %{buildroot}/%_sysconfdir/ssl/%{name}
sh %{SOURCE13}
popd

%if %{alternatives}
mv %{buildroot}%{_sbindir}/sendmail %{buildroot}%{_sbindir}/sendmail.sendmail
mv %{buildroot}/%{sendmaildir}/sendmail %{buildroot}/%{sendmaildir}/sendmail.sendmail
%endif

# (sb) logrotate
install -d %{buildroot}%_sysconfdir/logrotate.d
cat << EOF > %{buildroot}%_sysconfdir/logrotate.d/statistics
/var/log/statistics {
    missingok
    compress
    postrotate
        service sendmail reload
    endscript
}
EOF

# make strip able to touch these
chmod 755 %{buildroot}%{_bindir}/* %{buildroot}%{_sbindir}/*

%pre
%_pre_useradd mailnull /var/spool/mqueue /dev/null
%_pre_useradd smmsp /var/spool/mqueue /dev/null

%_postun_userdel mailnull
%_postun_userdel smmsp

%post
#
# Convert old format to new
#
if [ -f %_sysconfdir/mail/deny ] ; then
    cat %_sysconfdir/mail/deny | \
	awk 'BEGIN{ print "# Entries from obsoleted /etc/mail/deny"} \
		  {print $1" REJECT"}' >> %_sysconfdir/mail/access
    cp %_sysconfdir/mail/deny %_sysconfdir/mail/deny.rpmorig
fi
for oldfile in relay_allow ip_allow name_allow ; do
    if [ -f %_sysconfdir/mail/$oldfile ] ; then
	cat %_sysconfdir/mail/$oldfile | \
		awk "BEGIN { print \"# Entries from obsoleted /etc/mail/$oldfile\" ;} \
	     { print \$1\" RELAY\" }" >> %_sysconfdir/mail/access
	cp %_sysconfdir/mail/$oldfile %_sysconfdir/mail/$oldfile.rpmorig
     fi
done

%if %{alternatives}
#
# Set up the alternatives files for MTAs.
#
/usr/sbin/update-alternatives --install %{_sbindir}/sendmail sendmail-command %{_sbindir}/sendmail.sendmail 10 \
        --slave %{sendmaildir}/sendmail sendmail-command-in_libdir %{_sbindir}/sendmail.sendmail \
        #--initscript sendmail
%endif


#
# Oops, these files moved
#
if [ -f %_sysconfdir/sendmail.cf -a ! -f %_sysconfdir/mail/sendmail.cf ] ; then
	sed -e 's/^O AutoRebuildAliases/#O AutoRebuildAliases/'  %_sysconfdir/sendmail.cf > %_sysconfdir/mail/sendmail.cf
	mv %_sysconfdir/sendmail.cf %_sysconfdir/sendmail.cf.rpmorig
fi

if [ -f %_sysconfdir/sendmail.cw ] ; then
    cat %_sysconfdir/sendmail.cw  | \
      awk 'BEGIN { print "# Entries from obsoleted /etc/sendmail.cw" ;} \
           { print $1 }' >> %_sysconfdir/mail/local-host-names
    cp %_sysconfdir/sendmail.cw %_sysconfdir/sendmail.cw.rpmorig
fi
#
# Rebuild maps (next reboot will rebuild also)
#
{ /usr/bin/newaliases
  for map in virtusertable access domaintable mailertable bitdomain uudomain genericstable authinfo
  do
    if [ -f %_sysconfdir/mail/${map} ] ; then
      /usr/sbin/makemap hash %_sysconfdir/mail/${map} < %_sysconfdir/mail/${map}
      sleep 1
    fi
  done
  for map in userdb
  do
    if [ -f %_sysconfdir/mail/${map} ] ; then
      /usr/sbin/makemap btree %_sysconfdir/mail/${map} < %_sysconfdir/mail/${map}
      sleep 1
    fi
  done
} > /dev/null 2>&1

if [ "$1" = "1" ]; then
  touch /var/lib/rpm-helper/systemd-migration/sendmail
fi

if [ "$1" = "2" ]; then
  if ! [ -f /var/lib/rpm-helper/systemd-migration/sendmail ]; then
    export SENDMAIL_SYSTEMD_MIGRATION=1
  fi
fi

%_post_service sendmail

if [ "$1" = "2" ] && [ "$SENDMAIL_SYSTEMD_MIGRATION" = "1" ]; then
  if grep '^DAEMON=yes$' %{_sysconfdir}/sysconfig/sendmail >/dev/null 2>&1; then
     # do nothing
     :
  else
     # disable daemons...
     systemctl disable sendmail.service
     systemctl disable sm-client.service
     systemctl stop sendmail.service
     systemctl stop sm-client.service
  fi

  chkconfig --del sendmail
fi

%preun
%_preun_service sendmail
if [ $1 = 0 ]; then
        %if %alternatives
                update-alternatives --remove sendmail-command %{_sbindir}/sendmail.sendmail
        %endif
fi


%triggerpostun -- sendmail < 8.10.0
/sbin/chkconfig --add sendmail

%files
%license LICENSE
%attr(0555,bin,bin) /usr/bin/vacation
/usr/bin/hoststat
/usr/bin/purgestat
/usr/bin/makemap
%attr(0555,bin,bin) /usr/sbin/makemap
%attr(0555,bin,bin) /usr/sbin/editmap
%attr(0555,bin,bin) /usr/sbin/mail.local
%attr(0555,bin,bin) /usr/sbin/smrsh
%attr(0555,bin,bin) /usr/sbin/mailstats
%attr(0555,bin,bin) /usr/sbin/praliases
%if %{alternatives}
%attr(2555,root,mail)/usr/sbin/sendmail.sendmail
%{sendmaildir}/sendmail.sendmail
%else
%attr(2555,root,mail) /usr/sbin/sendmail
%attr(0555,bin,bin) /usr/bin/rmail
%{sendmaildir}/sendmail
%endif
/usr/bin/rmail
/usr/bin/newaliases
/usr/bin/mailq
%{_mandir}/man1/mailq.1.*
%{_mandir}/man1/newaliases.1.*
%{_mandir}/man1/vacation.1.*
%{_mandir}/man5/aliases.5.*
%{_mandir}/man8/editmap.8.*
%{_mandir}/man8/mail.local.8.*
%{_mandir}/man8/mailstats.8.*
%{_mandir}/man8/makemap.8.*
%{_mandir}/man8/praliases.8.*
%{_mandir}/man8/rmail.8.*
%{_mandir}/man8/sendmail.8.*
%{_mandir}/man8/smrsh.8.*

# XXX can't do noreplace here or new sendmail will not deliver.
%dir %_sysconfdir/smrsh
%dir %_sysconfdir/mail
%attr(0755,root,mail) %dir %_sysconfdir/ssl/%{name}
%attr(0600,root,mail) %config(noreplace)        %_sysconfdir/ssl/%{name}/*

%config(noreplace) %_sysconfdir/mail/Makefile
%attr(0444,root,mail) %config(noreplace)	%_sysconfdir/mail/sendmail.cf
%attr(0444,root,mail) %config(noreplace)	%_sysconfdir/mail/submit.cf
%attr(0644,root,mail) %config(noreplace) %_sysconfdir/mail/sendmail.mc
%attr(0644,root,mail) %config(noreplace) %_sysconfdir/mail/submit.mc
%config(noreplace)	%_sysconfdir/mail/local-host-names
%config(noreplace)	%_sysconfdir/aliases
%attr(0644,root,root) %ghost %_sysconfdir/aliases.db
%attr(0750,root,mail) %dir /var/spool/mqueue
%attr(0770,mail,mail) %dir /var/spool/clientmqueue
%attr(4555,root,mail) /var/log/statistics
%attr(0644,root,root) %ghost			%_sysconfdir/mail/virtusertable.db
%attr(0644,root,root) %config(noreplace)	%_sysconfdir/mail/virtusertable

%attr(0644,root,root) %ghost			%_sysconfdir/mail/access.db
%attr(0644,root,root) %config(noreplace)	%_sysconfdir/mail/access

%attr(0644,root,root) %ghost			%_sysconfdir/mail/domaintable.db
%attr(0644,root,root) %config(noreplace)	%_sysconfdir/mail/domaintable

%attr(0644,root,root) %ghost			%_sysconfdir/mail/mailertable.db
%attr(0644,root,root) %config(noreplace)	%_sysconfdir/mail/mailertable

%attr(0644,bin,bin) %config(noreplace)	%_sysconfdir/mail/helpfile
%attr(0644,root,root) %config(noreplace)	%_sysconfdir/mail/trusted-users

%config(noreplace) %_sysconfdir/sysconfig/sendmail

%{_unitdir}/sendmail.service
%{_unitdir}/sm-client.service

%config(noreplace) %{_libdir}/sasl2/Sendmail.conf
%config(noreplace) %_sysconfdir/logrotate.d/statistics
%config(noreplace) %_sysconfdir/pam.d/smtp

%files cf
%{_datadir}/sendmail-cf

%files doc
%doc contrib sendmail-docs%{_docdir}/sendmail

%files -n %{libname}
%license LICENSE
%{_libdir}/libmilter.so.%{miltersomajor}{,.*}

%files -n %{devname}
%doc libsm/{*.html,README} sendmail-docs%{_docdir}/sendmail/{libmilter,README.libmilter}
%{_includedir}/libmilter/
%{_libdir}/libmilter.so
