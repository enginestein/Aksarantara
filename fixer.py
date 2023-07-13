import Map as GM
from Roman import Avestan, IAST
from Core import (
    Ahom,
    Tamil,
    TamilGrantha,
    Limbu,
    MeeteiMayek,
    Urdu,
    Lepcha,
    Chakma,
    Kannada,
    Gurmukhi,
    Newa,
)
from East import (
    Lao,
    TaiTham,
    Tibetan,
    Burmese,
    Khmer,
    Balinese,
    Javanese,
    Thai,
    Sundanese,
    PhagsPa,
    Cham,
    Thaana,
    Rejang,
    ZanabazarSquare,
    Makasar,
)



import post_processing
import re


def lenSort(x, y):
    if len(x[0]) > len(y[0]):
        return -1
    else:
        return 0


def OriyaIPAFixPre(Strng):
    Strng = Strng.replace("ଂ", "ଙ୍")
    Strng = Strng.replace("ଃ", "ହ୍")

    return Strng


def SinhalaIPAFix(Strng):
    consonants = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, "IPA")) + ")"

    Strng = re.sub("^" + consonants + "(ə)", r"\1ʌ", Strng)
    Strng = re.sub("(\s)" + consonants + "(ə)", r"\1\2ʌ", Strng)

    Strng = re.sub("^" + consonants + consonants + "(ə)", r"\1ʌ", Strng)
    Strng = re.sub("(\s)" + consonants + consonants + "(ə)", r"\1\2ʌ", Strng)

    Strng = re.sub("^" + consonants + consonants + consonants + "(ə)", r"\1ʌ", Strng)
    Strng = re.sub(
        "(\s)" + consonants + consonants + consonants + "(ə)", r"\1\2ʌ", Strng
    )

    return Strng


def OriyaIPAFix(Strng):
    Strng = Strng.replace("ə", "ɔ")
    Strng = Strng.replace("j", "d͡ʒ")
    Strng = Strng.replace("\u1E8F", "j")
    Strng = Strng.replace("kʂ", "kʰ")
    Strng = Strng.replace("ʂ", "s̪")
    Strng = Strng.replace("ʃ", "s̪")
    Strng = Strng.replace("ʋ", "u̯")

    Strng = Strng.replace("t͡s", "t͡ʃ")

    Strng = Strng.replace("ɪ", "i")
    Strng = Strng.replace("iː", "i")
    Strng = Strng.replace("uː", "u")
    Strng = Strng.replace("eː", "e")
    Strng = Strng.replace("oː", "o")
    Strng = Strng.replace("ɾɨ", "ɾu")
    Strng = Strng.replace("ɾɨː", "ɾu")
    Strng = Strng.replace("lɨ", "lu")
    Strng = Strng.replace("lɨː", "lu")

    return Strng


def VedicSvarasLatinIndic(Strng, Source):
    Strng = Strng.replace("{\\m+}", "ꣳ")
    Strng = Strng.replace("\\m++", "ꣴ")
    Strng = Strng.replace("\\m+", "ꣳ")

    Strng = Strng.replace("\\`", "\\_")
    Strng = Strng.replace("\\''", '\\"')

    Ayogavaha = GM.CrunchList("AyogavahaMap", Source)
    Svaras = ["\\_", '\\"', "\\'"]

    for x in Ayogavaha:
        for y in Svaras:
            Strng = Strng.replace(y + x, x + y)

    Strng = Strng.replace('\\"', "᳚")
    Strng = Strng.replace("\\'", "॑")
    Strng = Strng.replace("\\_", "॒")

    return Strng


def VedicSvarsIndicLatin(Strng):
    Strng = Strng.replace("᳚", '\\"')
    Strng = Strng.replace("॑", "\\'")
    Strng = Strng.replace("॒", "\\_")
    Strng = Strng.replace("ꣳ", "\\m+")
    Strng = Strng.replace("ꣴ", "\\m++")

    return Strng


def VedicSvarasOthers(Strng, Target):
    Strng = Strng.replace('\\"', "↑↑").replace("\\_", "↓").replace("\\'", "↑")
    anu = GM.CrunchList("AyogavahaMap", Target)[1]
    Strng = Strng.replace("\\m++", "ꣴ")
    Strng = Strng.replace("\\m+", "ꣳ")

    Ayogavaha = GM.CrunchList("AyogavahaMap", Target)

    return Strng


def VedicSvarasDiacrtics(Strng, Target):
    Strng = Strng.replace("\\'", "̍")
    Strng = Strng.replace('\\"', "̎")
    Strng = Strng.replace("\\_", "̱")
    Strng = Strng.replace("\\m++", "gͫ̄")
    Strng = Strng.replace("\\m+", "gͫ")

    if Target == "ISO" or Target == "ISOPali":
        Strng = Strng.replace("\\’’", "̎")
        Strng = Strng.replace("\\’", "̍")

    Ayogavaha = GM.CrunchList("AyogavahaMap", Target)
    Svaras = ["̍", "̎", "̱"]

    for x in Ayogavaha:
        for y in Svaras:
            Strng = Strng.replace(x + y, y + x)

    return Strng


def VedicSvarasCyrillic(Strng, Target):
    Strng = Strng.replace("\\'", "̍")
    Strng = Strng.replace('\\"', "̎")
    Strng = Strng.replace("\\_", "̱")
    Strng = Strng.replace("\\м++", "г\u0361м")
    Strng = Strng.replace("\\м+", "г\u035Cм")
    Strng = Strng.replace("\\m++", "г\u0361м")
    Strng = Strng.replace("\\m+", "г\u035Cм")
    Ayogavaha = GM.CrunchList("AyogavahaMap", Target)
    Svaras = ["̍", "̎", "̱"]

    for x in Ayogavaha:
        for y in Svaras:
            Strng = Strng.replace(x + y, y + x)

    return Strng


def VedicSvarasNonDiacritic(Strng):
    Strng = Strng.replace("̍", "\\'")
    Strng = Strng.replace("̎", '\\"')
    Strng = Strng.replace("̱", "\\_")
    Strng = Strng.replace("gͫ̄", "\\m++")
    Strng = Strng.replace("gͫ", "\\m+")

    Strng = Strng.replace("г\u0361м", "\\m++")
    Strng = Strng.replace("г\u035Cм", "\\m+")

    return Strng


def FixRomanOutput(Strng, Target):
    Schwa = "\uF000"
    DepV = "\u1E7F"

    VowelSignList = (
        "|".join(GM.CrunchSymbols(GM.VowelSigns, Target))
        .replace("^", "\^")
        .replace(".", "\.")
    )
    VowelList = (
        "|".join(GM.CrunchSymbols(GM.Vowels, Target))
        .replace("^", "\^")
        .replace(".", "\.")
    )

    Virama = "".join(GM.CrunchSymbols(["ViramaMap"], Target))
    Nukta = "".join(GM.CrunchSymbols(["NuktaMap"], Target))

    VowelA = GM.CrunchSymbols(["VowelMap"], Target)[0]
    VowelIU = "|".join(
        GM.CrunchSymbols(["VowelMap"], Target)[2]
        + GM.CrunchSymbols(["VowelMap"], Target)[4]
    )

    TargetCons = GM.CrunchSymbols(["ConsonantMap"], Target)
    ConsH = TargetCons[32]
    UnAspCons = (
        "|".join([TargetCons[i] for i in [0, 2, 5, 7, 10, 12, 15, 17, 20, 22]])
        .replace("^", "\^")
        .replace(".", "\.")
    )

    if Target in ["IAST", "ISO", "ISOPali", "Titus"]:
        Strng = Strng.replace("u" + Virama, Virama + "ŭ")

    Strng = re.sub("(?<=" + Schwa + DepV + ")" + "(" + VowelIU + ")", r"_\1", Strng)

    Strng = re.sub("(?<=ṿ" + VowelA + "ṿ)" + "(" + VowelIU + ")", r"_\1", Strng)

    Strng = re.sub(
        "(" + UnAspCons + ")" "(" + Schwa + Virama + ")(" + ConsH + ")", r"\1_\3", Strng
    )

    Strng = re.sub(
        "(" + Schwa + ")(" + Virama + ")(?=" + VowelList + ")", r"_\2", Strng
    )

    Strng = re.sub("(" + Schwa + ")(" + Nukta + ")", r"\2\1", Strng)
    Strng = re.sub("(" + Schwa + ")(?=" + VowelSignList + ")", "", Strng)
    Strng = Strng.replace(Schwa, VowelA)
    Strng = Strng.replace(DepV, "")
    Strng = Strng.replace(Virama, "")

    return Strng


def FixVedic(Strng, Target):
    Strng = Strng.replace("{\\m+}", "\\m+")
    Strng = Strng.replace("\\`", "\\_")
    Strng = Strng.replace("\\''", '\\"')

    Strng = Strng.replace("\\\\м", "\\м")
    Strng = Strng.replace("\\\\m", "\\m")
    Strng = Strng.replace("\\\\'", "\\'")
    Strng = Strng.replace('\\\\"', '\\"')
    Strng = Strng.replace("\\\\_", "\\_")

    vedicDiacRoman = ["IAST", "IASTPali", "ISO", "Titus", "ISOPali"]
    vedicnonDiacRoman = ["HK", "Itrans", "Velthuis", "SLP1", "WX"]

    if Target in vedicDiacRoman:
        Strng = VedicSvarasDiacrtics(Strng, Target)
    elif Target == "IPA":
        Strng = Strng.replace('\\"', "↑↑").replace("\\_", "↓").replace("\\'", "↑")
        Strng = Strng.replace("\\m++", "gͫ̄")
        Strng = Strng.replace("\\m+", "gͫ")
    elif Target == "RomanReadable" or Target == "RomanColloquial":
        Strng = Strng.replace('\\"', "").replace("\\_", "").replace("\\'", "")
        Strng = Strng.replace("\\m++", "ggum")
        Strng = Strng.replace("\\m+", "gum")
    elif Target in vedicnonDiacRoman:
        pass
    elif Target == "RussianCyrillic":
        Strng = VedicSvarasCyrillic(Strng, Target)
    else:
        Strng = VedicSvarasOthers(Strng, Target)

    return Strng


def PostFixRomanOutput(Strng, Source, Target):
    Strng = Strng.replace("\u02BD", "")

    Strng = FixVedic(Strng, Target)

    if Target in ["IAST", "ISO", "ISOPali", "Titus"]:
        Strng = (
            Strng.replace("uʼ", "ü")
            .replace("ūʼ", "ǖ")
            .replace("aʼ", "ö")
            .replace("āʼ", "ȫ")
        )

    if Source == "Sinhala" and Target == "IPA":
        Strng = SinhalaIPAFix(Strng)

    if Target == "IPA":
        Strng = FixIPA(Strng)

    if Target == "Santali":
        Strng = FixSantali(Strng)

    if Target == "Avestan":
        Strng = FixAvestan(Strng)

    if Target == "SoraSompeng":
        Strng = FixSoraSompeng(Strng)

    if Target == "WarangCiti":
        Strng = FixWarangCiti(Strng)

    if Target == "Wancho":
        Strng = FixWancho(Strng)

    if Target == "Mro":
        Strng = FixMro(Strng)

    if Target == "RomanReadable":
        Strng = FixRomanReadable(Strng)
        if Source == "Tamil":
            Strng = Strng.replace("t", "th").replace("d", "dh").replace("h'", "")

    if Target == "RomanColloquial":
        if Source == "Tamil":
            Strng = Strng.replace("t", "th").replace("d", "dh").replace("h'", "")
        if Source == "Oriya":
            Strng = Strng.replace("ksh", "x")
            Strng = re.sub("x(?=[aeiou])", "ksh", Strng)
            Strng = Strng.replace("jny", "gy").replace("sh", "s").replace("r'", "d")
        if Source == "Bengali":
            Strng = Strng.replace("m'", "ng")

        Strng = FixRomanColloquial(Strng)

    if Target == "IAST" or Target == "IASTPali":
        Strng = Strng.replace("a_i", "aï")
        Strng = Strng.replace("a_u", "aü")

    if Target == "ISO" or Target == "ISOPali":
        Strng = Strng.replace("\\’", "\\'")
        Strng = Strng.replace("\\’\u02BD", "\\'")

        Strng = Strng.replace("a_i", "a:i")
        Strng = Strng.replace("a_u", "a:u")

    if Target == "Velthuis" or Target == "Itrans":
        Strng = Strng.replace("\\.a", "\\'")

    if Target == "Aksharaa":
        Strng = Strng.replace("\\a;", "\\'")

    if Target == "HanifiRohingya":
        Strng = FixHanifiRohingya(Strng)

    if Target == "Mongolian":
        Strng = FixMongolian(Strng)

    if Source == "RomanSemitic":
        pass

    return Strng


def FixSemiticOutput(Strng, Source, Target):
    Strng = Strng.replace("\u02DE", "")
    try:
        Strng = globals()["Fix" + Target.replace("-", "_")](Strng, Source)
    except KeyError:
        pass

    return Strng


def FixIndicOutput(Strng, Source, Target):
    vir = GM.CrunchList("ViramaMap", Target)[0]

    Strng = Strng.replace(vir + "_", vir)

    try:
        Strng = globals()["Fix" + Target](Strng)
    except KeyError:
        pass

    Strng = Strng.replace("\u02BD", "")
    Strng = ShiftDiacritics(Strng, Target, reverse=False)

    vedicScripts = [
        "Assamese",
        "Bengali",
        "Devanagari",
        "Gujarati",
        "Kannada",
        "Malayalam",
        "Oriya",
        "Gurmukhi",
        "Tamil",
        "Telugu",
        "TamilExtended",
        "Grantha",
        "Sharada",
    ]

    if Target not in vedicScripts:
        Strng = Strng.replace("॒", "↓")
        Strng = Strng.replace("᳚", "↑↑")
        Strng = Strng.replace("॑", "↑")

    return Strng


def FixHebr(Strng, Source, reverse=False):
    vowelsigns = (
        "(" + "|".join(GM.CrunchSymbols(GM.VowelSigns, "Hebrew") + ["\u05BC"]) + ")"
    )
    vowelsigns2 = (
        "(" + "|".join(GM.CrunchSymbols(GM.VowelSigns, "Hebrew") + ["\u05BC"]) + ")?"
    )

    if not reverse:
        Strng = re.sub("(׳)" + vowelsigns + vowelsigns2, r"\3\2\1", Strng)
        Strng = re.sub("(וֹ)(׳)", r"\2\1", Strng)
        Strng = re.sub("(וּ)(׳)", r"\2\1", Strng)
        Strng = re.sub("(׳)(\u05b7)", r"\2\1", Strng)
        Strng = re.sub("(׳)(\u05b7)", r"\1", Strng)
    else:
        vowels = [
            "ְ",
            "ֱ",
            "ֲ",
            "ֳ",
            "ִ",
            "ֵ",
            "ֶ",
            "ַ",
            "ָ",
            "ֹ",
            "ֺ",
            "ֻ",
            "ׇ",
            "\u05BC",
        ]
        vowelsR = "(" + "|".join(vowels + ["וֹ", "וּ"]) + ")"
        Strng = re.sub(vowelsR + "(׳)", r"\2\1", Strng)
        Strng = re.sub(vowelsR + "(׳)", r"\2\1", Strng)

        Strng = re.sub(vowelsR + "(׳)", r"\2\1", Strng)
        Strng = re.sub(vowelsR + "(׳)", r"\2\1", Strng)

    return Strng


