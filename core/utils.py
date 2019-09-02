def get_things(forWhoSummary):

    data = {}
    clothes_for_who = ""
    clothes_purpose = ""
    forWhoSummary = forWhoSummary.split('|')
    for item in forWhoSummary:
        if "do ponownego użycia" in item:
            clothes = item.split(':')
            data['clothes_type'] = clothes[0]
            for item2 in clothes[1].split(','):
                if "Sezon" in item2:
                    clothes_purpose += item2 + ", "
                else:
                    clothes_for_who += item2 + ", "
            data['clothes_for_who'] = clothes_for_who
            data['clothes_purpose'] = clothes_purpose
        if "do wyrzucenia" in item:
            data['useless_clothes'] = True
        if "zabawki" in item:
            data['toys'] = item.split(':')[1]
        if "książki" in item:
            data['books'] = item.split(':')[1]
        if "inne" in item:
            data['others'] = item.split(':')[1]
    return data
