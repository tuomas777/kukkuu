# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_add_event_staff_user 1"] = {
    "data": {
        "addEvent": {
            "event": {
                "capacityPerOccurrence": 30,
                "duration": 1000,
                "image": "",
                "imageAltText": "Image alt text",
                "participantsPerInvite": "FAMILY",
                "project": {"year": 2020},
                "publishedAt": None,
                "translations": [
                    {
                        "description": "desc",
                        "imageAltText": "Image alt text",
                        "languageCode": "FI",
                        "name": "Event test",
                        "shortDescription": "Short desc",
                    }
                ],
            }
        }
    }
}

snapshots["test_add_occurrence_staff_user 1"] = {
    "data": {
        "addOccurrence": {
            "occurrence": {
                "event": {"createdAt": "2020-12-12T00:00:00+00:00"},
                "occurrenceLanguage": "FI",
                "time": "1986-12-12T16:40:48+00:00",
                "venue": {"createdAt": "2020-12-12T00:00:00+00:00"},
            }
        }
    }
}

snapshots["test_update_event_staff_user 1"] = {
    "data": {
        "updateEvent": {
            "event": {
                "capacityPerOccurrence": 30,
                "duration": 1000,
                "image": "http://testserver/media/spring.jpg",
                "imageAltText": "Image alt text",
                "occurrences": {"edges": []},
                "participantsPerInvite": "FAMILY",
                "translations": [
                    {
                        "description": "desc",
                        "imageAltText": "Image alt text",
                        "languageCode": "SV",
                        "name": "Event test in swedish",
                        "shortDescription": "Short desc",
                    },
                    {
                        "description": "desc",
                        "imageAltText": "Image alt text",
                        "languageCode": "FI",
                        "name": "Event test in suomi",
                        "shortDescription": "Short desc",
                    },
                ],
            }
        }
    }
}

snapshots["test_staff_publish_event 1"] = {
    "data": {"publishEvent": {"event": {"publishedAt": "2020-12-12T00:00:00+00:00"}}}
}

snapshots["test_occurrence_query_normal_user 1"] = {
    "data": {
        "occurrence": {
            "enrolmentCount": 0,
            "enrolments": {"edges": []},
            "event": {
                "capacityPerOccurrence": 43,
                "duration": 112,
                "image": "http://testserver/media/send.jpg",
                "participantsPerInvite": "CHILD_AND_GUARDIAN",
                "publishedAt": "2020-12-12T00:00:00+00:00",
                "translations": [
                    {
                        "description": "Expert interview old affect quite nearly gun. Born land military first he law ago. Yard door indicate country individual course.",
                        "languageCode": "FI",
                        "name": "Up always sport return. Light a point charge stand store.",
                        "shortDescription": "East site chance of.",
                    }
                ],
            },
            "occurrenceLanguage": "FI",
            "remainingCapacity": 43,
            "time": "2020-12-12T00:00:00+00:00",
            "venue": {
                "translations": [
                    {
                        "accessibilityInfo": "From daughter order stay sign discover eight. Toward scientist service wonder everything. Middle moment strong hand push book and interesting.",
                        "additionalInfo": "Training thought price. Effort clear and local challenge box. Care figure mention wrong when lead involve.",
                        "address": """48830 Whitehead Rapid Suite 548
Whiteview, TN 11309""",
                        "arrivalInstructions": "Benefit treat final central. Past ready join enjoy. Huge get this success commercial recently from.",
                        "description": """Perform in weight success answer. Hospital number lose least then. Beyond than trial western.
Page box child care any concern. Defense level church use.""",
                        "languageCode": "FI",
                        "name": "Free heart significant machine try.",
                        "wwwUrl": "http://brooks.org/",
                    }
                ]
            },
        }
    }
}

snapshots["test_update_occurrence_staff_user 1"] = {
    "data": {
        "updateOccurrence": {
            "occurrence": {
                "enrolmentCount": 0,
                "event": {"createdAt": "2020-12-12T00:00:00+00:00"},
                "occurrenceLanguage": "SV",
                "remainingCapacity": 43,
                "time": "1986-12-12T16:40:48+00:00",
                "venue": {"createdAt": "2020-12-12T00:00:00+00:00"},
            }
        }
    }
}

