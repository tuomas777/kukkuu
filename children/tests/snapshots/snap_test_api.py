# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_children_query_normal_user 1"] = {
    "data": {
        "children": {
            "edges": [
                {
                    "node": {
                        "birthdate": "2019-07-22",
                        "firstName": "Melissa",
                        "lastName": "Dorsey",
                        "relationships": {
                            "edges": [
                                {
                                    "node": {
                                        "guardian": {
                                            "email": "dianahenry@yahoo.com",
                                            "firstName": "Christopher",
                                            "lastName": "Johnson",
                                            "phoneNumber": "(171)012-3447x44685",
                                        },
                                        "type": "ADVOCATE",
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
                        "birthdate": "2019-07-22",
                        "firstName": "Melissa",
                        "lastName": "Dorsey",
                        "relationships": {
                            "edges": [
                                {
                                    "node": {
                                        "guardian": {
                                            "email": "dianahenry@yahoo.com",
                                            "firstName": "Christopher",
                                            "lastName": "Johnson",
                                            "phoneNumber": "(171)012-3447x44685",
                                        },
                                        "type": "ADVOCATE",
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
                        "relationships": {
                            "edges": [
                                {
                                    "node": {
                                        "guardian": {
                                            "email": "adamsrobert@hotmail.com",
                                            "firstName": "Robert",
                                            "lastName": "Crane",
                                            "phoneNumber": "011-715-9102",
                                        },
                                        "type": "PARENT",
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

snapshots["test_submit_child_authenticated 1"] = {
    "data": {
        "submitChildrenAndGuardian": {
            "children": [
                {
                    "birthdate": "2020-01-01",
                    "firstName": "Matti",
                    "lastName": "Mainio",
                    "relationship": {"type": "OTHER_GUARDIAN"},
                },
                {
                    "birthdate": "2020-02-02",
                    "firstName": "Jussi",
                    "lastName": "Juonio",
                    "relationship": {"type": None},
                },
            ],
            "guardian": {
                "email": "gulle@example.com",
                "firstName": "Gulle",
                "lastName": "Guardian",
                "phoneNumber": "777-777777",
            },
        }
    }
}
