divert(-1)
dnl This is the macro config file used to generate the /etc/sendmail.cf
dnl file. If you modify the file you will have to regenerate the
dnl /etc/sendmail.cf by running this macro config through the m4
dnl preprocessor:
dnl
dnl        m4 /etc/mail/sendmail.mc > /etc/mail/sendmail.cf
dnl
dnl You will need to have the sendmail-cf package installed for this to
dnl work.
include(`/usr/share/sendmail-cf/m4/cf.m4')dnl
define(`confDEF_USER_ID',``mail:mail'')dnl
OSTYPE(`linux')dnl
undefine(`UUCP_RELAY')dnl
undefine(`BITNET_RELAY')dnl
define(`confALIAS_WAIT', `30')dnl
define(`confTO_CONNECT', `1m')dnl
define(`confTRY_NULL_MX_LIST',true)dnl
define(`confDONT_PROBE_INTERFACES',true)dnl
define(`PROCMAIL_MAILER_PATH',`/usr/bin/procmail')dnl
dnl define delivery mode: interactive, background, or queued
dnl define(`confDELIVERY_MODE', `i')
MASQUERADE_AS(`localhost.localdomain')dnl
FEATURE(`limited_masquerade')dnl
FEATURE(`masquerade_envelope')dnl
FEATURE(`smrsh',`/usr/sbin/smrsh')dnl
FEATURE(mailertable)dnl
dnl virtusertable: redirect incoming mail to virtual domain to particular user or domain 
FEATURE(`virtusertable',`hash -o /etc/mail/virtusertable')dnl
dnl genericstable: rewrite sender address for outgoing mail 
FEATURE(genericstable)dnl
FEATURE(always_add_domain)dnl
FEATURE(redirect)dnl
FEATURE(use_cw_file)dnl
FEATURE(local_procmail)dnl
FEATURE(`access_db')dnl
FEATURE(`blacklist_recipients')dnl
FEATURE(`relay_based_on_MX')dnl
dnl FEATURE(dnsbl, `blackholes.mail-abuse.org', `Rejected - see  http://www.mail-abuse.org/rbl/')dnl
dnl FEATURE(dnsbl, `dialups.mail-abuse.org', `Dialup - see http://www.mail-abuse.org/dul/')dnl
dnl FEATURE(dnsbl, `relays.mail-abuse.org', `Open spam relay - see http://www.mail-abuse.org/rss/')dnl
FEATURE(`delay_checks')dnl
FEATURE(`stickyhost')dnl
dnl SASL Configuration
dnl extract from http://www.sendmail.org/~ca/email/auth.html
dnl
dnl Next two lines are for SMTP Authentication
TRUST_AUTH_MECH(`LOGIN PLAIN')dnl
define(`confAUTH_MECHANISMS', `LOGIN PLAIN')dnl
dnl
dnl Next line stops sendmail from allowing auth without encryption
define(`confAUTH_OPTIONS', `Apy')dnl
dnl
dnl # which realm to use in SASL database (sasldb2)
dnl #
define(`confAUTH_REALM', `mail')dnl
dnl # 
dnl STARTTLS configuration
dnl extract from http://www.sendmail.org/~ca/email/starttls.html
dnl
define(`CERT_DIR', `/etc/ssl/sendmail')dnl
define(`confCACERT_PATH', `CERT_DIR')dnl
define(`confCACERT', `CERT_DIR/CAcert.pem')dnl
define(`confSERVER_CERT', `CERT_DIR/MYcert.pem')dnl
define(`confSERVER_KEY', `CERT_DIR/MYkey.pem')dnl
define(`confCLIENT_CERT', `CERT_DIR/MYcert.pem')dnl
define(`confCLIENT_KEY', `CERT_DIR/MYkey.pem')dnl
dnl
dnl Uncomment next lines to hide identity of mail serve
define(`confPRIVACY_FLAGS',`goaway,restrictqrun,restrictmailq')dnl
dnl define(`confSMTP_LOGIN_MSG', `$j server ready at $b')dnl
MAILER(smtp)dnl
MAILER(procmail)dnl