def FixHebrew(Strng, reverse=False):
    vowelsigns = "(" + "|".join(GM.CrunchSymbols(GM.VowelSigns, "Hebrew")) + ")"
    consonants = (
        "(" + "|".join(GM.CrunchSymbols(GM.Consonants, "Hebrew") + ["צּ", "גּ"]) + ")"
    )

    vowelsignsA = (
        "(" + "|".join(GM.CrunchSymbols(GM.VowelSigns, "Hebrew") + ["ַ"]) + ")"
    )
    vowelsignsAD = (
        "(" + "|".join(GM.CrunchSymbols(GM.VowelSigns, "Hebrew") + ["ַ", "ּ"]) + ")"
    )

    vowelsignsADShin = (
        "("
        + "|".join(GM.CrunchSymbols(GM.VowelSigns, "Hebrew") + ["ַ", "ּ", "ׁ"])
        + ")"
    )
    vowelsignsADShinG = (
        "("
        + "|".join(GM.CrunchSymbols(GM.VowelSigns, "Hebrew") + ["ַ", "ּ", "ׁ", "׳"])
        + ")"
    )

    finalCons = ["כ", "מ", "נ", "פ", "צ", "פּ", "כּ"]
    finals = ["ך", "ם", "ן", "ף", "ץ", "ףּ", "ךּ"]

    otherCons = "ב,ח,ע,צ,ש,ת".split(",")
    consonantsAll = (
        "("
        + "|".join(
            GM.CrunchSymbols(GM.Consonants, "Hebrew") + finals + otherCons + ["׳"]
        )
        + ")"
    )

    if not reverse:
        Strng = Strng.replace("\u02BD", "")
        Strng = Strng.replace("\u02BE", "")
        Strng = Strng.replace("ג׳ְג׳", "גּ׳").replace("צ׳ְצ׳", "צּ׳")
        Strng = re.sub("מְ" + "\u02BC" + "([גדזטכצקת])", "נְ" + r"\1", Strng)
        Strng = re.sub("מְ" + "\u02BC", "מְ", Strng)
        Strng = re.sub(
            consonants + "(?!" + vowelsigns + ")", r"\1" + "\u05B7" + r"\2", Strng
        )

        Strng = Strng.replace("\u05b7\u05Bc", "\u05Bc\u05b7")
        Strng = Strng.replace("\u05b7\u05b7", "\u05B7")
        Strng = Strng.replace("\u05b7\u05bc\u05B0", "\u05bc\u05B0")
        Strng = re.sub("(׳)" + vowelsigns, r"\2\1", Strng)
        Strng = re.sub("(וֹ)(׳)", r"\2\1", Strng)
        Strng = re.sub("(וּ)(׳)", r"\2\1", Strng)
        Strng = re.sub("(׳)(\u05b7)", r"\2\1", Strng)
        Strng = re.sub("(׳)(\u05b7)", r"\1", Strng)
        Strng = re.sub("(\u05b7)" + vowelsigns, r"\2", Strng)
        Strng = re.sub("(\u05b7)" + "(\u05BC)" + vowelsigns, r"\2\3", Strng)
        Strng = re.sub(
            "([" + "ושרקסנמליזטײ" + "הגדת" + "])(ְ)" + r"\1", r"\1" + "ּ", Strng
        )
        Strng = re.sub("(שׁ)(ְ)" + r"\1", r"\1" + "ּ", Strng)
        Strng = (
            Strng.replace("כְּכּ", "קּ").replace("פְּפּ", "פּ").replace("בְּבּ", "בּ")
        )
        shortVowels = (
            "("
            + "|".join(
                [
                    "\u05B7",
                    "\u05B8",
                    "\u05B4",
                    "\u05BB",
                    "\u05B5",
                    "\u05B6",
                    "\u05B9",
                    "\u05B0",
                ]
            )
            + ")"
        )

        vowelsAll = (
            "("
            + "|".join(
                [
                    "\u05B7",
                    "\u05B8",
                    "\u05B4",
                    "\u05BB",
                    "\u05B5",
                    "\u05B6",
                    "\u05B9",
                    "\u05B0",
                    "י",
                    "וֹ",
                    "וּ",
                ]
                + ["׳"]
            )
            + ")"
        )

        for c, f in zip(finalCons, finals):
            Strng = re.sub(
                vowelsAll
                + "("
                + c
                + ")"
                + shortVowels
                + "(׳?)"
                + "(?!"
                + consonantsAll
                + "|י|ו)",
                r"\1" + f + r"\3" + r"\4",
                Strng,
            )

        Strng = re.sub(
            "(?<!ה)(ְ)(׳?)" + "(?!" + consonantsAll + "|י|ו)", r"\2\3", Strng
        )

        Strng = Strng.replace("װ" + "\u05B9", "\u05D5\u05BA")

        Strng = Strng.replace("װ", "\u05D5")
        Strng = Strng.replace("ײ", "י")

        Strng = Strng.replace("\u02BC", "")

    else:
        vowels = ["ְ", "ֱ", "ֲ", "ֳ", "ִ", "ֵ", "ֶ", "ַ", "ָ", "ֹ", "ֺ", "ֻ", "ׇ"]
        vowelsR = "(" + "|".join(vowels + ["וֹ", "וּ"]) + ")"

        for f, c in zip(finals, finalCons):
            Strng = Strng.replace(f, c)

        Strng = re.sub(vowelsR + "([ּׁׂ])", r"\2\1", Strng)
        Strng = Strng.replace("אֲ", "אַ")
        Strng = Strng.replace("עֲ", "אַ")

        Strng = (
            Strng.replace("\u05B1", "\u05B6")
            .replace("\u05B3", "\u05B9")
            .replace("\u05B2", "\u05b7")
        )

        Strng = re.sub("(?<=[ֵֶַָֹ])([א])" + "(?!" + vowelsignsA + ")", "", Strng)
        Strng = re.sub("(?<=[ִֵֶַָֹֻ])([ה])" + "(?!" + vowelsignsAD + ")", "", Strng)
        Strng = re.sub("(?<=[ֵֶ])([י])" + "(?!" + vowelsR + vowelsigns + ")", "", Strng)
        Strng = Strng.replace("הּ", "ה")
        Strng = re.sub("([" + "שרקסנמליזט" + "])(ּ)", r"\1" + "ְ" + "ְ" + r"\1", Strng)
        Strng = re.sub("([דתצה])(ּ)", r"\1" + "ְ" + "ְ" + r"\1", Strng)
        Strng = (
            Strng.replace("ת", "ט")
            .replace("ח", "כ")
            .replace("ע", "א")
            .replace("שׂ", "ס")
        )
        Strng = re.sub("ש(?![ׂׄ])", "שׁ", Strng)
        Strng = Strng.replace("ׁׁ", "ׁ")
        Strng = re.sub("ב(?!ּ)", "װ", Strng)
        Strng = re.sub(vowelsR + "(׳)", r"\2\1", Strng)
        Strng = Strng.replace("גּ׳", "ג׳ְג׳").replace("צּ׳", "צ׳ְצ׳")
        Strng = re.sub("צ" + "(?!׳)", "טְְס", Strng)
        Strng = re.sub("(\s|^|\.|,|א)" + "(וֹ|וּ)", "א" + r"\1\2", Strng)
        Strng = re.sub("(וּ)" + vowelsignsA, "װְװ" + r"\2", Strng)
        Strng = re.sub("י" + "(?=" + vowelsigns + "|ַ)", "ײ", Strng)
        Strng = re.sub("ו" + "(?=" + "[ְִֵֶַָׇֺֻ]" + "|ַ)", "װ", Strng)
        Strng = re.sub("(?<!ִ)(י)", "ײ", Strng)
        Strng = re.sub("(ו)(?![ֹֺּ])", "װ", Strng)
        Strng = Strng.replace("ֺ", "ֹ")
        Strng = re.sub("[א](?!" + vowelsR + ")", "", Strng)
        Strng = re.sub(
            consonantsAll + "(?!" + vowelsignsADShinG + ")", r"\1" + "ְ" + r"\2", Strng
        )
        Strng = Strng.replace("אְ", "")
        if "௞" in Strng:
            Strng = Strng.replace("௞", "")
            Strng = Strng.replace("ְ" + "ְ", "ְ")
        else:
            Strng = re.sub("(\s|\.|,|^)" + consonantsAll + "(ְ)", r"\1\2" + "ֶ", Strng)
            Strng = re.sub("(ּ)" + "(ְ)", r"\1" + "ֶ", Strng)
            Strng = re.sub(
                consonantsAll + "(" "ְ" + "ְ" + ")" + "(" + r"\1" + ")(" + "ְ" + ")",
                r"\1\2\3" + "ֶ",
                Strng,
            )
            Strng = re.sub(
                consonantsAll + "(ְ)" + "(" + r"\1" + ")" + "(?!(\s|\.|\n|,|$))",
                r"\1" + "ֶ" + r"\3",
                Strng,
            )
            Strng = re.sub(
                consonantsAll + "(ְ)" + consonantsAll + "(ְ)" + "(?!(\s|\.|\n|,|$))",
                r"\1\2" + r"\3" + "ֶ",
                Strng,
            )

            Strng = Strng.replace("ְ" + "ְ", "ְ")
            Strng = Strng.replace("ֶ" + "ְ", "ְ")

        Strng = re.sub("(?<![אע])\u05B7", "", Strng)

    Strng = Strng.replace("௞", "")

    return Strng


def FixMongolian(Strng, reverse=False):
    vowels = "(" + "|".join(GM.CrunchSymbols(GM.Vowels, "Mongolian")) + ")"
    consonants = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, "Mongolian")) + ")"

    if not reverse:
        Strng = re.sub("(\u180B)" + consonants, r"\2", Strng)
        Strng = re.sub("(\u180B)" + vowels, r"\2", Strng)

        Strng = re.sub(
            consonants + consonants + consonants + vowels + "(\u1880)",
            r"\5\1\2\3\4",
            Strng,
        )
        Strng = re.sub(
            consonants + consonants + vowels + "(\u1880)", r"\4\1\2\3", Strng
        )
        Strng = re.sub(consonants + "?" + vowels + "(\u1880)", r"\3\1\2", Strng)
        Strng = Strng.replace(" \u02BC", "\u200B")
        Strng = Strng.replace("\u02BC", "\u200B")

    else:
        Strng = re.sub("(ᠠ)(?<!\u180B)", r"\1" + "\u180B", Strng)

    return Strng


def FixHanifiRohingya(Strng, reverse=False):
    consList = (
        "("
        + "|".join(
            GM.CrunchSymbols(GM.Consonants, "HanifiRohingya")
            + ["\U00010D17", "\U00010D19"]
        )
        + ")"
    )
    vowList = "(" + "|".join(GM.CrunchSymbols(GM.Vowels, "HanifiRohingya")) + ")"

    vowListNotA = (
        "(" + "|".join(GM.CrunchSymbols(GM.Vowels, "HanifiRohingya")[1:]) + ")"
    )

    consListLookBehind = "".join(
        map(
            lambda x: "(?<!" + x + ")",
            GM.CrunchSymbols(GM.Consonants, "HanifiRohingya"),
        )
    )

    if not reverse:
        Strng = re.sub(consListLookBehind + vowList, "\U00010D00" + r"\1", Strng)
        Strng = re.sub(consList + r"\1", r"\1" + "\U00010D27", Strng)

        Strng = re.sub(vowListNotA + "𐴀𐴟", r"\1" + "\U00010D17", Strng)
        Strng = re.sub(vowListNotA + "𐴀𐴞", r"\1" + "\U00010D19", Strng)

        Strng = Strng.replace("\U00010D24\\", "\U00010D25")
        Strng = Strng.replace("\U00010D24/", "\U00010D26")

        Strng = Strng.replace("_", "\U00010D22")

    else:
        tones = "([\U00010D24\U00010D25\U00010D26])"
        Strng = re.sub("(\U00010D00)" + tones + vowList, r"\1\3\2", Strng)
        Strng = re.sub(consList + tones + vowList, r"\1\3\2", Strng)

        Strng = re.sub(
            vowListNotA.replace("\U00010D00", "") + "\U00010D17", r"\1" + "𐴀𐴟", Strng
        )
        Strng = re.sub(
            vowListNotA.replace("\U00010D00", "") + "\U00010D19", r"\1" + "𐴀𐴞", Strng
        )

        Strng = Strng.replace("\U00010D00", "")
        Strng = re.sub("(.)" + "\U00010D27", r"\1\1", Strng)

        Strng = Strng.replace("\U00010D25", "\U00010D24\\")
        Strng = Strng.replace("\U00010D26", "\U00010D24/")

        Strng = re.sub(consList + "\U00010D17", r"\1" + "\U00010D16\u02BE", Strng)

        Strng = re.sub(consList + "\U00010D19", r"\1" + "\U00010D18\u02BE", Strng)

        Strng = Strng.replace("\U00010D22", "_")

        Strng = Strng.replace("𐴜", "𐴖")

    if not reverse:
        for x, y in zip([",", "?", ";"], ["،", "؟", "؛"]):
            Strng = Strng.replace(x, y)
    else:
        for x, y in zip([",", "?", ";"], ["،", "؟", "؛"]):
            Strng = Strng.replace(y, x)

    return Strng


def FixMasaramGondi(Strng, reverse=False):
    consList = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, "MasaramGondi")) + ")"

    if not reverse:
        Strng = Strng.replace("𑴌𑵅𑴪", "\U00011D2E")
        Strng = Strng.replace("𑴓𑵅𑴕", "\U00011D2F")
        Strng = Strng.replace("𑴛𑵅𑴦", "\U00011D30")

        Strng = re.sub(consList + "\U00011D45\U00011D26", r"\1" + "\U00011D47", Strng)
        Strng = re.sub("\U00011D26\U00011D45" + consList, "\U00011D46" + r"\1", Strng)

        Strng = re.sub("\U00011D45(?!" + consList + ")", "\U00011D44", Strng)
    else:
        Strng = Strng.replace("\U00011D2E", "𑴌𑵅𑴪")
        Strng = Strng.replace("\U00011D2F", "𑴓𑵅𑴕")
        Strng = Strng.replace("\U00011D30", "𑴛𑵅𑴦")

        Strng = Strng.replace(
            "\U00011D47",
            "\U00011D45\U00011D26",
        )
        Strng = Strng.replace("\U00011D46", "\U00011D26\U00011D45")

        Strng = Strng.replace("\U00011D44", "\U00011D45")

    return Strng


def FixGunjalaGondi(Strng, reverse=False):
    consList = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, "GunjalaGondi")) + ")"

    if not reverse:
        Strng = re.sub(
            "(\U00011D7A\u02BE)([\U00011D7B\U00011D7C\U00011D80\U00011D81])",
            "\U00011D95" + r"\1",
            Strng,
        )
        Strng = re.sub(
            "(\U00011D7A\u02BF)([\U00011D7D\U00011D7E\U00011D82\U00011D83])",
            "\U00011D95" + r"\1",
            Strng,
        )

        Strng = Strng.replace("\u02BE", "")
        Strng = Strng.replace("\u02BF", "")
        Strng = re.sub("\U00011D97(?!" + consList + ")", "", Strng)
    else:
        pass

    return Strng


def FixSoyombo(Strng, reverse=False):
    finVir = [
        "\U00011A5E\U00011A99",
        "\U00011A5C\U00011A99",
        "\U00011A60\U00011A99",
        "\U00011A6D\U00011A99",
        "\U00011A6F\U00011A99",
        "\U00011A72\U00011A99",
        "\U00011A74\U00011A99",
        "\U00011A7C\U00011A99",
        "\U00011A7D\U00011A99",
        "\U00011A7F\U00011A99",
        "\U00011A81\U00011A99",
    ]
    fin = [
        "\U00011A8A",
        "\U00011A8B",
        "\U00011A8C",
        "\U00011A8D",
        "\U00011A8E",
        "\U00011A8F",
        "\U00011A90",
        "\U00011A91",
        "\U00011A92",
        "\U00011A93",
        "\U00011A94",
    ]
    consList = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, "Soyombo")) + ")"

    if not reverse:
        Strng = Strng.replace("𑩜𑪙𑪀", "\U00011A83")
        Strng = re.sub(
            "\U00011A7F\U00011A99" + "(?=" + consList + ")", "\U00011A88", Strng
        )
        Strng = re.sub("(?<!𑪙)(.)𑪙" + r"\1", r"\1" + "\U00011A98", Strng)
        if "\u02BE" in Strng:
            for x, y in zip(finVir, fin):
                Strng = re.sub(x + "(?!" + consList + ")", y, Strng)

            Strng = re.sub("𑪈(?!" + consList + ")", "\U00011A93", Strng)

            Strng = Strng.replace("\u02BE", "")

        Strng = re.sub("\U00011A99(?!" + consList + ")", "", Strng)
    else:
        Strng = Strng.replace("\U00011A9A", " ")
        Strng = Strng.replace("\U00011A83", "𑩜𑪙𑪀")

        Strng = re.sub("(.)\U00011A98", r"\1" + "\U00011A99" + r"\1", Strng)

        viraCon = [
            "\U00011A7C\U00011A99",
            "\U00011A7D\U00011A99",
            "\U00011A81\U00011A99",
            "\U00011A7F\U00011A99",
        ]
        initial = ["\U00011A86", "\U00011A87", "\U00011A89", "\U00011A88"]

        for x, y in zip(viraCon, initial):
            Strng = Strng.replace(y, x)

        tsaSeries = ["𑩵", "𑩶", "𑩷"]
        caSeries = ["𑩡", "𑩢", "𑩣"]

        for x, y in zip(tsaSeries, caSeries):
            Strng = Strng.replace(y, x)

        for x, y in zip(finVir, fin):
            Strng = Strng.replace(y, x)

    return Strng


def FixKharoshthi(Strng, reverse=False):
    Strng = KharoshthiNumerals(Strng, reverse)

    return Strng


def FixMarchen(Strng, reverse=False):
    subjoinCons = "𑱲 𑱳 𑱴 𑱵 𑱶 𑱷 𑱸 𑱹 𑱺 𑱻 𑱼 𑱽 𑱾 𑱿 𑲀 𑲁 𑲂 𑲃 𑲄 𑲅 𑲆 𑲇 𑲉 𑲊 𑲋 𑲌 𑲍 𑲎".split(" ")
    subjoined = "𑲒 𑲓 𑲔 𑲕 𑲖 𑲗 𑲘 𑲙 𑲚 𑲛 𑲜 𑲝 𑲞 𑲟 𑲠 𑲡 𑲢 𑲣 𑲤 𑲥 𑲦 𑲧 𑲩 𑲪 𑲫 𑲬 𑲭 𑲮".split(" ")

    if not reverse:
        for x, y in zip(subjoinCons, subjoined):
            Strng = Strng.replace("ʾ" + x, y)

        Strng = Strng.replace("ʾ", "")
        Strng = Strng.replace("\u02BF", "")

    else:
        tsaSeries = ["\U00011C82", "\U00011C83", "\U00011C84"]
        jaSereis = ["\U00011C76", "\U00011C77", "\U00011C78"]

        for x, y in zip(tsaSeries, jaSereis):
            Strng = Strng.replace(y, x)

        for x, y in zip(subjoinCons, subjoined):
            Strng = Strng.replace(y, "ʾ" + x)

    return Strng


