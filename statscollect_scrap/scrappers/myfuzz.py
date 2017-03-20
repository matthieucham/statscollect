from fuzzywuzzy import fuzz, utils
import statistics

# Token Set
#   find all alphanumeric tokens in each string...treat them as a set
#   construct two strings of the form
#       <sorted_intersection><sorted_remainder>
#   take ratios of those two strings
#   controls for unordered partial matches
def _token_set(s1, s2, partial=True, force_ascii=True, use_avg=False):

    if s1 is None:
        raise TypeError("s1 is None")
    if s2 is None:
        raise TypeError("s2 is None")

    p1 = utils.full_process(s1, force_ascii=force_ascii)
    p2 = utils.full_process(s2, force_ascii=force_ascii)

    if not utils.validate_string(p1):
        return 0
    if not utils.validate_string(p2):
        return 0

    # pull tokens
    tokens1 = set(utils.full_process(p1).split())
    tokens2 = set(utils.full_process(p2).split())

    intersection = tokens1.intersection(tokens2)
    diff1to2 = tokens1.difference(tokens2)
    diff2to1 = tokens2.difference(tokens1)

    sorted_sect = " ".join(sorted(intersection))
    sorted_1to2 = " ".join(sorted(diff1to2))
    sorted_2to1 = " ".join(sorted(diff2to1))

    combined_1to2 = sorted_sect + " " + sorted_1to2
    combined_2to1 = sorted_sect + " " + sorted_2to1

    # strip
    sorted_sect = sorted_sect.strip()
    combined_1to2 = combined_1to2.strip()
    combined_2to1 = combined_2to1.strip()

    if partial:
        ratio_func = fuzz.partial_ratio
    else:
        ratio_func = fuzz.ratio

    pairwise = [
        ratio_func(sorted_sect, combined_1to2),
        ratio_func(sorted_sect, combined_2to1),
        ratio_func(combined_1to2, combined_2to1)
    ]
    if use_avg:
        return statistics.mean(pairwise)
    else:
        return max(pairwise)


def partial_token_set_ratio_with_avg(s1, s2, force_ascii=True):
    return _token_set(s1, s2, partial=True, force_ascii=force_ascii, use_avg=True)