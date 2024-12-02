from nyoibo import Entity, fields


class Category(Entity):
    _uuid = fields.StrField()
    _name = fields.StrField()
    _created_at = fields.DatetimeField()
    _updated_at = fields.DatetimeField()
    _deleted_at = fields.DatetimeField()

    def to_dict(self) -> dict:
        return {
            "uuid": self._uuid if self._uuid else None,
            "name": self._name if self._name else None,
            "created_at": self._created_at if self._created_at else None,
            "updated_at": self._updated_at if self._updated_at else None,
            "deleted_at": self._deleted_at if self._deleted_at else None,
        }
