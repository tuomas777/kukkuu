# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_language_query 1"] = {
    "data": {
        "language": {
            "alpha3Code": "fin",
            "name": "suomi",
            "translations": [
                {"languageCode": "EN", "name": "Finnish"},
                {"languageCode": "FI", "name": "suomi"},
                {"languageCode": "SV", "name": "Finska"},
            ],
        }
    }
}

snapshots["test_languages_query 1"] = {
    "data": {
        "languages": {
            "edges": [
                {
                    "node": {
                        "alpha3Code": "eng",
                        "name": "englanti",
                        "translations": [
                            {"languageCode": "EN", "name": "English"},
                            {"languageCode": "FI", "name": "englanti"},
                            {"languageCode": "SV", "name": "Engelska"},
                        ],
                    }
                },
                {
                    "node": {
                        "alpha3Code": "swe",
                        "name": "ruotsi",
                        "translations": [
                            {"languageCode": "EN", "name": "Swedish"},
                            {"languageCode": "FI", "name": "ruotsi"},
                            {"languageCode": "SV", "name": "Svenska"},
                        ],
                    }
                },
                {
                    "node": {
                        "alpha3Code": "fin",
                        "name": "suomi",
                        "translations": [
                            {"languageCode": "EN", "name": "Finnish"},
                            {"languageCode": "FI", "name": "suomi"},
                            {"languageCode": "SV", "name": "Finska"},
                        ],
                    }
                },
            ]
        }
    }
}