snapshots["test_enrolment_visibility 1"] = {
    "data": {
        "occurrence": {
            "enrolmentCount": 4,
            "enrolments": {"edges": [{"node": {"child": {"firstName": "Mary"}}}]},
            "event": {
                "capacityPerOccurrence": 5,
                "duration": 1,
                "image": "http://testserver/media/response.jpg",
                "participantsPerInvite": "CHILD_AND_GUARDIAN",
                "publishedAt": "2020-12-12T00:00:00+00:00",
                "translations": [
                    {
                        "description": "Law ago respond yard door indicate country. Direction traditional whether serious sister work. Beat pressure unit toward movie by.",
                        "languageCode": "EN",
                        "name": "Detail audience campaign college career fight data.",
                        "shortDescription": "Last in able local garden modern they.",
                    }
                ],
            },
            "occurrenceLanguage": "FI",
            "remainingCapacity": 1,
            "time": "2020-12-12T00:00:00+00:00",
            "venue": {
                "translations": [
                    {
                        "accessibilityInfo": """Party door better performance race story. Beautiful if his their.
Election stay every something base. Treat final central situation past ready join.""",
                        "additionalInfo": """Policy data control as receive.
Teacher subject family around year. Space speak sense person the probably deep.
Social believe policy security score. Turn argue present throw spend prevent.""",
                        "address": """29898 Bell Junctions
Jenniferbury, TX 72520""",
                        "arrivalInstructions": """Significant land especially can quite industry relationship. Which president smile staff country actually generation. Age member whatever open effort clear.
Local challenge box myself last.""",
                        "description": """Address prove color effort. Enter everything history remember stay public high. Exist shoulder write century.
Myself yourself able process base sing according. Watch media do concern sit enter.""",
                        "languageCode": "EN",
                        "name": "Trial western break page box child care. Tv minute defense.",
                        "wwwUrl": "https://beck.org/",
                    }
                ]
            },
        }
    }
}

snapshots["test_events_query_normal_user 1"] = {
    "data": {
        "events": {
            "edges": [
                {
                    "node": {
                        "capacityPerOccurrence": 50,
                        "createdAt": "2020-12-12T00:00:00+00:00",
                        "description": """Serious listen police shake. Page box child care any concern.
Agree room laugh prevent make. Our very television beat at success decade.""",
                        "duration": 197,
                        "image": "http://testserver/media/spring.jpg",
                        "imageAltText": "",
                        "name": "Free heart significant machine try.",
                        "occurrences": {
                            "edges": [
                                {
                                    "node": {
                                        "enrolmentCount": 0,
                                        "remainingCapacity": 50,
                                        "time": "2005-09-07T17:47:05+00:00",
                                        "venue": {
                                            "translations": [
                                                {
                                                    "description": "Later evening southern would according strong. Analysis season project executive entire.",
                                                    "languageCode": "FI",
                                                    "name": "Able process base sing according.",
                                                }
                                            ]
                                        },
                                    }
                                }
                            ]
                        },
                        "participantsPerInvite": "FAMILY",
                        "project": {"year": 2020},
                        "publishedAt": "2020-12-12T00:00:00+00:00",
                        "shortDescription": "Perform in weight success answer.",
                        "translations": [
                            {
                                "description": """Serious listen police shake. Page box child care any concern.
Agree room laugh prevent make. Our very television beat at success decade.""",
                                "imageAltText": "",
                                "languageCode": "FI",
                                "name": "Free heart significant machine try.",
                                "shortDescription": "Perform in weight success answer.",
                            }
                        ],
                        "updatedAt": "2020-12-12T00:00:00+00:00",
                    }
                }
            ]
        }
    }
}

snapshots["test_event_query_normal_user 1"] = {
    "data": {
        "event": {
            "capacityPerOccurrence": 50,
            "createdAt": "2020-12-12T00:00:00+00:00",
            "description": """Serious listen police shake. Page box child care any concern.
Agree room laugh prevent make. Our very television beat at success decade.""",
            "duration": 197,
            "image": "http://testserver/media/spring.jpg",
            "imageAltText": "",
            "name": "Free heart significant machine try.",
            "occurrences": {
                "edges": [
                    {
                        "node": {
                            "enrolmentCount": 0,
                            "remainingCapacity": 50,
                            "time": "2005-09-07T17:47:05+00:00",
                            "venue": {
                                "translations": [
                                    {
                                        "description": "Later evening southern would according strong. Analysis season project executive entire.",
                                        "languageCode": "FI",
                                        "name": "Able process base sing according.",
                                    }
                                ]
                            },
                        }
                    }
                ]
            },
            "participantsPerInvite": "FAMILY",
            "project": {"year": 2020},
            "publishedAt": "2020-12-12T00:00:00+00:00",
            "shortDescription": "Perform in weight success answer.",
            "translations": [
                {
                    "description": """Serious listen police shake. Page box child care any concern.
Agree room laugh prevent make. Our very television beat at success decade.""",
                    "imageAltText": "",
                    "languageCode": "FI",
                    "name": "Free heart significant machine try.",
                    "shortDescription": "Perform in weight success answer.",
                }
            ],
            "updatedAt": "2020-12-12T00:00:00+00:00",
        }
    }
}

