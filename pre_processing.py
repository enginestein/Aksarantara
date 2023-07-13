from ast import Str
from asyncio import constants
import Map as GM
import re
import string
import post_processing
import fixer as CF
from East import PhagsPa, Burmese
from Core import Tamil, Malayalam, Limbu, Chakma


def BengaliSubojinedVa(Strng):
    Strng = re.sub("(?<![মব])(্ব)", "্ভ়", Strng)

    return Strng


def IASTLOCBurmeseSource(Strng):
    chars_misc = {"e*": "၏", "n*": "၌", "r*": "၍", "l*": "၎"}

    for lat, bur in chars_misc.items():
        Strng = Strng.replace(lat, bur)

    Strng = Strng.replace("ṁ", "ṃ")

    Strng = Strng.replace(",", "၊").replace(".", "။")

    Strng = Strng.replace("˝", "ʺ").replace("ʺ", "ḥ")

    Strng = Strng.replace("´", "ʹ").replace("ʹ", "˳")

    vowelSigns = "|".join(GM.CrunchSymbols(GM.VowelSignsNV, "IAST"))
    Strng = re.sub("(ʼ)(a|" + vowelSigns + ")", "’" + r"\2", Strng)

    consonants = "|".join(GM.CrunchSymbols(GM.Consonants, "IAST"))
    Strng = re.sub("(" + consonants + ")(‘)", r"\1" + "ʻ", Strng)

    Strng = Strng.replace("o‘", "oʻ")

    Strng = Strng.replace("oʻ", "au")

    return Strng


def segmentBurmeseSyllables(Strng):
    myConsonant = r"က-အ"
    otherChar = r"ဣဤဥဦဧဩဪဿ၌၍၏၀-၉၊။!-/:-@[-`{-~\s"
    ssSymbol = r"္"
    aThat = r"်"

    BreakPattern = re.compile(
        r"((?<!"
        + ssSymbol
        + r")["
        + myConsonant
        + r"](?!["
        + aThat
        + ssSymbol
        + r"])"
        + r"|["
        + otherChar
        + r"])",
        re.UNICODE,
    )
    Strng = Strng.replace("့်", "့်")
    Strng = BreakPattern.sub(" " + r"\1", Strng)

    return Strng


def IASTLOCBurmeseTarget(Strng):
    Strng = Strng.replace("\u103A\u1039", "\u1039")

    Strng = Strng.replace("\u102D\u102F", "\u102F\u102D")

    Strng = Strng.replace("ဪ", "ဩʻ")

    yrvh = (
        Burmese.ConsonantMap[25:27]
        + Burmese.ConsonantMap[28:29]
        + Burmese.ConsonantMap[32:33]
    )
    yrvhsub = ["\u103B", "\u103C", "\u103D", "\u103E"]
    vir = Burmese.ViramaMap[0]

    for x, y in zip(yrvh, yrvhsub):
        Strng = Strng.replace(y, vir + vir + x)

    Strng = Strng.replace("့်", "့်")

    aThat = r"်"
    Strng = Strng.replace(aThat, aThat + "ʻ")

    Strng = Strng.replace("အ", "’အ")

    vowDep = "အော် အော အိ အီ အု အူ အေ".split(" ")
    vowIndep = "ဪ ဩ ဣ ဤ ဥ ဦ ဧ".split(" ")

    for x, y in zip(vowDep, vowIndep):
        Strng = Strng.replace(x, y)

    Strng = Strng.replace("၊", ",").replace("။", ".")

    return Strng


def insertViramaSyriac(Strng):
    Strng += "\uF001"
    return Strng


def BengaliSwitchYaYYa(Strng):
    Strng = re.sub("(?<!\u09CD)য", "@#$", Strng)
    Strng = re.sub("য়", "য", Strng)
    Strng = Strng.replace("@#$", "য়")

    return Strng


def removeFinalSchwaArab(Strng):
    diacrtics = ["\u0652", "\u064E", "\u0650", "\u064F"]
    Strng = re.sub(
        "([\u0628-\u0647])(?![\u0652\u064E\u0650\u064F\u0651\u064B\u064C\u064D\u0649])(?=(\W|$))",
        r"\1" + "\u0652",
        Strng,
    )
    Strng = re.sub(
        "([\u0628-\u0647]\u0651)(?![\u0652\u064E\u0650\u064F\u064B\u064C\u064D\u0649])(?=(\W|$))",
        r"\1" + "\u0652",
        Strng,
    )
    Strng = re.sub(
        "(?<!\u0650)([\u064A])(?![\u0651\u0652\u064E\u0650\u064F\u064B\u064C\u064D\u0649])(?=(\W|$))",
        r"\1" + "\u0652",
        Strng,
    )
    Strng = re.sub(
        "(?<!\u0650)([\u064A]\u0651)(?![\u0652\u064E\u0650\u064F\u064B\u064C\u064D\u0649])(?=(\W|$))",
        r"\1" + "\u0652",
        Strng,
    )
    Strng = re.sub(
        "(?<!\u064F)([\u0648])(?![\u0651\u0652\u064E\u0650\u064F\u064B\u064C\u064D\u0649])(?=(\W|$))",
        r"\1" + "\u0652",
        Strng,
    )
    Strng = re.sub(
        "(?<!\u064F)([\u0648]\u0651)(?![\u0652\u064E\u0650\u064F\u064B\u064C\u064D\u0649])(?=(\W|$))",
        r"\1" + "\u0652",
        Strng,
    )

    return Strng


def AlephMaterLectionis(Strng, target="semitic"):
    Strng += "\u05CD"

    return Strng


