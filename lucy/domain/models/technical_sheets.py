from nyoibo import Entity, fields

from lucy.domain.models.product import Product


class TechnicalSheet(Entity):
    _uuid = fields.StrField()
    _documents = fields.StrField()
    _product = fields.LinkField(to=Product)
    _created_at = fields.DatetimeField()
    _update_at = fields.DatetimeField()
    _delete_at = fields.DatetimeField()

    def to_dict(self) -> dict:
        return {
            "uuid": self._uuid if self._uuid else None,
            "documents": self._documents if self._documents else None,
            "product": self._product.to_dict() if self._product else None,
            "created_at": self._created_at if self._created_at else None,
            "update_at": self._update_at if self._update_at else None,
            "delete_at": self._delete_at if self._delete_at else None,
        }
