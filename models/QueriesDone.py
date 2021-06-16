from database.Model import Model


class QueriesDone(Model):
    # Targeted table
    table = 'queries_done'

    # Fillable fields
    fillable = ['query', 'time', 'success', 'type']
