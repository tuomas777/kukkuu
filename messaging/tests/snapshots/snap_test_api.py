# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_add_message[None] 1"] = {
    "data": {
        "addMessage": {
            "message": {
                "event": None,
                "occurrences": {"edges": []},
                "project": {"year": 2020},
                "recipientCount": 0,
                "recipientSelection": "ALL",
                "sentAt": None,
                "translations": [
                    {
                        "bodyText": "Testiteksti",
                        "languageCode": "FI",
                        "subject": "Testiotsikko",
                    }
                ],
            }
        }
    }
}

snapshots["test_add_message[event] 1"] = {
    "data": {
        "addMessage": {
            "message": {
                "event": {"name": "Free heart significant machine try."},
                "occurrences": {"edges": []},
                "project": {"year": 2020},
                "recipientCount": 0,
                "recipientSelection": "ALL",
                "sentAt": None,
                "translations": [
                    {
                        "bodyText": "Testiteksti",
                        "languageCode": "FI",
                        "subject": "Testiotsikko",
                    }
                ],
            }
        }
    }
}

snapshots["test_add_message[occurrences] 1"] = {
    "data": {
        "addMessage": {
            "message": {
                "event": {"name": "Free heart significant machine try."},
                "occurrences": {
                    "edges": [
                        {"node": {"time": "1986-02-27T01:22:35+00:00"}},
                        {"node": {"time": "1990-03-28T12:56:55+00:00"}},
                        {"node": {"time": "2005-09-07T17:47:05+00:00"}},
                    ]
                },
                "project": {"year": 2020},
                "recipientCount": 0,
                "recipientSelection": "ALL",
                "sentAt": None,
                "translations": [
                    {
                        "bodyText": "Testiteksti",
                        "languageCode": "FI",
                        "subject": "Testiotsikko",
                    }
                ],
            }
        }
    }
}

snapshots["test_cannot_do_message_query_unauthorized_wrong_project 1"] = {
    "data": {"message": None}
}

snapshots["test_delete_message 1"] = {
    "data": {"deleteMessage": {"clientMutationId": None}}
}

snapshots["test_message_query 1"] = {
    "data": {
        "message": {
            "bodyText": "Ruumisteksti.",
            "event": None,
            "occurrences": {"edges": []},
            "project": {"year": 2020},
            "recipientCount": 0,
            "recipientSelection": "ALL",
            "sentAt": None,
            "subject": "Otsikko",
        }
    }
}

snapshots["test_messages_query 1"] = {
    "data": {
        "messages": {
            "edges": [
                {
                    "node": {
                        "bodyText": "Ruumisteksti.",
                        "event": None,
                        "occurrences": {"edges": []},
                        "project": {"year": 2020},
                        "recipientCount": 0,
                        "recipientSelection": "ALL",
                        "sentAt": None,
                        "subject": "Otsikko",
                    }
                }
            ]
        }
    }
}

snapshots["test_messages_query_project_filter 1"] = {
    "data": {
        "messages": {
            "edges": [
                {
                    "node": {
                        "bodyText": "Ruumisteksti.",
                        "event": None,
                        "occurrences": {"edges": []},
                        "project": {"year": 2020},
                        "recipientCount": 0,
                        "recipientSelection": "ALL",
                        "sentAt": None,
                        "subject": "Otsikko",
                    }
                }
            ]
        }
    }
}

snapshots["test_send_message 1"] = {
    "data": {
        "sendMessage": {
            "message": {
                "recipientCount": 1,
                "sentAt": "2020-12-12T00:00:00+00:00",
                "subject": "Otsikko",
            }
        }
    }
}

snapshots["test_update_message[None] 1"] = {
    "data": {
        "updateMessage": {
            "message": {
                "event": {"name": "Free heart significant machine try."},
                "occurrences": {"edges": []},
                "project": {"year": 2020},
                "recipientCount": 0,
                "recipientSelection": "ATTENDED",
                "sentAt": None,
                "translations": [
                    {
                        "bodyText": "Päivitetty testiteksti.",
                        "languageCode": "FI",
                        "subject": "Päivitetty testiotsikko",
                    }
                ],
            }
        }
    }
}

snapshots["test_update_message[event] 1"] = {
    "data": {
        "updateMessage": {
            "message": {
                "event": {
                    "name": "Property work indeed take. Popular care receive camera."
                },
                "occurrences": {"edges": []},
                "project": {"year": 2020},
                "recipientCount": 0,
                "recipientSelection": "ATTENDED",
                "sentAt": None,
                "translations": [
                    {
                        "bodyText": "Päivitetty testiteksti.",
                        "languageCode": "FI",
                        "subject": "Päivitetty testiotsikko",
                    }
                ],
            }
        }
    }
}

snapshots["test_update_message[event_and_occurrences] 1"] = {
    "data": {
        "updateMessage": {
            "message": {
                "event": {
                    "name": "Property work indeed take. Popular care receive camera."
                },
                "occurrences": {
                    "edges": [{"node": {"time": "2016-08-16T07:10:00+00:00"}}]
                },
                "project": {"year": 2020},
                "recipientCount": 0,
                "recipientSelection": "ATTENDED",
                "sentAt": None,
                "translations": [
                    {
                        "bodyText": "Päivitetty testiteksti.",
                        "languageCode": "FI",
                        "subject": "Päivitetty testiotsikko",
                    }
                ],
            }
        }
    }
}
