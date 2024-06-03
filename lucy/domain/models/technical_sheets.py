from nyoibo import Entity, fields

from lucy.domain.models.product import Product


class TechnicalSheet(Entity):
    _uuid = fields.StrField()
    _documents = fields.StrField()
    _product = fields.LinkField(to=Product)
    _created_at = fields.DatetimeField()
    _update_at = fields.DatetimeField()
    _delete_at = fields.DatetimeField()
