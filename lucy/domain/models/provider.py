from nyoibo import Entity, fields

from lucy.domain.models.brand import Brand


class Provider(Entity):
    _uuid = fields.StrField()
    _types_person = fields.StrField()
    _nit = fields.StrField()
    _name = fields.StrField()
    _represent = fields.StrField()
    _phone = fields.StrField()
    _email = fields.StrField()
    _brands = fields.ListField()
    _created_at = fields.DatetimeField()
    _updated_at = fields.DatetimeField()
    _deleted_at = fields.DatetimeField()

    def add_brand(self, brand: Brand):
        data = [brand]
        self._brands = data

    def to_dict(self) -> dict:
        return {
            "uuid": self._uuid if self._uuid else None,
            "types_person": self._types_person if self._types_person else None,
            "nit": self._nit if self._nit else None,
            "name": self._name if self._name else None,
            "represent": self._represent if self._represent else None,
            "phone": self._phone if self._phone else None,
            "email": self._email if self._email else None,
            "brands": self._brands if self._brands else None,
            "created_at": self._created_at.isoformat() if self._created_at else None,
            "updated_at": self._updated_at.isoformat() if self._updated_at else None,
            "deleted_at": self._deleted_at.isoformat() if self._deleted_at else None,
        }