def FixSemiticRoman(Strng, Source):
    vir = "\u033D"

    if "\u05CD" in Strng:
        Strng = post_processing.AlephMaterLectionis(Strng)

    if "\u05CC" in Strng:
        Strng = post_processing.removeSemiticLetters(Strng)

        AyinAlephInitial = [
            ("ʾa", "ʾ"),
            ("ʾā", "ā̂"),
            ("ʾi", "î"),
            ("ʾī", "ī̂"),
            ("ʾu", "û"),
            ("ʾū", "ū̂"),
            ("ʾe", "ê"),
            ("ʾē", "ē̂"),
            ("ʾo", "ô"),
            ("ʾō", "ō̂"),
        ]

        for x, y in AyinAlephInitial:
            Strng = Strng.replace(x, y)

        if Source == "Arab":
            Strng = post_processing.arabizeLatn(Strng, target="indic")
        elif Source == "Arab-Ur" or Source == "Arab-Pa" or Source == "Arab-Fa":
            Strng = post_processing.urduizeLatn(Strng, target="indic")
        elif Source == "Syrn":
            Strng = post_processing.syricizeLatn(Strng, target="indic")
        elif Source == "Syrj" or Source == "Hebr":
            Strng = post_processing.hebraizeLatn(Strng, target="indic")

    Strng = Strng.replace("\u032A", "").replace("\u032E", "")

    Strng = re.sub("([ʰ])(꞉)", r"\2\1", Strng)

    Strng = re.sub("([aiuāīū])(꞉)", r"\2\1", Strng)
    Strng = re.sub("(.)(꞉)", r"\1" + vir + r"\1", Strng)

    Strng = Strng.replace("ʿ" + vir, "ʿ" + vir + "\u200B")

    cons_prev = "|".join(GM.SemiticConsonants)

    if "Syr" in Source:
        consSyrc = "|".join(
            [
                "ʾ",
                "b",
                "v",
                "g",
                "ġ",
                "d",
                "ḏ",
                "h",
                "w",
                "z",
                "ḥ",
                "ṭ",
                "y",
                "k",
                "ḫ",
                "l",
                "m",
                "n",
                "s",
                "ʿ",
                "p",
                "f",
                "ṣ",
                "q",
                "r",
                "š",
                "t",
                "ṯ",
                "č",
                "ž",
                "j",
            ]
        )
        vowelSyrc = ["a", "ā", "e", "ē", "ū", "ō", "ī", "â", "ā̂", "ê", "ē̂"]

        vowelsDepSyrc = "|".join(["a", "ā", "e", "ē", "u", "i", "o"])
        vowelsInDepSyrc1 = ["i", "u", "o"]
        vowelsInDepSyrc2 = ["ī̂", "û", "ô"]

        if any([vow in Strng for vow in vowelSyrc]):
            Strng = Strng.replace("ī", "i").replace("ū", "u").replace("ō", "o")

            for vow1, vow2 in zip(vowelsInDepSyrc1, vowelsInDepSyrc2):
                Strng = re.sub("(?<!\w)" + vow1, vow2, Strng)

            Strng = Strng.replace("̂̂", "̂").replace("ô̂", "ô")

            if "\uF001" in Strng:
                Strng = re.sub(
                    "(" + consSyrc + ")" + "(?!" + vowelsDepSyrc + ")",
                    r"\1" + vir,
                    Strng,
                )

            Strng = re.sub("(?<=" + cons_prev + ")" + "a(?!\u0304)", "", Strng)

        Strng = Strng.replace("\uF001", "")

    if (
        "Arab" in Source
        or Source == "Latn"
        or Source == "Hebr"
        or Source == "Thaa"
        or Source == "Type"
    ):
        basic_vowels = (
            "("
            + "|".join(["a", "ā", "i", "ī", "u", "ū", "ē", "ō", "e", "o", "#", vir])
            + ")"
        )
        Strng = re.sub("(ŵ)(?=" + basic_vowels + ")", "w", Strng)
        Strng = re.sub("(ŷ)(?=" + basic_vowels + ")", "y", Strng)

        Strng = re.sub("(?<=" + cons_prev + ")" + "a(?!(ŵ|ŷ|\u0304|\u032E))", "", Strng)
        Strng = re.sub("(?<=ḧ)" + "a(?!(ŵ|ŷ|\u0304|\u032E))", "", Strng)

        if "Arab" in Source:
            simp_vow = "a ā i ī u ū".split(" ")
            init_vow = "â ā̂ î ī̂ û ū̂".split(" ")

            for x, y in zip(simp_vow, init_vow):
                Strng = re.sub("ʔ" + x, y, Strng)

            if "\u05CC" in Strng:
                Strng = Strng.replace("ʔ", "")

    SemiticIndic = [
        ("ṣ", "sQ"),
        ("ʿ", "ʾQ"),
        ("ṭ", "tQ"),
        ("ḥ", "hQ"),
        ("ḍ", "dQ"),
        ("p̣", "pQ"),
        ("ž", "šQ"),
        ("ẓ", "jʰQ"),
        ("ḏ", "dʰQ"),
        ("ṯ", "tʰQ"),
        ("w", "vQ"),
        ("ḵ", "k"),
        ("\u032A", ""),
        ("\u032E", ""),
        ("a̮", "ā"),
        ("\u0308", ""),
        ("ĕ\u0302", "ê"),
        ("ă\u0302", "â"),
        ("ŏ\u0302", "ô"),
        ("ĕ", "e"),
        ("ă", ""),
        ("ŏ", "o"),
        ("ḵ", "k"),
        ("ʾQā", "ā̂Q"),
        ("ʾQi", "îQ"),
        ("ʾQī", "ī̂Q"),
        ("ʾQu", "ûQ"),
        ("ʾQū", "ū̂Q"),
        ("ʾQe", "êQ"),
        ("ʾQē", "ē̂Q"),
        ("ʾQo", "ôQ"),
        ("ʾQō", "ō̂Q"),
        ("ⁿ", "n\u033D"),
        ("ʾā", "ā̂"),
    ]

    for s, i in SemiticIndic:
        Strng = Strng.replace(s, i)

    if "Arab" in Source:
        Strng = re.sub("(\u033D)([iuā])", r"\2", Strng)
        Strng = re.sub("(\u033D)([a])", "", Strng)

    Strng = Strng.replace("ʾ", "â")

    return Strng


def perisanizeArab(Strng):
    arabKafYe = "ك ي".split(" ")
    persKafYe = "ک ی".split(" ")

    for x, y in zip(arabKafYe, persKafYe):
        Strng = Strng.replace(x, y)

    return Strng


def ArabizePersian(Strng):
    arabKafYe = "ك ي".split(" ")
    persKafYe = "ک ی".split(" ")

    for x, y in zip(arabKafYe, persKafYe):
        Strng = Strng.replace(y, x)

    return Strng


def semiticizeUrdu(Strng):
    urduSpecific = "ے ڈ ٹ ہ".split(" ")
    semitic = "ي د ت ه".split(" ")

    for x, y in zip(urduSpecific, semitic):
        Strng = Strng.replace(x, y)

    Strng = Strng.replace("ھ", "")

    return Strng


def ShowChillus(Strng):
    return post_processing.MalayalamChillu(Strng, True, True)


def ShowKhandaTa(Strng):
    print(Strng)
    Strng = Strng.replace("ৎ", "ত্ˍ")
    print(Strng)

    return Strng


def eiaudipthongs(Strng):
    return Strng


def wasvnukta(Strng):
    return Strng


def default(Strng):
    return Strng


def SogdReshAyin(Strng):
    Strng = Strng.replace("𐽀", "[\uEA01-\uEA02]")

    return Strng


def SogoReshAyinDaleth(Strng):
    Strng = Strng.replace("𐼘", "[\uEA01-\uEA02-\uEA06]")

    return Strng


def PhlpMemQoph(Strng):
    Strng = Strng.replace("𐮋", "[\uEA03-\uEA04]")

    return Strng


def PhlpWawAyinResh(Strng):
    Strng = Strng.replace("𐮅", "[\uEA05-\uEA02-\uEA01]")

    return Strng


def PhliWawAyinResh(Strng):
    Strng = Strng.replace("𐭥", "[\uEA05-\uEA02-\uEA01]")

    return Strng


def HatrDalethResh(Strng):
    Strng = Strng.replace("𐣣", "[\uEA06-\uEA01]")

    return Strng


def MalayalamHalfu(Strng):
    consu = "[കചടതറനണരലവഴളറ]"
    vir = GM.CrunchSymbols(GM.VowelSigns, "Malayalam")[0]
    consAll = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, "Malayalam")) + ")"

    Strng = re.sub(
        "(?<=" + consu + ")" + "(" + vir + ")" + "(?!" + consAll + ")",
        r"\2" + "ു്",
        Strng,
    )

    return Strng


