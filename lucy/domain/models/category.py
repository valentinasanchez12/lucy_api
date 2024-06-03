from nyoibo import Entity, fields


class Category(Entity):
    _uuid = fields.StrField()
    _name = fields.StrField()
    _created_at = fields.DatetimeField()
    _update_at = fields.DatetimeField()
    _delete_at = fields.DatetimeField()
