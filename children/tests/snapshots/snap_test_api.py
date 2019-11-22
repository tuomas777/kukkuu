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
                        "birthdate": "2019-02-22",
                        "firstName": "Daniel",
                        "lastName": "Hernandez",
                        "relationships": {
                            "edges": [
                                {
                                    "node": {
                                        "guardian": {
                                            "firstName": "Melissa",
                                            "lastName": "Dorsey",
                                            "phoneNumber": "(307)277-0898x17101",
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
                        "birthdate": "2019-02-22",
                        "firstName": "Daniel",
                        "lastName": "Hernandez",
                        "relationships": {
                            "edges": [
                                {
                                    "node": {
                                        "guardian": {
                                            "firstName": "Melissa",
                                            "lastName": "Dorsey",
                                            "phoneNumber": "(307)277-0898x17101",
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
                        "relationships": {
                            "edges": [
                                {
                                    "node": {
                                        "guardian": {
                                            "firstName": "Robert",
                                            "lastName": "Crane",
                                            "phoneNumber": "+1-034-669-7270x11715",
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
                "firstName": "Gulle",
                "lastName": "Guardian",
                "phoneNumber": "777-777777",
            },
        }
    }
}