def MalayalamTranscribe(Strng):
    Strng = MalayalamHalfu(Strng)

    script = "Malayalam"

    ListC = GM.CrunchList("ConsonantMap", script)
    ListSC = GM.CrunchList("SouthConsonantMap", script)
    vir = GM.CrunchSymbols(GM.VowelSigns, script)[0]

    ConUnVoiced = [ListC[x] for x in [0, 5, 10, 15, 20]]
    ConVoicedJ = [ListC[x] for x in [2, 7, 12, 17, 22]]
    ConVoicedS = [ListC[x] for x in [2, 5, 12, 17, 22]]

    ConNasalsAll = "|".join([ListC[x] for x in [4, 9, 14, 19, 24]])
    conNasalCa = "|".join([ListC[x] for x in [9]])
    ConNasalsGroup = [
        ConNasalsAll,
        conNasalCa,
        ConNasalsAll,
        ConNasalsAll,
        ConNasalsAll,
    ]

    ConMedials = "|".join(ListC[25:28] + ListSC[0:2] + ListSC[3:4])
    Vowels = "|".join(GM.CrunchSymbols(GM.Vowels + GM.VowelSignsNV, script))
    Aytham = GM.CrunchList("Aytham", script)[0]
    Consonants = "|".join(GM.CrunchSymbols(GM.Consonants, script))

    NRA = ListSC[3] + vir + ListSC[2]
    NDRA = ListC[14] + vir + ListC[12] + vir + ListC[26]

    for i in range(len(ConUnVoiced)):
        pass

        Strng = re.sub(
            "("
            + Vowels
            + "|"
            + Consonants
            + "|"
            + Aytham
            + ")"
            + ConUnVoiced[i]
            + "(?!"
            + vir
            + ")",
            r"\1" + ConVoicedS[i],
            Strng,
        )
        Strng = re.sub(
            "(" + ConVoicedS[i] + ")" + ConUnVoiced[i] + "(?!" + vir + ")",
            r"\1" + ConVoicedS[i],
            Strng,
        )

        Strng = re.sub(
            "(" + ConNasalsGroup[i] + ")" + "(" + vir + ")" + ConUnVoiced[i],
            r"\1\2" + ConVoicedJ[i],
            Strng,
        )

        Strng = re.sub(
            "("
            + ConMedials
            + ")"
            + "("
            + vir
            + ")"
            + ConUnVoiced[i]
            + "(?!"
            + vir
            + ")",
            r"\1\2" + ConVoicedS[i],
            Strng,
        )

    Strng = Strng.replace("റ്റ", "ട്ട").replace("ന്റ", "ണ്ഡ")

    return Strng


def retainLatin(Strng, reverse=False):
    latn_basic_lower = (
        "a b c d e f g h i j k l m n o p q r s t u v w x y z ḥ ṭ ṣ ʾ ʿ š ā ī ū ē ō"
    )
    latn_basic_upper = latn_basic_lower.upper()
    latn_all = latn_basic_lower + latn_basic_upper
    latn_all = latn_all.split(" ")

    if not reverse:
        for i, c in enumerate(latn_all):
            Strng = Strng.replace(c, chr(60929 + i))

        Strng = (
            Strng.replace("\uEA01", "r")
            .replace("\uEA02", "ʿ")
            .replace("\uEA03", "m")
            .replace("\uEA04", "q")
            .replace("\uEA05", "w")
            .replace("\uEA06", "d")
        )

    else:
        for i, c in enumerate(latn_all):
            Strng = Strng.replace(chr(60929 + i), c)

    return Strng


def JapanesePreProcess(src, txt, preoptions):
    import pykakasi
    import convert

    if src == "Hiragana" or src == "Katakana":
        kks = pykakasi.kakasi()

        txt = convert.convertScript(txt.lower(), "ISO", "Devanagari")

        cv = kks.convert(txt)
        txt = ""

        for item in cv:
            txt = txt + " " + item["hepburn"]

        if "eiaudipthongs" in preoptions:
            txt = txt.replace("ou", "o\u02BDu").replace("ei", "e\u02BDi")

        txt = re.sub("(r)([aiueo])(\u309A\u309A)", "l" + r"\2\2", txt)
        txt = re.sub("(r)([aāiīuūeēoō])(\u309A)", "l" + r"\2", txt)

        txt = re.sub("(k)([aiueo])(\u309A\u309A)", "ṅ" + r"\2\2", txt)
        txt = re.sub("(k)([aāiīuūeēoō])(\u309A)", "ṅ" + r"\2", txt)

        txt = (
            txt.replace("aa", "ā")
            .replace("ii", "ī")
            .replace("ee", "ē")
            .replace("oo", "ō")
            .replace("uu", "ū")
        )
        txt = (
            txt.replace("a-", "ā")
            .replace("i-", "ī")
            .replace("e-", "ē")
            .replace("o-", "ō")
            .replace("u-", "ū")
        )
        txt = (
            txt.replace("n'", "n_")
            .replace("ch", "c")
            .replace("sh", "ṣ")
            .replace("sṣ", "ṣṣ")
            .replace("ai", "a_i")
            .replace("au", "a_u")
        )
        txt = txt.replace("w", "v")
        txt = txt.replace("ou", "ō").replace("ei", "ē")
        txt = txt.replace("、", ",").replace("。", ".")

        txt = (
            txt.replace("ng", "ṅg")
            .replace("nk", "ṅk")
            .replace("nk", "ṅk")
            .replace("np", "mp")
            .replace("nb", "mb")
            .replace("nm", "mm")
        )

        if "wasvnukta" in preoptions:
            txt = txt.replace("v", "v̈")

        txt = txt.replace("、", ",").replace("。", ".")

    return txt


def holamlong(Strng):
    Strng = Strng.replace("ֹּ", "ֹּ")
    Strng = re.sub("(?<!ו)ֹ", "וֹ", Strng)

    return Strng


def novowelshebrewIndic(Strng):
    Strng = novowelshebrewSemitic(Strng)

    finals = ["ך", "ם", "ן", "ף", "ץ", "ףּ", "ךּ"]
    otherCons = "ב,ח,ע,צ,ש,ת".split(",")
    consonantsAll = (
        "("
        + "|".join(
            GM.CrunchSymbols(GM.Consonants, "Hebrew")
            + finals
            + otherCons
            + ["׳", "י", "ו", "א"]
        )
        + ")"
    )
    vowelsignsADShinG = (
        "("
        + "|".join(GM.CrunchSymbols(GM.VowelSigns, "Hebrew") + ["ַ", "ּ", "ׁ", "׳"])
        + ")"
    )

    Strng = re.sub(
        consonantsAll + "(?!" + vowelsignsADShinG + ")", r"\1" + "ַ" + r"\2", Strng
    )

    return Strng


def novowelshebrewSemitic(Strng):
    Strng = Strng.replace("כ", "כּ").replace("פ", "פּ").replace("ב", "בּ")
    Strng = Strng.replace("ך", "ךּ").replace("ף", "ףּ")

    return Strng


def shvanakhall(Strng):
    Strng = Strng + " \u0BDE"

    return Strng


def longEOISO(Strng):
    Strng = Strng.replace("e", "ē").replace("o", "ō")

    return Strng


def SanskritLexicaizeHK(Strng):
    return Strng


def ThaiPhonetic(Strng):
    Strng = Strng.replace("ด", "ท")
    Strng = Strng.replace("บ", "พ")
    Strng = Strng.replace("ก\u0325", "ค")
    Strng = Strng.replace("จ\u0325", "ช")
    Strng = Strng.replace("งํ", "ง")

    Strng = Strng.replace("\u035C", "")

    Strng = Strng.replace("\u0E47", "")

    Strng += "\u02BB\u02BB"

    return Strng


def LaoPhonetic(Strng):
    Strng = Strng.replace("ດ", "ທ")
    Strng = Strng.replace("ບ", "ພ")
    Strng = Strng.replace("ງໍ", "ງ")

    Strng = Strng.replace("\u035C", "")

    Strng += "\u02BB\u02BB"

    return Strng


def SaurastraHaaruColonTamil(Strng):
    Strng = Strng.replace("ன", "ந")

    ListVS = "|".join(GM.CrunchSymbols(GM.VowelSigns, "Tamil"))

    Strng = re.sub("(" + ListVS + ")" + "(:)", r"\2\1", Strng)

    chars = "([நமரல])"

    Strng = re.sub(chars + ":", r"\1" + "\uA8B4", Strng)

    return Strng


