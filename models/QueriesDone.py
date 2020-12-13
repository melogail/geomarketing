from database.Model import Model


class QueriesDone(Model):
    # Targeted table
    table = 'queries_done'

    # Fillable fields
    fillable = ['query', 'time']


for query in QueriesDone.all():
    print('GYM in قسم  ثان مدينة نصر, محافظة القاهرة' in query[1])