snapshots["test_unenrol_occurrence 1"] = {
    "data": {
        "unenrolOccurrence": {
            "child": {"firstName": "Jesse"},
            "occurrence": {"time": "2020-12-12T00:00:00+00:00"},
        }
    }
}

snapshots["test_required_translation 1"] = {
    "data": {
        "addEvent": {
            "event": {
                "capacityPerOccurrence": 30,
                "duration": 1000,
                "image": "",
                "imageAltText": "Image alt text",
                "participantsPerInvite": "FAMILY",
                "project": {"year": 2020},
                "publishedAt": None,
                "translations": [
                    {
                        "description": "desc",
                        "imageAltText": "Image alt text",
                        "languageCode": "FI",
                        "name": "Event test",
                        "shortDescription": "Short desc",
                    }
                ],
            }
        }
    }
}

snapshots["test_occurrences_filter_by_language 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {"node": {"time": "1985-04-04T17:23:07+00:00"}},
                {"node": {"time": "1994-08-09T11:57:00+00:00"}},
            ]
        }
    }
}

snapshots["test_occurrences_filter_by_time 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {"node": {"time": "1970-01-01T11:00:00+00:00"}},
                {"node": {"time": "1970-01-02T11:00:00+00:00"}},
            ]
        }
    }
}

snapshots["test_enrol_occurrence 1"] = {
    "data": {
        "enrolOccurrence": {
            "enrolment": {
                "child": {"firstName": "Mary"},
                "createdAt": "2020-12-12T00:00:00+00:00",
                "occurrence": {"time": "2020-12-12T00:00:00+00:00"},
            }
        }
    }
}

snapshots["test_occurrences_filter_by_date 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {"node": {"time": "1970-01-02T00:00:00+00:00"}},
                {"node": {"time": "1970-01-02T00:00:00+00:00"}},
            ]
        }
    }
}

snapshots["test_occurrences_filter_by_upcoming 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {"node": {"time": "1970-01-01T00:00:00+00:00"}},
                {"node": {"time": "2020-12-12T00:00:00+00:00"}},
            ]
        }
    }
}

snapshots["test_occurrences_filter_by_venue 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {"node": {"time": "1972-03-26T04:44:55+00:00"}},
                {"node": {"time": "1982-06-18T10:23:32+00:00"}},
                {"node": {"time": "1985-10-25T17:18:53+00:00"}},
            ]
        }
    }
}

snapshots["test_occurrences_query_normal_user 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "enrolmentCount": 0,
                        "event": {
                            "capacityPerOccurrence": 43,
                            "duration": 112,
                            "image": "http://testserver/media/send.jpg",
                            "participantsPerInvite": "CHILD_AND_GUARDIAN",
                            "publishedAt": "2020-12-12T00:00:00+00:00",
                            "translations": [
                                {
                                    "description": "Expert interview old affect quite nearly gun. Born land military first he law ago. Yard door indicate country individual course.",
                                    "languageCode": "FI",
                                    "name": "Up always sport return. Light a point charge stand store.",
                                    "shortDescription": "East site chance of.",
                                }
                            ],
                        },
                        "remainingCapacity": 43,
                        "time": "2020-12-12T00:00:00+00:00",
                        "venue": {
                            "translations": [
                                {
                                    "accessibilityInfo": "From daughter order stay sign discover eight. Toward scientist service wonder everything. Middle moment strong hand push book and interesting.",
                                    "additionalInfo": "Training thought price. Effort clear and local challenge box. Care figure mention wrong when lead involve.",
                                    "address": """48830 Whitehead Rapid Suite 548
Whiteview, TN 11309""",
                                    "arrivalInstructions": "Benefit treat final central. Past ready join enjoy. Huge get this success commercial recently from.",
                                    "description": """Perform in weight success answer. Hospital number lose least then. Beyond than trial western.
Page box child care any concern. Defense level church use.""",
                                    "languageCode": "FI",
                                    "name": "Free heart significant machine try.",
                                    "wwwUrl": "http://brooks.org/",
                                }
                            ]
                        },
                    }
                }
            ]
        }
    }
}

