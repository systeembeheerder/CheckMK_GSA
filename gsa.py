#!/usr/bin/python3
#
# Systeembeheerder, 2023-04-26
# Monitor Geenbone via CheckMK
#

from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import Gmp
from gvm.errors import GvmError
from gvm.transforms import EtreeTransform

path = '/run/gvmd/gvmd.sock'
connection = UnixSocketConnection(path=path)
transform = EtreeTransform()

username = 'gvm-admin'
password = '<fixme>'


try:
    with Gmp(connection=connection, transform=transform) as gmp:
        gmp.authenticate(username, password)

        medium_results = gmp.get_results (filter_string='created>-1w and severity>=4 and severity<7 min_qod=70 apply_overrides=1 first=1 rows=1000')
        medium_count = int(medium_results.xpath('result_count/filtered/text()')[0])

        high_results = gmp.get_results (filter_string='created>-1w and severity>=7 and severity<9 min_qod=70 apply_overrides=1 first=1 rows=1000')
        high_count = int(high_results.xpath('result_count/filtered/text()')[0])

        crit_results = gmp.get_results (filter_string='created>-1w and severity>=9 min_qod=70 apply_overrides=1 first=1 rows=1000')
        crit_count = int(crit_results.xpath('result_count/filtered/text()')[0])

        print(f"P \"Greenbone Security Assistant results\" medium={medium_count}|high={high_count};1|ciritcal={crit_count};1;1 ")



except GvmError as e:
    print('1 \"Greenbone Security Assistant results\" - An error occurred', e, file=sys.stderr)