def ChakmaPali(Strng):
    Strng = Strng.replace("\U00011147", "𑄤")
    Strng = Strng.replace("𑄠", "𑄡")

    listC = (
        "("
        + "|".join(
            sorted(
                GM.CrunchSymbols(GM.Consonants, "Chakma") + Chakma.VowelMap[:1],
                key=len,
                reverse=True,
            )
        )
        + ")"
    )
    listV = (
        "("
        + "|".join(
            sorted(
                GM.CrunchSymbols(GM.VowelSigns, "Chakma")
                + Chakma.ViramaMap
                + ["\U00011133"],
                key=len,
                reverse=True,
            )
        )
        + ")"
    )

    Strng = Strng.replace("\u02BD", "")

    Strng = Strng.replace("\U00011102", "\U00011127")

    Strng = re.sub("(" + listC + ")" + "(?!" + listV + ")", r"\1" "\u02BE", Strng)
    Strng = Strng.replace("\U00011127", "")
    Strng = Strng.replace("\u02BE", "\U00011127")

    return Strng


def TakriArchaicKha(Strng):
    return Strng.replace("𑚋", "𑚸")


def UrduShortNotShown(Strng):
    Strng += "\u02BB\u02BB"

    return Strng


def AnuChandraEqDeva(Strng):
    return AnuChandraEq(Strng, "Devanagari")


def AnuChandraEq(Strng, script):
    Chandrabindu = GM.CrunchList("AyogavahaMap", script)[0]
    Anusvara = GM.CrunchList("AyogavahaMap", script)[1]

    Strng = Strng.replace(Chandrabindu, Anusvara)

    return Strng


def TamilNumeralSub(Strng):
    ListC = "(" + "[கசடதபஜஸ]" + ")"
    ListV = "(" + "|".join(GM.CrunchSymbols(GM.VowelSigns, "Tamil")) + ")"

    Strng = re.sub(ListC + ListV + "2", r"\1\2" + "²", Strng)
    Strng = re.sub(ListC + ListV + "3", r"\1\2" + "³", Strng)
    Strng = re.sub(ListC + ListV + "4", r"\1\2" + "⁴", Strng)

    Strng = re.sub(ListC + "2", r"\1" + "²", Strng)
    Strng = re.sub(ListC + "3", r"\1" + "³", Strng)
    Strng = re.sub(ListC + "4", r"\1" + "⁴", Strng)

    Strng = Strng.replace("ரு'", "ருʼ")
    Strng = Strng.replace("ரு’", "ருʼ")

    Strng = Strng.replace("ம்'", "ம்ʼ")
    Strng = Strng.replace("ம்’", "ம்ʼ")

    return Strng


def swapEe(Strng):
    Strng = Strng.replace("E", "X@X@")
    Strng = Strng.replace("e", "E")
    Strng = Strng.replace("X@X@", "e")

    Strng = Strng.replace("O", "X@X@")
    Strng = Strng.replace("o", "O")
    Strng = Strng.replace("X@X@", "o")

    return Strng


def swapEeItrans(Strng):
    Strng = Strng.replace("^e", "X@X@")
    Strng = Strng.replace("e", "^e")
    Strng = Strng.replace("X@X@", "e")

    Strng = Strng.replace("^o", "X@X@")
    Strng = Strng.replace("o", "^o")
    Strng = Strng.replace("X@X@", "o")

    return Strng


def egrantamil(Strng):
    return Strng


def siddhammukta(Strng):
    return Strng


def TaiKuen(Strng):
    return Strng


def TaiThamLao(Strng):
    return Strng


def ThaiSajjhayaOrthography(Strng):
    Script = "Thai"

    Strng = Strng.replace("ัง", "ังฺ")
    Strng = Strng.replace("์", "ฺ")
    Strng = Strng.replace("๎", "ฺ")
    Strng = Strng.replace("ั", "")

    return Strng


def ThaiSajjhayawithA(Strng):
    Strng = Strng.replace("ะ", "")
    Strng = ThaiSajjhayaOrthography(Strng)

    return Strng


def LaoSajhayaOrthography(Strng):
    Strng = Strng.replace("ັງ", "ັງ຺")

    Strng = re.sub("([ເໂໄ])(.๎)([ຍຣລວຨຩສຫຬ])", r"\2\1\3", Strng)

    Strng = Strng.replace("໌", "຺")
    Strng = Strng.replace("๎", "຺")
    Strng = Strng.replace("ັ", "")

    return Strng


def LaoSajhayaOrthographywithA(Strng):
    Strng = Strng.replace("ະ", "")
    Strng = LaoSajhayaOrthography(Strng)

    return Strng


def RemoveSchwaHindi(Strng, showschwa=False):
    VowI = "(" + "|".join(GM.CrunchSymbols(GM.Vowels, "Devanagari")) + ")"
    VowS = "(" + "|".join(GM.CrunchSymbols(GM.VowelSignsNV, "Devanagari")) + ")"
    Cons = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, "Devanagari")) + ")"
    Char = "(" + "|".join(GM.CrunchSymbols(GM.Characters, "Devanagari")) + ")"
    Nas = "([ंःँ]?)"
    ISyl = "((" + VowI + "|" + "(" + Cons + VowS + "?" + "))" + Nas + ")"
    Syl = "((" + Cons + VowS + ")" + Nas + ")"
    SylAny = "((" + Cons + VowS + "?" + ")" + Nas + ")"

    if not showschwa:
        vir = "्"
        vir2 = "्"
    else:
        vir = "\u0954"
        vir2 = "\u0954"

    Strng = re.sub(
        ISyl + Cons + Cons + SylAny + "(?!" + Char + ")",
        r"\1\8" + vir + r"\9\10",
        Strng,
    )
    Strng = re.sub(
        ISyl + Cons + Syl + SylAny + "(?!" + Char + ")", r"\1\8" + vir + r"\9\15", Strng
    )
    Strng = re.sub(ISyl + Cons + Syl + "(?!" + Char + ")", r"\1\8" + vir + r"\9", Strng)

    Strng = re.sub(ISyl + Cons + "(?!" + Char + ")", r"\1\8" + vir, Strng)

    Cons_sss = "((" + Cons + vir + ")" + "([शषस]))"
    Strng = re.sub(ISyl + Cons_sss + "(?!" + Char + ")", r"\1\8" + vir, Strng)

    Target = "Devanagari"

    ConUnAsp = [
        GM.CrunchList("ConsonantMap", Target)[x]
        for x in [
            0,
            2,
            5,
            7,
            10,
            12,
            15,
            17,
            20,
            22,
            4,
            9,
            14,
            19,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31,
            32,
        ]
    ]
    ConUnAsp = (
        ConUnAsp
        + GM.CrunchList("SouthConsonantMap", Target)
        + GM.CrunchList("NuktaConsonantMap", Target)
    )
    ConAsp = [
        GM.CrunchList("ConsonantMap", Target)[x]
        for x in [1, 3, 6, 8, 11, 13, 16, 18, 21, 23]
    ]

    Strng = re.sub(
        ISyl
        + "("
        + "|".join(ConUnAsp)
        + ")"
        + "("
        + vir
        + ")("
        + r"\8"
        + ")(?!"
        + Char
        + ")",
        r"\1\8\9\10" + vir,
        Strng,
    )

    for i in range(len(ConAsp)):
        Strng = re.sub(
            ISyl
            + "("
            + ConUnAsp[i]
            + ")"
            + "("
            + vir
            + ")"
            + "("
            + ConAsp[i]
            + ")"
            + '(?!" + Char + ")',
            r"\1\8\9\10" + vir,
            Strng,
        )

    cons_pyramid = ["[यरलव]", "[नमण]", "[शषस]", "[कखपफगघबभ]", "[टठतथडढदध]", "[चछजझज़]"]
    for c1, cons1 in enumerate(cons_pyramid):
        for c2, cons2 in enumerate(cons_pyramid):
            if c1 < c2:
                Cons_pyr = "((" + cons1 + vir + ")" + "(" + cons2 + "))"
                Strng = re.sub(
                    ISyl + Cons_pyr + "(?!" + Char + ")", r"\1\8" + vir, Strng
                )

    Strng = Strng.replace(vir, vir2)

    return Strng


