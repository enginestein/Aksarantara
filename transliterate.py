import Map
from trans import Transliterator
import convert, post_options, post_processing, pre_processing
import fixer
import json
import requests
import html
import itertools
from collections import Counter
import unicodedata
import collections
import yaml
import warnings
import langcodes
from inspect import getmembers, isfunction


def removeA(a):
    if a.count("a") == 1:
        return a.replace("a", "")


def unique_everseen(iterable, key=None):
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in itertools.filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element


def auto_detect(text, plugin=False):
    scripts = []

    for uchar in text:
        try:
            script_name = unicodedata.name(uchar).split(" ")[0].lower()
            if script_name != "old":
                scripts.append(script_name)
            else:
                scripts.append(unicodedata.name(uchar).split(" ")[1].lower())
        except ValueError:
            pass

    counts = Counter(scripts)
    script_percent = []

    for script, count in counts.items():
        percent = count / len(scripts) * 100
        script_percent.append((percent, script))

    if not plugin:
        if len(script_percent) > 0:
            script = sorted(script_percent)[-1][1]
        else:
            script = ""
    else:
        if len(script_percent) > 0:
            if sorted(script_percent)[-1][1] == "latin":
                script = sorted(script_percent)[-2][1]
            else:
                script = sorted(script_percent)[-1][1]
        else:
            script = ""

    inputScript = script[0].upper() + script[1:]

    laoPali = [
        "ຆ",
        "ຉ",
        "ຌ",
        "ຎ",
        "ຏ",
        "ຐ",
        "ຑ",
        "ຒ",
        "ຓ",
        "ຘ",
        "ຠ",
        "ຨ",
        "ຩ",
        "ຬ",
        "຺",
    ]

    if inputScript == "Bengali":
        if "ৰ" in text or "ৱ" in text:
            inputScript = "Assamese"
    elif inputScript == "Lao":
        if any(char in text for char in laoPali):
            inputScript = "LaoPali"
    elif inputScript == "Batak":
        inputScript = "BatakKaro"
    elif inputScript == "Myanmar":
        inputScript = "Burmese"

        mon = ["ၚ", "ၛ", "္ည", "ၞ", "ၟ", "ၠ", "ဳ", "ဨ"]
        if any([char in text for char in mon]):
            inputScript = "Mon"

        countSub = {"Shan": 0, "TaiLaing": 0, "KhamtiShan": 0}

        text = text.replace("ႃ", "")

        for uchar in text:
            try:
                char = unicodedata.name(uchar).lower()
            except:
                pass
            if "shan" in char:
                countSub["Shan"] += 1
            elif "tai laing" in char:
                countSub["TaiLaing"] += 1
            elif "khamti" in char:
                countSub["KhamtiShan"] += 1

        import operator

        sorted_x = sorted(countSub.items(), key=operator.itemgetter(1))

        if (
            countSub["Shan"] > 0
            or countSub["TaiLaing"] > 0
            or countSub["KhamtiShan"] > 0
        ):
            inputScript = sorted_x[-1][0]

    elif inputScript == "Meetei":
        inputScript = "MeeteiMayek"
    elif inputScript == "Persian":
        inputScript = "OldPersian"
    elif inputScript == "Phags-pa":
        inputScript = "PhagsPa"
    elif inputScript == "Ol":
        inputScript = "Santali"
    elif inputScript == "Sora":
        inputScript = "SoraSompeng"
    elif inputScript == "Syloti":
        inputScript = "SylotiNagri"
    elif inputScript == "Tai":
        inputScript = "TaiTham"
    elif inputScript == "Warang":
        inputScript = "WarangCiti"
    elif inputScript == "Siddham":
        preOptions = "siddhamUnicode"
    elif inputScript == "Cyrillic":
        inputScript = "RussianCyrillic"
    elif inputScript == "Zanabazar":
        inputScript = "ZanabazarSquare"
    elif inputScript == "Syriac":
        inputScript = "Syre"
        eastern_dia = "ܲ ܵ ܝܼ ܘܼ ܸ ܹ ܘܿ".split(" ")
        if any(char in text for char in eastern_dia):
            inputScript = "Syrn"
        western_dia = "ܰ ܺ ܶ ّ ܽ".split(" ")
        if any(char in text for char in western_dia):
            inputScript = "Syrj"
    elif inputScript == "Arabic":
        inputScript = "Arab"
        persian_char = "چ گ ژ پ هٔ".split(" ")
        if any(char in text for char in persian_char):
            inputScript = "Arab-Fa"
        urdu_char = "ڈ ٹ ڑ ھ".split(" ")
        if any(char in text for char in urdu_char):
            inputScript = "Urdu"
        shahmukh_char = "ݨ لؕ مھ نھ یھ رھ لھ وھ".split(" ")
        if any(char in text for char in shahmukh_char):
            inputScript = "Shahmukhi"
    elif inputScript == "Latin":
        diacritics = [
            "ā",
            "ī",
            "ū",
            "ṃ",
            "ḥ",
            "ś",
            "ṣ",
            "ṇ",
            "ṛ",
            "ṝ",
            "ḷ",
            "ḹ",
            "ḻ",
            "ṉ",
            "ṟ",
            "ṭ",
            "ḍ",
            "ṅ",
            "ñ",
        ]
        Itrans = ["R^i", "R^I", "L^i", "L^I", ".N", "~N", "~n", "Ch", "sh", "Sh"]
        semitic = ["ʾ", "ʿ", "š", "w"]
        BurmeseLOC = ["´", "˝", "ʻ"]
        if "ʰ" in text:
            inputScript = "Titus"
        elif any(char in text for char in semitic):
            inputScript = "Latn"
        elif any(char in text for char in BurmeseLOC):
            inputScript = "IASTLOC"
        elif any(char in text for char in diacritics):
            if "ē" in text or "ō" in text or "r̥" in text:
                inputScript = "ISO"
            else:
                inputScript = "IAST"
        elif any(char in text for char in Itrans):
            inputScript = "Itrans"
        else:
            inputScript = "HK"
    elif (
        inputScript in Map.IndicScripts
        or inputScript in Map.LatinScripts
        or inputScript in ["Hiragana", "Katakana"]
    ):
        pass
    else:
        import trans

        tr = trans.Transliterator()
        inputScript = tr.auto_script(text)

    return inputScript


