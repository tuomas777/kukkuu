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
                        "firstName": "Sandra",
                        "lastName": "Meyer",
                        "phoneNumber": "(727)708-9817",
                        "relationships": {
                            "edges": [
                                {
                                    "node": {
                                        "child": {
                                            "birthdate": "2019-11-23",
                                            "firstName": "Christopher",
                                            "lastName": "Jones",
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
                                        "type": "ADVOCATE",
                                    }
                                }
                            ]
                        },
                    }
                },
                {
                    "node": {
                        "firstName": "Sandra",
                        "lastName": "Meyer",
                        "phoneNumber": "(727)708-9817",
                        "relationships": {
                            "edges": [
                                {
                                    "node": {
                                        "child": {
                                            "birthdate": "2019-11-23",
                                            "firstName": "Christopher",
                                            "lastName": "Jones",
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