def FixMro(Strng, reverse=False):
    extracons = [
        "\U00016A4E",
        "\U00016A59",
        "\U00016A5A",
        "\U00016A5B",
        "\U00016A5C",
        "\U00016A5E",
    ]
    consnormaldig = ["𖩃𖩢", "𖩌𖩢", "𖩍𖩢", "𖩍𖩣", "𖩉𖩢", "𖩀𖩢"]
    consnormal = ["𖩃", "𖩌", "𖩍", "𖩍", "𖩉", "𖩀"]

    if not reverse:
        for x, y in zip(consnormaldig, extracons):
            Strng = Strng.replace(x, y)
    else:
        for x, y in zip(extracons, consnormal):
            Strng = Strng.replace(x, y)

    return Strng


def FixWancho(Strng, reverse=False):
    tonemarks = ["\U0001E2EC", "\U0001E2ED", "\U0001E2EE", "\U0001E2EF"]
    tonewri = ["\\_", "\\-", "\\!", "\\;"]

    nasalization = [
        "\U0001E2E6",
        "\U0001E2E7",
        "\U0001E2E8",
        "\U0001E2EA",
    ]
    nasvowels = ["\U0001E2D5", "\U0001E2DB", "\U0001E2C0", "\U0001E2DE"]

    Anusvaras = ["\U0001E2E2", "\U0001E2E3", "\U0001E2E4", "\U0001E2E5"]
    AnusvaraVowels = ["\U0001E2D5", "\U0001E2C0", "\U0001E2C1", "\U0001E2DC"]

    if not reverse:
        for x, y in zip(tonemarks, tonewri):
            Strng = Strng.replace(y, x)

        for x, y in zip(nasvowels, nasalization):
            Strng = Strng.replace(x + "ʿ", y)

        Strng = Strng.replace("ʿ", "𞋉")

        for x, y in zip(AnusvaraVowels, Anusvaras):
            Strng = Strng.replace(x + "ʾ", y)

        Strng = Strng.replace("ʾ", "𞋝")

        Strng = Strng.replace("𞋋𞋗", "\U0001E2E1")
        Strng = Strng.replace("𞋋𞋎", "\U0001E2E0")

        Strng = Strng.replace("𞋓Ø", "\U0001E2D2")
        Strng = Strng.replace("Ø", "")

    else:
        for x, y in zip(tonemarks, tonewri):
            Strng = Strng.replace(x, y)

        for x, y in zip(nasvowels, nasalization):
            Strng = Strng.replace(y, x + "ʿ")

        for x, y in zip(AnusvaraVowels, Anusvaras):
            Strng = Strng.replace(y, x + "ʾ")

        Strng = Strng.replace("\U0001E2E1", "𞋋𞋗")
        Strng = Strng.replace("\U0001E2E0", "𞋋𞋎")

        Strng = Strng.replace("\U0001E2D2", "𞋓Ø")

    return Strng


def FixSiddham(Strng, reverse=False):
    if not reverse:
        pass
    else:
        Strng = Strng.replace("𑗜", "𑖲")
        Strng = Strng.replace("𑗝", "𑖳")
        Strng = Strng.replace("𑗛", "𑖄")
        Strng = Strng.replace("𑗘", "𑖂")
        Strng = Strng.replace("𑗙", "𑖂")
        Strng = Strng.replace("𑗚", "𑖃")

    return Strng


def FixBhaiksuki(Strng, reverse=False):
    if not reverse:
        Strng = Strng.replace(" ", "𑱃")
    else:
        Strng = Strng.replace("𑱃", " ")

    return Strng


def FixKhudawadi(Strng, reverse=False):
    sindhi = ["𑊽", "𑋃", "𑋉", "𑋕"]
    sindhiapprox = ["ˍ𑊼", "ˍ𑋂", "ˍ𑋈", "ˍ𑋔"]

    if not reverse:
        for x, y in zip(sindhi, sindhiapprox):
            Strng = Strng.replace(y, x)
    else:
        for x, y in zip(sindhi, sindhiapprox):
            Strng = Strng.replace(x, y)

    return Strng


def FixTamil(Strng, reverse=False):
    Strng = CorrectRuLu(Strng, "Tamil", reverse)

    ava = Tamil.SignMap[0]
    avaA = "\u0028\u0B86\u0029"

    VedicSign = ["॑", "॒", "᳚"]
    TamilDiacritic = ["ʼ", "ˮ", "꞉"]

    if not reverse:
        Strng = Strng.replace(ava + ava, avaA)
        Strng = post_processing.RetainDandasIndic(Strng, "Tamil", True)
        Strng = post_processing.RetainIndicNumerals(Strng, "Tamil", True)

        for x in TamilDiacritic:
            for y in VedicSign:
                Strng = Strng.replace(x + y, y + x)
    else:
        Strng = Strng.replace(avaA, ava + ava)
        Strng = Strng.replace("ஷ²", "ஶ")

        Strng = Strng.replace("𑌃", "꞉")

        for x in TamilDiacritic:
            for y in VedicSign:
                Strng = Strng.replace(y + x, x + y)

    return Strng


def FixOriya(Strng, reverse=False):
    if not reverse:
        pass
    else:
        Strng = Strng.replace("ଵ", "ୱ")

    return Strng


def FixGurmukhi(Strng, reverse=False):
    Strng = CorrectRuLu(Strng, "Gurmukhi", reverse)

    ava = Gurmukhi.SignMap[0]
    avaA = "\u0028\u0A06\u0029"

    if not reverse:
        Strng = Strng.replace(ava + ava, avaA)
        Strng = post_processing.InsertGeminationSign(Strng, "Gurmukhi")
        Strng = post_processing.RetainIndicNumerals(Strng, "Gurmukhi", True)

        Vedicomp = "([" + "".join(GM.VedicSvarasList) + "])"

        Strng = re.sub(
            Vedicomp + "\u0A71" + "(.)",
            r"\1" + r"\2" + Gurmukhi.ViramaMap[0] + r"\2",
            Strng,
        )

    else:
        Strng = Strng.replace(avaA, ava + ava)
        Strng = post_processing.ReverseGeminationSign(Strng, "Gurmukhi")
        Strng = Strng.replace("ੰਨ", "ਨ੍ਨ")
        Strng = Strng.replace("ੰਮ", "ਮ੍ਮ")
        Strng = Strng.replace("\u0A70", "\u0A02")
        Strng = post_processing.GurmukhiYakaash(Strng, True)

    return Strng


def CorrectRuLu(Strng, Target, reverse=False):
    ra = GM.CrunchList("ConsonantMap", Target)[26]
    la = GM.CrunchList("ConsonantMap", Target)[27]
    uuu = GM.CrunchSymbols(GM.VowelSigns, Target)[4:6]
    ap = "\u02BC"
    ruCons = [ra + x + ap for x in uuu] + [la + x + ap for x in uuu]
    for x, y in zip(ruCons, GM.CrunchSymbols(GM.Vowels, Target)[6:10]):
        if not reverse:
            Strng = Strng.replace(x, y)
        else:
            Strng = Strng.replace(y, x)

    return Strng


def ShiftDiacritics(Strng, Target, reverse=False):
    VS = "|".join(GM.CrunchSymbols(GM.VowelSigns, Target))
    Diac = "|".join(GM.Diacritics)

    if not reverse:
        Strng = re.sub("(" + Diac + ")" + "(" + VS + ")", r"\2\1", Strng)

        if Target == "Tamil":
            Strng = Strng.replace(
                "³்",
                "்³",
            )

    else:
        if Target == "Tamil":
            Strng = Strng.replace(
                "்³",
                "³்",
            )

        Strng = re.sub("(" + VS + ")" + "(" + Diac + ")", r"\2\1", Strng)

    return Strng


def FixTamilExtended(Strng, reverse=False):
    if not reverse:
        Strng = Strng.replace("ക്‌ഷ", "ക്ഷ")
        Strng = Strng.replace("ശ്‌ര", "ശ്‍ര")
        Strng = Strng.replace("ൗ", "ൌ")

        for svara in GM.VedicSvarasList:
            Strng = Strng.replace("\u200C" + svara, svara + "\u200C")
    else:
        for svara in GM.VedicSvarasList:
            Strng = Strng.replace(svara + "\u200C", "\u200C" + svara)

        Strng = Strng.replace("\u0D4D", "\u0D4D\u200C")

    return Strng


def FixTamilGrantha(Strng, reverse=False):
    ListC = "|".join(GM.CrunchSymbols(GM.Consonants, "TamilGrantha"))
    ListEAI = "|".join(
        TamilGrantha.VowelSignMap[9:11] + TamilGrantha.SouthVowelSignMap[0:1]
    )
    ListOAU = TamilGrantha.VowelSignMap[11:13] + TamilGrantha.SouthVowelSignMap[1:2]

    if not reverse:
        Strng = re.sub(
            "(" + ListC + ")" + "(" + ListEAI + ")",
            "\u200B\u200C\u200D\u200C" + r"\2\1",
            Strng,
        )
        Strng = re.sub(
            "(" + ListC + ")" + "(" + ListOAU[0] + ")",
            "\u200B\u200C\u200D\u200C"
            + TamilGrantha.VowelSignMap[9]
            + r"\1"
            + TamilGrantha.VowelSignMap[0],
            Strng,
        )
        Strng = re.sub(
            "(" + ListC + ")" + "(" + ListOAU[2] + ")",
            "\u200B\u200C\u200D\u200C"
            + TamilGrantha.SouthVowelSignMap[0]
            + r"\1"
            + TamilGrantha.VowelSignMap[0],
            Strng,
        )
        Strng = re.sub(
            "(" + ListC + ")" + "(" + ListOAU[1] + ")",
            "\u200B\u200C\u200D\u200C"
            + TamilGrantha.SouthVowelSignMap[0]
            + r"\1"
            + Tamil.SouthConsonantMap[0],
            Strng,
        )
        Strng = re.sub(
            "(\u200B\u200C\u200D\u200C.)" + "(" + ListC + ")" + "(்ˆ)", r"\2\3\1", Strng
        )

    else:
        Strng = re.sub(
            "\u200B"
            + TamilGrantha.VowelSignMap[9]
            + "("
            + ListC
            + ")"
            + TamilGrantha.VowelSignMap[0],
            r"\1" + ListOAU[0],
            Strng,
        )
        Strng = re.sub(
            "\u200B"
            + TamilGrantha.SouthVowelSignMap[0]
            + "("
            + ListC
            + ")"
            + TamilGrantha.VowelSignMap[0],
            r"\1" + ListOAU[2],
            Strng,
        )
        Strng = re.sub(
            "\u200B"
            + TamilGrantha.SouthVowelSignMap[0]
            + "("
            + ListC
            + ")"
            + Tamil.SouthConsonantMap[0],
            r"\1" + ListOAU[1],
            Strng,
        )
        Strng = re.sub(
            "\u200B" + "(" + ListEAI + ")" + "(" + ListC + ")", r"\2\1", Strng
        )

    return Strng


def FixKhmer(Strng, reverse=False):
    ListC = "|".join(GM.CrunchSymbols(GM.Consonants, "Khmer"))
    ra = Khmer.ConsonantMap[26]
    vir = Khmer.ViramaMap[0]

    if not reverse:
        Strng = re.sub(vir + "(" + ListC + ")", "\u17D2" + r"\1", Strng)
        Strng = re.sub(
            "(?<!\u17D2)(" + ra + ")" + "\u17D2" + "(" + ListC + ")",
            r"\2" + "\u17CC",
            Strng,
        )
        Strng = Strng.replace("\u1787\u17C6", "\u17B9")
    else:
        Strng = Strng.replace("\u17D2", vir)
        Strng = re.sub(vir + "(?=[\u17AB\u17AC\u17AD\u17AE])", "\u17D2", Strng)
        Strng = re.sub("(" + ListC + ")" + "\u17CC", ra + vir + r"\1", Strng)
        Strng = Strng.replace("\u17B9", "\u1787\u17C6")

    return Strng


def FixKhamtiShan(Strng, reverse=False):
    if not reverse:
        Strng = Strng.replace("်ရ", "ြ")
        Strng = Strng.replace("်ယ", "ျ")
        Strng = Strng.replace("်ဝ", "ွ")
        Strng = Strng.replace("\u103C\u103B", "\u103B\u103C")
        Strng = Strng.replace("\u103D\u103B", "\u103B\u103D")
        Strng = Strng.replace("ႂ\u103C", "\u103Cွ")
    else:
        Strng = Strng.replace("ꩳ", "ရ")
        Strng = Strng.replace("\u103B\u103C", "\u103C\u103B")
        Strng = Strng.replace("\u103B\u103D", "\u103D\u103B")
        Strng = Strng.replace("\u103Cႂ", "ႂ\u103C")

        Strng = Strng.replace("ြ", "်ꩳ")
        Strng = Strng.replace("ꩳ", "ရ")
        Strng = Strng.replace("ျ", "်ယ")
        Strng = Strng.replace("ွ", "်ဝ")

    return Strng


def FixTaiLaing(Strng, reverse=False):
    if not reverse:
        Strng = Strng.replace("်ꩺ", "ြ")
        Strng = Strng.replace("်ယ", "ျ")
        Strng = Strng.replace("်ဝ", "ႂ")
        Strng = Strng.replace("\u103C\u103B", "\u103B\u103C")
        Strng = Strng.replace("\u103D\u103B", "\u103B\u103D")
        Strng = Strng.replace("ႂ\u103C", "\u103Cႂ")
        Strng = Strng.replace("ႂျ", "်၀ျ")

    else:
        Strng = Strng.replace("\u103B\u103C", "\u103C\u103B")
        Strng = Strng.replace("\u103B\u103D", "\u103D\u103B")
        Strng = Strng.replace("\u103Cႂ", "ႂ\u103C")

        Strng = Strng.replace("ြ", "်ꩺ")
        Strng = Strng.replace("ျ", "်ယ")
        Strng = Strng.replace("ႂ", "်ဝ")

    return Strng


def FixShan(Strng, reverse=False):
    if not reverse:
        Strng = Strng.replace("်ရ", "ြ")
        Strng = Strng.replace("်ယ", "ျ")
        Strng = Strng.replace("်ဝ", "\u1082")
        Strng = Strng.replace("်ႁ", "ှ")
        Strng = re.sub("(ှ)" + "([ျြွ])", r"\2\1", Strng)
        Strng = Strng.replace("\u103C\u103B", "\u103B\u103C")
        Strng = Strng.replace("\u103D\u103B", "\u103B\u103D")
        Strng = Strng.replace("ွ\u103C", "\u103Cွ")

    else:
        Strng = re.sub("([ျြွ])" + "(ှ)", r"\2\1", Strng)
        Strng = Strng.replace("\u103B\u103C", "\u103C\u103B")
        Strng = Strng.replace("\u103B\u103D", "\u103D\u103B")
        Strng = Strng.replace("\u103Cွ", "ွ\u103C")
        Strng = Strng.replace("ြ", "်ရ")
        Strng = Strng.replace("ျ", "်ယ")
        Strng = Strng.replace("ွ", "်ဝ")
        Strng = Strng.replace("\u1082", "်ဝ")
        Strng = Strng.replace("ှ", "်ႁ")

    return Strng


def FixMon(Strng, reverse=False):
    pairs = [("င", "ၚ"), ("ဉ", "ည"), ("ဈ", "ၛ")]

    for x, y in pairs:
        Strng = Strng.replace(y, x)

    Strng = FixBurmese(Strng, reverse)

    Strng = Strng.replace("ည", "\uE001")

    for x, y in pairs:
        Strng = Strng.replace(x, y)

    Strng = Strng.replace("\uE001", "ည\u1039ည")

    medials_cons_mon = ["\u1039န", "\u1039မ", "\u1039လ"]
    medials_mon = ["ၞ", "ၟ", "ၠ"]

    if not reverse:
        for x, y in zip(medials_cons_mon, medials_mon):
            Strng = Strng.replace(x, y)

        Strng = Strng.replace("ၠြ", "ြၠ")

        for i, med1 in enumerate(medials_mon):
            for j, med2 in enumerate(medials_mon):
                Strng = Strng.replace(
                    med1 + med2, medials_cons_mon[i] + medials_cons_mon[j]
                )
        for i, med in enumerate(medials_mon):
            Strng = Strng.replace(med + "ျ", medials_cons_mon[i] + "ျ")

            Strng = Strng.replace("ရ်" + med, "ရ်" + medials_cons_mon[i])
            Strng = Strng.replace("ၚ်" + med, "ၚ်" + medials_cons_mon[i])
    else:
        Strng = Strng.replace("်ရၠ", "ၠ်ရ")

        for x, y in zip(medials_cons_mon, medials_mon):
            Strng = Strng.replace(y, x)

        Strng = Strng.replace("\u1039", "်")

    return Strng


