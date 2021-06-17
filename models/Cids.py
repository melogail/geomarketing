from database.Model import Model


class Cids(Model):
    table = 'cids'

    fillable = ['cid', 'type', 'governorate', 'quism', 'shiakha']
