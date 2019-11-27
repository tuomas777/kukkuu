# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_submit_child_authenticated 1"] = {
    "data": {
        "submitChildrenAndGuardian": {
            "children": [
                {
                    "birthdate": "2020-01-01",
                    "firstName": "Matti",
                    "lastName": "Mainio",
                    "postalCode": "00840",
                    "relationship": {"type": "OTHER_GUARDIAN"},
                },
                {
                    "birthdate": "2020-02-02",
                    "firstName": "Jussi",
                    "lastName": "Juonio",
                    "postalCode": "00820",
                    "relationship": {"type": None},
                },
            ],
            "guardian": {
                "email": "mperez@cox.com",
                "firstName": "Gulle",
                "lastName": "Guardian",
                "phoneNumber": "777-777777",
            },
        }
    }
}

snapshots["test_children_query_normal_user 1"] = {
    "data": {
        "children": {
            "edges": [
                {
                    "node": {
                        "birthdate": "2019-03-02",
                        "firstName": "Jason",
                        "lastName": "Owens",
                        "postalCode": "70898",
                        "relationships": {
                            "edges": [
                                {
                                    "node": {
                                        "guardian": {
                                            "email": "mperez@cox.com",
                                            "firstName": "Selena",
                                            "lastName": "Roy",
                                            "phoneNumber": "123-447-4468",
                                        },
                                        "type": "OTHER_RELATION",
                                    }
                                }
                            ]
                        },
                    }
                }
            ]
        }
    }
}

snapshots["test_children_query_staff_user 1"] = {
    "data": {
        "children": {
            "edges": [
                {
                    "node": {
                        "birthdate": "2019-03-02",
                        "firstName": "Jason",
                        "lastName": "Owens",
                        "postalCode": "70898",
                        "relationships": {
                            "edges": [
                                {
                                    "node": {
                                        "guardian": {
                                            "email": "mperez@cox.com",
                                            "firstName": "Selena",
                                            "lastName": "Roy",
                                            "phoneNumber": "123-447-4468",
                                        },
                                        "type": "OTHER_RELATION",
                                    }
                                }
                            ]
                        },
                    }
                },
                {
                    "node": {
                        "birthdate": "2019-09-08",
                        "firstName": "John",
                        "lastName": "Terrell",
                        "postalCode": "77671",
                        "relationships": {
                            "edges": [
                                {
                                    "node": {
                                        "guardian": {
                                            "email": "kelly76@allen.com",
                                            "firstName": "Ashley",
                                            "lastName": "Castillo",
                                            "phoneNumber": "(117)159-1023x202",
                                        },
                                        "type": "OTHER_RELATION",
                                    }
                                }
                            ]
                        },
                    }
                },
            ]
        }
    }
}
