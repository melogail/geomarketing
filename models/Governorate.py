from database.Model import Model


class Governorate(Model):
    table = 'governorates'

    fillable = ['name']