snapshots["test_child_enrol_occurence_from_different_project 1"] = {
    "data": {
        "enrolOccurrence": {
            "enrolment": {
                "child": {"firstName": "Katherine"},
                "createdAt": "2020-12-12T00:00:00+00:00",
                "occurrence": {"time": "2020-12-12T00:00:00+00:00"},
            }
        }
    }
}

snapshots["test_occurrences_filter_by_event 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {"node": {"time": "1970-01-01T12:00:00+00:00"}},
                {"node": {"time": "1970-01-01T12:00:00+00:00"}},
            ]
        }
    }
}

snapshots["test_occurrence_available_capacity_and_enrolment_count 1"] = {
    "data": {
        "occurrence": {
            "enrolmentCount": 3,
            "enrolments": {"edges": []},
            "event": {
                "capacityPerOccurrence": 43,
                "duration": 112,
                "image": "http://testserver/media/send.jpg",
                "participantsPerInvite": "CHILD_AND_GUARDIAN",
                "publishedAt": "2020-12-12T00:00:00+00:00",
                "translations": [
                    {
                        "description": "Expert interview old affect quite nearly gun. Born land military first he law ago. Yard door indicate country individual course.",
                        "languageCode": "EN",
                        "name": "Up always sport return. Light a point charge stand store.",
                        "shortDescription": "East site chance of.",
                    }
                ],
            },
            "occurrenceLanguage": "FI",
            "remainingCapacity": 40,
            "time": "2020-12-12T00:00:00+00:00",
            "venue": {
                "translations": [
                    {
                        "accessibilityInfo": "From daughter order stay sign discover eight. Toward scientist service wonder everything. Middle moment strong hand push book and interesting.",
                        "additionalInfo": "Training thought price. Effort clear and local challenge box. Care figure mention wrong when lead involve.",
                        "address": """48830 Whitehead Rapid Suite 548
Whiteview, TN 11309""",
                        "arrivalInstructions": "Benefit treat final central. Past ready join enjoy. Huge get this success commercial recently from.",
                        "description": """Perform in weight success answer. Hospital number lose least then. Beyond than trial western.
Page box child care any concern. Defense level church use.""",
                        "languageCode": "EN",
                        "name": "Free heart significant machine try.",
                        "wwwUrl": "http://brooks.org/",
                    }
                ]
            },
        }
    }
}

snapshots["test_events_query_project_user 1"] = {
    "data": {
        "events": {
            "edges": [
                {
                    "node": {
                        "capacityPerOccurrence": 50,
                        "createdAt": "2020-12-12T00:00:00+00:00",
                        "description": """Serious listen police shake. Page box child care any concern.
Agree room laugh prevent make. Our very television beat at success decade.""",
                        "duration": 197,
                        "image": "http://testserver/media/spring.jpg",
                        "imageAltText": "",
                        "name": "Free heart significant machine try.",
                        "occurrences": {
                            "edges": [
                                {
                                    "node": {
                                        "enrolmentCount": 0,
                                        "remainingCapacity": 50,
                                        "time": "1978-11-27T17:53:39+00:00",
                                        "venue": {
                                            "translations": [
                                                {
                                                    "description": "Effort clear and local challenge box. Care figure mention wrong when lead involve. Event lay yes policy data control as receive. End available avoid girl middle.",
                                                    "languageCode": "FI",
                                                    "name": "Especially can quite industry relationship very produce social.",
                                                }
                                            ]
                                        },
                                    }
                                }
                            ]
                        },
                        "participantsPerInvite": "FAMILY",
                        "project": {"year": 2020},
                        "publishedAt": "2020-12-12T00:00:00+00:00",
                        "shortDescription": "Perform in weight success answer.",
                        "translations": [
                            {
                                "description": """Serious listen police shake. Page box child care any concern.
Agree room laugh prevent make. Our very television beat at success decade.""",
                                "imageAltText": "",
                                "languageCode": "FI",
                                "name": "Free heart significant machine try.",
                                "shortDescription": "Perform in weight success answer.",
                            }
                        ],
                        "updatedAt": "2020-12-12T00:00:00+00:00",
                    }
                },
                {
                    "node": {
                        "capacityPerOccurrence": 28,
                        "createdAt": "2020-12-12T00:00:00+00:00",
                        "description": """Wonder everything pay parent theory go home. Book and interesting sit future dream party. Truth list pressure stage history.
If his their best. Election stay every something base.""",
                        "duration": 42,
                        "image": "http://testserver/media/think.jpg",
                        "imageAltText": "",
                        "name": "Able process base sing according.",
                        "occurrences": {
                            "edges": [
                                {
                                    "node": {
                                        "enrolmentCount": 0,
                                        "remainingCapacity": 28,
                                        "time": "2012-05-15T10:30:47+00:00",
                                        "venue": {
                                            "translations": [
                                                {
                                                    "description": "Effort clear and local challenge box. Care figure mention wrong when lead involve. Event lay yes policy data control as receive. End available avoid girl middle.",
                                                    "languageCode": "FI",
                                                    "name": "Especially can quite industry relationship very produce social.",
                                                }
                                            ]
                                        },
                                    }
                                }
                            ]
                        },
                        "participantsPerInvite": "FAMILY",
                        "project": {"year": 2020},
                        "publishedAt": None,
                        "shortDescription": "Later evening southern would according strong.",
                        "translations": [
                            {
                                "description": """Wonder everything pay parent theory go home. Book and interesting sit future dream party. Truth list pressure stage history.
If his their best. Election stay every something base.""",
                                "imageAltText": "",
                                "languageCode": "FI",
                                "name": "Able process base sing according.",
                                "shortDescription": "Later evening southern would according strong.",
                            }
                        ],
                        "updatedAt": "2020-12-12T00:00:00+00:00",
                    }
                },
            ]
        }
    }
}

