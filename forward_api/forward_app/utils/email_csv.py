def update_txt():
    with open("contact_list_sorted.csv", "r") as f:
        emails = f.readlines()
        with open("contact_list.txt", "w+") as fp:
            for email in emails[1:]:
                e = email.split(',')[0]
                fp.write(e + '\n')
            fp.close()


from bisect import bisect_left


def process(emails):
    return [e.split(',')[0] for e in emails]


def bsearch(a, x):
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    else:
        return -1


def search(e, path):
    with open(path, "r") as f:
        emails = [e.strip('\n') for e in f.readlines()]
    return bsearch(emails, e) > -1


if __name__ == '__main__':
    print(search("stevensm90@gmail.com", "contact_list.txt"))