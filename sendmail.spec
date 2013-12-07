%if %{_use_internal_dependency_generator}
%define __noautoreq 'perl\\(Net::CIDR\\)'
%endif

%define _enable_debug_packages	%{nil}
%define debug_package		%{nil}

%define initdir 	/etc/rc.d/init.d
%define	alternatives	1
%define sendmaildir	%{_prefix}/lib

Summary:	A widely used Mail Transport Agent (MTA)
Name:		sendmail
Version: 	8.14.5
Release: 	5
License:	BSD
Group:		System/Servers
Url:		http://www.sendmail.org
Source0:	ftp://ftp.sendmail.org/pub/sendmail/%{name}.%{version}.tar.gz
Source1:	sendmail.init
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
Patch1:		sendmail-8.10.0-makemapman.patch
Patch3:		sendmail-8.8.7-rmail.patch
Patch5:		sendmail-8.12.10-movefiles.patch
Patch9:		sendmail-8.14.0-mdk.patch
# (cjw) set .pid file for queue runner and set some other mandriva defaults
#       adapted from fedora sendmail package
Patch12:	sendmail-submit.mc-mandriva.patch
Patch50:	sendmail-8.11.1-up-limit.patch

BuildRequires:	cyrus-sasl
BuildRequires:	groff-base
BuildRequires:	openssl
BuildRequires:	db-devel
BuildRequires:	gdbm-devel
BuildRequires:	sasl-devel
BuildRequires:	tcp_wrappers-devel
BuildRequires:	openldap-devel
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	pkgconfig(openssl)
Requires(pre):	rpm-helper
Requires(pre):	update-alternatives
Requires:	procmail
Requires:	bash >= 2.0
Requires:	cyrus-sasl
Requires:	openssl
Requires:	setup
Provides:	mail-server
Provides:	sendmail-command
Conflicts:	vacation
Conflicts:	postfix

%description
The Sendmail program is a very widely used Mail Transport Agent (MTA).
MTAs send mail from one machine to another.

Sendmail is not a client program, which you use to read your e-mail.
Sendmail is a behind-the-scenes program which actually moves your
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
Requires:	make, m4

%description cf
This package includes the configuration files which you'd need to generate the
sendmail.cf file distributed with the sendmail package.

You'll need the sendmail-cf package if you ever need to reconfigure and rebuild
your sendmail.cf file. For example, the default sendmail.cf file is not
configured for UUCP. If someday you needed to send and receive mail over UUCP,
you'd need to install the sendmail-cf package to help you reconfigure Sendmail.

Install the sendmail-cf package if you need to reconfigure your
sendmail.cf file.

%package devel
Summary:	Sendmail static libraries and headers file
Group: 		Development/Other

%description devel
This package includes the static libraries and header files

%prep
%setup -q
%apply_patches

# XXX REVERTING
sed -e 's|@@PATH@@|\.\.|' < %{SOURCE6} > cf/cf/mandrake.mc
sed -e 's|@@PATH@@|\.\.|' < %{SOURCE9} > cf/cf/real-time.mc
# (sb) smrsh path fixes in docs
perl -pi -e 's|\/usr\/libexec|\/usr\/sbin|g' smrsh/README
perl -pi -e 's|\/usr\/adm\/sm.bin|\/etc\/smrsh|g' smrsh/README
perl -pi -e 's|\/usr\/lib\/sendmail|\/usr\/sbin\/sendmail|g' smrsh/README
echo 'Paths modified for Mandriva Linux mailto:sbenedict@mandriva.com' >> smrsh/README

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
export RPM_OPT_FLAGS="%optflags -DNETINET6"
export LDFLAGS="%ldflags"
export confLIBDIR=%{_libdir}

%make

%install
mkdir -p %{buildroot}/{%{_sysconfdir}/sysconfig,%{initdir},%{_sysconfdir}/pam.d}
mkdir -p %{buildroot}/{%{_bindir},%{_libdir},%{sendmaildir},%{_mandir}/man{1,5,8},%{_sbindir}}
mkdir -p %{buildroot}/{var/log,var/spool,%{_datadir}/sendmail-cf,%{_includedir}/libmilter}
mkdir -p %{buildroot}/%{_docdir}/sendmail

OBJDIR=obj.$(uname -s).$(uname -r).$(arch)

# fix default id and gid during install steps

nameuser=`id -nu`
namegroup=`id -ng`

export confLIBDIR=%{_libdir}
export ID="SBINOWN=${nameuser} SBINGRP=${namegroup} UBINOWN=${nameuser} UBINGRP=${namegroup} MANOWN=${nameuser} MANGRP=${namegroup} MSPQOWN=${nameuser} GBINGRP=${namegroup} GBINOWN=${nameuser} GBINGRP=${namegroup} MSPQOWN=${nameuser} MBINOWN=${nameuser} MBINGRP=${namegroup} LIBOWN=${nameuser} LIBGRP=${namegroup} CFOWN=${nameuser} CFGRP=${namegroup} INCOWN=${nameuser} INCGRP=${namegroup} CFMODE=0644"

