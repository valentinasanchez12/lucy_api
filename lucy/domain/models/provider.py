from nyoibo import Entity, fields

from lucy.domain.models.brand import Brand


class Provider(Entity):
    _uuid = fields.StrField()
    _name = fields.StrField()
    _represent = fields.StrField()
    _phone = fields.StrField()
    _email = fields.StrField()
    _brands = fields.ListField()
    _created_at = fields.DatetimeField()
    _update_at = fields.DatetimeField()
    _delete_at = fields.DatetimeField()

    def add_brand(self, brand: Brand):
        self._brands.append(brand)

    def to_dict(self) -> dict:
        return {
            "uuid": self._uuid if self._uuid else None,
            "name": self._name if self._name else None,
            "represent": self._represent if self._represent else None,
            "phone": self._phone if self._phone else None,
            "email": self._email if self._email else None,
            "created_at": self._created_at if self._created_at else None,
            "update_at": self._update_at if self._update_at else None,
            "delete_at": self._delete_at if self._delete_at else None,
        }
