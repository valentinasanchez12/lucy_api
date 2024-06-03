from nyoibo import Entity, fields

from lucy.domain.models import Product


class Observation (Entity):
    _uuid = fields.StrField()
    _observation = fields.StrField()
    _product = fields.LinkField(to=Product)
    _created_at = fields.DatetimeField()
    _update_at = fields.DatetimeField()
    _delete_at = fields.DatetimeField()
