


class Modul(object):
    id = -1
    svi = []

    def __init__(self, imeKursa, *args, **kwargs):
        self.id = Modul.id + 1
        Modul.id = self.id
        self.imeKursa = imeKursa
        Modul.svi.append(self)
        return super().__init__(*args, **kwargs)


print(*range(0))
for k in range(len([])):
    print(k)
