from nyoibo import Entity, fields

from lucy.domain.models.product import Product


class TechnicalSheet(Entity):
    _uuid = fields.StrField()
    _document = fields.StrField()
    _product = fields.LinkField(to=Product)
    _created_at = fields.DatetimeField()
    _updated_at = fields.DatetimeField()
    _deleted_at = fields.DatetimeField()

    def to_dict(self) -> dict:
        return {
            "uuid": self._uuid if self._uuid else None,
            "documents": self._document if self._document else None,
            "product": self._product.to_dict() if self._product else None,
            "created_at": self._created_at if self._created_at else None,
            "updated_at": self._updated_at if self._updated_at else None,
            "deleted_at": self._deleted_at if self._deleted_at else None,
        }
