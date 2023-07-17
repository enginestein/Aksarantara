import transliterate

print(transliterate.process("hk", "siddham", "buddhaH"))
print(transliterate.process("autodetect", "iast", "சித்தம்_சூதம்"))
print(transliterate.process("HK", "Tamil", "மங்கள", False))

print(
    transliterate.process(
        "HK",
        "Tamil",
        "பிரஹ்ஸ்பதி கங்கா",
        False,
        post_options=["TamilSubScript", "TamilRemoveApostrophe"],
    )
)
print(
    transliterate.process(
        "Thai", "Devanagari", "ภุทธัง สะระณัง คัจฉามิ", pre_options=["ThaiOrthography"]
    )
)
print(transliterate.process("autodetect", "IAST", "ภุทธัง สะระณัง คัจฉามิ"))
print(transliterate.process("autodetect", "Vatteluttu", "ภุทธัง สะระณัง คัจฉามิ"))
print(transliterate.auto_detect("சித்தம்_சூதம்"))
print(
    transliterate.process(
        "Devanagari",
        "IAST",
        "धर्म भारत की श्रमण परम्परा से निकला धर्म और दर्शन है",
        pre_options=["RemoveSchwaHindi"],
    )
)
print(transliterate.process("deva", "taml", "धर्म भारत की ", param="script_code"))
print(transliterate.process("te", "ur", "ధర్మ భారత", param="lang_code"))
print(transliterate.process("odia", "ho", "ଧର୍ମ ଭାରତ", param="lang_name"))
print(transliterate.process("hindi", "kannada", "धर्म भारत की ", param="lang_name"))
print(transliterate.process("devanagari", "granthapandya", "धर्म"))
print(transliterate.process("hi", "pa", "धर्म भारत की ", param="lang_code"))
print(transliterate.process("deva", "arab", "धर्म भारत की ", param="script_code"))
print(
    transliterate.process(
        "autodetect", "latn-iast", "धर्म भारत की ", param="script_code"
    )
)
print(transliterate.process("la-HK", "pa-guru", "namo buddhAya", param="lang_code"))
print(transliterate.process("hi-Deva", "hi-kthi", "धर्म भारत की ", param="lang_code"))
print(transliterate.process("hi-Deva", "mak", "धर्म भारत की ", param="lang_code"))
print(transliterate.process("hi-Deva", "cyrl", "धर्म भारत की ", param="script_code"))
print(transliterate.process("sa-Deva", "ru", "धर्म भारत की ", param="lang_code"))
print(transliterate.process("deva", "taml", "धर्म भारत की ", param="script_code"))
print(transliterate.process("te", "ur", "ధర్మ భారత", param="lang_code"))
print(transliterate.process("odia", "ho", "ଧର୍ମ ଭାରତ", param="lang_name"))
print(transliterate.process("Devanagari", "Phnx", "तांश्च"))
print(transliterate.process("HK", "Syrc", "buddha"))