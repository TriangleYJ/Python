def recurrence(a1, n):
    if n == 1:
        return a1
    else:
        return recurrence(a1, n - 1) + 3 * n


for i in range(1, 20):
    print("%d : %d\n" % (i, recurrence(2, i)))
