# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_events_query_normal_user 1"] = {
    "data": {
        "events": {
            "edges": [
                {
                    "node": {
                        "createdAt": "2019-12-12T00:00:00+00:00",
                        "description": """Least then top sing. Serious listen police shake. Page box child care any concern.
Agree room laugh prevent make. Our very television beat at success decade.""",
                        "duration": 362,
                        "name": "Worker position late leg him president.",
                        "occurrences": {
                            "edges": [
                                {
                                    "node": {
                                        "time": "1986-12-12T16:40:48+00:00",
                                        "venue": {
                                            "description": "Later evening southern "
                                            "would according strong. "
                                            "Analysis season project "
                                            "executive entire.",
                                            "name": "Never skill down subject town.",
                                            "seatCount": 88,
                                        },
                                    }
                                }
                            ]
                        },
                        "shortDescription": "Together history perform.",
                        "updatedAt": "2019-12-12T00:00:00+00:00",
                    }
                }
            ]
        }
    }
}

snapshots["test_event_query_normal_user 1"] = {
    "data": {
        "event": {
            "createdAt": "2019-12-12T00:00:00+00:00",
            "description": """Serious listen police shake. Page box child care any concern.
Agree room laugh prevent make. Our very television beat at success decade.""",
            "duration": 760,
            "id": "RXZlbnROb2RlOjM=",
            "name": "Free heart significant machine try.",
            "occurrences": {"edges": []},
            "shortDescription": "Fall long respond draw military dog.",
            "updatedAt": "2019-12-12T00:00:00+00:00",
        }
    }
}

snapshots["test_occurrences_query_normal_user 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "event": {
                            "description": """Least then top sing. Serious listen police shake. Page box child care any concern.
Agree room laugh prevent make. Our very television beat at success decade.""",
                            "duration": 362,
                            "name": "Worker position late leg him president.",
                            "shortDescription": "Together history perform.",
                        },
                        "time": "1986-12-12T16:40:48+00:00",
                    }
                }
            ]
        }
    }
}

snapshots["test_occurrence_query_normal_user 1"] = {
    "data": {
        "occurrence": {
            "event": {
                "description": """Least then top sing. Serious listen police shake. Page box child care any concern.
Agree room laugh prevent make. Our very television beat at success decade.""",
                "duration": 362,
                "name": "Worker position late leg him president.",
                "shortDescription": "Together history perform.",
            },
            "id": "T2NjdXJyZW5jZU5vZGU6NA==",
            "time": "1986-12-12T16:40:48+00:00",
            "venue": {
                "description": "Later evening southern would according strong. "
                "Analysis season project executive entire.",
                "name": "Never skill down subject town.",
                "seatCount": 88,
            },
        }
    }
}
