# only string-number-number is valid
# str-i-j: str is replication of treatment, 1 <= i <= 4, 1 <= j <= 3
def check(treatment):
    if isinstance(treatment, str):
        code = treatment.split("-")
        return len(code) == 3 and int(code[1]) <= 4 and int(code[2]) <= 3
    else:
        return False


# Get the standard treatment name: [a, SiTj] where 1 <= i <= 4, 1 <= j <= 3
def standard(treatment):
    str = treatment.split("-")
    return [str[0], "S" + str[1] + "T" + str[2]]


# Get the standard treatment: [a, Si, Tj] where 1 <= i <= 4, 1 <= j <= 3
# replication, spacing type, truss type
def standard3(treatment):
    str = treatment.split("-")
    return [str[0], int(str[1]), int(str[2])]
