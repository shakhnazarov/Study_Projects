"""
Basic routine to calculate date + some days
"""

# extra 0 to make indexation consistent
month_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

date = "12.04.1999"

dd, mm, yyyy = map(int, date.split("."))
N = 10000
while N > 0:
    if yyyy % 4 == 0 and yyyy % 100 != 0:
        month_days[2] = 29
    elif yyyy % 400 == 0:
        month_days[2] = 29
    else:
        month_days[2] = 28

    if N > month_days[mm] - dd:
        N -= month_days[mm] - dd + 1
        dd = 1
        mm += 1
        if mm == 13:
            mm = 1
            yyyy += 1
    else:
        dd += N
        N = 0

ans = ""
if dd < 10:
    ans += "0"
ans += str(dd) + "."
if mm < 10:
    ans += "0"
ans += str(mm) + "."
ans += "0"*(4-len(str(yyyy))) + str(yyyy)
print(ans)