# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots[
    "test_no_arguments 1"
] = """Nothing to do. Hint: try --help.
"""

snapshots[
    "test_add_default_languages 1"
] = """Created Afar (aar)
Created Abkhazian (abk)
Created Afrikaans (afr)
Created Akan (aka)
Created Amharic (amh)
Created Arabic (ara)
Created Aragonese (arg)
Created Assamese (asm)
Created Avaric (ava)
Created Aymara (aym)
Created Azerbaijani (aze)
Created Bashkir (bak)
Created Bambara (bam)
Created Belarusian (bel)
Created Bengali (ben)
Created Bihari languages (bih)
Created Bislama (bis)
Created Tibetan (bod)
Created Bosnian (bos)
Created Bulgarian (bul)
Created Catalan (cat)
Created Czech (ces)
Created Chamorro (cha)
Created Chechen (che)
Created Chuvash (chv)
Created Cree (cre)
Created Welsh (cym)
Created Danish (dan)
Created German (deu)
Created Dhivehi (div)
Created Dzongkha (dzo)
Created Modern Greek (1453-) (ell)
Created English (eng)
Created Esperanto (epo)
Created Estonian (est)
Created Basque (eus)
Created Ewe (ewe)
Created Faroese (fao)
Created Persian (fas)
Created Fijian (fij)
Created Finnish (fin)
Created French (fra)
Created Western Frisian (fry)
Created Fulah (ful)
Created Irish (gle)
Created Galician (glg)
Created Guarani (grn)
Created Gujarati (guj)
Created Hausa (hau)
Created Serbo-Croatian (hbs)
Created Hebrew (heb)
Created Herero (her)
Created Hindi (hin)
Created Croatian (hrv)
Created Hungarian (hun)
Created Armenian (hye)
Created Igbo (ibo)
Created Indonesian (ind)
Created Icelandic (isl)
Created Italian (ita)
Created Ingrian (izh)
Created Javanese (jav)
Created Japanese (jpn)
Created Kalaallisut (kal)
Created Kannada (kan)
Created Kashmiri (kas)
Created Georgian (kat)
Created Kanuri (kau)
Created Kazakh (kaz)
Created Central Khmer (khm)
Created Kikuyu (kik)
Created Kinyarwanda (kin)
Created Kirghiz (kir)
Created Komi (kom)
Created Kongo (kon)
Created Korean (kor)
Created Kuanyama (kua)
Created Kurdish (kur)
Created Lao (lao)
Created Latin (lat)
Created Latvian (lav)
Created Limburgan (lim)
Created Lingala (lin)
Created Lithuanian (lit)
Created Luxembourgish (ltz)
Created Luba-Katanga (lub)
Created Ganda (lug)
Created Malayalam (mal)
Created Marathi (mar)
Created Macedonian (mkd)
Created Malagasy (mlg)
Created Maltese (mlt)
Created Mongolian (mon)
Created Malay (macrolanguage) (msa)
Created Burmese (mya)
Created Nauru (nau)
Created South Ndebele (nbl)
Created North Ndebele (nde)
Created Ndonga (ndo)
Created Nepali (macrolanguage) (nep)
Created Dutch (nld)
Created Norwegian (nor)
Created Nyanja (nya)
Created Oriya (macrolanguage) (ori)
Created Oromo (orm)
Created Ossetian (oss)
Created Panjabi (pan)
Created Polish (pol)
Created Portuguese (por)
Created Pushto (pus)
Created Quechua (que)
Created Romansh (roh)
Created Romany (rom)
Created Romanian (ron)
Created Rundi (run)
Created Russian (rus)
Created Sango (sag)
Created Scots (sco)
Created Sinhala (sin)
Created Slovak (slk)
Created Slovenian (slv)
Created Sami languages (smi)
Created Samoan (smo)
Created Shona (sna)
Created Sindhi (snd)
Created Somali (som)
Created Southern Sotho (sot)
Created Spanish (spa)
Created Albanian (sqi)
Created Serbian (srp)
Created Swati (ssw)
Created Sundanese (sun)
Created Swahili (macrolanguage) (swa)
Created Swedish (swe)
Created Syriac (syr)
Created Tahitian (tah)
Created Tamil (tam)
Created Tatar (tat)
Created Telugu (tel)
Created Tajik (tgk)
Created Tagalog (tgl)
Created Thai (tha)
Created Tigrinya (tir)
Created Tonga (Tonga Islands) (ton)
Created Tswana (tsn)
Created Tsonga (tso)
Created Turkmen (tuk)
Created Turkish (tur)
Created Twi (twi)
Created Uighur (uig)
Created Ukrainian (ukr)
Created Urdu (urd)
Created Uzbek (uzb)
Created Venda (ven)
Created Vietnamese (vie)
Created Wolof (wol)
Created Xhosa (xho)
Created Yiddish (yid)
Created Yoruba (yor)
Created Zhuang (zha)
Created Chinese (zho)
Created Zulu (zul)
All done!
"""

