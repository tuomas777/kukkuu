# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_signup_notification 1"] = [
    """kukkuu@example.com|['gulle@example.com']|SIGNUP-notifikaation aihe|
SIGNUP-notifikaation sisältö tekstimuodossa.
Lapset: [<Child: Matti Mainio (2020-01-01)>, <Child: Jussi Juonio (2020-02-02)>]
Huoltajat: Gulle Guardian (gulle@example.com)"""
]