def FixBurmese(Strng, reverse=False):
    ListC = "|".join(GM.CrunchSymbols(GM.Consonants, "Burmese"))
    vir = Burmese.ViramaMap[0]

    AA = Burmese.VowelSignMap[0]
    E = Burmese.VowelSignMap[9]

    yrvh = (
        Burmese.ConsonantMap[25:27]
        + Burmese.ConsonantMap[28:29]
        + Burmese.ConsonantMap[32:33]
    )
    yrvhsub = ["\u103B", "\u103C", "\u103D", "\u103E"]

    TallACons = "|".join([Burmese.ConsonantMap[x] for x in [1, 2, 4, 17, 20, 28]])

    if not reverse:
        Strng = re.sub("(?<!ာ)" + vir + "(" + ListC + ")", "\u1039" + r"\1", Strng)
        Strng = re.sub(
            "(" + Burmese.ConsonantMap[4] + ")" + "(" + "\u1039" + ")",
            r"\1" + vir + r"\2",
            Strng,
        )

        Strng = re.sub("(ရ)" + "(" + "\u1039" + ")", r"\1" + vir + r"\2", Strng)

        Strng = re.sub(
            "(?<!\u1039)(" + TallACons + ")" + "(" + E + "?)" + AA,
            r"\1\2" + "\u102B",
            Strng,
        )

        Strng = re.sub(
            "(" + TallACons + ")(\u1039)(" + ListC + ")" + "(" + E + "?)" + AA,
            r"\1\2\3\4" + "\u102B",
            Strng,
        )
        Strng = re.sub(
            "("
            + TallACons
            + ")(\u1039)("
            + ListC
            + ")"
            + "(\u1039)("
            + ListC
            + ")"
            + "("
            + E
            + "?)"
            + AA,
            r"\1\2\3\4\5\6" + "\u102B",
            Strng,
        )

        Strng = re.sub(
            "(?<=်္)" + "(" + TallACons + ")" + "(" + E + "?)" + AA,
            r"\1\2" + "\u102B",
            Strng,
        )

        for x, y in zip(yrvh, yrvhsub):
            Strng = re.sub("(?<!်)\u1039" + x, y, Strng)

        Strng = re.sub("ျါ", "ျာ", Strng)

        Strng = re.sub("(?<!ဂ)ြါ", "ြာ", Strng)

        Strng = re.sub("ျေါ", "ျော", Strng)

        Strng = re.sub("(?<!ဂ)ြေါ", "ြော", Strng)

        Strng = Strng.replace("သ္သ", "ဿ")
        Strng = Strng.replace("ဉ္ဉ", "ည")

        Strng = Strng.replace("\u02F3", "့")
        Strng = Strng.replace(
            "့်",
            "့်",
        )

        Strng = Strng.replace("ာ္", "ာ်")

        Strng = re.sub("(ရ်္င်္)" + "(" + ListC + ")", "ရ်္င္" + r"\2", Strng)

        Strng = Strng.replace("ါ္", "ါ်")

        Strng = Strng.replace("\u103A\u1039\u101A", "\u103B")
        Strng = Strng.replace("\u103C\u103A\u1039ဝ", "\u103Cွ")
        Strng = re.sub("(ှ)" + "([ျြွ])", r"\2\1", Strng)
        Strng = Strng.replace("\u103C\u103B", "\u103B\u103C")
        Strng = Strng.replace("\u103D\u103B", "\u103B\u103D")
        Strng = Strng.replace("ွ\u103C", "\u103Cွ")
        Strng = Strng.replace("ရျ", "ရ်္ယ")
        Strng = Strng.replace("ငျ", "င်္ယ")

    else:
        Strng = re.sub("([ျြွ])" + "(ှ)", r"\2\1", Strng)
        Strng = Strng.replace("\u103B\u103C", "\u103C\u103B")
        Strng = Strng.replace("\u103B\u103D", "\u103D\u103B")
        Strng = Strng.replace("\u103Cွ", "ွ\u103C")

        Strng = Strng.replace("ဿ", "သ္သ")
        Strng = Strng.replace("ည", "ဉ္ဉ")

        Strng = Strng.replace("့်", "့်")
        Strng = Strng.replace("့", "\u02F3")
        Strng = Strng.replace("\u1039", vir)
        Strng = Strng.replace("\u102B", AA)
        Strng = Strng.replace(
            Burmese.ConsonantMap[4] + vir + vir, Burmese.ConsonantMap[4] + vir
        )
        Strng = Strng.replace("ရ" + vir + vir, "ရ" + vir)

        for x, y in zip(yrvh, yrvhsub):
            Strng = Strng.replace(y, vir + x)

    return Strng


def AddRepha(Strng, Script, Repha, reverse=False):
    vir = GM.CrunchSymbols(GM.VowelSigns, Script)[0]
    ra = GM.CrunchSymbols(GM.Consonants, Script)[26]

    ListC = "|".join(GM.CrunchSymbols(GM.Consonants, Script))
    ListV = "|".join(GM.CrunchSymbols(GM.Vowels, Script))
    ListVS = "|".join(GM.CrunchSymbols(GM.VowelSignsNV, Script))

    if not reverse:
        Strng = re.sub(
            "(" + ListC + "|" + ListV + "|" + ListVS + ")" + "(" + ra + vir + ")",
            r"\1" + Repha,
            Strng,
        )
    else:
        Strng = Strng.replace(Repha, ra + vir)

    return Strng


def FixTagbanwa(Strng, reverse=False):
    if not reverse:
        Strng = post_processing.InsertGeminationSign(Strng, "Tagbanwa")
    else:
        pass

    return Strng


def FixBuhid(Strng, reverse=False):
    if not reverse:
        Strng = post_processing.InsertGeminationSign(Strng, "Buhid")
    else:
        pass

    return Strng


def FixBuginese(Strng, reverse=False):
    if not reverse:
        Strng = Strng.replace("ᨂ\u02BEᨀ", "ᨃ")
        Strng = Strng.replace("ᨆ\u02BEᨄ", "ᨇ")
        Strng = Strng.replace("ᨊ\u02BEᨑ", "ᨋ")
        Strng = Strng.replace("ᨎ\u02BEᨌ", "ᨏ")

        Strng = post_processing.InsertGeminationSign(Strng, "Buginese")

        Strng = Strng.replace("\u02BE", "")
    else:
        Strng = Strng.replace("ᨃ", "ᨂ\u02BEᨀ")
        Strng = Strng.replace("ᨇ", "ᨆ\u02BEᨄ")
        Strng = Strng.replace("ᨋ", "ᨊ\u02BEᨑ")
        Strng = Strng.replace("ᨏ", "ᨎ\u02BEᨌ")

    return Strng


def FixBalinese(Strng, reverse=False):
    Repha = "\u1B03"

    Strng = AddRepha(Strng, "Balinese", Repha, reverse)

    return Strng


def FixJavanese(Strng, reverse=False):
    Repha = "\uA982"
    vir = Javanese.ViramaMap[0]
    ra, ya = Javanese.ConsonantMap[26], Javanese.ConsonantMap[25]
    SubRa, SubYa = "\uA9BF", "\uA9BE"

    Strng = AddRepha(Strng, "Javanese", Repha, reverse)

    if not reverse:
        Strng = Strng.replace(vir + ra, SubRa).replace(vir + ya, SubYa)
    else:
        Strng = Strng.replace(SubRa, vir + ra).replace(SubYa, vir + ya)

    return Strng


def FixUrdu(Strng, reverse=False):
    return FixUrduShahmukhi("Urdu", Strng, reverse)


def FixShahmukhi(Strng, reverse=False):
    return FixUrduShahmukhi("Shahmukhi", Strng, reverse)


def FixUrduShahmukhi(Target, Strng, reverse=False):
    Strng = Strng.replace("\u02BD", "")

    vir = GM.CrunchSymbols(GM.VowelSigns, Target)[0]

    ConUnAsp = [
        GM.CrunchList("ConsonantMap", Target)[x]
        for x in [0, 2, 5, 7, 10, 12, 15, 17, 20, 22, 4, 9, 14, 19, 24]
        + list(range(25, 33))
    ]

    ConUnAsp = (
        ConUnAsp
        + GM.CrunchList("SouthConsonantMap", Target)
        + GM.CrunchList("NuktaConsonantMap", Target)
    )

    ShortVowels = "|".join(["\u0652", "\u064E", "\u0650", "\u064F"])
    a = "\u064E"
    ya = "\u06CC"
    va = "\u0648"
    yaBig = "\u06D2"
    Aa = Urdu.VowelSignMap[0]

    if not reverse:
        ListVS = "(" + "|".join(GM.CrunchSymbols(GM.VowelSigns, Target)) + ")"
        ListV = "(" + "|".join(GM.CrunchSymbols(GM.Vowels, Target)) + ")"
        ListVSA = "(" + "|".join(GM.CrunchSymbols(GM.VowelSigns, Target) + [a]) + ")"

        hamzaFull = "\u0621"
        hamzaChair = "\u0626"

        Strng = re.sub(ListVS + ListV, r"\1" + hamzaFull + r"\2", Strng)
        Strng = re.sub(ListV + ListV, r"\1" + hamzaFull + r"\2", Strng)
        Strng = re.sub(
            "(" + a + ")" + ListV + "(?!" + ListVSA + ")",
            r"\1" + hamzaFull + r"\2",
            Strng,
        )

        Strng = re.sub("(" + a + ")" + "(" + ShortVowels + ")", r"\2", Strng)
        Strng = re.sub(
            "(?<!"
            + Aa
            + ")"
            + "("
            + a
            + ")"
            + "("
            + va
            + "|"
            + ya
            + ")"
            + "(?!"
            + ShortVowels
            + ")",
            r"\2",
            Strng,
        )
        ListC = "|".join(GM.CrunchSymbols(GM.Consonants, Target)).replace(a, "")
        Ayoga = "|".join(Urdu.AyogavahaMap[0] + Urdu.AyogavahaMap[1])

        Strng = Strng.replace(ya, yaBig)
        Strng = re.sub(
            "(" + yaBig + ")" + "(?=" + "|".join(ConUnAsp) + ShortVowels + ")",
            ya,
            Strng,
        )
        Strng = re.sub("(" + yaBig + ")" + "(" + ListC + ")", ya + r"\2", Strng)
        Strng = re.sub("(" + yaBig + ")" + "(" + Ayoga + ")", ya + r"\2", Strng)

        Strng = Strng.replace("\u0650" + yaBig, "\u0650" + ya)

        ConAsp = [
            GM.CrunchList("ConsonantMap", Target)[x]
            for x in [1, 3, 6, 8, 11, 13, 16, 18, 21, 23]
        ]
        ConUnAsp_a = [x.replace("\u064e", "") for x in ConUnAsp]

        Strng = re.sub(
            "(" + "|".join(ConUnAsp_a) + ")" + "(" + vir + ")" + r"\1",
            r"\1" + GM.Gemination[Target],
            Strng,
        )

        Strng = re.sub("(.)(ّ)(\u06BE)", r"\1\3\2", Strng)

        Strng = Strng.replace("ےے", "یے")
        Strng = Strng.replace("ےی", "یی")
        Strng = Strng.replace("ےْ", "یْ")
        Strng = Strng.replace("ءاِی", "\u0626\u0650\u06CC")
        Strng = Strng.replace("ءاے", "ئے")
        Strng = Strng.replace("ءای", "ئی")
        Strng = Strng.replace("ءاو", "ؤ")
        Strng = Strng.replace("ءاُو", "\u0624\u064F")

        Strng = Strng.replace("ءاُ", "\u0624\u064F")

        Strng = re.sub("(" + hamzaFull + ")(اُو)", r"\1" + "\u0624\u064F", Strng)
        Strng = re.sub("(" + hamzaFull + ")(اُ)", r"\1" + "\u0624\u064F", Strng)

        Strng = re.sub("(" + hamzaFull + ")(او)", r"\1" + "\u0624", Strng)

        Strng = Strng.replace("ءاِ", "\u0626\u0650")
        Strng = Strng.replace("ئِءآ", "\u0626\u0650\u0627")

        Strng = re.sub(
            "(" + hamzaFull + ")(\u0627\u0650)", r"\1" + "\u0626\u0650", Strng
        )

        Strng = re.sub("(" + hamzaFull + ")(ا)(ے|ی)", r"\1" + "\u0626" + r"\3", Strng)

        Strng = Strng.replace("ئِئ", "ئِ")
        Strng = Strng.replace("ئِؤ", "ئِو")

        Strng = Strng.replace("ࣇ", "لؕ")

        if Target == "Shahmukhi":
            Strng = re.sub("(ن|م|ی|ر|ل|و)(\u0652)(ہ)", r"\1" + "\u06BE", Strng)

    else:
        if True:
            Strng = re.sub("(\s)\u06BE", r"\1" + "ہ", Strng)

            Strng = Strng.replace("ۓ", "_\u06d2")

            if Target == "Shahmukhi":
                Strng = re.sub("(ن|م|ی|ر|ل|و)(\u06BE)", r"\1" + "\u0652ہ", Strng)

            Strng = Strng.replace("لؕ", "ࣇ")

            ListC = GM.CrunchSymbols(GM.Consonants, Target)

            Strng = Strng.replace("ص", "س")
            Strng = Strng.replace("ث", "س")

            Strng = Strng.replace("ح", "ہ")
            Strng = Strng.replace("ۃ", "ہ")

            Strng = Strng.replace("ذ", "ز")
            Strng = Strng.replace("ض", "ز")
            Strng = Strng.replace("ظ", "ز")

            Strng = Strng.replace("ط", "ت")

            Strng = Strng.replace("ژ", "ز")

            Strng = Strng.replace("ع", "اَ")

            Strng = Strng.replace("ً", "نْ")

            Strng = Strng.replace("ئ", "_" + ya)

            Strng = Strng.replace("ؤ", "_" + va + a)

            Strng = Strng.replace("ء", "_")

            Strng = Strng.replace("یٰ", "ا")

            Strng = Strng.replace("ك", "ک")

            Strng = Strng.replace("ي", "ی")

            Strng = re.sub("(\u06BE)(ّ)", r"\2\1", Strng)

            Strng = re.sub("(" + ShortVowels + ")(ّ)", r"\2" + r"\1", Strng)
            Strng = re.sub("(.)(ّ)", r"\1" + "ْ" + r"\1", Strng)

            if "\u02BB\u02BB" in Strng:
                Strng = Strng.replace("ا", "اَ")

                Strng = Strng.replace("لؕ", "لَؕ")
                for c in ListC:
                    Strng = Strng.replace(c.replace(a, ""), c)
                    Strng = Strng.replace(c + "اَ", c + "ا")
                    Strng = Strng.replace(c + "ا" + "و", c + "ا" + "\u200B" + "و")
                    Strng = Strng.replace(c + "ا" + "ی", c + "ا" + "\u200B" + "ی")

                Strng = Strng.replace(a + "ھ", "ھ" + a)

                Strng = Strng.replace("ھ" + a + "اَ", "ھ" + a + "ا")

                Strng = Strng.replace(
                    "ھ" + a + "ا" + "و", "ھ" + a + "ا" + "\u200B" + "و"
                )
                Strng = Strng.replace(
                    "ھ" + a + "ا" + "ی", "ھ" + a + "ا" + "\u200B" + "ی"
                )

                Strng = Strng.replace(a + a, a)

                Strng = Strng.replace("اَے", "اے")
                Strng = Strng.replace(yaBig, ya)

                Strng = Strng.replace("\u02BB\u02BB", "")

            else:
                ShortVowelsR = "|".join(["\u0652", "\u0650", "\u064F"])
                longVowels = "|".join(["و", "ا", ya])

                Strng = Strng.replace(yaBig, ya)

                ListCR = "|".join(GM.CrunchSymbols(GM.Consonants, Target)).replace(
                    a, ""
                )

                Strng = re.sub(
                    "(" + ListCR + ")" + "(" + ShortVowelsR + ")",
                    r"\1" + a + r"\2",
                    Strng,
                )
                Strng = re.sub(
                    "("
                    + ListCR
                    + ")"
                    + "("
                    + longVowels
                    + ")"
                    + "(?!"
                    + ShortVowels
                    + ")",
                    r"\1" + a + r"\2",
                    Strng,
                )

                Strng = re.sub("(" + ListCR + ")" + "(_)", r"\1" + a + r"\2", Strng)

            VowelVS = "|".join(GM.CrunchSymbols(GM.VowelSigns, Target))

    if not reverse:
        pass
    else:
        pass

    Strng = PersoArabicPuntuation(Strng, reverse)

    return Strng


def PersoArabicPuntuation(Strng, reverse=False):
    if not reverse:
        for x, y in zip([",", "?", ";"], ["،", "؟", "؛"]):
            Strng = Strng.replace(x, y)
        Strng = Strng.replace(".", "۔")
    else:
        for x, y in zip([",", "?", ";"], ["،", "؟", "؛"]):
            Strng = Strng.replace(y, x)
        Strng = Strng.replace("۔", ".")

    return Strng


