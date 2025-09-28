def progresbar(curr, max):
    progres = curr*100/max
    empty = "." * (100 - int(progres))
    if curr/max == 1:
        progresstring = "=" * int(progres)
        print(f"[{progresstring}{empty}] {int(progres)}% ")
    else:
        progresstring = "=" * (int(progres) - 1)
        print(f"[{progresstring}>{empty}] {int(progres)}% ", end='\r')
