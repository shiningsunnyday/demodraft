import datetime


def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

"""
Updates score of every Persona
"""
def update_scores(pers, comments):
    for p in pers:
        per_comments = comments.filter(user=p.user)
        p.score = sum([comment.likes for comment in per_comments])
        p.save()


"""
Computes cutoff from Persona QuerySet object
Sorts all scores and gets 10th percentile
Should later replace with Select O(n) algo
"""
def cutoff(pers):
    scores = sorted([p.score for p in pers])
    return scores[int(9 * len(scores) / 10)]


def sweep(pers):
    cut = cutoff(pers)
    line_prepender('forward_app/utils/cutoffs.txt', '%s,%f' % (str(datetime.date.today()), cut))
    for p in pers:
        if p.score >= cut and p.stage == 1:  # regular user that meets cutoff
            p.stage = 2
            p.save()
        elif p.score < cut and p.stage == 2:
            p.stage = 1
            p.save()



