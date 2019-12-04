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
                }
            ]
        }
    }
}

snapshots["test_update_child_mutation 1"] = {
    "data": {
        "updateChild": {
            "child": {
                "birthdate": "2020-01-01",
                "firstName": "Matti",
                "lastName": "Mainio",
                "postalCode": "00840",
            }
        }
    }
}

snapshots["test_delete_child_mutation 1"] = {
    "data": {"deleteChild": {"__typename": "DeleteChildMutationPayload"}}
}

snapshots["test_add_child_mutation 1"] = {
    "data": {
        "addChild": {
            "child": {
                "birthdate": "2020-11-11",
                "firstName": "Pekka",
                "lastName": "Perälä",
                "postalCode": "00820",
            }
        }
    }
}
