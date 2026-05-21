class ተማሪ:

    def __init__(self, ስም, ዕድሜ, ውጤት):
        self.ስም = ስም
        self.ዕድሜ = ዕድሜ
        self.ውጤት = ውጤት

    def መረጃ_አሳይ(self):
        print(f'ስም: {self.ስም}')
        print(f'ዕድሜ: {self.ዕድሜ}')
        print(f'ውጤት: {self.ውጤት}')

    def ደረጃ(self):
        if self.ውጤት >= 90:
            return 'A'
        elif self.ውጤት >= 80:
            return 'B'
        elif self.ውጤት >= 70:
            return 'C'
        else:
            return 'F'
ት1 = ተማሪ('ቻሉ', 20, 92)
ት2 = ተማሪ('አበበ', 22, 75)
ት1.መረጃ_አሳይ()
print(f'ደረጃ: {ት1.ደረጃ()}')
ት2.መረጃ_አሳይ()
print(f'ደረጃ: {ት2.ደረጃ()}')