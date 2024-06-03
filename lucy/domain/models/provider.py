from nyoibo import Entity, fields


class Provider(Entity):
    _uuid = fields.StrField()
    _name = fields.StrField()
    _represent = fields.StrField()
    _phone = fields.StrField()
    _email = fields.StrField()
    _created_at = fields.DatetimeField()
    _update_at = fields.DatetimeField()
    _delete_at = fields.DatetimeField()