def FixThaana(Strng, reverse=False):
    ListC = "|".join(GM.CrunchSymbols(GM.Consonants, "Thaana"))
    VowelVS = "|".join(GM.CrunchSymbols(GM.VowelSigns, "Thaana"))
    aBase = "\u0787"

    if not reverse:
        Strng = post_processing.InsertGeminationSign(Strng, "Thaana")
        Strng = re.sub("(\u07A6)" + "(?=(" + VowelVS + "))", "", Strng)
        Strng = Strng.replace("\u02BE", "")

        for x, y in zip([",", "?", ";"], ["،", "؟", "؛"]):
            Strng = Strng.replace(x, y)

        Strng = Strng.replace("ʔ", "އް")

    else:
        Strng = Strng.replace("ޢ", "އ")
        Strng = Strng.replace("ޡ", "ތ")
        Strng = Strng.replace("ޥ", "ވ")
        Strng = Strng.replace("ޠ", "ތ")
        Strng = Strng.replace("ޟ", "ސ")
        Strng = Strng.replace("ޞ", "ސ")
        Strng = Strng.replace("ޜ", "ށ")
        Strng = Strng.replace("ޛ", "ދ")
        Strng = Strng.replace("ޘ", "ތ")
        Strng = Strng.replace("ޛ", "ދ")
        Strng = Strng.replace("ޙ", "ހ")

        Strng = re.sub(
            "(" + ListC.replace("ަ", "") + ")" + "(?!" + VowelVS + "|ަ" + ")",
            r"\1" + "ް",
            Strng,
        )

        Strng = re.sub(
            "(?<!" + aBase + ")(?<!" + "\u02BD\u02BD\u02BD" + ")(" + VowelVS + ")",
            "\u07A6" + r"\1",
            Strng,
        )
        Strng = post_processing.ReverseGeminationSign(Strng, "Thaana")

        Strng = Strng.replace("އް", "ʔ")

        for x, y in zip([",", "?", ";"], ["،", "؟", "؛"]):
            Strng = Strng.replace(y, x)

    return Strng


def FixSaurashtra(Strng, reverse=False):
    if not reverse:
        Strng = Strng.replace("ꢒ꣄ꢰ", "ꢒ꣄‍ꢰ")
    else:
        Strng = Strng.replace("ꢴ", "꣄ꢲ")

    return Strng


def FixTibetan(Strng, reverse=False):
    ListC = [Tibetan.ViramaMap[0] + chr(x) for x in range(0x0F40, 0x0F68)]
    ListSubC = [chr(x + 80) for x in range(0x0F40, 0x0F68)]

    SubC = ["ཝྭ", "ཡྱ", "རྱ", "རྭ", "ྺྭ"]
    SubMinC = ["ཝྺ", "ཡྻ", "ཪྻ", "ཪྺ", "ྺྺ"]

    if not reverse:
        for x, y in zip(ListC, ListSubC):
            Strng = Strng.replace(x, y)

        for x, y in zip(SubC, SubMinC):
            Strng = Strng.replace(x, y)

        Strng = Strng.replace(" ", "\u0F0B")

        Strng = Strng.replace("ཛྷ༹", "ཞ")

        Strng = Strng.replace("(", "༺")
        Strng = Strng.replace(")", "༻")

        Strng = Strng.replace("{", "༼")
        Strng = Strng.replace("}", "༽")

    if reverse:
        AspirateDecom = ["གྷ", "ཌྷ", "དྷ", "བྷ", "ཛྷ", "ྒྷ", "ྜྷ", "ྡྷ", "ྦྷ", "ྫྷ"]
        AspirateAtomic = ["གྷ", "ཌྷ", "དྷ", "བྷ", "ཛྷ", "ྒྷ", "ྜྷ", "ྡྷ", "ྦྷ", "ྫྷ"]

        Strng = Strng.replace("ཇྷ", "ཛྷ")

        for x, y in zip(AspirateDecom, AspirateAtomic):
            Strng = Strng.replace(x, y)

        for x, y in zip(SubC, SubMinC):
            Strng = Strng.replace(y, x)

        for x, y in zip(ListC, ListSubC):
            Strng = Strng.replace(y, x)

        for x, y in zip(["྄རྀ", "྄རཱྀ", "྄ལྀ", "྄ལཱྀ"], ["ྲྀ", "ྲཱྀ", "ླྀ", "ླཱྀ"]):
            Strng = Strng.replace(x, y)

        Strng = Strng.replace("་", " ")
        Strng = Strng.replace("༔", "།")
        Strng = Strng.replace("༈", "།")

        Strng = Strng.replace("༺", "(")
        Strng = Strng.replace("༻", ")")

        Strng = Strng.replace("༼", "{")
        Strng = Strng.replace("༽", "}")

        Strng = Strng.replace("འ", "ཨ")
        Strng = Strng.replace("ཇ", "ཛ")

        Strng = Strng.replace("ཞ", "ཛྷ༹")

    return Strng


def ReverseVowelSigns(Strng, Script, reverse=False):
    EAIO = "|".join(
        sorted(
            GM.CrunchSymbols(GM.VowelSignsNV, Script)[9:12]
            + GM.CrunchSymbols(GM.VowelSignsNV, Script)[17:],
            key=len,
            reverse=True,
        )
    )
    cons = "|".join(GM.CrunchSymbols(GM.Consonants, Script))
    a = GM.CrunchSymbols(GM.Vowels, Script)[0].split()[0]
    consa = "|".join(GM.CrunchSymbols(GM.Consonants, Script) + [a])

    if Script == "Thai":
        EAIO += "|ใ"
        cons = "|".join(
            GM.CrunchSymbols(GM.Consonants, Script) + ["ฮ", "บ", "ฝ", "ด", "ฦ", "ฤ"]
        )

    if Script == "Lao":
        cons = "|".join(GM.CrunchSymbols(GM.Consonants, Script) + ["ດ", "ບ", "ຟ"])

    a = GM.CrunchSymbols(GM.Vowels, Script)[0]

    if not reverse:
        Strng = re.sub("(" + consa + ")(" + EAIO + ")", r"\2\1", Strng)
    else:
        Strng = re.sub("(" + EAIO + ")" + "(" + consa + ")", r"\2\1", Strng)

    return Strng


def FixKhomThai(Strng, reverse=False):
    if not reverse:
        Strng = Strng.replace("โ", "เา")
        Strng = ThaiReverseVowelSigns(Strng, reverse)
        Strng = re.sub("(.\u0E3A)(.\u0E3A)(ใ)", r"\3\1\2", Strng)
        Strng = re.sub("(.\u0E3A)(ใ)", r"\2\1", Strng)

        Strng = re.sub("((.\u0E3A)+)(เ)", r"\3\1", Strng)
        Strng = re.sub("(.\u0E3A)?(.)(ฺร)", r"\3\1\2", Strng)
        Strng = Strng.replace("เอา", "โอ")

        Strng = Strng.replace("เอำ", "เาอํ")
        Strng = Strng.replace("เาอํ", "โอํ")
    else:
        Strng = re.sub("(ใ)(.\u0E3A)(.\u0E3A)", r"\2\3\1", Strng)
        Strng = re.sub("(ใ)(.\u0E3A)", r"\2\1", Strng)

        Strng = re.sub("(ฺร)(.\u0E3A)?(.)", r"\2\3\1", Strng)
        Strng = re.sub("(เ)((.\u0E3A)+)", r"\2\1", Strng)
        Strng = ThaiReverseVowelSigns(Strng, reverse)
        Strng = Strng.replace("เา", "โ")

    return Strng


def FixThai(Strng, reverse=False):
    Strng = ThaiReverseVowelSigns(Strng, reverse)
    Strng = ThaiDigraphConjuncts(Strng, reverse)

    if "\u02BB\u02BB" in Strng:
        Strng = post_processing.ThaiLaoTranscription(
            Strng, "Thai", "\u0E30", "\u0E31", True
        )
        Strng = Strng.replace("\u02BB\u02BB", "")

        Strng = Strng.replace("หฺ์", "ห์")

    return Strng


def ThaiReverseVowelSigns(Strng, reverse=False):
    Strng = ReverseVowelSigns(Strng, "Thai", reverse)
    if not reverse:
        Strng = Strng.replace("\u0E32\u0E4D", "\u0E33").replace(
            "\u0E34\u0E4D", "\u0E36"
        )
    else:
        Strng = Strng.replace("\u0E33", "\u0E32\u0E4D").replace(
            "\u0E36", "\u0E34\u0E4D"
        )

    return Strng


def FixLaoPali(Strng, reverse=False):
    Strng = ReverseVowelSigns(Strng, "LaoPali", reverse)

    if "\u02BB\u02BB" in Strng:
        Strng = LaoPaliTranscribe(Strng, True)
        Strng = Strng.replace("\u02BB\u02BB", "")

        Strng = Strng.replace("ຫ຺໌", "ຫ໌")

    if not reverse:
        Strng = Strng.replace("\u0EB2\u0ECD", "\u0EB3")
    else:
        Strng = Strng.replace("\u0EB3", "\u0EB2\u0ECD")

    return Strng


def FixMakasar(Strng, reverse=False):
    ListC = "|".join(Makasar.ConsonantMap)
    ListV = "|".join(Makasar.VowelSignMap)
    Anka = "\U00011EF2"

    if not reverse:
        Strng = post_processing.InsertGeminationSign(Strng, "Makasar")
        Strng = Strng.replace("\u02BE", "")
        Strng = re.sub(
            "(" + ListC + ")" + "(" + ListV + ")?" + r"\1", r"\1" + r"\2" + Anka, Strng
        )
    else:
        Strng = re.sub(
            "(" + ListC + ")" + "(" + ListV + ")?" + Anka, r"\1" + r"\2" + r"\1", Strng
        )

    return Strng


def FixAvestan(Strng, reverse=False):
    extraCons = ["\U00010B33", "\U00010B32", "\U00010B1D", "\U00010B12", "𐬣", "𐬝"]
    ListC = "|".join(GM.CrunchSymbols(GM.Consonants, "Avestan") + extraCons)
    ListV = "|".join(GM.CrunchSymbols(GM.Vowels, "Avestan"))

    ya = Avestan.ConsonantMap[25]
    va = Avestan.ConsonantMap[28]
    ii = Avestan.VowelMap[2] * 2
    uu = Avestan.VowelMap[4] * 2

    if not reverse:
        Strng = Strng.replace("𐬀𐬩", "𐬄")
        Strng = Strng.replace("𐬁𐬩", "𐬅")

        Strng = re.sub(
            "((" + ListV + ")" + "|" + "(" + ListC + "))" + "(" + ya + ")",
            r"\1" + ii,
            Strng,
        )
        Strng = re.sub(
            "((" + ListV + ")" + "|" + "(" + ListC + "))" + "(" + va + ")",
            r"\1" + uu,
            Strng,
        )

        Strng = Strng.replace(Avestan.ConsonantMap[15] + "\u02BF", "\U00010B1D")
        Strng = Strng.replace(va + "\u02BF", "\U00010B21")

        Strng = Strng.replace("𐬰\u02BF", "𐬲").replace("𐬱\u02BF", "𐬲")
        Strng = Strng.replace("𐬢\u02BF", "𐬤")
        Strng = Strng.replace("𐬁_𐬋", "𐬃")

        Strng = Strng.replace("\u02BF", "")

    else:
        Strng = Strng.replace("𐬄", "𐬀𐬩")
        Strng = Strng.replace("𐬅", "𐬁𐬩")

        Strng = Strng.replace(ii, ya).replace(uu, va)

        Strng = Strng.replace("\U00010B1D", Avestan.ConsonantMap[15] + "\u02BF")
        Strng = Strng.replace("𐬣", Avestan.ConsonantMap[4])

        Strng = Strng.replace("\U00010B12", Avestan.ConsonantMap[1])
        Strng = Strng.replace("\U00010B33", Avestan.ConsonantMap[29])
        Strng = Strng.replace("𐬡", va + "\u02BF")

        Strng = Strng.replace("𐬲", "𐬰\u02BF")
        Strng = Strng.replace("𐬤", "𐬢\u02BF")
        Strng = Strng.replace("𐬃", "𐬁_𐬋")

    return Strng


def FixLao(Strng, reverse=False):
    if reverse:
        Strng = Strng.replace("ດ", "ທ\uEB0A")
        Strng = Strng.replace("ບ", "ປ\uEB0A")
        Strng = Strng.replace("ຟ", "ພ\uEB0A")
        Strng = Strng.replace("ັ", "ະ")

    if not reverse:
        Strng = Strng.replace("ທ\uEB0A", "ດ")
        Strng = Strng.replace("ປ\uEB0A", "ບ")
        Strng = Strng.replace("ພ\uEB0A", "ຟ")

        Strng = re.sub("(?<!ດ)(?<!ບ)(?<!ຟ)\uEB0A", "", Strng)

    Strng = ReverseVowelSigns(Strng, "Lao", reverse)
    Strng = LaoTranscribe(Strng, reverse)

    if not reverse:
        Strng = Strng.replace("\u0EB2\u0ECD", "\u0EB3")

        Strng = Strng.replace("\uEB0A", "")

    else:
        Strng = Strng.replace("\u0EB3", "\u0EB2\u0ECD")

        Strng = Strng.replace("\u0EBA\uEB0A", "\uEB0A\u0EBA")

        Strng = Strng.replace("຺ະ", "")

        Strng = Strng.replace("ອ\u0EBAົ", "ອົ")

    return Strng


def ThaiDigraphConjuncts(Strng, reverse=False):
    EAIO = "".join(Thai.VowelSignMap[9:12])
    cons = "|".join(GM.CrunchSymbols(GM.Consonants, "Thai"))
    yrlvh = "|".join(
        GM.CrunchSymbols(GM.Consonants, "Thai")[25:29]
        + GM.CrunchSymbols(GM.Consonants, "Thai")[32:33]
    )
    sh = "|".join(Thai.ConsonantMap[31:33])
    vir = Thai.ViramaMap[0]
    if not reverse:
        Strng = re.sub(
            "(?<=\s)("
            + cons
            + ")"
            + "("
            + vir
            + ")"
            + "(["
            + EAIO
            + "])"
            + "("
            + cons
            + ")",
            r"\3\1\2\4",
            Strng,
        )
        Strng = re.sub(
            "(" + cons + ")" + "(" + vir + ")" + "([" + EAIO + "])" + "(" + yrlvh + ")",
            r"\3\1\2\4",
            Strng,
        )
        Strng = re.sub(
            "(" + sh + ")" + "(" + vir + ")" + "([" + EAIO + "])" + "(" + cons + ")",
            r"\3\1\2\4",
            Strng,
        )
    else:
        Strng = re.sub(
            "([" + EAIO + "])" + "(" + vir + ")" + "(" + cons + ")", r"\2\3\1", Strng
        )

    return Strng


def FixOldPersian(Strng, reverse=False):
    Strng = OldPersianSyllable(Strng, reverse)
    Strng = OldPersianNumeral(Strng, reverse)

    return Strng


def OldPersianSyllable(Strng, reverse=True):
    ICons = [
        x + "\U000103A1"
        for x in [
            "\U000103AD",
            "\U000103B6",
            "\U000103A9",
            "\U000103BA",
            "\U000103AB",
            "\U000103B4",
            "\U000103BC",
        ]
    ]
    ICons_ = [
        x + "_\U000103A1"
        for x in [
            "\U000103AD",
            "\U000103B6",
            "\U000103A9",
            "\U000103BA",
            "\U000103AB",
            "\U000103B4",
            "\U000103BC",
        ]
    ]
    ISyll = [
        x + "\U000103A1"
        for x in [
            "\U000103AE",
            "\U000103B7",
            "\U000103AA",
            "\U000103BB",
            "\U000103AB",
            "\U000103B4",
            "\U000103BC",
        ]
    ]

    UCons = [
        x + "\U000103A2"
        for x in [
            "\U000103AD",
            "\U000103B6",
            "\U000103A3",
            "\U000103A5",
            "\U000103AB",
            "\U000103B4",
            "\U000103BC",
        ]
    ]
    UCons_ = [
        x + "_\U000103A2"
        for x in [
            "\U000103AD",
            "\U000103B6",
            "\U000103A3",
            "\U000103A5",
            "\U000103AB",
            "\U000103B4",
            "\U000103BC",
        ]
    ]
    USyll = [
        x + "\U000103A2"
        for x in [
            "\U000103AF",
            "\U000103B8",
            "\U000103A4",
            "\U000103A6",
            "\U000103AC",
            "\U000103B5",
            "\U000103BD",
        ]
    ]

    ACons = [
        x + "<\U000103A0"
        for x in [
            "\U000103AD",
            "\U000103B6",
            "\U000103A3",
            "\U000103A5",
            "\U000103A9",
            "\U000103BA",
            "𐎼",
            "𐎴",
            "𐎫",
        ]
    ]
    ASyll = [
        "\U000103AD",
        "\U000103B6",
        "\U000103A3",
        "\U000103A5",
        "\U000103A9",
        "\U000103BA",
        "𐎼",
        "𐎴",
        "𐎫",
    ]

    SylAlpha = "([𐎧𐎨𐏂𐎰𐎱𐎳𐎲𐎹𐎾𐎿𐏀𐏁𐏃])"

    ListC = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, "OldPersian")) + ")"

    if not reverse:
        Strng = Strng.replace(" ", "\U000103D0").replace("_", "").replace("<", "")
        for x, y in zip(ICons + UCons + ACons, ISyll + USyll + ASyll):
            Strng = Strng.replace(x, y)

    else:
        Strng = re.sub("𐎻(?!\U000103A1)", "𐎻\U000103A1", Strng)

        for x, y in zip(ICons_ + UCons_, ISyll + USyll):
            Strng = Strng.replace(y, x)

        Strng = re.sub(SylAlpha + "(𐎠𐎡)", r"\1<\2", Strng)
        Strng = re.sub(SylAlpha + "(𐎠𐎢)", r"\1<\2", Strng)

        Strng = re.sub(ListC + "\U000103A0", r"\1" + "_\U000103A0", Strng)
        Strng = re.sub(SylAlpha + "([\U000103A1\U000103A2])", r"\1_\2", Strng)

        Strng = re.sub(
            "([" + "".join(ASyll) + "])" + "([\U000103A1\U000103A2])",
            r"\1" + "<" + "\U000103A0" + r"\2",
            Strng,
        )

        Strng = Strng.replace("𐏐", " ")

    if not reverse:
        pass

    else:
        pass

    return Strng


