# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_guardians_query_normal_user 1"] = {
    "data": {
        "guardians": {
            "edges": [
                {
                    "node": {
                        "email": "angelahawkins@gmail.com",
                        "firstName": "Jessica",
                        "lastName": "Chavez",
                        "phoneNumber": "(012)344-7446x8581",
                        "relationships": {
                            "edges": [
                                {
                                    "node": {
                                        "child": {
                                            "birthdate": "2019-05-16",
                                            "firstName": "Patrick",
                                            "lastName": "Thompson",
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

snapshots["test_guardians_query_staff_user 1"] = {
    "data": {
        "guardians": {
            "edges": [
                {
                    "node": {
                        "email": "angelahawkins@gmail.com",
                        "firstName": "Jessica",
                        "lastName": "Chavez",
                        "phoneNumber": "(012)344-7446x8581",
                        "relationships": {
                            "edges": [
                                {
                                    "node": {
                                        "child": {
                                            "birthdate": "2019-05-16",
                                            "firstName": "Patrick",
                                            "lastName": "Thompson",
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
                        "email": "nwilliams@yahoo.com",
                        "firstName": "Christy",
                        "lastName": "Jenkins",
                        "phoneNumber": "+1-270-117-1591x02320",
                        "relationships": {
                            "edges": [
                                {
                                    "node": {
                                        "child": {
                                            "birthdate": "2019-03-24",
                                            "firstName": "Sandra",
                                            "lastName": "Meyer",
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
