def ቁጥር_ዓይነት(ቁ):
    if ቁ > 0:
        return 'አዎ ቁጥር'
    elif ቁ == 0:
        return 'ዜሮ'
    else:
        return 'አሉታዊ ቁጥር'
print(ቁጥር_ዓይነት(5))
print(ቁጥር_ዓይነት(0))
print(ቁጥር_ዓይነት(-3))
ቆጠራ = 1
while ቆጠራ <= 5:
    print(ቆጠራ)
    ቆጠራ = ቆጠራ + 1
for i in range(1, 6):
    if i % 2 == 0:
        print(f'{i} — ሰርጎ ቁጥር')
    else:
        print(f'{i} — ነጠላ ቁጥር')