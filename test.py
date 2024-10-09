def error_rate_from_phred(phred_score):
    error_rate = 10 ** (-phred_score / 10)
    return error_rate

array_of_chr3_original = [93] * 14
array_of_chr3_original.append(89)
total_error_rate = 1
for score in array_of_chr3_original:
    total_error_rate *= (error_rate_from_phred(score))
print(total_error_rate)

likelihood = 0.000_001 / (0.000_001 + total_error_rate)
print(likelihood)

array_of_chr3_modified = [25, 42, 24, 40, 34, 34, 46, 34, 38]
total_error_rate = 1
for score in array_of_chr3_modified:
    total_error_rate *= (error_rate_from_phred(score))
print(total_error_rate)


likelihood = 0.000_001 / (0.000_001 + total_error_rate)
print(likelihood)