def OldPersianNumeral(Strng, reverse=False):
    One = "\U000103D1"
    Two = "\U000103D2"
    Ten = "\U000103D3"
    Twenty = "\U000103D4"
    Hundred = "\U000103D5"

    Numbers = sorted(map(int, re.findall("\d+", Strng)), reverse=True)

    if not reverse:
        for num in Numbers:
            hN = int(num / 100)
            tW = int((num - (hN * 100)) / 20)
            tN = int((num - (hN * 100) - (tW * 20)) / 10)
            t2 = int((num - (hN * 100) - (tW * 20) - (tN * 10)) / 2)
            n1 = int(num - (hN * 100) - (tW * 20) - (tN * 10) - (t2 * 2))

            perNum = (
                (Hundred * hN) + (Twenty * tW) + (Ten * tN) + (Two * t2) + (One * n1)
            )

            Strng = Strng.replace(str(num), perNum)
    else:
        Strng = Strng.replace(One, "1#")
        Strng = Strng.replace(Two, "2#")
        Strng = Strng.replace(Ten, "10#")
        Strng = Strng.replace(Twenty, "20#")
        Strng = Strng.replace(Hundred, "100#")

    return Strng


def KharoshthiNumerals(Strng, reverse=False):
    Numbers = sorted(map(int, re.findall("\d+", Strng)), reverse=True)

    if not reverse:
        for num in Numbers:
            Strng = Strng.replace(str(num), kharoshthiNumber(num))
    else:
        one = "𐩀"
        two = "𐩁"
        three = "𐩂"
        four = "𐩃"
        ten = "𐩄"
        twenty = "𐩅"
        hundred = "𐩆"
        thousand = "𐩇"

        Strng = Strng.replace(one, "1#")
        Strng = Strng.replace(two, "2#")
        Strng = Strng.replace(three, "3#")
        Strng = Strng.replace(four, "4#")
        Strng = Strng.replace(ten, "10#")
        Strng = Strng.replace(twenty, "20#")
        Strng = Strng.replace(hundred, "100#")
        Strng = Strng.replace(thousand, "1000#")

    return Strng


def kharoshthiNumber(Strng):
    one = "𐩀"
    two = "𐩁"
    three = "𐩂"
    four = "𐩃"
    ten = "𐩄"
    twenty = "𐩅"
    hundred = "𐩆"
    thousand = "𐩇"

    num = int(Strng)
    kharnum = ""
    thou = int(num / 1000)
    if thou > 0:
        if thou > 1:
            kharnum += kharoshthiNumber(thou)
        kharnum += thousand
    hund = int((num - (thou * 1000)) / 100)
    if hund > 0:
        if hund > 1:
            kharnum += kharoshthiNumber(hund)
        kharnum += hundred
    twen = int((num - (thou * 1000) - (hund * 100)) / 20)
    if twen > 0:
        kharnum += twenty * twen
    tenn = int((num - (thou * 1000) - (hund * 100) - (twen * 20)) / 10)
    if tenn > 0:
        if tenn > 1:
            kharnum += kharoshthiNumber(tenn)
        kharnum += ten
    ones = int((num - (thou * 1000) - (hund * 100) - (twen * 20) - (tenn * 10)))
    if ones > 0:
        if ones == 1:
            kharnum += one
        elif ones == 2:
            kharnum += two
        elif ones == 3:
            kharnum += three
        elif ones == 4:
            kharnum += four
        elif ones == 5:
            kharnum += four + one
        elif ones == 6:
            kharnum += four + two
        elif ones == 7:
            kharnum += four + three
        elif ones == 8:
            kharnum += four + four
        elif ones == 9:
            kharnum += four + four + one

    return kharnum


def FixSinhala(Strng, reverse=False):
    Strng = post_processing.SinhalaDefaultConjuncts(Strng)

    if not reverse:
        Strng = Strng.replace("\u0DA2\u0DCA\u0DA4", "\u0DA5")

        Strng = Strng.replace("(අ)(අ)", "(ආ)")
    else:
        Strng = Strng.replace("\u0DA5", "\u0DA2\u0DCA\u0DA4")

        Strng = Strng.replace("‍", "")
        Strng = Strng.replace("(ආ)", "(අ)(අ)")

    return Strng


def FixSantali(Strng, reverse=False):
    if not reverse:
        Strng = Strng.replace("ᱹᱸ", "ᱺ")
        Strng = Strng.replace("ᱻᱸ", "ᱸᱻ")
    else:
        Strng = Strng.replace("ᱺ", "ᱹᱸ")
        Strng = Strng.replace("ᱽ", "’")
        Strng = Strng.replace("ᱸᱻ", "ᱻᱸ")

    return Strng


def FixSoraSompeng(Strng, reverse=False):
    ListC = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, "SoraSompeng")) + ")"

    if not reverse:
        Strng = re.sub(ListC + "(ə)", r"\1", Strng)
        Strng = Strng.replace("ə", "\U000110E6\U000110E8")
    else:
        ListV = "(" + "|".join(GM.CrunchSymbols(GM.Vowels, "SoraSompeng")) + ")"
        Strng = re.sub(ListC + "(?!" + ListV + ")", r"\1" + "ə", Strng)

        Strng = Strng.replace("𑃔ə𑃨", "𑃔𑃨ə")

        Strng = Strng.replace("𑃦𑃨", "ə")
        Strng = Strng.replace("ə𑃨", "𑃨")

    return Strng


def FixRomanReadable(Strng, reverse=False):
    if not reverse:
        Strng = Strng.replace("\\n", "\uE001")
        Strng = re.sub("([aiueo])nj([aeiou])", r"\1" + "ny" + r"\2", Strng)
        Strng = re.sub("(\W)nj([aeiou])", r"\1" + "ny" + r"\2", Strng)
        Strng = re.sub("^nj([aeiou])", "ny" + r"\1", Strng)

        Strng = Strng.replace("njnj", "nny")

        Strng = Strng.replace("Mk", "ngk")
        Strng = Strng.replace("Mg", "ngg")
        Strng = Strng.replace("Mc", "njc")
        Strng = Strng.replace("Mj", "njj")
        Strng = Strng.replace("Md", "nd")
        Strng = Strng.replace("Mt", "nt")
        Strng = Strng.replace("Mb", "mb")
        Strng = Strng.replace("Mp", "mp")

        Strng = Strng.replace("M", "m\u034F'")

        Strng = Strng.replace("ngk", "nk")
        Strng = Strng.replace("ngg", "ng")
        Strng = Strng.replace("njc", "nc")
        Strng = Strng.replace("njj", "nj")

        Strng = Strng.replace("jnj", "jny")

        Strng = Strng.replace("\uE001", "\\n")
    else:
        pass

    return Strng


def FixRomanColloquial(Strng, reverse=False):
    if not reverse:
        Strng = Strng.replace("\\n", "\uE001")
        Strng = re.sub("([aiueo])nj([aeiou])", r"\1" + "ny" + r"\2", Strng)
        Strng = re.sub("(\W)nj([aeiou])", r"\1" + "ny" + r"\2", Strng)
        Strng = re.sub("^nj([aeiou])", "ny" + r"\1", Strng)

        Strng = Strng.replace("njnj", "nny")

        Strng = Strng.replace("Mk", "ngk")
        Strng = Strng.replace("Mg", "ngg")
        Strng = Strng.replace("Mc", "njc")
        Strng = Strng.replace("Mj", "njj")
        Strng = Strng.replace("Md", "nd")
        Strng = Strng.replace("Mt", "nt")
        Strng = Strng.replace("Mb", "mb")
        Strng = Strng.replace("Mp", "mp")

        Strng = Strng.replace("M", "m\u034F")

        Strng = Strng.replace("ngk", "nk")
        Strng = Strng.replace("ngg", "ng")
        Strng = Strng.replace("njc", "nc")
        Strng = Strng.replace("njj", "nj")

        Strng = Strng.replace("jnj", "jny")

        Strng = Strng.replace("\uE001", "\\n")

        Strng = Strng.replace("'", "").replace("_", "")
    else:
        pass

    return Strng


def FixWarangCiti(Strng, reverse=False):
    ListC = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, "WarangCiti")) + ")"
    ListV = "(" + "|".join(GM.CrunchSymbols(GM.Vowels, "WarangCiti") + ["\u200D"]) + ")"

    if not reverse:
        Strng = re.sub(ListC + ListC, r"\1" + "\u200D" + r"\2", Strng)

        Strng = re.sub(ListC + "(\U000118C1\U000118D9\u02BE)", r"\1" + "\u00BD", Strng)

        Strng = re.sub(ListC + "(\U000118C1)", r"\1", Strng)

        Strng = re.sub(ListV + "(\U000118C0)", r"\1" + "\u200D" + r"\2", Strng)

        Strng = Strng.replace("\u02BE", "")

        Strng = Strng.replace("𑣟\u02BF", "𑣙𑣗")

        Strng = Strng.replace("\u00BD", "\U000118C1")

        Strng = Strng.replace("\u02BF", "")

    else:
        Strng = Strng.lower()

        Strng = Strng.replace("𑣙𑣗", "𑣟\u02BF")
        Strng = Strng.replace("\u00D7", "\u200D")

        Strng = re.sub(ListC + "(\U000118C1)", r"\1" + "\u00BD", Strng)
        Strng = re.sub("(\u02BF)" + "(\U000118C1)", r"\1" + "\U000118C1\u00BD", Strng)

        Strng = re.sub(ListC + "(?!" + ListV + ")", r"\1" + "\U000118C1", Strng)

        Strng = re.sub(
            "([\U000118D4\U000118D5\U000118CC\U000118CB\U000118CF\U000118CE\U000118D2\U000118D1\U000118D5\U000118D4\U000118D8\U000118D7\U000118DB])(\u200D)(𑣙)",
            r"\1" + "\u00D6" + r"\3",
            Strng,
        )
        Strng = Strng.replace("\u200D", "")
        Strng = Strng.replace("\u00D6", "\u200D")

        Strng = re.sub("(𑣁)" + "(\u02BF)" + ListV, r"\2\3", Strng)

        Strng = Strng.replace("𑣁" + "\u02BB", "")

        Strng = Strng.replace("\U000118C1\u00BD", "\U000118C1\U000118D9\u02BE")

    return Strng


def FixLimbu(Strng, reverse=False):
    vir = Limbu.ViramaMap[0]

    SCons = [vir + x for x in [Limbu.ConsonantMap[x] for x in [25, 26, 28]]]
    SubCons = ["\u1929", "\u192A", "\u192B"]

    for x, y in zip(SCons, SubCons):
        if not reverse:
            Strng = Strng.replace(x, y)
        else:
            Strng = Strng.replace(y, x)

    signAll = "|".join(
        GM.CrunchSymbols(GM.Consonants + GM.Vowels + GM.VowelSignsNV, "Limbu")
    )

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

    if reverse:
        Strng = re.sub(
            "(" + "|".join(FinalCons) + ")" + "(?=[ᤕᤖᤘ])", r"\1" + "\u200C", Strng
        )
        Strng = re.sub("([ᤀᤁᤂᤃᤄᤅᤆᤇᤈᤉᤊᤋᤌᤍᤎᤏᤐᤑᤒᤓᤔᤕᤖᤗᤘᤚᤛᤜᤠᤣᤥᤧᤨᤩᤪᤫ])᤺", r"\1" + "꞉", Strng)

    else:
        Strng = Strng.replace("꞉", "᤺")

    for x, y in zip(FCons, FinalCons):
        if not reverse:
            Strng = re.sub(
                "(" + signAll + ")" + "(\u193A?)" + "(" + x + ")", r"\1\2" + y, Strng
            )
        else:
            Strng = Strng.replace(y, x)

    if not reverse:
        Strng = Strng.replace("ʔ", "᤹")
        Strng = Strng.replace("!", "᥄")
        Strng = Strng.replace("?", "᥅")
    else:
        Strng = Strng.replace("᤹", "ʔ")
        Strng = Strng.replace("᥄", "!")
        Strng = Strng.replace("᥅", "?")

    return Strng


def FixDevanagari(Strng, reverse=False):
    Sindhi = ["ॻ", "ॼ", "ॾ", "ॿ"]
    SindhiApprox = ["ˍग", "ˍज", "ˍड", "ˍब"]
    if not reverse:
        Strng = Strng.replace("ʔ", "ॽ")

        for x, y in zip(Sindhi, SindhiApprox):
            Strng = Strng.replace(y, x)

        Strng = Strng.replace("ज़़", "ॹ")
        Strng = Strng.replace("श़", "ॹ")
        Strng = Strng.replace("ऱ्", "ऱ्‌")
        Strng = Strng.replace("ऱ्‌य", "ऱ्य")
        Strng = Strng.replace("ऱ्‌ह", "ऱ्ह")

        ListC = "|".join(GM.CrunchSymbols(GM.Consonants, "Devanagari"))

        Strng = re.sub("(" + ListC + ")" + "ʼ", r"\1" + "\u093A", Strng)
        Strng = Strng.replace("\u093Eʼ", "\u093B")

    else:
        Strng = Strng.replace("\u0954", "")

        Strng = post_processing.DevanagariPrishtamatra(Strng, reverse=True)
        Strng = Strng.replace("ॽ", "ʔ")
        Strng = Strng.replace("ॹ", "ज़़")

        for x, y in zip(Sindhi, SindhiApprox):
            Strng = Strng.replace(x, y)

    return Strng


def FixKaithi(Strng, reverse=False):
    if not reverse:
        Strng = Strng.replace(" ", "⸱")
    else:
        Strng = Strng.replace("⸱", " ")

    return Strng


def FixLao2(Strng, reverse=False):
    return FixLao(Strng, reverse)


def FixNandinagari(Strng, reverse=False):
    if not reverse:
        pass
    else:
        Strng = post_processing.NandinagariPrishtamatra(Strng, reverse=True)

    return Strng


def FixLepcha(Strng, reverse=False):
    vir = Lepcha.ViramaMap[0]
    la = Lepcha.ConsonantMap[27]

    conLa = [
        x + vir + la
        for x in [Lepcha.ConsonantMap[c] for c in [0, 2, 20, 22, 24, 32]]
        + [Lepcha.NuktaConsonantMap[6]]
    ]
    conL = ["\u1C01", "\u1C04", "\u1C0F", "\u1C14", "\u1C16", "\u1C1E", "\u1C12"]

    for x, y in zip(conLa, conL):
        if not reverse:
            Strng = Strng.replace(x, y)
        else:
            Strng = Strng.replace(y, x)

    yr = [vir + x for x in Lepcha.ConsonantMap[25:27]]
    yrSub = ["\u1C24", "\u1C25"]

    for x, y in zip(yr, yrSub):
        if not reverse:
            Strng = Strng.replace(x, y)
        else:
            Strng = Strng.replace(y, x)

    listNF = [
        Lepcha.ConsonantMap[x]
        for x in [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            16,
            17,
            18,
            21,
            22,
            23,
            29,
            30,
            31,
        ]
    ]
    listF = [
        (Lepcha.ConsonantMap + Lepcha.AyogavahaMap)[x]
        for x in [
            0,
            0,
            0,
            34,
            0,
            0,
            0,
            0,
            19,
            15,
            15,
            15,
            15,
            19,
            15,
            15,
            15,
            20,
            20,
            20,
            15,
            15,
            15,
        ]
    ]

    listNF += Lepcha.ConsonantMap[25:26] + Lepcha.ConsonantMap[28:29]
    listF += Lepcha.VowelMap[2:3] + Lepcha.VowelMap[4:5]

    if not reverse:
        Strng = Strng.replace(Lepcha.NuktaMap[0] + vir, vir)
        Strng = Strng.replace(Lepcha.ConsonantMap[32] + vir, "")
        consAll = (
            "("
            + "|".join(Lepcha.ConsonantMap + Lepcha.VowelMap + Lepcha.VowelSignMap)
            + ")"
        )
        for x, y in zip(listNF, listF):
            Strng = re.sub(consAll + "(" + x + vir + ")", r"\1" + y + vir, Strng)

    else:
        pass

    conFinal = [
        x + vir for x in [Lepcha.ConsonantMap[c] for c in [0, 15, 19, 20, 24, 26, 27]]
    ]
    conF = [
        "\u1C2D",
        "\u1C33",
        "\u1C30",
        "\u1C31",
        "\u1C2E",
        "\u1C32",
        "\u1C2F",
    ]

    signAll = "|".join(
        GM.CrunchSymbols(GM.Consonants + GM.Vowels + GM.VowelSignsNV, "Lepcha")
    )

    for x, y in zip(conFinal, conF):
        if not reverse:
            Strng = re.sub("(" + signAll + ")" + "(" + x + ")", r"\1" + y, Strng)
        else:
            Strng = Strng.replace(y, x)

    signVow = "|".join(GM.CrunchSymbols(GM.VowelSignsNV, "Lepcha"))

    if not reverse:
        Strng = Strng.replace(vir, "")
        Strng = re.sub(
            "(" + signVow + ")" + "(" + Lepcha.AyogavahaMap[1] + ")",
            r"\1" + "\u1C35",
            Strng,
        )
        Strng = Strng.replace("ᰧᰶᰵ", "ᰧᰵᰶ")
    else:
        Strng = Strng.replace("\u1C35", Lepcha.AyogavahaMap[1])
        Strng = Strng.replace("ᰧᰵᰶ", "ᰧᰶᰵ")

    return Strng