def RemoveFinal(Strng, Target):
    if Target == "Bengali":
        Strng = post_processing.KhandaTa(Strng, Target, True)

    VowI = "(" + "|".join(GM.CrunchSymbols(GM.Vowels, Target)) + ")"
    VowS = "(" + "|".join(GM.CrunchSymbols(GM.VowelSignsNV, Target)) + ")"
    Cons = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, Target)) + ")"
    Char = "(" + "|".join(GM.CrunchSymbols(GM.Characters, Target)) + ")"

    Nas = "([" + "|".join(GM.CrunchList("AyogavahaMap", Target)) + "]?)"

    ISyl = "((" + VowI + "|" + "(" + Cons + VowS + "?" + ")" + Nas + "))"
    Syl = "((" + Cons + VowS + ")" + Nas + ")"
    SylAny = "((" + Cons + VowS + "?" + ")" + Nas + ")"

    vir = GM.CrunchList("ViramaMap", Target)[0]
    if Target != "Bengali":
        Cons2 = "((" + Cons + vir + ")?" + Cons + ")"
    else:
        Cons2 = "(()?" + Cons + ")"

    Strng = re.sub(ISyl + Cons2 + "(?!" + Char + ")", r"\1\8" + vir, Strng)
    Strng = re.sub(ISyl + Cons2 + "(?!" + Char + ")", r"\1\8" + vir, Strng)

    return Strng


def SchwaFinalGurmukhi(Strng):
    Strng = RemoveFinal(Strng, "Gurmukhi")

    return Strng


def SchwaFinalGujarati(Strng):
    Strng = RemoveFinal(Strng, "Gujarati")

    return Strng


def SchwaFinalBengali(Strng):
    Strng = RemoveFinal(Strng, "Bengali")

    return Strng


def SchwaFinalWarangCiti(Strng):
    Target = "WarangCiti"

    VowI = "(" + "|".join(GM.CrunchSymbols(GM.Vowels, Target)) + ")"
    VowS = "(" + "|".join(GM.CrunchSymbols(GM.VowelSignsNV, Target)) + ")"
    Cons = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, Target)) + ")"
    Char = "(" + "|".join(GM.CrunchSymbols(GM.Characters, Target)) + ")"

    Nas = "([" + "|".join(GM.CrunchList("AyogavahaMap", Target)) + "]?)"

    ISyl = "((" + VowI + "|" + "(" + Cons + VowS + "?" + ")" + Nas + "))"
    Syl = "((" + Cons + VowS + ")" + Nas + ")"
    SylAny = "((" + Cons + VowS + "?" + ")" + Nas + ")"

    vir = "\u02BB"
    Cons2 = "((" + Cons + vir + ")?" + Cons + ")"

    Strng = re.sub(ISyl + Cons2 + "(?!" + Char + ")", r"\1\8" + vir, Strng)

    return Strng


def siddhamUnicode(Strng):
    return Strng


def ThaiOrthography(Strng):
    Strng += "\u02BB\u02BB"

    return Strng


def LaoTranscription(Strng):
    Strng += "\u02BB\u02BB"

    return Strng


def LimbuDevanagariConvention(Strng):
    Strng = Strng.replace("ए़", "ऎ")
    Strng = Strng.replace("ओ़", "ऒ")
    Strng = Strng.replace("े़", "ॆ")
    Strng = Strng.replace("ो़", "ॊ")
    Strng = Strng.replace("ः", "꞉")

    return Strng


def LimbuSpellingSaI(Strng):
    vir = Limbu.ViramaMap[0]

    FCons = [
        x + vir for x in [Limbu.ConsonantMap[x] for x in [0, 4, 15, 19, 20, 24, 26, 27]]
    ]
    FinalCons = [
        "\u1930",
        "\u1931",
        "\u1933",
        "\u1934",
        "\u1935",
        "\u1936",
        "\u1937",
        "\u1938",
    ]

    for x, y in zip(FCons, FinalCons):
        Strng = Strng.replace(x, "\u193A" + y)

    return Strng


def removeChillus(Strng):
    Chillus = ["\u0D7A", "\u0D7B", "\u0D7C", "\u0D7D", "\u0D7E"]

    vir = Malayalam.ViramaMap[0]
    ConVir = [
        Malayalam.ConsonantMap[14] + vir,
        Malayalam.ConsonantMap[19] + vir,
        Malayalam.ConsonantMap[26] + vir,
        Malayalam.ConsonantMap[27] + vir,
        Malayalam.SouthConsonantMap[0] + vir,
    ]

    for x, y in zip(Chillus, ConVir):
        Strng = Strng.replace(x, y)

    return Strng


def SinhalaPali(Strng):
    Strng = post_processing.SinhalaPali(Strng, reverse=True)

    return Strng


def IASTPali(Strng):
    Strng = Strng.replace("ḷ", "l̤")

    return Strng


def CyrillicPali(Strng):
    Strng = Strng.replace(
        "л̣",
        "л̤",
    )

    return Strng


def MalayalamPrakrit(Strng):
    Strng = post_processing.ReverseGeminationSign(Strng, "Malayalam")
    Strng = Strng.replace("ഀ", "ം")

    return Strng


def GranthaPrakrit(Strng):
    Strng = post_processing.ReverseGeminationSign(Strng, "Grantha")

    Strng = Strng.replace("𑌀", "𑌂")

    return Strng


def RomanPreFix(Strng, Source):
    DepV = "\u1E7F"
    Asp = "\u02B0"

    Vir = GM.CrunchList("ViramaMap", Source)[0]
    Nuk = GM.CrunchList("NuktaMap", Source)[0]
    VowelA = GM.CrunchSymbols(["VowelMap"], Source)[0]

    ListV = "|".join(GM.CrunchSymbols(GM.VowelSigns, Source))
    ListC = "|".join(GM.CrunchSymbols(GM.Consonants, Source))

    Strng = re.sub(
        "(" + ListC + ")" + "(?!" + ListV + "|" + VowelA + ")",
        r"\1" + DepV + Vir,
        Strng,
    )

    Strng = re.sub(
        "(" + ListC + "|" + Nuk + ")" + "(" + ListV + ")", r"\1" + DepV + r"\2", Strng
    )

    Strng = re.sub("(?<=" + ListC + ")" + "(" + VowelA + ")", r"", Strng)
    Strng = Strng.replace(DepV + Vir + Nuk + VowelA, Nuk)
    Strng = re.sub(DepV + Vir + Nuk + "(?=[" + DepV + "])", Nuk, Strng)
    Strng = Strng.replace(DepV + Vir + Nuk, Nuk + DepV + Vir)

    return Strng


def joinVowelCons(Strng, script):
    consonantsAll = (
        "("
        + "|".join(
            sorted(GM.CrunchSymbols(GM.Consonants, script), key=len, reverse=True)
        )
        + ")"
    )
    vowelsAll = (
        "("
        + "|".join(sorted(GM.CrunchSymbols(GM.Vowels, script), key=len, reverse=True))
        + ")"
    )

    Strng = re.sub(consonantsAll + " " + vowelsAll, r"\1\2", Strng)
    Strng = re.sub(consonantsAll + " " + consonantsAll, r"\1\2", Strng)

    return Strng


def joinVowelConsIAST(Strng):
    return joinVowelCons(Strng, "IAST")