def detect_preoptions(text, inputScript):
    preoptions = []
    if inputScript == "Thai":
        textNew = text.replace("ห์", "")
        if "\u035C" in text or "\u0325" in text or "งํ" in text or "\u0E47" in text:
            preoptions = ["ThaiPhonetic"]
        elif "์" in textNew and ("ะ" in text):
            preoptions = ["ThaiSajjhayawithA"]
        elif "์" in textNew:
            preoptions = ["ThaiSajjhayaOrthography"]
        elif "ะ" in text or "ั" in text:
            preoptions = ["ThaiOrthography"]
    elif inputScript == "Lao" or inputScript == "LaoPali":
        textNew = text.replace("ຫ໌", "")
        if "໌" in textNew and ("ະ" in text):
            preoptions = ["LaoSajhayaOrthographywithA"]
        elif "໌" in textNew:
            preoptions = ["LaoSajhayaOrthography"]
        elif "ະ" in text or "ັ" in text:
            preoptions = ["LaoTranscription"]
    elif inputScript == "Urdu":
        preoptions = ["UrduShortNotShown"]

    return preoptions


def Convert(src, tgt, txt, nativize, preoptions, postoptions):
    tgtOld = ""

    if tgt == "IASTLOC" and src != "Burmese":
        txt = Convert(src, "Burmese", txt, nativize, preoptions, postoptions)
        src = "Burmese"

    if tgt == "IASTLOC" and src == "Burmese":
        preoptions = preoptions + [tgt + src + "Target"]
        postoptions = [tgt + src + "Target"] + postoptions
        nativize = False

    if src == "IASTLOC" and tgt == "Burmese":
        preoptions = [src + tgt + "Source"] + preoptions
        postoptions = [src + tgt + "Source"] + postoptions
        nativize = False

    if src == "IASTLOC" and tgt != "Burmese":
        txt = Convert(src, "Burmese", txt, nativize, preoptions, postoptions)
        src = "Burmese"

    if tgt in Map.semiticISO.keys():
        if Map.semiticISO[tgt] != src:
            txt = Convert(
                src, Map.semiticISO[tgt], txt, nativize, preoptions, postoptions
            )
            src = Map.semiticISO[tgt]

        if Map.semiticISO[tgt] == src:
            preoptions = [tgt + "Target"] + preoptions
            postoptions = [tgt + "Target"] + postoptions
            nativize = False
            tgt = "Latn"

    if src in Map.semiticISO.keys():
        if Map.semiticISO[src] == tgt:
            preoptions = [src + "Source"] + preoptions
            postoptions = [src + "Source"] + postoptions
            src = "Latn"
        else:
            txt = Convert(
                src, Map.semiticISO[src], txt, nativize, preoptions, postoptions
            )
            src = Map.semiticISO[src]

    if tgt == "" or tgt == "Ignore":
        return txt
    if preoptions == [] and postoptions == [] and nativize == False and src == tgt:
        return txt

    IndicSemiticMapping = {
        "Hebrew": "Hebr",
        "Thaana": "Thaa",
        "Urdu": "Arab-Ur",
        "Shahmukhi": "Arab-Pa",
    }

    if (
        tgt in Map.SemiticScripts or tgt in Map.semiticISO.keys()
    ) and src in IndicSemiticMapping.keys():
        src = IndicSemiticMapping[src]
    if (
        src in Map.SemiticScripts or src in Map.semiticISO.keys()
    ) and tgt in IndicSemiticMapping.keys():
        tgt = IndicSemiticMapping[tgt]
    if src in IndicSemiticMapping.keys() and tgt in IndicSemiticMapping.keys():
        src = IndicSemiticMapping[src]
        tgt = IndicSemiticMapping[tgt]

    if not nativize and src == "Hebrew":
        src = "Hebr"
    if not nativize and src == "Urdu":
        src = "Arab-Ur"
    if not nativize and src == "Shahmukhi":
        src = "Arab-Pa"
    if not nativize and src == "Thaana":
        src = "Thaa"

    if src in ["Arab-Ur", "Arab-Pa"] and tgt in Map.IndicScripts:
        txt += "\u05CD"

    if nativize:
        if src in Map.SemiticScripts and tgt in Map.IndicScripts:
            txt += "\u05CC"

    if (
        src == tgt
        and (src != "Hiragana" and src != "Katakana")
        and src not in Map.SemiticScripts
    ):
        tgtOld = tgt
        tgt = "Devanagari"

    txt = pre_processing.PreProcess(txt, src, tgt)

    if "siddhammukta" in postoptions and tgt == "Siddham":
        tgt = "SiddhamDevanagari"
    if "siddhamap" in postoptions and tgt == "Siddham":
        tgt = "SiddhamDevanagari"
    if "siddhammukta" in preoptions and src == "Siddham":
        src = "SiddhamDevanagari"
    if "LaoNative" in postoptions and tgt == "Lao":
        tgt = "Lao2"
    if "egrantamil" in preoptions and src == "Grantha":
        src = "GranthaGrantamil"
    if "egrantamil" in postoptions and tgt == "Grantha":
        tgt = "GranthaGrantamil"
    if "nepaldevafont" in postoptions and tgt == "Newa":
        tgt = "Devanagari"
    if "ranjanalantsa" in postoptions and tgt == "Ranjana":
        tgt = "Tibetan"
        nativize = False
    if "ranjanawartu" in postoptions and tgt == "Ranjana":
        tgt = "Tibetan"
        nativize = False
    if "SoyomboFinals" in postoptions and tgt == "Soyombo":
        txt = "\u02BE" + txt

    for options in preoptions:
        txt = getattr(pre_processing, options)(txt)

    if "novowelshebrew" in preoptions and src == "Hebr":
        txt = txt.replace("\u05B7", "")

    srcOld = ""

    if (
        (src != "Latn" and src != "Type" and src in Map.SemiticScripts)
        or (
            src in Map.IndicScripts
            and tgt in Map.SemiticScripts
            and src not in Map.LatinScripts
        )
        or (src in ["Hiragana", "Katakana"])
    ):
        txt = pre_processing.retainLatin(txt)

    if src == "Hiragana" or src == "Katakana":
        txt = pre_processing.JapanesePreProcess(src, txt, preoptions)
        srcOld = "Japanese"
        src = "ISO"

    if tgt == "Hiragana" or tgt == "Katakana":
        txt = post_processing.JapanesePostProcess(src, tgt, txt, nativize, postoptions)

    if src == "Oriya" and tgt == "IPA":
        txt = fixer.OriyaIPAFixPre(txt)

    if src == "Itrans" and "##" in txt:
        transliteration = ""
        for i, word in enumerate(txt.split("##")):
            if i % 2 == 0:
                transliteration += convert.convertScript(word, src, tgt)
            else:
                transliteration += word
    else:
        transliteration = convert.convertScript(txt, src, tgt)

    if (
        srcOld == "Japanese"
        and tgt != "Devanagari"
        and "siddhammukta" not in postoptions
    ):
        transliteration = convert.convertScript(transliteration, "Devanagari", "ISO")

    if src == tgtOld:
        tgt = tgtOld
        transliteration = convert.convertScript(transliteration, "Devanagari", tgt)

    if (
        src not in Map.SemiticScripts and tgt == "Arab" and nativize
    ) or "arabicRemoveAdditionsPhonetic" in postoptions:
        transliteration = getattr(post_processing, "arabicRemoveAdditionsPhonetic")(
            transliteration
        )

    if nativize:
        transliteration = post_options.ApplyScriptDefaults(
            transliteration, src, tgt, postoptions
        )
        if tgt != "Latn":
            if tgt != "Tamil":
                transliteration = post_processing.RemoveDiacritics(transliteration)
            else:
                transliteration = post_processing.RemoveDiacriticsTamil(transliteration)

    if "RemoveDiacritics" in postoptions:
        if tgt == "Tamil":
            postoptions = map(
                lambda x: "RemoveDiacriticsTamil" if x == "RemoveDiacritics" else x,
                postoptions,
            )

    for options in postoptions:
        transliteration = getattr(post_processing, options)(transliteration)

    if src == "Tamil" and tgt == "IPA":
        r = requests.get("http://anunaadam.appspot.com/api?text=" + txt + "&method=2")
        r.encoding = r.apparent_encoding
        transliteration = r.text

    if src == "Oriya" and tgt == "IPA":
        transliteration = fixer.OriyaIPAFix(transliteration)

    transliteration = pre_processing.retainLatin(transliteration, reverse=True)
    transliteration = post_processing.defaultPost(transliteration)

    return transliteration


