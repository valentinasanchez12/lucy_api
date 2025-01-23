from nyoibo import Entity, fields

from lucy.domain.models.product import Product


class Comments (Entity):
    _uuid = fields.StrField()
    _comment = fields.StrField()
    _product_uuid = fields.StrField()
    _created_at = fields.DatetimeField()
    _updated_at = fields.DatetimeField()
    _deleted_at = fields.DatetimeField()

    def to_dict(self) -> dict:
        return {
            "uuid": self._uuid if self._uuid else None,
            "comment": self._comment if self._comment else None,
            "product_uuid": self._product_uuid if self._product_uuid else None,
            "created_at": self._created_at.isoformat() if self._created_at else None,
            "updated_at": self._updated_at.isoformat() if self._updated_at else None,
            "deleted_at": self._deleted_at.isoformat() if self._deleted_at else None,
        }