def FixSundanese(Strng, reverse=False):
    vir = Sundanese.ViramaMap[0]

    r = Sundanese.ConsonantMap[26] + vir
    ListC = "|".join(
        GM.CrunchSymbols(GM.Consonants + GM.Vowels + GM.VowelSignsNV, "Sundanese")
    )

    if not reverse:
        Strng = re.sub("(" + ListC + ")" + r, r"\1" + "\u1B81", Strng)
    else:
        Strng = Strng.replace("\u1B81", r)
        Strng = post_processing.SundaneseHistoricConjuncts(Strng, reverse)

    yrl = [vir + x for x in Sundanese.ConsonantMap[25:28]]
    yrlSub = ["\u1BA1", "\u1BA2", "\u1BA3"]

    for x, y in zip(yrl, yrlSub):
        if not reverse:
            Strng = Strng.replace(x, y)
        else:
            Strng = Strng.replace(y, x)

    return Strng


def FixRejang(Strng, reverse=False):
    vir = Rejang.ViramaMap[0]

    r = Rejang.ConsonantMap[26] + vir
    n = Rejang.ConsonantMap[19] + vir
    ListC = "|".join(
        GM.CrunchSymbols(GM.Consonants + GM.Vowels + GM.VowelSignsNV, "Rejang")
    )

    if not reverse:
        Strng = re.sub("(" + ListC + ")" + r, r"\1" + "\uA951", Strng)
        Strng = re.sub("(" + ListC + ")" + n, r"\1" + "\uA950", Strng)
    else:
        Strng = Strng.replace("\uA951", r)
        Strng = Strng.replace("\uA950", n)

    return Strng


def FixChakma(Strng, reverse=False):
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

    if not reverse:
        Strng = re.sub("(" + listC + ")" + "(?!" + listV + ")", r"\1" "\u02BE", Strng)
        Strng = Strng.replace("\U00011127", "")
        Strng = Strng.replace("\u02BE", "\U00011127")

        Strng = Strng.replace("𑄣𑄳𑄦", "𑅄")
        Strng = Strng.replace("𑄣𑄴𑄦", "𑅄")
        Strng = re.sub("(" + listC + ")" + "(𑄃𑄨)", r"\1" + "\U0001112D", Strng)
        Strng = Strng.replace(
            "\U0001112C𑄃𑄨ʼ",
            "\U00011146",
        )

    else:
        Strng = post_processing.ChakmaGemination(Strng, reverse=True)

        Strng = Strng.replace("𑅄", "𑄣𑄳𑄦")

        Strng = Strng.replace("\U00011133\U00011103", "\U00011145")
        Strng = Strng.replace("\U00011133\U00011104", "\U00011146")

        Strng = Strng.replace("\U0001112D", "𑄃𑄨")
        Strng = Strng.replace("\U00011146", "\U0001112C𑄃𑄨ʼ")

        Strng = Strng.replace("\U00011127", "\u02BE")
        Strng = re.sub(
            "(" + listC + ")" + "(?!" + listV + "|\u02BE" + ")",
            r"\1" "\U00011127",
            Strng,
        )
        Strng = Strng.replace("\u02BE", "")

    yrlvn = (
        "(" + "|".join(Chakma.ConsonantMap[19:20] + Chakma.ConsonantMap[26:29]) + ")"
    )

    if not reverse:
        Strng = re.sub("\U00011134" + "(?=" + yrlvn + ")", "\U00011133", Strng)

        Strng = post_processing.ChakmaGemination(Strng)
    else:
        Strng = Strng.replace("\U00011133", "\U00011134")

        vowelDepA = ["𑄃𑄨", "𑄃𑄪", "𑄃𑄬"]
        vowelIndep = ["\U00011104", "\U00011105", "\U00011106"]

        for x, y in zip(vowelDepA, vowelIndep):
            Strng = Strng.replace(y, x)

    return Strng


def FixIAST(Strng, reverse=False):
    if reverse:
        Strng = Strng.replace("ṁ", IAST.AyogavahaMap[1])

    return Strng


def FixIPA(Strng, reverse=False):
    colon_tilde = "\u02D0\u0303"
    tilde_colon = "\u0303\u02D0"

    if not reverse:
        Strng = Strng.replace(colon_tilde, tilde_colon)

        Strng = re.sub("(.)(\u02D0?)(\u0068)", r"\1\2\3\1" + "\u0306", Strng)
        Strng = Strng.replace("ə̸ə̸", "ɑ̷ː")
    else:
        Strng = Strng.replace("ɑ̷ː", "ə̸ə̸")

        Strng = Strng.replace(tilde_colon, colon_tilde)

        Strng = re.sub("(.)(\u02D0?)(\u0068)" + r"\1" + "\u0306", r"\1\2\3", Strng)

    return Strng


def FixPhagsPa(Strng, reverse=False):
    candraBindu = PhagsPa.AyogavahaMap[0]
    ListC = "|".join(sorted(PhagsPa.ConsonantMap, key=len, reverse=True))
    ListV = "|".join(sorted(PhagsPa.VowelMap, key=len, reverse=True))
    ListVS = "|".join(sorted(PhagsPa.VowelSignMap, key=len, reverse=True))

    vir = PhagsPa.ViramaMap[0]
    Virrvy = [vir + x for x in [PhagsPa.ConsonantMap[c] for c in [25, 26, 28]]]
    Subrvy = ["\uA868", "\uA871", "\uA867"]

    SubrvyE = ["ꡱꡨ"] + Subrvy

    if not reverse:
        for x, y in zip(Virrvy, Subrvy):
            Strng = Strng.replace(x, y)

        Strng = re.sub("(" + ListV + ")" + "(" + candraBindu + ")", r"\2\1", Strng)

        Strng = re.sub(
            "("
            + ListC
            + ")"
            + "(("
            + "|".join(SubrvyE)
            + ")?)"
            + "(("
            + ListVS
            + ")?)"
            + "("
            + candraBindu
            + ")",
            r"\6\1\2\4",
            Strng,
        )

    else:
        ListV = ListV.replace("\u1E7F", "")

        Strng = Strng.replace("ꡖꡘꡟ", "ꡱꡖꡟ")

        Aspirate = [
            ("\uA842\uA85C", "\u1E7E\uA842\u1E7E\uA85C\u1E7E"),
            ("\uA852\uA85C", "\u1E7E\uA852\u1E7E\uA85C\u1E7E"),
            ("\uA86B\uA85C", "\u1E7E\uA86B\u1E7E\uA85C\u1E7E"),
            ("\uA84A\uA85C", "\u1E7E\uA84A\u1E7E\uA85C\u1E7E"),
            ("\uA84E\uA85C", "\u1E7E\uA84E\u1E7E\uA85C\u1E7E"),
        ]

        for x, y in Aspirate:
            Strng = Strng.replace(x, y)

        Strng = re.sub(
            "(" + PhagsPa.VowelSignMap[0] + ")" + "([" + "".join(Subrvy[1]) + "])",
            r"\2\1",
            Strng,
        )
        Strng = re.sub(
            "("
            + candraBindu
            + ")"
            + "("
            + ListC
            + ")"
            + "(("
            + "|".join(SubrvyE)
            + ")?)"
            + "(("
            + ListVS
            + ")?)",
            r"\2\3\5\1",
            Strng,
        )
        Strng = re.sub("(" + candraBindu + ")" + "(" + ListV + ")", r"\2\1", Strng)

        for x, y in zip(Virrvy, Subrvy):
            Strng = Strng.replace(y, x)

        Strng = re.sub("(" + ListV + ")", "\u1E7F" r"\1", Strng)
        Strng = re.sub("(" + ListC + "|ꡖ)" + "(" + "\u1E7F" + ")", r"\1", Strng)

    if not reverse:
        Strng = Strng.replace(" ", "᠂")
        Strng = Strng.replace("\u02BD", "")

        Strng = re.sub(
            "(("
            + candraBindu
            + ")?"
            + "("
            + ListC
            + ")"
            + "(("
            + "|".join(SubrvyE)
            + ")?)"
            + "(("
            + ListVS
            + ")?))"
            + "(("
            + candraBindu
            + ")?"
            + "("
            + ListC
            + ")"
            + "(("
            + "|".join(SubrvyE)
            + ")?)"
            + "(("
            + ListVS
            + ")?))"
            + "(?!"
            + vir
            + ")",
            r"\1 \8",
            Strng,
        )
        Strng = re.sub(
            "(("
            + candraBindu
            + ")?"
            + "("
            + ListC
            + ")"
            + "(("
            + "|".join(SubrvyE)
            + ")?)"
            + "(("
            + ListVS
            + ")?))"
            + "(("
            + candraBindu
            + ")?"
            + "("
            + ListC
            + ")"
            + "(("
            + "|".join(SubrvyE)
            + ")?)"
            + "(("
            + ListVS
            + ")?))"
            + "(?!"
            + vir
            + ")",
            r"\1 \8",
            Strng,
        )

        Strng = re.sub(
            "(("
            + candraBindu
            + ")?"
            + "("
            + ListV
            + "))"
            + "(("
            + candraBindu
            + ")?"
            + "("
            + ListC
            + ")"
            + "(("
            + "|".join(SubrvyE)
            + ")?)"
            + "(("
            + ListVS
            + ")?))"
            + "(?!"
            + vir
            + ")",
            r"\1 \4",
            Strng,
        )
        Strng = re.sub(
            "(("
            + candraBindu
            + ")?"
            + "("
            + ListV
            + "))"
            + "(("
            + candraBindu
            + ")?"
            + "("
            + ListC
            + ")"
            + "(("
            + "|".join(SubrvyE)
            + ")?)"
            + "(("
            + ListVS
            + ")?))"
            + "(?!"
            + vir
            + ")",
            r"\1 \4",
            Strng,
        )

        Strng = re.sub(
            "(("
            + candraBindu
            + ")?"
            + "("
            + ListC
            + ")"
            + "(("
            + "|".join(SubrvyE)
            + ")?)"
            + "(("
            + ListVS
            + ")?))"
            + "(("
            + candraBindu
            + ")?"
            + "("
            + ListV
            + "))"
            + "(?!"
            + vir
            + ")",
            r"\1 \8",
            Strng,
        )
        Strng = re.sub(
            "(("
            + candraBindu
            + ")?"
            + "("
            + ListC
            + ")"
            + "(("
            + "|".join(SubrvyE)
            + ")?)"
            + "(("
            + ListVS
            + ")?))"
            + "(("
            + candraBindu
            + ")?"
            + "("
            + ListV
            + "))"
            + "(?!"
            + vir
            + ")",
            r"\1 \8",
            Strng,
        )

        Strng = re.sub(
            "(("
            + candraBindu
            + ")?"
            + "("
            + ListV
            + "))"
            + "(?!"
            + vir
            + ")"
            + "(("
            + candraBindu
            + ")?"
            + "("
            + ListV
            + "))"
            + "(?!"
            + vir
            + ")",
            r"\1 \4",
            Strng,
        )
        Strng = re.sub(
            "(("
            + candraBindu
            + ")?"
            + "("
            + ListV
            + "))"
            + "(?!"
            + vir
            + ")"
            + "(("
            + candraBindu
            + ")?"
            + "("
            + ListV
            + "))"
            + "(?!"
            + vir
            + ")",
            r"\1 \4",
            Strng,
        )

        Strng = Strng.replace("\n", "\n")

        Strng = "\u12BA᠂" + Strng

        ListCE = ListC + "|" + "|".join(SubrvyE)

        Strng = re.sub(
            '(?:(?<!\n)(?<!᠂)(?<![,\."\?\&\(\)]))'
            + "(?<!"
            + vir
            + ")"
            + "("
            + ListC
            + ")"
            + vir
            + "(("
            + candraBindu
            + ")?"
            + "("
            + ListC
            + "))",
            r"\1 \2",
            Strng,
        )
        Strng = re.sub(
            "(?<!᠂)"
            + "("
            + ListC
            + ")"
            + vir
            + "(("
            + candraBindu
            + ")?"
            + "("
            + ListV
            + "))",
            r" \1",
            Strng,
        )

        Strng = Strng.replace(vir, "")
        Strng = Strng.replace("\u1E7F", "")
        Strng = Strng.replace("\u1E7E", "")
        Strng = Strng.replace("\u12BA᠂", "")

        Strng = Strng.replace("᠂", " ᠂ ")

    else:
        Strng = Strng.replace("ꡆ", "ꡒ")

        for x, y in zip(Virrvy, Subrvy):
            Strng = Strng.replace(x, y)

        Strng = re.sub(
            "(("
            + ListC
            + ")"
            + "(("
            + "|".join(SubrvyE)
            + ")?)"
            + "(?!"
            + ListVS
            + "))"
            + "((("
            + ListC
            + ")"
            + "(("
            + "|".join(SubrvyE)
            + ")?)"
            + "(("
            + ListVS
            + "))"
            + "("
            + candraBindu
            + ")?))",
            r"\1" + vir + r"\6",
            Strng,
        )

        Strng = re.sub(
            "((("
            + ListC
            + ")"
            + "(("
            + "|".join(SubrvyE)
            + ")?)"
            + "(("
            + ListVS
            + ")?)"
            + "("
            + candraBindu
            + ")?)"
            + "(("
            + ListC
            + ")"
            + "(("
            + "|".join(SubrvyE)
            + ")?)"
            + "(?!"
            + ListVS
            + ")))",
            r"\1" + vir,
            Strng,
        )

        Strng = re.sub(
            "((("
            + ListV
            + ")"
            + "("
            + candraBindu
            + ")?)"
            + "(("
            + ListC
            + ")"
            + "(("
            + "|".join(SubrvyE)
            + ")?)"
            + "(?!"
            + ListVS
            + ")))",
            r"\1" + vir,
            Strng,
        )

        for x, y in zip(Virrvy, Subrvy):
            Strng = Strng.replace(y, x)

        Strng = Strng.replace(" ", "")
        Strng = Strng.replace("᠂", " ")
        Strng = Strng.replace("᠃", " ")

        Strng = Strng.replace(vir + vir, vir)

    return Strng


def FixLatn(Strng, Source, reverse=False):
    vir = ""

    if not reverse:
        Strng = re.sub("([aiuāīū" + vir + "])(꞉)", r"\2\1", Strng)
        Strng = re.sub("(꞉)(\u033D)", r"\2\1", Strng)

        Strng = Strng.replace("aʰ", "ʰ")

    else:
        Strng = re.sub("([aiuāīū" + vir + "])(꞉)", r"\2\1", Strng)
        Strng = re.sub("(\u033D)(꞉)", r"\2\1", Strng)

    return Strng


def FixArab(Strng, Source, reverse=False):
    Strng = PersoArabicPuntuation(Strng, reverse)
    if not reverse:
        pass

    else:
        Strng = Strng.replace("آ", "آ").replace("ـ", "")

        Strng = Strng.replace("\u064E\u0651", "\u0651\u064E")

    return Strng


def FixThaa(Strng, Source, reverse=False):
    Strng = PersoArabicPuntuation(Strng, reverse)
    if not reverse:
        pass

    else:
        pass

    return Strng


def FixArab_Ph(Strng, Source, reverse=False):
    return FixArab(Strng, Source, reverse)


def FixArab_Fa(Strng, Source, reverse=False):
    Strng = FixArab(Strng, Source, reverse)

    return Strng


def FixArab_Ur(Strng, Source, reverse=False):
    Strng = FixArab(Strng, Source, reverse)

    if not reverse:
        if Source != "Type":
            pass
    else:
        pass

    return Strng


def FixUgar(Strng, Source, reverse=False):
    if not reverse:
        Strng = Strng.replace("𐎒²", "𐎝")
        Strng = Strng.replace(" ", "𐎟")
    else:
        Strng = Strng.replace("𐎟", "")

    return Strng


def FixSogd(Strng, Source, reverse=False):
    if not reverse:
        Strng = Strng.replace("𐼹²", "𐽄")
    else:
        pass

    return Strng