def process(
    src, tgt, txt, nativize=True, post_options=[], pre_options=[], param="default"
):
    if param == "default":
        return process_default(src, tgt, txt, nativize, post_options, pre_options)

    if param == "script_code":
        return process_script_tag(src, tgt, txt, nativize, post_options, pre_options)

    if param == "lang_code":
        return process_lang_tag(src, tgt, txt, nativize, post_options, pre_options)

    if param == "lang_name":
        return process_lang_name(src, tgt, txt, nativize, post_options, pre_options)


import functools


@functools.cache
def _load_data(file_path):
    import os

    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(file_path, "r", encoding="utf8") as stream:
        data_loaded = yaml.safe_load(stream)
    return data_loaded


def convert_default(src, tgt, txt, nativize=True, post_options=[], pre_options=[]):
    data_loaded = _load_data("scripts.yaml")

    scriptList = Map.IndicScripts + Map.LatinScripts + Map.SemiticScripts

    preOptionList = list(map(lambda x: x[0], getmembers(pre_processing, isfunction)))
    preOptionListLower = list(map(lambda x: x.lower(), preOptionList))

    postOptionList = list(map(lambda x: x[0], getmembers(post_processing, isfunction)))
    postOptionListLower = list(map(lambda x: x.lower(), postOptionList))

    post_options = [
        option_id
        for option in post_options
        for option_id in postOptionList
        if option.lower() == option_id.lower()
    ]
    pre_options = [
        option_id
        for option in pre_options
        for option_id in preOptionList
        if option.lower() == option_id.lower()
    ]

    font_hack_warning = (
        tgt
        + " uses an hacked font to display the script. In the absence of this font, you text may appear different. \n See: https://aksharamukha.appspot.com/describe/"
        + tgt
        + " for the font used"
    )

    if tgt in data_loaded and "font_hack" in data_loaded[tgt]:
        warnings.warn(font_hack_warning)

    if src not in scriptList:
        script_not_found = (
            "Source script: "
            + src
            + " not found in the list of scripts supported. The text will not be transliterated."
        )
        warnings.warn(script_not_found)

    if tgt not in scriptList:
        script_not_found = (
            "Target script: "
            + tgt
            + " not found in the list of scripts supported. The text will not be transliterated."
        )
        warnings.warn(script_not_found)

    return Convert(src, tgt, txt, nativize, pre_options, post_options)