def joinVowelConsISO(Strng):
    return joinVowelCons(Strng, "ISO")


def PreProcess(Strng, Source, Target):
    if Source in GM.RomanDiacritic or Source == "Latn":
        Strng = Strng.lower()

    pipeScripts = ["HK", "IASTPali", "IAST", "ISO"]

    if Source in pipeScripts:
        Strng = Strng.replace("|", ".").replace("||", "..")

    if "Arab" in Source:
        Strng = re.sub(
            "([وي])(?=[\u064E\u0650\u064F\u0651\u064B\u064C\u064D])",
            "\u02DE" + r"\1",
            Strng,
        )

    if Source in ["Syrj", "Syrn"]:
        Strng = Strng.replace("\u0323", "\u0742")

    if Source == "Itrans":
        sOm = "OM"
        tOm = "oM"

        punc = (
            "("
            + "|".join(
                ["\u005C" + x for x in list(string.punctuation)]
                + ["\s"]
                + [
                    x.replace(".", "\.")
                    for x in GM.CrunchSymbols(GM.Signs, Source)[1:3]
                ]
            )
            + ")"
        )

        Strng = re.sub(punc + sOm + punc, r"\1" + tOm + r"\2", Strng)
        Strng = re.sub("^" + sOm + punc, tOm + r"\1", Strng)
        Strng = re.sub(punc + sOm + "$", r"\1" + tOm, Strng)
        Strng = re.sub("^" + sOm + "$", tOm, Strng)

        punc = "(\s)"

        Strng = re.sub(punc + sOm + punc, r"\1" + tOm + r"\2", Strng)
        Strng = re.sub("^" + sOm + punc, tOm + r"\1", Strng)
        Strng = re.sub(punc + sOm + "$", r"\1" + tOm, Strng)
        Strng = re.sub("^" + sOm + "$", tOm, Strng)

        AltForm = [
            "O",
            "aa",
            "ii",
            "uu",
            "RRi",
            "RRI",
            "LLi",
            "LLI",
            "N^",
            "JN",
            "chh",
            "shh",
            "x",
            "GY",
            ".n",
            ".m",
            ".h",
            "AUM",
            "E",
            "J",
            "c.o",
            "c.e",
        ]
        NormForm = [
            "^o",
            "A",
            "I",
            "U",
            "R^i",
            "R^I",
            "L^i",
            "L^I",
            "~N",
            "~n",
            "Ch",
            "Sh",
            "kSh",
            "j~n",
            "M",
            "M",
            "",
            "oM",
            "^e",
            "z",
            "A.c",
            "e.c",
        ]

        for x, y in zip(AltForm, NormForm):
            Strng = Strng.replace(x, y)

        AltForms = [
            ("ee", "I"),
            ("dny", "j~n"),
            ("oo", "U"),
            ("kS", "kSh"),
            ("w", "v"),
            ("|", "."),
            ("kShh", "kSh"),
        ]

        for x, y in AltForms:
            Strng = Strng.replace(x, y)

        Strng = Strng.replace("OM", "oM")

    if Source == "BarahaNorth" or Source == "BarahaSouth":
        Strng = Strng.replace("A", "aa")
        Strng = Strng.replace("I", "ee")
        Strng = Strng.replace("U", "oo")

        Strng = Strng.replace("ou", "au")
        Strng = Strng.replace("K", "kh")
        Strng = Strng.replace("G", "gh")
        Strng = Strng.replace("ch", "c")
        Strng = Strng.replace("Ch", "C")
        Strng = Strng.replace("J", "jh")
        Strng = Strng.replace("w", "v")
        Strng = Strng.replace("sh", "S")
        Strng = Strng.replace("~h", "_h")
        Strng = Strng.replace("^", "()")
        Strng = Strng.replace("^^", "{}")

        Strng = Strng.replace("tx", "rx")
        Strng = Strng.replace("zh", "Lx")

        Strng = Strng.replace("q", "\_")
        Strng = Strng.replace("#", "\\'")
        Strng = Strng.replace("$", '\\"')

    if Source == "IAST":
        Strng = Strng.replace("aï", "a_i")
        Strng = Strng.replace("aü", "a_u")
        Strng = Strng.replace("\u0303", "ṃ")

    if Source == "ISO":
        Strng = Strng.replace("a:i", "a_i")
        Strng = Strng.replace("a:u", "a_u")
        Strng = Strng.replace("\u0303", "ṁ")

    if Source == "Titus":
        Strng = Strng

    if Source == "ISO" or Source == "IAST" or Source == "Titus" or "RussianCyrillic":
        Strng = CF.VedicSvarasNonDiacritic(Strng)

    if Source == "Latn" and "Syr" in Target:
        Strng = (
            Strng.replace("ḇ", "v")
            .replace("ḡ", "ḡ")
            .replace("ḵ", "ḫ")
            .replace("p̄", "f")
        )

    if ("↓" in Strng or "↑" in Strng) and Target in GM.IndicScripts:
        Strng = Strng.replace("↓", "॒")
        Strng = Strng.replace("↑↑", "᳚")
        Strng = Strng.replace("↑", "॑")

    if ("↓" in Strng or "↑" in Strng) and Target in GM.LatinScripts:
        Strng = Strng.replace("↓", "\\_")
        Strng = Strng.replace("↑↑", '\\"')
        Strng = Strng.replace("↑", "\\'")

    if Source == "WarangCiti":
        Strng = Strng.replace("\u200D", "\u00D7")

    if Source == "Hebr-Ar":
        dot_var = [("עׄ", "ג"), ("תׄ", "ת֒"), ("ת", "ת̈"), ("ק", "ק̈")]

        for char, char_var in dot_var:
            Strng = Strng.replace(char_var, char)

    Strng = normalize(Strng, Source)

    return Strng


def ISO259Target(Strng):
    Strng = Strng.replace("א", "ʾ").replace("׳", "’")

    return Strng


def ISO233Target(Strng):
    replacements = [("أ", "ˈʾ"), ("ء", "¦"), ("إ", "ˌʾ")]

    for x, y in replacements:
        Strng = Strng.replace(x, y)

    return Strng


def PersianDMGTarget(Strng):
    replacements = [("ا", "ʾ")]

    for x, y in replacements:
        Strng = Strng.replace(x, y)

    return Strng


def ISO233Source(Strng):
    replacements = [("أ", "ˈʾ"), ("ء", "¦"), ("إ", "ˌʾ")]

    for x, y in replacements:
        Strng = Strng.replace(y, x)

    replacements = [
        ("j", "ǧ"),
        ("g", "ǧ"),
        ("ḧ", "ẗ"),
        ("ḫ", "ẖ"),
        ("a̮", "ỳ"),
        ("aⁿ", "á"),
        ("iⁿ", "í"),
        ("uⁿ", "ú"),
        ("ā̂", "ʾâ"),
        ("ˀ", "ˈ"),
    ]

    for x, y in replacements:
        Strng = Strng.replace(y, x)

    return Strng


def HebrewSBLTarget(Strng):
    Strng = Strng.replace("א", "ʾ").replace("׳", "’")

    return Strng


def HebrewSBLSource(Strng):
    Strng = Strng.replace(
        "ʾ",
        "א",
    ).replace("’", "׳")
    Strng = Strng.replace("\u0307\u00B0", "\u00B0\u0307")

    replacements = [
        ("v", "ḇ"),
        ("f", "p̄"),
        ("d꞉", "d"),
        ("d", "ḏ"),
        ("g꞉", "g"),
        ("g", "ḡ"),
        ("t꞉", "t"),
        ("t", "ṯ"),
        ("š̮", "š"),
        ("š̪", "ś"),
        ("o", "ō"),
        ("ō", "ô"),
        ("ū", "û"),
        ("\u033D", "ĕ"),
    ]

    for x, y in replacements:
        Strng = Strng.replace(y, x)

    return Strng


