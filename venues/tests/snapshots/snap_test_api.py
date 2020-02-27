# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_venues_query_normal_user 1"] = {
    "data": {
        "venues": {
            "edges": [
                {
                    "node": {
                        "accessibilityInfo": "From daughter order stay sign discover eight. Toward scientist service wonder everything. Middle moment strong hand push book and interesting.",
                        "additionalInfo": "Training thought price. Effort clear and local challenge box. Care figure mention wrong when lead involve.",
                        "address": """48830 Whitehead Rapid Suite 548
Whiteview, TN 11309""",
                        "arrivalInstructions": "Benefit treat final central. Past ready join enjoy. Huge get this success commercial recently from.",
                        "description": """Perform in weight success answer. Hospital number lose least then. Beyond than trial western.
Page box child care any concern. Defense level church use.""",
                        "name": "Free heart significant machine try.",
                        "occurrences": {
                            "edges": [
                                {
                                    "node": {
                                        "event": {
                                            "capacityPerOccurrence": 712,
                                            "duration": 300,
                                            "image": "http://testserver/media/hand.jpg",
                                            "participantsPerInvite": "CHILD_AND_GUARDIAN",
                                            "publishedAt": None,
                                            "translations": [
                                                {
                                                    "description": """Leg simple various be various. College able physical almost. Audience actually send address attorney candidate. Rock tough plant traditional.
Build natural middle however.""",
                                                    "languageCode": "EN",
                                                    "name": "Think turn argue present. Spend prevent pressure point exist.",
                                                    "shortDescription": "Others not authority develop identify ready.",
                                                }
                                            ],
                                        },
                                        "remainingCapacity": 712,
                                        "time": "1984-07-02T07:57:10+00:00",
                                    }
                                }
                            ]
                        },
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
                                "wwwUrl": "http://www.hernandez.net/",
                            }
                        ],
                        "wwwUrl": "http://www.hernandez.net/",
                    }
                }
            ]
        }
    }
}

snapshots["test_venue_query_normal_user 1"] = {
    "data": {
        "venue": {
            "accessibilityInfo": "From daughter order stay sign discover eight. Toward scientist service wonder everything. Middle moment strong hand push book and interesting.",
            "additionalInfo": "Training thought price. Effort clear and local challenge box. Care figure mention wrong when lead involve.",
            "address": """48830 Whitehead Rapid Suite 548
Whiteview, TN 11309""",
            "arrivalInstructions": "Benefit treat final central. Past ready join enjoy. Huge get this success commercial recently from.",
            "description": """Perform in weight success answer. Hospital number lose least then. Beyond than trial western.
Page box child care any concern. Defense level church use.""",
            "name": "Free heart significant machine try.",
            "occurrences": {
                "edges": [
                    {
                        "node": {
                            "event": {
                                "capacityPerOccurrence": 712,
                                "duration": 300,
                                "image": "http://testserver/media/hand.jpg",
                                "participantsPerInvite": "CHILD_AND_GUARDIAN",
                                "publishedAt": None,
                                "translations": [
                                    {
                                        "description": """Leg simple various be various. College able physical almost. Audience actually send address attorney candidate. Rock tough plant traditional.
Build natural middle however.""",
                                        "languageCode": "EN",
                                        "name": "Think turn argue present. Spend prevent pressure point exist.",
                                        "shortDescription": "Others not authority develop identify ready.",
                                    }
                                ],
                            },
                            "remainingCapacity": 712,
                            "time": "1984-07-02T07:57:10+00:00",
                        }
                    }
                ]
            },
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
                    "wwwUrl": "http://www.hernandez.net/",
                }
            ],
            "wwwUrl": "http://www.hernandez.net/",
        }
    }
}

snapshots["test_add_venue_staff_user 1"] = {
    "data": {
        "addVenue": {
            "venue": {
                "translations": [
                    {
                        "accessibilityInfo": "Accessibility info",
                        "additionalInfo": "Additional info",
                        "address": "Address",
                        "arrivalInstructions": "Arrival instruction",
                        "description": "Venue description",
                        "languageCode": "FI",
                        "name": "Venue name",
                        "wwwUrl": "www.url.com",
                    }
                ]
            }
        }
    }
}

snapshots["test_update_venue_staff_user 1"] = {
    "data": {
        "updateVenue": {
            "venue": {
                "translations": [
                    {
                        "accessibilityInfo": "Accessibility info",
                        "additionalInfo": "Additional info",
                        "address": "Address",
                        "arrivalInstructions": "Arrival instruction",
                        "description": "Venue description",
                        "languageCode": "FI",
                        "name": "Venue name",
                        "wwwUrl": "www.url.com",
                    },
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
                        "wwwUrl": "http://www.hernandez.net/",
                    },
                ]
            }
        }
    }
}
