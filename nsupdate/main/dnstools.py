"""
Misc. DNS related code: query, dynamic update, etc.
"""

from django.conf import settings
import dns.name
import dns.resolver
import dns.query
import dns.update
import dns.tsig
import dns.tsigkeyring


SERVER = settings.SERVER  # ns1.thinkmo.de (master / dynamic upd server for nsupdate.info)
BASEDOMAIN = settings.BASEDOMAIN

NONEXISTING_HOST = settings.NONEXISTING_HOST
WWW_HOST = settings.WWW_HOST
WWW_IPV4_HOST = settings.WWW_IPV4_HOST
WWW_IPV6_HOST = settings.WWW_IPV6_HOST
WWW_IPV4_IP = settings.WWW_IPV4_IP
WWW_IPV6_IP = settings.WWW_IPV6_IP

UPDATE_ALGO = dns.tsig.HMAC_SHA512
UPDATE_KEY = settings.UPDATE_KEY


def query_ns(qname, rdtype):
    """
    query a dns name from our master server

    :param qname: the query name
    :type qname: dns.name.Name object or str
    :param rdtype: the query type
    :type rdtype: int or str
    :return: IP (as str)
    """
    resolver = dns.resolver.Resolver(configure=False)
    # we do not configure it from resolv.conf, but patch in the values we
    # want into the documented attributes:
    resolver.nameservers = [SERVER, ]
    resolver.search = [dns.name.from_text(BASEDOMAIN), ]
    answer = resolver.query(qname, rdtype)
    return str(list(answer)[0])


def parse_name(fqdn, origin=None):
    """
    Parse a fully qualified domain name into a relative name
    and a origin zone. Please note that the origin return value will
    have a trailing dot.

    :param fqdn: fully qualified domain name (str)
    :param origin: origin zone (optional, str)
    :return: origin, relative name (both dns.name.Name)
    """
    fqdn = dns.name.from_text(fqdn)
    if origin is None:
        origin = dns.resolver.zone_for_name(fqdn)
        rel_name = fqdn.relativize(origin)
    else:
        origin = dns.name.from_text(origin)
        rel_name = fqdn - origin
    return origin, rel_name


def update_ns(fqdn, rdtype='A', ipaddr=None, origin=None, action='upd', ttl=60):
    """
    update our master server

    :param qname: the name to update
    :param rdtype: the record type
    :param action: 'add', 'del' or 'upd'
    """
    assert action in ['add', 'del', 'upd', ]
    origin, name = parse_name(fqdn, origin)
    upd = dns.update.Update(origin,
                            keyring=dns.tsigkeyring.from_text({BASEDOMAIN+'.': UPDATE_KEY}),
                            keyalgorithm=UPDATE_ALGO)
    if action == 'add':
        assert ipaddr is not None
        upd.add(name, ttl, rdtype, ipaddr)
    elif action == 'del':
        upd.delete(name, rdtype)
    elif action == 'upd':
        assert ipaddr is not None
        upd.replace(name, ttl, rdtype, ipaddr)
    response = dns.query.tcp(upd, SERVER)
    return response
