from nyoibo import Entity, fields

from lucy.domain.models.product import Product


class Characteristic(Entity):
    _uuid = fields.StrField()
    _characteristic = fields.StrField()
    _description = fields.StrField()
    _product = fields.LinkField(to=Product)
    _created_at = fields.DatetimeField()
    _updated_at = fields.DatetimeField()
    _deleted_at = fields.DatetimeField()

    def to_dict(self) -> dict:
        return {
            "uuid": self._uuid if self._uuid else None,
            "characteristic": self._characteristic if self._characteristic else None,
            "description": self._description if self._description else None,
            "product": self._product.to_dict() if self._product else None,
            "created_at": self._created_at.isoformat() if self._created_at else None,
            "updated_at": self._updated_at.isoformat() if self._updated_at else None,
            "deleted_at": self._deleted_at.isoformat() if self._deleted_at else None,
        }
