# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_occurrence_enrolment_notifications 1"] = [
    """kukkuu@example.com|['mperez@cox.com']|Occurrence enrolment FI|
        Event FI: Up always sport return. Light a point charge stand store.
        Guardian FI: Kathryn Scott
        Occurrence: 2020-12-12 00:00:00+00:00
        Child: Jessica Sanders (2020-09-25)""",
    """kukkuu@example.com|['mperez@cox.com']|Occurrence unenrolment FI|
        Event FI: Up always sport return. Light a point charge stand store.
        Guardian FI: Kathryn Scott
        Occurrence: 2020-12-12 00:00:00+00:00
        Child: Jessica Sanders (2020-09-25)""",
]

snapshots["test_occurrence_cancelled_notification[True] 1"] = [
    """kukkuu@example.com|['mperez@cox.com']|Occurrence cancelled FI|
        Event FI: Address prove color effort.
        Guardian FI: I Should Receive A Notification Thompson
        Occurrence: 2020-12-12 01:00:00+00:00
        Child: John Terrell (2020-09-07)"""
]

snapshots["test_occurrence_cancelled_notification[False] 1"] = [
    """kukkuu@example.com|['mperez@cox.com']|Occurrence cancelled FI|
        Event FI: Address prove color effort.
        Guardian FI: I Should Receive A Notification Thompson
        Occurrence: 2020-12-12 01:00:00+00:00
        Child: John Terrell (2020-09-07)"""
]