def FixMalayalam(Strng, reverse=False):
    Strng = post_processing.MalayalamChillu(Strng, reverse)

    if not reverse:
        Strng = post_processing.RetainDandasIndic(Strng, "Malayalam", True)
        Strng = post_processing.RetainIndicNumerals(Strng, "Malayalam", True)

    Chillus = ["\u0D7A", "\u0D7B", "\u0D7C", "\u0D7D", "\u0D7E", "ഩ‍്"]

    Anu = GM.CrunchSymbols(GM.CombiningSigns, "Malayalam")[1]

    return Strng


def FixTelugu(Strng, reverse=False):
    if not reverse:
        Strng = post_processing.RetainDandasIndic(Strng, "Telugu", True)
        Strng = post_processing.RetainIndicNumerals(Strng, "Telugu", True)
    else:
        Strng = Strng.replace("ఁ", "ఀ")

    return Strng


def FixMeeteiMayek(Strng, reverse=False):
    vir = MeeteiMayek.ViramaMap[0]
    listC = [
        x + vir
        for x in [MeeteiMayek.ConsonantMap[x] for x in [0, 27, 24, 20, 19, 15, 4, 25]]
    ]
    finalC = [
        "\uABDB",
        "\uABDC",
        "\uABDD",
        "\uABDE",
        "\uABDF",
        "\uABE0",
        "\uABE1",
        "\uABE2",
    ]

    for x, y in zip(listC, finalC):
        if not reverse:
            Strng = re.sub(x, y, Strng)
        else:
            Strng = Strng.replace(y, x)

    return Strng


def FixBatakSima(Strng, reverse=False):
    if not reverse:
        Strng = Strng.replace("ᯙᯮ", "ᯙᯯ")
    else:
        Strng = Strng.replace("ᯙᯯ", "ᯙᯮ")

    return Strng


def FixCham(Strng, reverse=False):
    Strng = Strng.replace("\u02BD", "")

    ListCAll = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, "Cham")) + ")"
    ListVow = "(" + "|".join(GM.CrunchSymbols(GM.Vowels, "Cham")) + ")"
    ListVowS = "(" + "|".join(GM.CrunchSymbols(GM.VowelSignsNV, "Cham")) + ")"

    vir = Cham.ViramaMap[0]
    nja = Cham.ConsonantMap[9] + vir + Cham.ConsonantMap[7]

    listC = [vir + x for x in Cham.ConsonantMap[25:29]]
    SubC = [
        "\uAA33",
        "\uAA34",
        "\uAA35",
        "\uAA36",
    ]
    for x, y in zip(listC, SubC):
        if not reverse:
            Strng = Strng.replace(x, y)
        else:
            Strng = Strng.replace(y, x)

    listNF = [
        Cham.ConsonantMap[x] for x in [1, 3, 6, 7, 8, 9, 16, 17, 18, 21, 22, 23, 31, 29]
    ]
    listF = [
        Cham.ConsonantMap[x]
        for x in [0, 2, 5, 5, 5, 19, 15, 15, 15, 20, 20, 20, 30, 30]
    ]

    for x, y in zip(listNF, listF):
        if not reverse:
            Strng = Strng.replace(x + vir, y + vir)
        else:
            pass

    listC = [
        x + vir
        for x in [
            Cham.ConsonantMap[x] for x in [0, 2, 4, 5, 15, 19, 20, 25, 26, 27, 30, 24]
        ]
    ]
    finalC = [
        "\uAA40",
        "\uAA41",
        "\uAA42",
        "\uAA44",
        "\uAA45",
        "\uAA46",
        "\uAA47",
        "\uAA48",
        "\uAA49",
        "\uAA4A",
        "\uAA4B",
        "\uAA4C",
    ]

    for x, y in zip(listC, finalC):
        if not reverse:
            Strng = Strng.replace(x, y)
            Strng = re.sub(
                "(" + ListCAll + "|" + ListVow + "|" + ListVowS + ")" + "ꨨ" + vir,
                r"\1" + "ꩍ",
                Strng,
            )

        else:
            Strng = Strng.replace("ꩍ", "ꨨ" + vir)
            if y not in Cham.AyogavahaMap:
                Strng = Strng.replace(y, x)

    va = Cham.ConsonantMap[28]
    if not reverse:
        Strng = Strng.replace(va + vir, va)

    else:
        pass

    return Strng


def FixTaiTham(Strng, reverse=False):
    vir = TaiTham.ViramaMap[0]
    Cons = [vir + x for x in [TaiTham.ConsonantMap[x] for x in [26, 27]]]
    Sub = ["\u1A55", "\u1A56"]
    for x, y in zip(Cons, Sub):
        if not reverse:
            Strng = Strng.replace(x, y)
        else:
            Strng = Strng.replace(y, x)

    if not reverse:
        pass
    else:
        pass

    ListC = "|".join(GM.CrunchSymbols(GM.Consonants, "TaiTham"))
    ng = TaiTham.ConsonantMap[4] + vir

    if not reverse:
        Strng = re.sub("(" + ng + ")" + "(" + ListC + ")", "\u1A58" + r"\2", Strng)

        Strng = re.sub(vir + "(" + ListC + ")", "\u1A60" + r"\1", Strng)

        Strng = Strng.replace("ᩈ᩠ᩈ", "ᩔ")

        TallACons = "|".join(["ᩅ", "ᨴ", "ᨵ", "ᨣ"])

        Strng = post_processing.FixTallA(Strng, TallACons)

        Strng = Strng.replace("\u1A55\u1A60\u1A3F", "\u1A60\u1A3F\u1A55")

        Strng = Strng.replace("\u1A60\u1A47", vir + "\u1A47")

    else:
        AA = "ᩣ"
        Strng = Strng.replace("ᩔ", "ᩈ᩠ᩈ")
        Strng = re.sub("(" + ListC + ")" + "\u1A58", r"\1" + ng, Strng)
        Strng = Strng.replace("\u1A60", vir)
        Strng = Strng.replace("ᩤ", AA)

        Strng = Strng.replace("\u1A60\u1A3F\u1A55", "\u1A55\u1A60\u1A3F")

    return Strng


def FixLaoTham(Strng, reverse=False):
    Strng = FixTaiTham(Strng, reverse)

    return Strng


def FixLueTham(Strng, reverse=False):
    Strng = FixTaiTham(Strng, reverse)

    ListC = "|".join(GM.CrunchSymbols(GM.Consonants, "TaiTham"))
    if not reverse:
        E = "ᩮ"
        AA = "ᩣ"
        TallACons = "|".join(["ᩅ", "ᨴ", "ᨵ", "ᨣ"])
        Strng = re.sub(
            "(" + TallACons + ")(᩠)(" + ListC + ")" + "(" + E + "?)" + AA,
            r"\1\2\3\4" + "ᩤ",
            Strng,
        )
        Strng = re.sub(
            "("
            + TallACons
            + ")(᩠)("
            + ListC
            + ")"
            + "(᩠)("
            + ListC
            + ")"
            + "("
            + E
            + "?)"
            + AA,
            r"\1\2\3\4\5\6" + "ᩤ",
            Strng,
        )
    else:
        pass

    return Strng


def FixKhuenTham(Strng, reverse=False):
    Strng = FixTaiTham(Strng, reverse)

    ListC = "|".join(GM.CrunchSymbols(GM.Consonants, "TaiTham"))
    if not reverse:
        E = "ᩮ"
        AA = "ᩣ"
        TallACons = "|".join(["ᩅ", "ᨴ", "ᨵ", "ᨣ"])
        Strng = re.sub(
            "(" + TallACons + ")(᩠)(" + ListC + ")" + "(" + E + "?)" + AA,
            r"\1\2\3\4" + "ᩤ",
            Strng,
        )
        Strng = re.sub(
            "("
            + TallACons
            + ")(᩠)("
            + ListC
            + ")"
            + "(᩠)("
            + ListC
            + ")"
            + "("
            + E
            + "?)"
            + AA,
            r"\1\2\3\4\5\6" + "ᩤ",
            Strng,
        )
    else:
        pass

    return Strng


def LaoTranscribe(Strng, reverse=False):
    import post_processing as pp

    shortA, conjA = "\u0EB0", "\u0EB1"

    if not reverse:
        Strng = pp.ThaiLaoTranscription(Strng, "Lao", shortA, conjA)
    else:
        Strng = pp.ThaiLaoTranscription(Strng, "Lao", shortA, conjA, reverse=True)

    return Strng


def LaoPaliTranscribe(Strng, reverse=False, anusvaraChange=True):
    import post_processing as pp

    shortA, conjA = "\u0EB0", "\u0EB1"

    if not reverse:
        Strng = pp.ThaiLaoTranscription(
            Strng, "LaoPali", shortA, conjA, anusvaraChange=anusvaraChange
        )
    else:
        Strng = pp.ThaiLaoTranscription(Strng, "LaoPali", shortA, conjA, reverse=True)

    return Strng


def FixBengali(Strng, reverse=False):
    Virama = "".join(GM.CrunchSymbols(["ViramaMap"], "Bengali"))
    ba = "ব"

    if not reverse:
        Strng = re.sub("(?<![রবম])" + Virama + ba, Virama + "\u200C" + ba, Strng)

        Strng = Strng.replace("\u09CD\u09AD\u09BC", "\u09CD\u09AC")
    else:
        pass

    Strng = post_processing.KhandaTa(Strng, "Bengali", reverse)

    return Strng


def FixAssamese(Strng, reverse=False):
    Ra = "\u09B0"
    AssRa = "\u09F0"

    Strng = post_processing.KhandaTa(Strng, "Assamese", reverse)

    if not reverse:
        Strng = Strng.replace(Ra, AssRa)
    else:
        Strng = Strng.replace(AssRa, Ra)

    return Strng


def FixSharada(Strng, reverse=False):
    Strng = post_processing.KhandaTa(Strng, "Assamese", reverse)

    ListC = "|".join(GM.CrunchSymbols(GM.Consonants, "Sharada"))
    Nukta = "|".join(GM.CrunchSymbols(GM.CombiningSigns, "Sharada")[-1])
    Virama = "".join(GM.CrunchSymbols(["ViramaMap"], "Sharada"))

    if not reverse:
        Strng = Strng.replace(Nukta + Virama, Nukta + Virama + "\u200C")
        Strng = re.sub(
            "(" + Virama + ")" + "(" + ListC + ")" + "(" + Nukta + ")",
            r"\1" + "\u200C" + r"\2\3",
            Strng,
        )

    else:
        pass

    return Strng


def FixKannada(Strng, reverse=False):
    if not reverse:
        Strng = post_processing.RetainDandasIndic(Strng, "Kannada", True)
        Strng = post_processing.RetainIndicNumerals(Strng, "Kannada", True)

        Strng = re.sub(
            "(\u0CCD)([^\u0CAB\u0C9C])(\u0CBC)", r"\1" + "\u200C" + r"\2\3", Strng
        )

    return Strng


def FixGrantha(Strng, reverse=False):
    if not reverse:
        Strng = Strng.replace("॑", "᳴")
        Strng = Strng.replace("᳚", "॑")
        Strng = Strng.replace("ꣳ", "𑍞")
        Strng = Strng.replace("ꣴ", "𑍟")
        Strng = Strng.replace("𑌼𑍍", "𑌼𑍍\u200C")
    else:
        Strng = Strng.replace("𑌼𑍍\u200C", "𑌼𑍍")
        Strng = Strng.replace("॑", "᳚")
        Strng = Strng.replace("᳴", "॑")
        Strng = Strng.replace("𑍞", "ꣳ")
        Strng = Strng.replace("𑍟", "ꣴ")

    return Strng


def FixMahajani(Strng, reverse=False):
    if not reverse:
        Strng = Strng.replace("𑅰𑅳ʾ𑅭ʿ𑅑", "\U00011176")
        Strng = Strng.replace("\u02BE", "").replace("\u02BF", "")
    else:
        Strng = Strng.replace("\U00011176", "𑅰𑅳ʾ𑅭ʿ𑅑")

    return Strng


def FixAhom(Strng, reverse=False):
    ListVS = "(" + "|".join(GM.CrunchSymbols(GM.VowelSignsNV, "Ahom")) + ")"
    Anu = "(" + GM.CrunchList("AyogavahaMap", "Ahom")[1] + ")"

    if not reverse:
        Strng = Strng.replace("\U0001172B\U0001170D", "\U0001171E")
        Strng = Strng.replace("\U0001172B\U0001170E", "\U0001171D")

        Strng = re.sub(ListVS + Anu, r"\2\1", Strng)
        Strng = re.sub(Anu + "(𑜦)", r"\2\1", Strng)

    else:
        Strng = Strng.replace("\U0001171E", "\U0001172B\U0001170D")
        Strng = Strng.replace("\U0001171D", "\U0001172B\U0001170E")

        vir = Ahom.ViramaMap[0]
        anu = Ahom.AyogavahaMap[1]

        Strng = re.sub(
            anu + "\U00011727" + "(?!\U00011728)",
            "\U00011726\U00011727\U0001172A",
            Strng,
        )
        Strng = re.sub(
            "(\U00011726)(.)(" + vir + ")", "\U00011726\U00011727" + r"\2\3", Strng
        )

        Strng = re.sub(
            "(\U00011728)(.)(" + vir + ")", "\U00011726\U00011721" + r"\2\3", Strng
        )

        Strng = Strng.replace(anu + "\U00011728", "\U00011726\U00011721\U0001172A")

        Strng = re.sub(Anu + ListVS, r"\2\1", Strng)

    return Strng


def FixMultani(Strng, reverse=False):
    if not reverse:
        Strng = Strng.replace("\u02BE", "").replace("\u02BF", "")
        Strng = Strng.replace("ˍ\U0001128C", "\U0001128D").replace(
            "ˍ\U00011282", "\U00011293"
        )

    else:
        Strng = Strng.replace("\U0001128D", "ˍ\U0001128C").replace(
            "\U00011293", "ˍ\U00011292"
        )

    return Strng


def FixGujarati(Strng, reverse=False):
    if not reverse:
        Strng = post_processing.RetainDandasIndic(Strng, "Gujarati", True)
        Strng = Strng.replace("જ઼઼", "ૹ").replace("શ઼", "ૹ")
    else:
        pass
        Strng = Strng.replace("ૹ", "જ઼઼").replace("ૹ", "શ઼")

    return Strng


def FixZanabazarSquare(Strng, reverse=False):
    ListC = "|".join(GM.CrunchSymbols(GM.Consonants, "ZanabazarSquare"))
    yrlv = ZanabazarSquare.ConsonantMap[25:29]
    yrlv_sub = ["\U00011A3B", "\U00011A3C", "\U00011A3D", "\U00011A3E"]

    vir = ZanabazarSquare.ViramaMap[0]

    if not reverse:
        Strng = re.sub(vir + "(" + ListC + ")", "\U00011A47" + r"\1", Strng)

        Strng = Strng.replace("𑨋𑩇𑨯", "𑨲")
    else:
        Strng = Strng.replace("\U00011A41", " ")

        tsaSeries = ["𑨣", "𑨤", "𑨥"]
        caSeries = ["𑨐", "𑨑", "𑨒"]

        for x, y in zip(tsaSeries, caSeries):
            Strng = Strng.replace(y, x)

        for x, y in zip(yrlv, yrlv_sub):
            Strng = Strng.replace(y, "\U00011A47" + x)

        Strng = Strng.replace("\U00011A3A", yrlv[1] + "\U00011A47")

        Strng = Strng.replace("𑨲", "𑨋𑩇𑨯")

        Strng = Strng.replace("\U00011A07", "\U00011A04\U00011A0A")
        Strng = Strng.replace("\U00011A08", "\U00011A06\U00011A0A")

        Strng = Strng.replace("\U00011A33", vir)

        Strng = Strng.replace("\U00011A47", vir)

    return Strng


def FixKhojki(Strng, reverse=False):
    sindhi = ["\U0001120B", "\U00011211", "\U0001121C", "\U00011222"]
    sindhiapprox = ["ˍ\U0001120A", "ˍ\U00011210", "ˍ\U00011216", "ˍ\U00011221"]

    if not reverse:
        for x, y in zip(sindhi, sindhiapprox):
            Strng = Strng.replace(y, x)
        Strng = post_processing.InsertGeminationSign(Strng, "Khojki")

        Strng = re.sub("(\U00011237)(.)", r"\2\1", Strng)

        Strng = Strng.replace("𑈷𑈶", "𑈶𑈷")

        Strng = Strng.replace(" ", "\U0001123A")
    else:
        Strng = Strng.replace("\U0001123A", " ")

        for x, y in zip(sindhi, sindhiapprox):
            Strng = Strng.replace(x, y)

        Strng = Strng.replace("𑈶𑈷", "𑈷𑈶")

        Strng = re.sub("(.)(\U00011237)", r"\2\1", Strng)
        Strng = post_processing.ReverseGeminationSign(Strng, "Khojki")

    return Strng


def FixNewa(Strng, reverse=False):
    if not reverse:
        ListC = "|".join(GM.CrunchSymbols(GM.Consonants, "Newa"))
        ra = Newa.ConsonantMap[26]
        vir = Newa.ViramaMap[0]

    else:
        pass

    return Strng
