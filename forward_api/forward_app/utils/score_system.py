import datetime


def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)


"""
Computes cutoff from Persona QuerySet
"""
def cutoff(personas):
    pass


def sweep():
    # cutoff = cutoff()
    # for p in Persona.objects.all():
    #     if p.score > cutoff and p.stage == 1:  # regular user that meets cutoff
    #         p.stage = 2
    line_prepender('forward_app/utils/cutoffs.txt', '%s,%f' % (str(datetime.date.today()), 1.0))


if __name__ == '__main__':
    sweep()
