divert(-1)
dnl This is the macro config file used to generate the /etc/sendmail.cf
dnl file. If you modify the file you will have to regenerate the
dnl /etc/sendmail.cf by running this macro config through the m4
dnl preprocessor:
dnl
dnl        m4 /etc/mail/sendmail.mc > /etc/sendmail.cf
dnl
dnl You will need to have the sendmail-cf package installed for this to
dnl work.
include(`../m4/cf.m4')dnl
define(`confDEF_USER_ID',``8:12'')dnl
OSTYPE(`linux')dnl
undefine(`UUCP_RELAY')dnl
undefine(`BITNET_RELAY')dnl
dnl define(`confAUTO_REBUILD')dnl
define(`confALIAS_WAIT', `30')dnl
define(`confTO_CONNECT', `1m')dnl
define(`confTRY_NULL_MX_LIST',true)dnl
define(`confDONT_PROBE_INTERFACES',true)dnl
define(`PROCMAIL_MAILER_PATH',`/usr/bin/procmail')dnl
FEATURE(`limited_masquerade')dnl
FEATURE(`masquerade_envelope')dnl
FEATURE(`smrsh',`/usr/sbin/smrsh')dnl
FEATURE(mailertable)dnl
FEATURE(`virtusertable',`hash -o /etc/mail/virtusertable')dnl
FEATURE(redirect)dnl
FEATURE(always_add_domain)dnl
FEATURE(use_cw_file)dnl
FEATURE(`access_db')dnl
FEATURE(`blacklist_recipients')dnl
FEATURE(`relay_based_on_MX')dnl
dnl FEATURE(dnsbl, `blackholes.mail-abuse.org', `Rejected - see  http://www.mail-abuse.org/rbl/')dnl
dnl FEATURE(dnsbl, `dialups.mail-abuse.org', `Dialup - see http://www.mail-abuse.org/dul/')dnl
dnl FEATURE(dnsbl, `relays.mail-abuse.org', `Open spam relay - see http://www.mail-abuse.org/rss/')dnl
FEATURE(`delay_checks')dnl
dnl
dnl If you have AMaViS and want to do virus scanning, comment out the
dnl FEATURE(local_procmail) line, and uncomment these:
dnl define(`LOCAL_MAILER_PATH',`/usr/sbin/scanmails')dnl
dnl define(`LOCAL_MAILER_ARGS',`scanmails -Y -a $h -d $u')dnl
dnl
dnl If you want to deliver locally using procmail, use the below:
FEATURE(local_procmail)dnl
dnl
dnl Uncomment below to set up authentication information file
dnl define(`confDEF_AUTH_INFO', `/etc/mail/default-auth-info')dnl
dnl
dnl Next two lines are for SMTP Authentication
dnl TRUST_AUTH_MECH(`LOGIN PLAIN')dnl
dnl define(`confAUTH_MECHANISMS', `LOGIN PLAIN')dnl
dnl
dnl Next four lines are for StartTLS Support
dnl define(`confCACERT_PATH', `/etc/ssl/certs')dnl
dnl define(`confCACERT', `/etc/ssl/certs/sendmail.ca')dnl
dnl define(`confSERVER_CERT', `/etc/ssl/certs/sendmail.crt')dnl
dnl define(`confSERVER_KEY', `/etc/ssl/certs/sendmail.key')dnl
dnl
dnl Next line stops sendmail from allowing auth without encryption
dnl define(`confAUTH_OPTIONS', `Ap')dnl
dnl
dnl Uncomment next lines to hide identity of mail server
dnl define(`confPRIVACY_FLAGS',`goaway')dnl
dnl define(`confSMTP_LOGIN_MSG', `$j server ready at $b')dnl
MAILER(smtp)dnl
MAILER(procmail)dnl
MASQUERADE_AS(`localhost.localdomain')dnl

