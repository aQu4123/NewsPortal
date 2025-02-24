flag = []
# ddd = {None, 'aqu4a@mail.ru'}
ddd = {'aqu4a@mail.ru', None}
for i in ddd:
    print(i)
ss = {'dsa'}
print(ss.pop())

# set(Post.objects.filter(date_in__gte=week_ago).values_list('category__subscribers__email', flat=True)).remove(None)
# set(Post.objects.filter(date_in__gte=week_ago).values_list('category__subscribers', flat=True)).remove(None)
