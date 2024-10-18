def error_rate_from_phred(phred_score):
    error_rate = 10 ** (-phred_score / 10)
    return error_rate

array_of_chr3_original = [93]
total_error_rate = 1
for score in array_of_chr3_original:
    total_error_rate *= (error_rate_from_phred(score))
print(total_error_rate)

likelihood = 0.000_001 / (0.000_001 + total_error_rate)
print(likelihood * 100)

array_of_chr3_modified = [23]
total_error_rate = 1
for score in array_of_chr3_modified:
    total_error_rate *= (error_rate_from_phred(score))
print(total_error_rate)


likelihood = 0.000_001 / (0.000_001 + total_error_rate)
print(likelihood * 100)
