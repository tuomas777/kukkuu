# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_event_publish_notification 1"] = [
    """kukkuu@example.com|['jennifer66@farrell-dunn.com']|Event published FI|
        Event FI: Free heart significant machine try.
        Guardian FI: Donna Hull""",
    """kukkuu@example.com|['samuel43@yahoo.com']|Event published FI|
        Event FI: Free heart significant machine try.
        Guardian FI: Stacey Mcclure""",
    """kukkuu@example.com|['mhunter@gmail.com']|Event published FI|
        Event FI: Free heart significant machine try.
        Guardian FI: Kimberly Baker""",
]

snapshots["test_occurrence_enrolment_notifications 1"] = [
    """kukkuu@example.com|['mperez@cox.com']|Occurrence enrolment FI|
        Event FI: Worker position late leg him president.
        Guardian FI: Dana Hernandez
        Occurrence: 1986-12-12 18:20:48+01:40
        Child: David Payne (2020-07-19)""",
    """kukkuu@example.com|['mperez@cox.com']|Occurrence unenrolment FI|
        Event FI: Worker position late leg him president.
        Guardian FI: Dana Hernandez
        Occurrence: 1986-12-12 16:40:48+00:00
        Child: David Payne (2020-07-19)""",
]
