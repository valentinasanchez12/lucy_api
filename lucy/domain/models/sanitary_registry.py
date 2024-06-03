from nyoibo import Entity, fields


class SanitaryRegistry(Entity):
    _uuid = fields.StrField()
    _documents = fields.StrField()
    _expiration_date = fields.DateField()
    _cluster = fields.StrField()
    _status = fields.StrField()
    _type_risk = fields.StrField()
    _created_at = fields.DatetimeField()
    _update_at = fields.DatetimeField()
    _delete_at = fields.DatetimeField()
