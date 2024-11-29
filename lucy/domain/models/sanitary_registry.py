from nyoibo import Entity, fields


class SanitaryRegistry(Entity):
    _uuid = fields.StrField()
    _url = fields.StrField()
    _number_registry = fields.StrField()
    _expiration_date = fields.DateField()
    _cluster = fields.StrField()
    _status = fields.StrField()
    _type_risk = fields.StrField()
    _created_at = fields.DatetimeField()
    _update_at = fields.DatetimeField()
    _delete_at = fields.DatetimeField()

    def to_dict(self) -> dict:
        return {
            "uuid": self._uuid if self._uuid else None,
            "url": self._url if self._url else None,
            "number_registry": self._number_registry if self._number_registry else None,
            "expiration_date": self._expiration_date if self._expiration_date else None,
            "cluster": self._cluster if self._cluster else None,
            "status": self._status if self._status else None,
            "type_risk": self._type_risk if self._type_risk else None,
            "created_at": self._created_at if self._created_at else None,
            "update_at": self._update_at if self._update_at else None,
            "delete_at": self._delete_at if self._delete_at else None,
        }