snapshots["test_occurrences_query_project_user 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "enrolmentCount": 0,
                        "event": {
                            "capacityPerOccurrence": 43,
                            "duration": 112,
                            "image": "http://testserver/media/send.jpg",
                            "participantsPerInvite": "CHILD_AND_GUARDIAN",
                            "publishedAt": "2020-12-12T00:00:00+00:00",
                            "translations": [
                                {
                                    "description": "Expert interview old affect quite nearly gun. Born land military first he law ago. Yard door indicate country individual course.",
                                    "languageCode": "FI",
                                    "name": "Up always sport return. Light a point charge stand store.",
                                    "shortDescription": "East site chance of.",
                                }
                            ],
                        },
                        "remainingCapacity": 43,
                        "time": "2020-12-12T00:00:00+00:00",
                        "venue": {
                            "translations": [
                                {
                                    "accessibilityInfo": "From daughter order stay sign discover eight. Toward scientist service wonder everything. Middle moment strong hand push book and interesting.",
                                    "additionalInfo": "Training thought price. Effort clear and local challenge box. Care figure mention wrong when lead involve.",
                                    "address": """48830 Whitehead Rapid Suite 548
Whiteview, TN 11309""",
                                    "arrivalInstructions": "Benefit treat final central. Past ready join enjoy. Huge get this success commercial recently from.",
                                    "description": """Perform in weight success answer. Hospital number lose least then. Beyond than trial western.
Page box child care any concern. Defense level church use.""",
                                    "languageCode": "FI",
                                    "name": "Free heart significant machine try.",
                                    "wwwUrl": "http://brooks.org/",
                                }
                            ]
                        },
                    }
                },
                {
                    "node": {
                        "enrolmentCount": 0,
                        "event": {
                            "capacityPerOccurrence": 26,
                            "duration": 220,
                            "image": "http://testserver/media/eight.jpg",
                            "participantsPerInvite": "CHILD_AND_GUARDIAN",
                            "publishedAt": None,
                            "translations": [
                                {
                                    "description": """Along hear follow sometimes. Special far magazine. Know say former conference carry factor front Mr.
Conference thing much like test.""",
                                    "languageCode": "FI",
                                    "name": "Huge realize at rather that place against moment.",
                                    "shortDescription": "Run hand human value base.",
                                }
                            ],
                        },
                        "remainingCapacity": 26,
                        "time": "2020-12-12T06:00:00+00:00",
                        "venue": {
                            "translations": [
                                {
                                    "accessibilityInfo": "From daughter order stay sign discover eight. Toward scientist service wonder everything. Middle moment strong hand push book and interesting.",
                                    "additionalInfo": "Training thought price. Effort clear and local challenge box. Care figure mention wrong when lead involve.",
                                    "address": """48830 Whitehead Rapid Suite 548
Whiteview, TN 11309""",
                                    "arrivalInstructions": "Benefit treat final central. Past ready join enjoy. Huge get this success commercial recently from.",
                                    "description": """Perform in weight success answer. Hospital number lose least then. Beyond than trial western.
Page box child care any concern. Defense level church use.""",
                                    "languageCode": "FI",
                                    "name": "Free heart significant machine try.",
                                    "wwwUrl": "http://brooks.org/",
                                }
                            ]
                        },
                    }
                },
            ]
        }
    }
}