def process_default(src, tgt, txt, nativize, post_options, pre_options):
    scriptList = Map.IndicScripts + Map.LatinScripts
    scriptListLower = list(map(lambda x: x.lower(), scriptList))

    if src == "autodetect":
        src = auto_detect(txt)
        pre_options = detect_preoptions(txt, src)
    elif src.lower() in scriptListLower:
        src = [
            script_id for script_id in scriptList if src.lower() == script_id.lower()
        ][0]

    if tgt.lower() in scriptListLower:
        tgt = [
            script_id for script_id in scriptList if tgt.lower() == script_id.lower()
        ][0]

    return convert_default(src, tgt, txt, nativize, post_options, pre_options)


def process_script_tag(src_tag, tgt_tag, txt, nativize, post_options, pre_options):
    data_loaded = _load_data("scripts.yaml")

    data_loaded_wiki = _load_data("data.yaml")

    src = []
    tgt = []

    if src_tag == "Syrc":
        src_tag = "Syre"
        warnings.warn(
            "Please specify the variety of Syriac script for the source: Estrangelo (Syre), Eastern (Syrn) or Wester (Syrj). Defaulting to Syre"
        )
    if tgt_tag == "Syrc":
        tgt_tag = "Syre"
        warnings.warn(
            "Please specify the variety of Syriac script for the target: Estrangelo (Syre), Eastern (Syrn) or Wester (Syrj). Defaulting to Syre"
        )

    for scrpt in data_loaded.keys():
        scrpt_tag = data_loaded[scrpt]["script"]

        if "lang" in data_loaded[scrpt].keys():
            lang_tag = data_loaded[scrpt]["lang"].split(",")[0]
            lang = list(map(lambda x: x.lower(), data_loaded[scrpt]["lang"].split(",")))
        else:
            population = 0
            lang = ""

        if (
            scrpt_tag in data_loaded_wiki.keys()
            and lang_tag in data_loaded_wiki[scrpt_tag].keys()
        ):
            population = data_loaded_wiki[scrpt_tag][lang_tag]["population"]
        else:
            population = 0
        if (
            "-" not in src_tag
            and data_loaded[scrpt]["script"].lower() == src_tag.lower()
        ):
            src.append((population, scrpt))

        if (
            "-" not in tgt_tag
            and data_loaded[scrpt]["script"].lower() == tgt_tag.lower()
        ):
            tgt.append((population, scrpt))

        if "-" in tgt_tag:
            lang_part = tgt_tag.split("-")[0].lower()
            script_part = tgt_tag.split("-")[1].lower()

            if (
                scrpt_tag.lower() == script_part.lower()
                and "lang" in data_loaded[scrpt].keys()
                and lang_part.lower() in lang
            ):
                tgt.append((0, scrpt))

        if "-" in src_tag:
            lang_part = src_tag.split("-")[0].lower()
            script_part = src_tag.split("-")[1].lower()

            if (
                scrpt_tag.lower() == script_part.lower()
                and "lang" in data_loaded[scrpt].keys()
                and lang_part.lower() in lang
            ):
                src.append((0, scrpt))



        tgt = [(0, "ISO")]

    if "-" in src_tag and src_tag.split("-")[0].lower() in ["latn", "en", "eng"]:
        src = [(0, src_tag.split("-")[1])]

    if "-" in tgt_tag and tgt_tag.split("-")[0].lower() in ["latn", "en", "eng"]:
        tgt = [(0, tgt_tag.split("-")[1])]

    if src_tag == "autodetect":
        src = [(0, auto_detect(txt))]
        pre_options = detect_preoptions(txt, src)

    if len(src) > 0:
        src_pop = sorted(src, reverse=True)[0][1]
    elif src_tag in Map.SemiticScripts:
        src_pop = src_tag
    else:
        raise Exception("Source script code: " + src_tag + " not found")

    if len(tgt) > 0:
        tgt_pop = sorted(tgt, reverse=True)[0][1]
    elif tgt_tag in Map.SemiticScripts:
        tgt_pop = tgt_tag
    else:
        raise Exception("Target script code: " + tgt_tag + " not found")


    return process_default(src_pop, tgt_pop, txt, nativize, post_options, pre_options)