snapshots["test_add_default_languages 2"] = {
    "aar": {"en": "Afar", "fi": "afar", "sv": "Afar"},
    "abk": {"en": "Abkhazian", "fi": "abhaasi", "sv": "Abchaziska"},
    "afr": {"en": "Afrikaans", "fi": "afrikaans", "sv": "Afrikaans"},
    "aka": {"en": "Akan", "fi": "akan", "sv": "Akan"},
    "amh": {"en": "Amharic", "fi": "amhara", "sv": "Amhariska"},
    "ara": {"en": "Arabic", "fi": "arabia", "sv": "Arabiska"},
    "arg": {"en": "Aragonese", "fi": "aragonia", "sv": "Aragonska"},
    "asm": {"en": "Assamese", "fi": "asami", "sv": "Assamesiska"},
    "ava": {"en": "Avaric", "fi": "avaari", "sv": "Avariska"},
    "aym": {"en": "Aymara", "fi": "aymara", "sv": "Aymara"},
    "aze": {"en": "Azerbaijani", "fi": "azeri", "sv": "Azerbajdzjanska"},
    "bak": {"en": "Bashkir", "fi": "baškiiri", "sv": "Basjkiriska"},
    "bam": {"en": "Bambara", "fi": "bambara", "sv": "Bambara"},
    "bel": {"en": "Belarusian", "fi": "valkovenäjä", "sv": "Vitryska"},
    "ben": {"en": "Bengali", "fi": "bengali", "sv": "Bengali"},
    "bih": {
        "en": "Bihari languages",
        "fi": "Bihari languages",
        "sv": "Bihari languages",
    },
    "bis": {"en": "Bislama", "fi": "bislama", "sv": "Bislama"},
    "bod": {"en": "Tibetan", "fi": "tiibetti", "sv": "Tibetanska"},
    "bos": {"en": "Bosnian", "fi": "bosnia", "sv": "Bosniska"},
    "bul": {"en": "Bulgarian", "fi": "bulgaria", "sv": "Bulgariska"},
    "cat": {"en": "Catalan", "fi": "katalaani", "sv": "Katalanska"},
    "ces": {"en": "Czech", "fi": "tšekki", "sv": "Tjeckiska"},
    "cha": {"en": "Chamorro", "fi": "chamorro", "sv": "Chamorro"},
    "che": {"en": "Chechen", "fi": "tšetšeeni", "sv": "Tjetjenska"},
    "chv": {"en": "Chuvash", "fi": "tšuvassi", "sv": "Tjuvasjiska"},
    "cre": {"en": "Cree", "fi": "cree", "sv": "Cree"},
    "cym": {"en": "Welsh", "fi": "kymri", "sv": "Kymriska"},
    "dan": {"en": "Danish", "fi": "tanska", "sv": "Danska"},
    "deu": {"en": "German", "fi": "saksa", "sv": "Tyska"},
    "div": {"en": "Dhivehi", "fi": "Dhivehi", "sv": "Divehi"},
    "dzo": {"en": "Dzongkha", "fi": "dzongkha", "sv": "Dzongkha"},
    "ell": {
        "en": "Modern Greek (1453-)",
        "fi": "Modern Greek (1453-)",
        "sv": "Modern Greek (1453-)",
    },
    "eng": {"en": "English", "fi": "englanti", "sv": "Engelska"},
    "epo": {"en": "Esperanto", "fi": "esperanto", "sv": "Esperanto"},
    "est": {"en": "Estonian", "fi": "viro", "sv": "Estniska"},
    "eus": {"en": "Basque", "fi": "baski", "sv": "Baskiska"},
    "ewe": {"en": "Ewe", "fi": "ewe", "sv": "Ewe"},
    "fao": {"en": "Faroese", "fi": "fääri", "sv": "Färöiska"},
    "fas": {"en": "Persian", "fi": "persia", "sv": "Persiska"},
    "fij": {"en": "Fijian", "fi": "fidži", "sv": "Fijianska"},
    "fin": {"en": "Finnish", "fi": "suomi", "sv": "Finska"},
    "fra": {"en": "French", "fi": "ranska", "sv": "Franska"},
    "fry": {"en": "Western Frisian", "fi": "Western Frisian", "sv": "frisiska"},
    "ful": {"en": "Fulah", "fi": "fulani", "sv": "Fulani"},
    "gle": {"en": "Irish", "fi": "iiri", "sv": "Iriska"},
    "glg": {"en": "Galician", "fi": "Galician", "sv": "Galiciska"},
    "grn": {"en": "Guarani", "fi": "guarani", "sv": "Guarani"},
    "guj": {"en": "Gujarati", "fi": "gujarati", "sv": "Gujarati"},
    "hau": {"en": "Hausa", "fi": "hausa", "sv": "Haussa"},
    "hbs": {"en": "Serbo-Croatian", "fi": "Serbo-Croatian", "sv": "Serbokroatiska"},
    "heb": {"en": "Hebrew", "fi": "heprea", "sv": "Hebreiska"},
    "her": {"en": "Herero", "fi": "herero", "sv": "Herero"},
    "hin": {"en": "Hindi", "fi": "hindi", "sv": "Hindi"},
    "hrv": {"en": "Croatian", "fi": "kroatia", "sv": "Kroatiska"},
    "hun": {"en": "Hungarian", "fi": "unkari", "sv": "Ungerska"},
    "hye": {"en": "Armenian", "fi": "armenia", "sv": "Armeniska"},
    "ibo": {"en": "Igbo", "fi": "igbo", "sv": "Ibo (Igbo)"},
    "ind": {"en": "Indonesian", "fi": "indonesia", "sv": "Indonesiska"},
    "isl": {"en": "Icelandic", "fi": "islanti", "sv": "Isländska"},
    "ita": {"en": "Italian", "fi": "italia", "sv": "Italienska"},
    "izh": {"en": "Ingrian", "fi": "Ingrian", "sv": "Ingriska"},
    "jav": {"en": "Javanese", "fi": "jaava", "sv": "Javanska"},
    "jpn": {"en": "Japanese", "fi": "japani", "sv": "Japanska"},
    "kal": {"en": "Kalaallisut", "fi": "Kalaallisut", "sv": "Grönländska"},
    "kan": {"en": "Kannada", "fi": "kannada", "sv": "Kanaresiska"},
    "kas": {"en": "Kashmiri", "fi": "kashmiri", "sv": "Kashmiri"},
    "kat": {"en": "Georgian", "fi": "georgia", "sv": "Georgiska"},
    "kau": {"en": "Kanuri", "fi": "kanuri", "sv": "Kanuri"},
    "kaz": {"en": "Kazakh", "fi": "kazakki", "sv": "Kazakiska"},
    "khm": {"en": "Central Khmer", "fi": "Central Khmer", "sv": "Kambodjanska (Khmer)"},
    "kik": {"en": "Kikuyu", "fi": "kikuyu", "sv": "Kikuya"},
    "kin": {"en": "Kinyarwanda", "fi": "ruanda", "sv": "Rwanda"},
    "kir": {"en": "Kirghiz", "fi": "kirgiisi", "sv": "Kirgisiska"},
    "kom": {"en": "Komi", "fi": "komi", "sv": "Komi"},
    "kon": {"en": "Kongo", "fi": "kongo", "sv": "Kikongo"},
    "kor": {"en": "Korean", "fi": "korea", "sv": "Koreanska"},
    "kua": {"en": "Kuanyama", "fi": "kuanjama", "sv": "Ovambo (Kuanyama)"},
    "kur": {"en": "Kurdish", "fi": "kurdi", "sv": "Kurdiska"},
    "lao": {"en": "Lao", "fi": "lao", "sv": "Laotiska"},
    "lat": {"en": "Latin", "fi": "latina", "sv": "Latin"},
    "lav": {"en": "Latvian", "fi": "latvia", "sv": "Lettiska"},
    "lim": {"en": "Limburgan", "fi": "Limburgan", "sv": "Limburgiska"},
    "lin": {"en": "Lingala", "fi": "lingala", "sv": "Lingala"},
    "lit": {"en": "Lithuanian", "fi": "liettua", "sv": "Litauiska"},
    "ltz": {
        "en": "Luxembourgish",
        "fi": "Luxembourgish",
        "sv": "Luxemburgiska (Letzebüergesch)",
    },
    "lub": {"en": "Luba-Katanga", "fi": "luba (Katanga)", "sv": "Luba-Katanga"},
    "lug": {"en": "Ganda", "fi": "ganda", "sv": "Luganda"},
    "mal": {"en": "Malayalam", "fi": "malayalam", "sv": "Malayalam"},
    "mar": {"en": "Marathi", "fi": "marathi", "sv": "Marathi"},
    "mkd": {"en": "Macedonian", "fi": "makedonia", "sv": "Makedonska"},
    "mlg": {"en": "Malagasy", "fi": "malagassi", "sv": "Malagasy"},
    "mlt": {"en": "Maltese", "fi": "malta", "sv": "Maltesiska"},
    "mon": {"en": "Mongolian", "fi": "mongoli", "sv": "Mongoliska"},
    "msa": {
        "en": "Malay (macrolanguage)",
        "fi": "Malay (macrolanguage)",
        "sv": "Malay (macrolanguage)",
    },
    "mya": {"en": "Burmese", "fi": "burma", "sv": "Burmesiska"},
    "nau": {"en": "Nauru", "fi": "nauru", "sv": "Nauru"},
    "nbl": {"en": "South Ndebele", "fi": "South Ndebele", "sv": "Ndebele (Sydafrika)"},
    "nde": {"en": "North Ndebele", "fi": "North Ndebele", "sv": "Ndebele (Zimbabwe)"},
    "ndo": {"en": "Ndonga", "fi": "ndonga", "sv": "Ndonga"},
    "nep": {
        "en": "Nepali (macrolanguage)",
        "fi": "Nepali (macrolanguage)",
        "sv": "Nepali",
    },
    "nld": {"en": "Dutch", "fi": "hollanti", "sv": "Nederländska"},
    "nor": {"en": "Norwegian", "fi": "norja", "sv": "Norska"},
    "nya": {"en": "Nyanja", "fi": "Nyanja", "sv": "Nyanja"},
    "ori": {
        "en": "Oriya (macrolanguage)",
        "fi": "Oriya (macrolanguage)",
        "sv": "Oriya",
    },
    "orm": {"en": "Oromo", "fi": "oromo", "sv": "Oromo"},
    "oss": {"en": "Ossetian", "fi": "Ossetian", "sv": "Ossetiska"},
    "pan": {"en": "Panjabi", "fi": "Panjabi", "sv": "Panjabi"},
    "pol": {"en": "Polish", "fi": "puola", "sv": "Polska"},
    "por": {"en": "Portuguese", "fi": "portugali", "sv": "Portugisiska"},
    "pus": {"en": "Pushto", "fi": "pašto", "sv": "Pashto"},
    "que": {"en": "Quechua", "fi": "ketšua", "sv": "Quechua"},
    "roh": {"en": "Romansh", "fi": "Romansh", "sv": "Rätoromanska"},
    "rom": {"en": "Romany", "fi": "romani", "sv": "Romani"},
    "ron": {"en": "Romanian", "fi": "romania", "sv": "Rumänska"},
    "run": {"en": "Rundi", "fi": "rundi", "sv": "Rundi"},
    "rus": {"en": "Russian", "fi": "venäjä", "sv": "Ryska"},
    "sag": {"en": "Sango", "fi": "sango", "sv": "Sango"},
    "sco": {"en": "Scots", "fi": "skotti", "sv": "Skotska"},
    "sin": {"en": "Sinhala", "fi": "Sinhala", "sv": "Singalesiska"},
    "slk": {"en": "Slovak", "fi": "slovakki", "sv": "Slovakiska"},
    "slv": {"en": "Slovenian", "fi": "sloveeni", "sv": "Slovenska"},
    "smi": {"en": "Sami languages", "fi": "Sami languages", "sv": "Sami languages"},
    "smo": {"en": "Samoan", "fi": "samoa", "sv": "Samoanska"},
    "sna": {"en": "Shona", "fi": "shona", "sv": "Shona"},
    "snd": {"en": "Sindhi", "fi": "sindhi", "sv": "Sindhi"},
    "som": {"en": "Somali", "fi": "somali", "sv": "Somali"},
    "sot": {"en": "Southern Sotho", "fi": "Southern Sotho", "sv": "Sotho"},
    "spa": {"en": "Spanish", "fi": "espanja", "sv": "Spanska"},
    "sqi": {"en": "Albanian", "fi": "albania", "sv": "Albanska"},
    "srp": {"en": "Serbian", "fi": "serbia", "sv": "Serbiska"},
    "ssw": {"en": "Swati", "fi": "swazi", "sv": "Swazi"},
    "sun": {"en": "Sundanese", "fi": "sunda", "sv": "Sundanesiska"},
    "swa": {
        "en": "Swahili (macrolanguage)",
        "fi": "Swahili (macrolanguage)",
        "sv": "Swahili",
    },
    "swe": {"en": "Swedish", "fi": "ruotsi", "sv": "Svenska"},
    "syr": {"en": "Syriac", "fi": "syyria", "sv": "Syriska"},
    "tah": {"en": "Tahitian", "fi": "tahiti", "sv": "Tahitiska"},
    "tam": {"en": "Tamil", "fi": "tamili", "sv": "Tamil"},
    "tat": {"en": "Tatar", "fi": "tataari", "sv": "Tatariska"},
    "tel": {"en": "Telugu", "fi": "telugu", "sv": "Telugu"},
    "tgk": {"en": "Tajik", "fi": "tadžikki", "sv": "Tadzjikiska"},
    "tgl": {"en": "Tagalog", "fi": "tagalog", "sv": "Tagalog"},
    "tha": {"en": "Thai", "fi": "thai", "sv": "Thailändska"},
    "tir": {"en": "Tigrinya", "fi": "tigrinya", "sv": "Tigrinja"},
    "ton": {
        "en": "Tonga (Tonga Islands)",
        "fi": "Tongan tonga",
        "sv": "Tonga (Tongaöarna)",
    },
    "tsn": {"en": "Tswana", "fi": "tswana", "sv": "Tswana"},
    "tso": {"en": "Tsonga", "fi": "tsonga", "sv": "Tsonga"},
    "tuk": {"en": "Turkmen", "fi": "turkmeeni", "sv": "Turkmeniska"},
    "tur": {"en": "Turkish", "fi": "turkki", "sv": "Turkiska"},
    "twi": {"en": "Twi", "fi": "twi", "sv": "Twi"},
    "uig": {"en": "Uighur", "fi": "uiguuri", "sv": "Uiguriska"},
    "ukr": {"en": "Ukrainian", "fi": "ukraina", "sv": "Ukrainska"},
    "urd": {"en": "Urdu", "fi": "urdu", "sv": "Urdu"},
    "uzb": {"en": "Uzbek", "fi": "uzbekki", "sv": "Uzbekiska"},
    "ven": {"en": "Venda", "fi": "venda", "sv": "Venda"},
    "vie": {"en": "Vietnamese", "fi": "vietnam", "sv": "Vietnamesiska"},
    "wol": {"en": "Wolof", "fi": "wolof", "sv": "Wolof"},
    "xho": {"en": "Xhosa", "fi": "xhosa", "sv": "Xhosa"},
    "yid": {"en": "Yiddish", "fi": "jiddiš", "sv": "Jiddisch"},
    "yor": {"en": "Yoruba", "fi": "yoruba", "sv": "Yoruba"},
    "zha": {"en": "Zhuang", "fi": "Zhuang", "sv": "Zhuang"},
    "zho": {"en": "Chinese", "fi": "kiina", "sv": "Kinesiska"},
    "zul": {"en": "Zulu", "fi": "zulu", "sv": "Zulu"},
}

snapshots[
    "test_add_languages 1"
] = """Created Manide (abd)
Created Ngelima (agh)
All done!
"""

snapshots["test_add_languages 2"] = {
    "abd": {"en": "Manide", "fi": "Manide", "sv": "Manide"},
    "agh": {"en": "Ngelima", "fi": "Ngelima", "sv": "Ngelima"},
}

snapshots[
    "test_add_languages_and_flush 1"
] = """Flushed existing languages
Created Manide (abd)
Created Ngelima (agh)
All done!
"""

snapshots["test_add_languages_and_flush 2"] = {
    "abd": {"en": "Manide", "fi": "Manide", "sv": "Manide"},
    "agh": {"en": "Ngelima", "fi": "Ngelima", "sv": "Ngelima"},
}
