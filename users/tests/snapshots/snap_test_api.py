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
                        "firstName": "Monique",
                        "lastName": "Smith",
                        "phoneNumber": "(028)130-7277",
                        "relationships": {
                            "edges": [
                                {
                                    "node": {
                                        "child": {
                                            "birthdate": "2019-02-06",
                                            "firstName": "Austin",
                                            "lastName": "George",
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
                        "firstName": "Christy",
                        "lastName": "Jenkins",
                        "phoneNumber": "001-803-466-9727x0117",
                        "relationships": {
                            "edges": [
                                {
                                    "node": {
                                        "child": {
                                            "birthdate": "2019-02-14",
                                            "firstName": "Robin",
                                            "lastName": "Moses",
                                        },
                                        "type": "OTHER_GUARDIAN",
                                    }
                                }
                            ]
                        },
                    }
                },
                {
                    "node": {
                        "firstName": "Monique",
                        "lastName": "Smith",
                        "phoneNumber": "(028)130-7277",
                        "relationships": {
                            "edges": [
                                {
                                    "node": {
                                        "child": {
                                            "birthdate": "2019-02-06",
                                            "firstName": "Austin",
                                            "lastName": "George",
                                        },
                                        "type": "ADVOCATE",
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