# (sb) fix example perl script interpreter paths
sed -i 's|/usr/local/bin/perl|/usr/bin/perl|' contrib/*.pl

# see https://bugzilla.mandriva.com/show_bug.cgi?id=34050
cat cf/cf/mandrake.mc | \
        sed -e "s,%{_datadir}/sendmail-cf/m4/cf\.m4,../../cf/m4/cf.m4," \
        > cf/cf/mandrake-build.mc
cat cf/cf/submit.mc | \
        sed -e "s,%{_datadir}/sendmail-cf/m4/cf\.m4,../../cf/m4/cf.m4," \
        > cf/cf/submit-build.mc
%makeinstall DESTDIR=%{buildroot} MANROOT=%{_mandir}/man CF=mandrake-build SUBMIT=submit-build $ID

%make DESTDIR=%{buildroot} MANROOT=%{_mandir}/man $ID force-install -C $OBJDIR/rmail
%make DESTDIR=%{buildroot} MANROOT=%{_mandir}/man $ID force-install -C $OBJDIR/mail.local

%make DESTDIR=%{buildroot} MANROOT=%{_mandir}/man $ID install -C $OBJDIR/smrsh

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
cp %{SOURCE10} sendmail-docs%{_docdir}/sendmail/
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

mkdir -p %{buildroot}/%{_sysconfdir}/mail
sed -e 's|@@PATH@@|/usr/share/sendmail-cf|' < %{SOURCE6} > %{buildroot}/%{_sysconfdir}/mail/sendmail.mc
cp cf/cf/submit.mc %{buildroot}/%{_sysconfdir}/mail/

echo "# local-host-names - include all aliases for your machine here." > %{buildroot}/%{_sysconfdir}/mail/local-host-names
( echo "# trusted-users - users that can send mail as others without a warning"
echo "# apache, mailman, majordomo, uucp, are good candidates" ) \
	> %{buildroot}/%{_sysconfdir}/mail/trusted-users


install -d -m755 %{buildroot}/var/spool/mqueue
install -d -m755 %{buildroot}/var/spool/clientmqueue

# dangling symlinks
ln -sf ../sbin/sendmail.sendmail %{buildroot}/%{sendmaildir}/sendmail
for f in hoststat mailq newaliases purgestat
  do
    ln -sf ../sbin/sendmail.sendmail %{buildroot}/%{_bindir}/${f}
  done

mkdir -p %{buildroot}/%{_sysconfdir}/smrsh

cat <<EOF > %{buildroot}/%{_sysconfdir}/mail/access
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
    touch %{buildroot}/%{_sysconfdir}/mail/${map}
    chmod 0644 %{buildroot}/%{_sysconfdir}/mail/${map}
    %{buildroot}/usr/sbin/makemap -C %{buildroot}/%{_sysconfdir}/mail/sendmail.cf hash %{buildroot}/%{_sysconfdir}/mail/${map}.db < %{buildroot}/%{_sysconfdir}/mail/${map}
    chmod 0644 %{buildroot}/%{_sysconfdir}/mail/${map}.db
  done
install -m644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/aliases
%{buildroot}/usr/sbin/makemap -C %{buildroot}/%{_sysconfdir}/mail/sendmail.cf hash %{buildroot}/%{_sysconfdir}/aliases.db < %{SOURCE3}

install -m644 %SOURCE4 %{buildroot}/%{_sysconfdir}/sysconfig/sendmail
install -m755 %SOURCE1 %{buildroot}%{initdir}/sendmail

install -m 644 %{SOURCE5} %{buildroot}/%{_sysconfdir}/mail/Makefile

chmod u+w %{buildroot}/usr/sbin/{mailstats,praliases}
chmod u+w %{buildroot}/usr/bin/rmail

install -m755 -d %{buildroot}%{_libdir}/sasl2
install -m 644 %{SOURCE7} %{buildroot}%{_libdir}/sasl2/Sendmail.conf
install -m 644 %{SOURCE8} %{buildroot}/%{_sysconfdir}/pam.d/smtp

# add certs directory for STARTTLS
mkdir -p %{buildroot}/%{_sysconfdir}/ssl/%{name}
# create placeholder certs
pushd %{buildroot}/%{_sysconfdir}/ssl/%{name}
sh %{SOURCE13}
popd

%if %{alternatives}
mv %{buildroot}%{_sbindir}/sendmail %{buildroot}%{_sbindir}/sendmail.sendmail
mv %{buildroot}/%{sendmaildir}/sendmail %{buildroot}/%{sendmaildir}/sendmail.sendmail
%endif

# (sb) logrotate
install -d %{buildroot}%{_sysconfdir}/logrotate.d
cat << EOF > %{buildroot}%{_sysconfdir}/logrotate.d/statistics
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

%postun
if [ "$1" -ge "1" ]; then
	${initdir}/sendmail condrestart > /dev/null 2>&1
fi
exit 0
%_postun_userdel mailnull
%_postun_userdel smmsp

%post
#
# Convert old format to new
#
if [ -f %{_sysconfdir}/mail/deny ] ; then
    cat %{_sysconfdir}/mail/deny | \
	awk 'BEGIN{ print "# Entries from obsoleted /etc/mail/deny"} \
		  {print $1" REJECT"}' >> %{_sysconfdir}/mail/access
    cp %{_sysconfdir}/mail/deny %{_sysconfdir}/mail/deny.rpmorig
fi
for oldfile in relay_allow ip_allow name_allow ; do
    if [ -f %{_sysconfdir}/mail/$oldfile ] ; then
	cat %{_sysconfdir}/mail/$oldfile | \
		awk "BEGIN { print \"# Entries from obsoleted /etc/mail/$oldfile\" ;} \
	     { print \$1\" RELAY\" }" >> %{_sysconfdir}/mail/access
	cp %{_sysconfdir}/mail/$oldfile %{_sysconfdir}/mail/$oldfile.rpmorig
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
if [ -f %{_sysconfdir}/sendmail.cf -a ! -f %{_sysconfdir}/mail/sendmail.cf ] ; then
	sed -e 's/^O AutoRebuildAliases/#O AutoRebuildAliases/'  %{_sysconfdir}/sendmail.cf > %{_sysconfdir}/mail/sendmail.cf
	mv %{_sysconfdir}/sendmail.cf %{_sysconfdir}/sendmail.cf.rpmorig
fi

if [ -f %{_sysconfdir}/sendmail.cw ] ; then
    cat %{_sysconfdir}/sendmail.cw  | \
      awk 'BEGIN { print "# Entries from obsoleted /etc/sendmail.cw" ;} \
           { print $1 }' >> %{_sysconfdir}/mail/local-host-names
    cp %{_sysconfdir}/sendmail.cw %{_sysconfdir}/sendmail.cw.rpmorig
fi
#
# Rebuild maps (next reboot will rebuild also)
#
{ /usr/bin/newaliases
  for map in virtusertable access domaintable mailertable
  do
    if [ -f %{_sysconfdir}/mail/${map} ] ; then
      /usr/sbin/makemap hash %{_sysconfdir}/mail/${map} < %{_sysconfdir}/mail/${map}
      sleep 1
    fi
  done
} > /dev/null 2>&1
%_post_service sendmail

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
%dir %{_sysconfdir}/smrsh
%dir %{_sysconfdir}/mail
%attr(0755,root,mail) %dir %{_sysconfdir}/ssl/%{name}
%attr(0600,root,mail) %config(noreplace)        %{_sysconfdir}/ssl/%{name}/*

%config(noreplace) %{_sysconfdir}/mail/Makefile
%attr(0444,root,mail) %config(noreplace)	%{_sysconfdir}/mail/sendmail.cf
%attr(0444,root,mail) %config(noreplace)	%{_sysconfdir}/mail/submit.cf
%attr(0644,root,mail) %config(noreplace) %{_sysconfdir}/mail/sendmail.mc
%attr(0644,root,mail) %config(noreplace) %{_sysconfdir}/mail/submit.mc
%config(noreplace)	%{_sysconfdir}/mail/local-host-names
%config(noreplace)	%{_sysconfdir}/aliases
%attr(0644,root,root) %ghost %{_sysconfdir}/aliases.db
%attr(0750,root,mail) %dir /var/spool/mqueue
%attr(0770,mail,mail) %dir /var/spool/clientmqueue
%attr(4555,root,mail) /var/log/statistics
%attr(0644,root,root) %ghost			%{_sysconfdir}/mail/virtusertable.db
%attr(0644,root,root) %config(noreplace)	%{_sysconfdir}/mail/virtusertable

%attr(0644,root,root) %ghost			%{_sysconfdir}/mail/access.db
%attr(0644,root,root) %config(noreplace)	%{_sysconfdir}/mail/access

%attr(0644,root,root) %ghost			%{_sysconfdir}/mail/domaintable.db
%attr(0644,root,root) %config(noreplace)	%{_sysconfdir}/mail/domaintable

%attr(0644,root,root) %ghost			%{_sysconfdir}/mail/mailertable.db
%attr(0644,root,root) %config(noreplace)	%{_sysconfdir}/mail/mailertable

%attr(0644,bin,bin) %config(noreplace)	%{_sysconfdir}/mail/helpfile
%attr(0644,root,root) %config(noreplace)	%{_sysconfdir}/mail/trusted-users

%config(noreplace) %{_sysconfdir}/sysconfig/sendmail

%config(noreplace) %{initdir}/sendmail

%config(noreplace) %{_libdir}/sasl2/Sendmail.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/statistics
%config(noreplace) %{_sysconfdir}/pam.d/smtp

%files cf
/usr/share/sendmail-cf

%files doc
%doc contrib sendmail-docs%{_docdir}/sendmail

%files devel
%doc libsm/{*.html,README} sendmail-docs%{_docdir}/sendmail/{libmilter,README.libmilter}
%dir %{_includedir}/libmilter
%{_includedir}/libmilter/*.h
%{_libdir}/lib*.a

