from nyoibo import Entity, fields

from lucy.domain.models import Brand, Category
from lucy.domain.models import SanitaryRegistry


class Product(Entity):
    _uuid = fields.StrField()
    _generic_name = fields.StrField()
    _commercial_name = fields.StrField()
    _description = fields.StrField()
    _measurement = fields.StrField()
    _formulation = fields.StrField()
    _composition = fields.StrField()
    _reference = fields.StrField()
    _use = fields.StrField()
    _status = fields.StrField()
    _sanitize_method = fields.StrField()
    _image = fields.StrField()
    _brands = fields.LinkField(to=Brand)
    _categories = fields.LinkField(to=Category)
    _sanitary_registry = fields.LinkField(to=SanitaryRegistry)
    _created_at = fields.DatetimeField()
    _update_at = fields.DatetimeField()
    _delete_at = fields.DatetimeField()