def ISO259Source(Strng):
    Strng = Strng.replace(
        "ʾ",
        "א",
    ).replace("’", "׳")
    Strng = Strng.replace("\u0307\u00B0", "\u00B0\u0307")

    replacements = [
        ("ḵ", "k"),
        ("v", "b"),
        ("f", "p"),
        ("b", "ḃ"),
        ("p", "ṗ"),
        ("k", "k̇"),
        ("꞉", "\u0307"),
        ("š̮", "š"),
        ("š", "s̀"),
        ("š̪", "ś"),
        ("ā", "å"),
        ("e", "ȩ"),
        ("ō", "ŵ"),
        ("ū", "ẇ"),
        ("\u033D", "°"),
        ("ĕ", "ḝ"),
    ]

    for x, y in replacements:
        Strng = Strng.replace(y, x)

    import unicodedata

    Strng = unicodedata.normalize("NFD", Strng)
    Strng = Strng.replace("\u0307", "꞉")
    Strng = unicodedata.normalize("NFC", Strng)

    return Strng


def UnSupThaana(Strng):
    return Strng


def RemoveJoiners(Strng):
    Strng = Strng.replace("\u200D", "")
    Strng = Strng.replace("\u200C", "")

    return Strng


def ArabicGimelJa(Strng):
    Strng = Strng.replace("ج", "ڨ")

    return Strng


def normalize(Strng, Source):
    nuktaDecom = [
        "\u0915\u093C",
        "\u0916\u093C",
        "\u0917\u093C",
        "\u091C\u093C",
        "\u0921\u093C",
        "\u0922\u093C",
        "\u092B\u093C",
        "\u092F\u093C",
        "\u0A32\u0A3C",
        "\u0A38\u0A3C",
        "\u0A16\u0A3C",
        "\u0A17\u0A3C",
        "\u0A1C\u0A3C",
        "\u0A2B\u0A3C",
        "\u09A1\u09BC",
        "\u09A2\u09BC",
        "\u09AF\u09BC",
        "\u0B21\u0B3C",
        "\u0B22\u0B3C",
    ]
    nuktaPrecom = [
        "\u0958",
        "\u0959",
        "\u095A",
        "\u095B",
        "\u095C",
        "\u095D",
        "\u095E",
        "\u095F",
        "\u0A33",
        "\u0A36",
        "\u0A59",
        "\u0A5A",
        "\u0A5B",
        "\u0A5E",
        "\u09DC",
        "\u09DD",
        "\u09DF",
        "\u0B5C",
        "\u0B5D",
    ]

    if Source not in ["Grantha", "TamilGrantha"]:
        for x, y in zip(nuktaDecom, nuktaPrecom):
            Strng = Strng.replace(x, y)

    if Source in ["IAST", "ISO", "ISOPali", "Titus"]:
        Strng = (
            Strng.replace("ü", "uʼ")
            .replace("ǖ", "ūʼ")
            .replace(
                "ö",
                "aʼ",
            )
            .replace("ȫ", "āʼ")
        )

    if Source == "Arab-Ur" or Source == "Arab-Pa":
        Strng = Strng.replace("ك", "ک")
        Strng = Strng.replace("ي", "ی")

    if Source == "Hebr":
        vowels = ["ְ", "ֱ", "ֲ", "ֳ", "ִ", "ֵ", "ֶ", "ַ", "ָ", "ֹ", "ֺ", "ֻ", "ׇ"]
        vowelsR = "(" + "|".join(vowels + ["וֹ", "וּ"]) + ")"
        Strng = re.sub(vowelsR + "([ּׁׂ])", r"\2\1", Strng)
        Strng = Strng.replace("\u05BC\u05B0\u05C1", "\u05C1\u05BC\u05B0")

    chilluZwj = ["ണ്‍", "ന്‍", "ര്‍", "ല്‍", "ള്‍", "ക്‍"]
    chilluAtom = ["ൺ", "ൻ", "ർ", "ൽ", "ൾ", "ൿ"]

    for x, y in zip(chilluZwj, chilluAtom):
        Strng = Strng.replace(x, y)

    Strng = Strng.replace("ൌ", "ൗ")
    Strng = Strng.replace("ൟ", "ഈ")
    Strng = Strng.replace("ൎ", "ര്")

    Strng = Strng.replace("ൻ്റ", "ന്റ")

    Strng = Strng.replace("ೝ", "ನ್")
    Strng = Strng.replace("ౝ", "న్")

    tamAlt = ["ஸ்ரீ", "க்‌ஷ", "ர‌ி", "ர‌ீ"]
    tamNorm = ["ஶ்ரீ", "க்ஷ", "ரி", "ரீ"]

    Strng = Strng.replace("ဿ", "သ္သ")

    Strng.replace("ஸ²", "ஶ")

    subNum = ["¹", "₁", "₂", "₃", "₄"]
    supNum = ["", "", "²", "³", "⁴"]

    for x, y in zip(tamAlt + subNum, tamNorm + supNum):
        Strng = Strng.replace(x, y)

    oldVow = ["ྲྀ", "ཷ", "ླྀ", "ཹ", "ཱི", "ཱུ", "ཀྵ", "ྐྵ"]
    newVow = ["ྲྀ", "ྲཱྀ", "ླྀ", "ླཱྀ", "ཱི", "ཱུ", "ཀྵ", "ྐྵ"]

    for x, y in zip(oldVow, newVow):
        Strng = Strng.replace(x, y)

    Strng = Strng.replace("ཅ", "ཙ")
    Strng = Strng.replace("ཆ", "ཚ")

    latinDecom = [
        "ā",
        "ī",
        "ū",
        "ē",
        "ō",
        "ṃ",
        "ṁ",
        "ḥ",
        "ś",
        "ṣ",
        "ṇ",
        "ṛ",
        "ṝ",
        "ḷ",
        "ḹ",
        "ḻ",
        "ṉ",
        "ṟ",
    ]
    latinPrecom = [
        "ā",
        "ī",
        "ū",
        "ē",
        "ō",
        "ṃ",
        "ṁ",
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
    ]

    for x, y in zip(latinDecom, latinPrecom):
        Strng = Strng.replace(x, y)

    Strng = Strng.replace("ํา", "ำ")

    Strng = Strng.replace("ໍາ", "ຳ")

    Strng = Strng.replace("।।", "॥")

    Strng = Strng.replace("ᤠ᤺ᤣ", "ᤠᤣ᤺")
    Strng = Strng.replace("᤺ᤣ", "ᤣ᤺")
    Strng = Strng.replace("ᤠᤣ", "ᤥ")

    Strng = Strng.replace("ฎ", "ฏ")

    Strng = Strng.replace("𑍌", "𑍗")

    Strng = Strng.replace("\u0F82", "\u0F83")

    Strng = Strng.replace("ॲ", "ऍ")

    Strng = Strng.replace("ো", "ো")
    Strng = Strng.replace("াে", "ো")

    Strng = Strng.replace("ৌ", "ৌ")
    Strng = Strng.replace("ৗে", "ৌ")

    Strng = Strng.replace("ொ", "ொ")
    Strng = Strng.replace("ாெ", "ொ")

    Strng = Strng.replace("ோ", "ோ")
    Strng = Strng.replace("ாே", "ோ")

    Strng = Strng.replace("ௌ", "ௌ")
    Strng = Strng.replace("ௗெ", "ௌ")

    Strng = Strng.replace("ൊ", "ൊ")
    Strng = Strng.replace("ാെ", "ൊ")

    Strng = Strng.replace("ോ", "ോ")
    Strng = Strng.replace("ാേ", "ോ")

    Strng = Strng.replace("𑍋", "𑍋")
    Strng = Strng.replace("𑌾𑍇", "𑍋")

    return Strng


