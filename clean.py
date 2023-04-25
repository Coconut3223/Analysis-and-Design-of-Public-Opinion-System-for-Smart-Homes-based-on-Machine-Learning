from setting import get_clean_data

origin = get_clean_data()
def clean_choujiang(origin):
    for k in origin.keys():
        comments = origin[k]
        max = {}
        choujiang = 0
        for comment in comments:
            if comment[2] not in max.keys():
                max[comment[2]]=1
            else:
                max[comment[2]]+=1

