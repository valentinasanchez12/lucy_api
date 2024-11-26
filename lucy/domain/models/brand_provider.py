from nyoibo import Entity, fields


class BrandProvider(Entity):
    _brand_uuid = fields.StrField()
    _provider_uuid = fields.StrField()