def removeZW(Strng):
    Strng = Strng.replace("\u200C").replace("\u200D")

    return Strng


def PhagsPaArrange(Strng, Source):
    if Source in GM.IndicScripts:
        ListC = "|".join(
            sorted(GM.CrunchSymbols(GM.Consonants, Source), key=len, reverse=True)
        )
        ListV = "|".join(
            sorted(GM.CrunchSymbols(GM.Vowels, Source), key=len, reverse=True)
        )
        ListVS = "|".join(
            sorted(GM.CrunchSymbols(GM.VowelSignsNV, Source), key=len, reverse=True)
        )
        ListCS = "|".join(
            sorted(GM.CrunchSymbols(GM.CombiningSigns, Source), key=len, reverse=True)
        )

        vir = GM.CrunchSymbols(GM.VowelSigns, Source)[0]

        yrv = "|".join(
            [GM.CrunchSymbols(GM.Consonants, Source)[i] for i in [25, 26, 28]]
        )

        Strng = re.sub(
            "("
            + ListC
            + ")"
            + "("
            + vir
            + ")"
            + "("
            + yrv
            + ")"
            + "("
            + "("
            + ListVS
            + ")?"
            + "("
            + ListCS
            + ")?"
            + ")",
            r" \1\2\3\4",
            Strng,
        )
        Strng = re.sub(
            "("
            + ListC
            + ListV
            + ")"
            + "("
            + "("
            + ListVS
            + ")?"
            + "("
            + ListCS
            + ")?"
            + ")"
            + "("
            + ListC
            + ")"
            + "("
            + vir
            + ")"
            + "(?!\s)",
            r"\1\2\5\6 ",
            Strng,
        )
        Strng = re.sub(
            "("
            + ListC
            + ListV
            + ")"
            + "("
            + "("
            + ListVS
            + ")?"
            + "("
            + ListCS
            + ")?"
            + ")"
            + "("
            + ListC
            + ")"
            + "(?!"
            + vir
            + ")",
            r"\1\2 \5",
            Strng,
        )
        Strng = re.sub(
            "("
            + ListC
            + ListV
            + ")"
            + "("
            + "("
            + ListVS
            + ")?"
            + "("
            + ListCS
            + ")?"
            + ")"
            + "("
            + ListC
            + ")"
            + "(?!"
            + vir
            + ")",
            r"\1\2 \5",
            Strng,
        )

    elif Source in GM.LatinScripts:
        pass

    return Strng


def TamilTranscribeCommon(Strng, c=31):
    script = "Tamil"

    ListC = GM.CrunchList("ConsonantMap", script)
    ListSC = GM.CrunchList("SouthConsonantMap", script)
    vir = GM.CrunchSymbols(GM.VowelSigns, script)[0]

    ConUnVoiced = [ListC[x] for x in [0, 5, 10, 15, 20]]
    ConVoicedJ = [ListC[x] for x in [2, 7, 12, 17, 22]]
    ConVoicedS = [ListC[x] for x in [2, 31, 12, 17, 22]]

    ConNasalsAll = "|".join([ListC[x] for x in [4, 9, 14, 19, 24]])
    conNasalCa = "|".join([ListC[x] for x in [9]])
    ConNasalsGroup = [
        ConNasalsAll,
        conNasalCa,
        ConNasalsAll,
        ConNasalsAll,
        ConNasalsAll,
    ]

    ConMedials = "|".join(ListC[25:28] + ListSC[0:2] + ListSC[3:4])
    Vowels = "|".join(GM.CrunchSymbols(GM.Vowels + GM.VowelSignsNV, script))
    Aytham = GM.CrunchList("Aytham", script)[0]
    Consonants = "|".join(GM.CrunchSymbols(GM.Consonants, script))
    NRA = ListSC[3] + vir + ListSC[2]
    NDRA = ListC[14] + vir + ListC[12] + vir + ListC[26]

    for i in range(len(ConUnVoiced)):
        pass

        Strng = re.sub(
            "("
            + Vowels
            + "|"
            + Consonants
            + "|"
            + Aytham
            + ")"
            + ConUnVoiced[i]
            + "(?!"
            + vir
            + ")",
            r"\1" + ConVoicedS[i],
            Strng,
        )
        Strng = re.sub(
            "([³])" + ConUnVoiced[i] + "(?!" + vir + ")", r"\1" + ConVoicedS[i], Strng
        )
        Strng = re.sub("³+", "³", Strng)

        Strng = re.sub(
            "(" + ConNasalsGroup[i] + ")" + "(" + vir + ")" + ConUnVoiced[i],
            r"\1\2" + ConVoicedJ[i],
            Strng,
        )

        Strng = re.sub(
            "("
            + ConMedials
            + ")"
            + "("
            + vir
            + ")"
            + ConUnVoiced[i]
            + "(?!"
            + vir
            + ")",
            r"\1\2" + ConVoicedS[i],
            Strng,
        )

    Strng = Strng.replace(NRA, NDRA)

    Strng = re.sub(
        "(?<!"
        + "("
        + ListC[5]
        + "|"
        + ListSC[2]
        + "|"
        + "ட"
        + ")"
        + vir
        + ")"
        + ListC[5]
        + "(?!"
        + vir
        + ")",
        ListC[c],
        Strng,
    )

    import string

    punct = (
        "|".join(
            [
                "\\" + x
                for x in list(string.punctuation.replace(".", "").replace("?", ""))
            ]
        )
        + "|\s"
    )

    Strng = re.sub(
        "(" + ListC[5] + vir + ")" + "((" + punct + ")+)" + "(" + ListC[c] + ")",
        r"\1\2" + ListC[5],
        Strng,
    )

    Strng = re.sub(
        "(" + ListC[9] + vir + ")" + "((" + punct + ")+)" + "(" + ListC[c] + ")",
        r"\1\2" + ListC[7],
        Strng,
    )

    Strng = re.sub(
        "(" + ListC[4] + vir + ")" + "((" + punct + ")+)" + "(" + ListC[0] + ")",
        r"\1\2" + ListC[2],
        Strng,
    )

    Strng = re.sub(
        "(" + ListC[14] + vir + ")" + "((" + punct + ")+)" + "(" + ListC[10] + ")",
        r"\1\2" + ListC[12],
        Strng,
    )

    Strng = re.sub(
        "(" + ListC[19] + vir + ")" + "((" + punct + ")+)" + "(" + ListC[15] + ")",
        r"\1\2" + ListC[17],
        Strng,
    )

    Strng = Strng.replace(Tamil.Aytham[0] + ListC[0], ListC[32] + vir + ListC[32])

    Strng = Strng.replace(Tamil.Aytham[0], ListC[32] + vir)

    Strng = re.sub(ListSC[2] + vir + ListSC[2], ListC[10] + vir + ListC[26], Strng)

    Strng = re.sub(
        "("
        + "["
        + ListC[10]
        + ListSC[2]
        + "]"
        + vir
        + ")"
        + "(\s)"
        + "("
        + ListC[c]
        + ")",
        r"\1\2" + ListC[5],
        Strng,
    )

    Strng = Strng.replace(ListSC[3], ListC[19])

    return Strng


def TamilTranscribe(Strng):
    Strng = TamilTranscribeCommon(Strng)

    return Strng


def TamilTranscribeDialect(Strng):
    Strng = TamilTranscribeCommon(Strng, c=29)

    return Strng


def IPAIndic(Strng):
    Strng = Strng.replace("ʊ", "u")
    Strng = Strng.replace("ɛ", "e")

    return
