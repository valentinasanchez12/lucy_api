from nyoibo import Entity, fields

from lucy.domain.models import Provider


class Brand(Entity):
    _uuid = fields.StrField()
    _name = fields.StrField()
    _provider = fields.LinkField(to=Provider)
    _created_at = fields.DatetimeField()
    _update_at = fields.DatetimeField()
    _delete_at = fields.DatetimeField()
