from database.Model import Model


class Landmark(Model):
    # Targeted table
    table = 'landmarks'

    # Fillable fields
    fillable = ['cid', 'name', 'sub_name', 'lat', 'lng', 'reviews', 'user_total_reviews', 'type', 'address_en',
                'address_ar', 'plus_code', 'phone_number', 'website', 'image']