def process_lang_tag(src_tag, tgt_tag, txt, nativize, post_options, pre_options):
    data_loaded = _load_data("scripts.yaml")

    data_loaded_wiki = _load_data("data.yaml")

    src = []
    tgt = []

    for scrpt in data_loaded.keys():
        if "lang" in data_loaded[scrpt].keys():
            lang = list(map(lambda x: x.lower(), data_loaded[scrpt]["lang"].split(",")))
        else:
            lang = ""

        scrpt_tag = data_loaded[scrpt]["script"]

        if scrpt_tag in data_loaded_wiki.keys():
            script_count = len(data_loaded_wiki[scrpt_tag])
        else:
            script_count = 1

        if src_tag.lower() in lang:
            src.append((script_count, scrpt))

        if tgt_tag.lower() in lang:
            tgt.append((script_count, scrpt))

        if "-" in tgt_tag:
            lang_part = tgt_tag.split("-")[0].lower()
            script_part = tgt_tag.split("-")[1].lower()

            if scrpt_tag.lower() == script_part and lang_part in lang:
                tgt.append((0, scrpt))

        if "-" in src_tag:
            lang_part = src_tag.split("-")[0].lower()
            script_part = src_tag.split("-")[1].lower()

            if scrpt_tag.lower() == script_part and lang_part in lang:
                src.append((0, scrpt))




        tgt = [(0, "Devanagari")]

    if "-" in src_tag and src_tag.split("-")[0].lower() in ["sa", "san", "pi", "pli"]:
        for scrpt in data_loaded.keys():
            scrpt_tag = data_loaded[scrpt]["script"]

            if scrpt_tag.lower() == src_tag.split("-")[1].lower():
                src = [(0, scrpt)]

    if "-" in tgt_tag and tgt_tag.split("-")[0].lower() in ["sa", "san", "pi", "pli"]:
        for scrpt in data_loaded.keys():
            scrpt_tag = data_loaded[scrpt]["script"]

            if scrpt_tag.lower() == tgt_tag.split("-")[1].lower():
                tgt = [(0, scrpt)]


    if "-" in src_tag and src_tag.split("-")[0].lower() in ["la", "en", "eng"]:
        src = [(0, src_tag.split("-")[1])]

    if "-" in tgt_tag and tgt_tag.split("-")[0].lower() in ["la", "en", "eng"]:
        tgt = [(0, tgt_tag.split("-")[1])]

    if src_tag == "autodetect":
        src = [(0, auto_detect(txt))]
        pre_options = detect_preoptions(txt, src)

    if len(src) > 0:
        src_pop = sorted(src, reverse=True)[0][1]
    else:
        raise Exception("Source language code: " + src_tag + " not found")

    if len(tgt) > 0:
        tgt_pop = sorted(tgt, reverse=True)[0][1]
    else:
        raise Exception("Target language code: " + tgt_tag + " not found")

    return process_default(src_pop, tgt_pop, txt, nativize, post_options, pre_options)


def process_lang_name(src_name, tgt_name, txt, nativize, post_options, pre_options):
    if src_name == "autodetect":
        src = auto_detect(txt)
        pre_options = detect_preoptions(txt, src)
    else:
        src = str(langcodes.find(src_name))

    tgt = str(langcodes.find(tgt_name))

    return process_lang_tag(src, tgt, txt, nativize, post_options, pre_options)


@functools.cache
def get_semitic_json():
    from pathlib import Path

    cwd = Path(Path(__file__).parent)
    with open(Path(cwd, "data.json"), "r", encoding="utf-8") as f:
        data = json.load(f)

    return data