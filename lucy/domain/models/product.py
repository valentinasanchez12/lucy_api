from nyoibo import Entity, fields

from lucy.domain.models.brand import Brand
from lucy.domain.models.category import Category
from lucy.domain.models.sanitary_registry import SanitaryRegistry


class Product(Entity):
    _uuid = fields.StrField()
    _generic_name = fields.StrField()
    _commercial_name = fields.StrField()
    _description = fields.StrField()
    _measurement = fields.StrField()
    _formulation = fields.StrField()
    _composition = fields.StrField()
    _reference = fields.StrField()
    _use = fields.StrField()
    _status = fields.StrField()
    _sanitize_method = fields.StrField()
    _images = fields.ListField()
    _brand = fields.LinkField(to=Brand)
    _category = fields.LinkField(to=Category)
    _sanitary_register = fields.LinkField(to=SanitaryRegistry)
    _comments = fields.ListField()
    _characteristics = fields.ListField()
    _technical_sheets = fields.ListField()
    _providers = fields.ListField()
    _created_at = fields.DatetimeField()
    _updated_at = fields.DatetimeField()
    _deleted_at = fields.DatetimeField()

    def to_dict(self) -> dict:
        return {
            "uuid": self._uuid if self._uuid else None,
            "generic_name": self._generic_name if self._generic_name else None,
            "commercial_name": self._commercial_name if self._commercial_name else None,
            "description": self._description if self._description else None,
            "measurement": self._measurement if self._measurement else None,
            "formulation": self._formulation if self._formulation else None,
            "composition": self._composition if self._composition else None,
            "reference": self._reference if self._reference else None,
            "use": self._use if self._use else None,
            "status": self._status if self._status else None,
            "sanitize_method": self._sanitize_method if self._sanitize_method else None,
            "images": self._images if self._images else [],
            "brand": self._brand.to_dict() if self._brand else None,
            "category": self._category.to_dict() if self._category else None,
            "sanitary_registry": self._sanitary_register.to_dict() if self._sanitary_register else None,
            "comments": self._comments if self._comments else None,
            "characteristics": self._characteristics if self._characteristics else None,
            "technical_sheets": self._technical_sheets if self._technical_sheets else None,
            "providers": self._providers if self._providers else None,
            "created_at": self._created_at.isoformat() if self._created_at else None,
            "updated_at": self._updated_at.isoformat() if self._updated_at else None,
            "deleted_at": self._deleted_at.isoformat() if self._deleted_at else None,
        }
