import pre_processing as PP


def ApplyPreProcessing(Strng, Source, Target):
    if Target == "PhagsPa":
        Options = ["PhagsPaArrange"]
    else:
        Options = []

    for Option in Options:
        if Option.find(Target) != -1:
            Strng = getattr(PP, Option)(Strng, Source)

        else:
            Strng = getattr(PP, Option)(Strng, Target)

    return Strng
