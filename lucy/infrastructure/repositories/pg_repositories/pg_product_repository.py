from lucy.application.repositories import ProductRepository
from lucy.domain.models.brand import Brand
from lucy.domain.models.category import Category
from lucy.domain.models.product import Product
from lucy.domain.models.sanitary_registry import SanitaryRegistry
from lucy.infrastructure.repositories.pg_repositories.pg_pool import get_pool


class PGProductRepository(ProductRepository):

    async def get_random(self, limit: int = 12):
        pool = get_pool()
        async with pool.acquire() as connection:
            rows = await connection.fetch(
                '''
                SELECT p.uuid, p.generic_name, p.image, b.uuid AS brand_uuid, b.name AS brand_name
                FROM products p
                LEFT JOIN brands b ON p.brand_id = b.uuid
                WHERE p.delete_at IS NULL
                ORDER BY RANDOM()
                LIMIT $1
                ''',
                limit
            )
            return [
                {
                    "uuid": row["uuid"],
                    "generic_name": row["generic_name"],
                    "image": row["image"],
                    "brand": {
                        "uuid": row["brand_uuid"],
                        "name": row["brand_name"]
                    }
                }
                for row in rows
            ]
    async def update(self, product_id: str, product: Product, images: list):
        pool = get_pool()
        async with pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
                    '''
                    UPDATE products
                    SET generic_name = COALESCE($2, generic_name),
                        commercial_name = COALESCE($3, commercial_name),
                        description = COALESCE($4, description),
                        measurement = COALESCE($5, measurement),
                        formulation = COALESCE($6, formulation),
                        composition = COALESCE($7, composition),
                        reference = COALESCE($8, reference),
                        use = COALESCE($9, use),
                        status = COALESCE($10, status),
                        sanitize_method = COALESCE($11, sanitize_method),
                        image = COALESCE($12, image),
                        brand_id = COALESCE($13, brand_id),
                        category_id = COALESCE($14, category_id),
                        sanitary_register_id = COALESCE($15, sanitary_register_id),
                        updated_at = LOCALTIMESTAMP
                    WHERE uuid = $1 AND delete_at IS NULL
                    ''',
                    product_id,
                    product.generic_name,
                    product.commercial_name,
                    product.description,
                    product.measurement,
                    product.formulation,
                    product.composition,
                    product.reference,
                    product.use,
                    product.status,
                    product.sanitize_method,
                    images,
                    product.brands.uuid,
                    product.categories.uuid,
                    product.sanitary_register.uuid,
                )
                updated_product = await self.get_by_id(product_id)
                return updated_product

    async def delete(self, product_id: str):
        pass

    async def get_by_id(self, product_id: str):
        pool = get_pool()
        async with pool.acquire() as connection:
            row = await connection.fetchrow(
                '''
                SELECT 
                    p.uuid, p.generic_name, p.commercial_name, p.description, p.measurement,
                    p.formulation, p.composition, p.reference, p.use, p.status,
                    p.sanitize_method, 
                    ARRAY(
                        SELECT pi.image_path
                        FROM product_images pi
                        WHERE pi.product_id = p.uuid
                    ) AS images,
                    p.created_at, p.updated_at,
                    b.uuid AS brand_uuid, b.name AS brand_name,
                    c.uuid AS category_uuid, c.name AS category_name,
                    sr.uuid AS sanitary_register_uuid, sr.number_registry,
                    ARRAY(
                        SELECT json_build_object(
                            'uuid', o.uuid,
                            'observation', o.observation
                        )
                        FROM observations o
                        WHERE o.product_id = p.uuid
                    ) AS observations,
                    ARRAY(
                        SELECT json_build_object(
                            'uuid', ch.uuid,
                            'characteristic', ch.characteristic,
                            'description', ch.description
                        )
                        FROM characteristics ch
                        WHERE ch.product_id = p.uuid
                    ) AS characteristics,
                    ARRAY(
                        SELECT json_build_object(
                            'uuid', ts.uuid,
                            'document', ts.document
                        )
                        FROM technical_sheets ts
                        WHERE ts.product_id = p.uuid
                    ) AS technical_sheets
                FROM products p
                LEFT JOIN brands b ON p.brand_id = b.uuid
                LEFT JOIN categories c ON p.category_id = c.uuid
                LEFT JOIN sanitary_registry sr ON p.sanitary_register_id = sr.uuid
                WHERE p.uuid = $1 AND p.delete_at IS NULL
                ''',
                product_id
            )
            if row:
                return Product(
                    uuid=row['uuid'],
                    generic_name=row['generic_name'],
                    commercial_name=row['commercial_name'],
                    description=row['description'],
                    measurement=row['measurement'],
                    formulation=row['formulation'],
                    composition=row['composition'],
                    reference=row['reference'],
                    use=row['use'],
                    status=row['status'],
                    sanitize_method=row['sanitize_method'],
                    image=row['images'],  # Lista de URLs de imágenes
                    brands=Brand(uuid=row['brand_uuid'], name=row['brand_name']),
                    categories=Category(uuid=row['category_uuid'], name=row['category_name']),
                    sanitary_register=SanitaryRegistry(uuid=row['sanitary_register_uuid'],
                                                       number_registry=row['number_registry']),
                    observations=[
                        Comment(uuid=o['uuid'], observation=o['observation'])
                        for o in row['observations']
                    ],
                    characteristics=[
                        Characteristic(uuid=ch['uuid'], characteristic=ch['characteristic'],
                                       description=ch['description'])
                        for ch in row['characteristics']
                    ],
                    technical_sheets=[
                        TechnicalSheet(uuid=ts['uuid'], document=ts['document'])
                        for ts in row['technical_sheets']
                    ],
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                )
            return None

    async def get_all(self):
        pass

    async def save(self, product: Product):
        pool = get_pool()
        async with pool.acquire() as connection:
            row = await connection.fetchrow(
                '''
                INSERT INTO products (
                    uuid, generic_name, commercial_name, description, measurement,
                    formulation, composition, reference, use, status, sanitize_method,
                    image, brand_id, category_id, sanitary_register_id, created_at, updated_at
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, LOCALTIMESTAMP, LOCALTIMESTAMP)
                RETURNING uuid, generic_name, commercial_name, description, measurement,
                          formulation, composition, reference, use, status, sanitize_method,
                          image, brand_id, category_id, sanitary_register_id, created_at, updated_at
                ''',
                product.uuid,
                product.generic_name,
                product.commercial_name,
                product.description,
                product.measurement,
                product.formulation,
                product.composition,
                product.reference,
                product.use,
                product.status,
                product.sanitize_method,
                product.image,
                product.brands.uuid,
                product.categories.uuid,
                product.sanitary_register.uuid,
            )
            if row:
                return Product(
                    uuid=row['uuid'],
                    generic_name=row['generic_name'],
                    commercial_name=row['commercial_name'],
                    description=row['description'],
                    measurement=row['measurement'],
                    formulation=row['formulation'],
                    composition=row['composition'],
                    reference=row['reference'],
                    use=row['use'],
                    status=row['status'],
                    sanitize_method=row['sanitize_method'],
                    image=row['image'],
                    brand=Brand(uuid=row['brand_id']),
                    category=Category(uuid=row['category_id']),
                    sanitary_register=SanitaryRegistry(uuid=row['sanitary_register_id']),
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                )
            return None

    async def search(self, query: str):
        pool = get_pool()
        async with pool.acquire() as connection:
            filters = self._parse_query(query)
            sql = '''
                SELECT DISTINCT p.uuid, p.generic_name, p.commercial_name, p.description, p.measurement,
                                p.formulation, p.composition, p.reference, p.use, p.status,
                                p.sanitize_method, p.image, p.created_at, p.updated_at,
                                b.uuid AS brand_uuid, b.name AS brand_name,
                                c.uuid AS category_uuid, c.name AS category_name,
                                sr.uuid AS sanitary_register_uuid, sr.number_registry
                FROM products p
                LEFT JOIN brands b ON p.brand_id = b.uuid
                LEFT JOIN categories c ON p.category_id = c.uuid
                LEFT JOIN sanitary_registry sr ON p.sanitary_register_id = sr.uuid
                LEFT JOIN brand_providers bp ON bp.brand_id = b.uuid
                LEFT JOIN providers pr ON bp.provider_id = pr.uuid
                WHERE p.delete_at IS NULL
            '''

            conditions = []
            params = []
            if "brand" in filters:
                conditions.append("LOWER(b.name) LIKE $1")
                params.append(f"%{filters['brand'].lower()}%")
            if "category" in filters:
                conditions.append("LOWER(c.name) LIKE $2")
                params.append(f"%{filters['category'].lower()}%")
            if "sanitary_registry" in filters:
                conditions.append("LOWER(sr.number_registry) LIKE $3")
                params.append(f"%{filters['sanitary_registry'].lower()}%")
            if "provider" in filters:
                conditions.append("LOWER(pr.name) LIKE $4")
                params.append(f"%{filters['provider'].lower()}%")
            if "general" in filters:
                general_conditions = '''
                    LOWER(p.generic_name) LIKE $5 OR
                    LOWER(p.commercial_name) LIKE $5 OR
                    LOWER(p.description) LIKE $5 OR
                    LOWER(p.measurement) LIKE $5 OR
                    LOWER(p.formulation) LIKE $5 OR
                    LOWER(p.composition) LIKE $5 OR
                    LOWER(p.reference) LIKE $5 OR
                    LOWER(p.use) LIKE $5 OR
                    LOWER(p.status) LIKE $5 OR
                    LOWER(p.sanitize_method) LIKE $5
                '''
                conditions.append(f"({general_conditions})")
                params.append(f"%{filters['general'].lower()}%")

            if conditions:
                sql += " AND " + " AND ".join(conditions)

            rows = await connection.fetch(sql, *params)

            return [
                {
                    "uuid": row["uuid"],
                    "generic_name": row["generic_name"],
                    "commercial_name": row["commercial_name"],
                    "description": row["description"],
                    "measurement": row["measurement"],
                    "formulation": row["formulation"],
                    "composition": row["composition"],
                    "reference": row["reference"],
                    "use": row["use"],
                    "status": row["status"],
                    "sanitize_method": row["sanitize_method"],
                    "image": row["image"],
                    "brand": {"uuid": row["brand_uuid"], "name": row["brand_name"]},
                    "category": {"uuid": row["category_uuid"], "name": row["category_name"]},
                    "sanitary_registry": {"uuid": row["sanitary_register_uuid"],
                                          "number_registry": row["number_registry"]},
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"]
                }
                for row in rows
            ]

    def _parse_query(self, query: str):
        filters = {}
        query = query.lower()
        if "in: marca" in query:
            filters["brand"] = query.split("in: marca '")[1].split("'")[0]
        if "in: categoría" in query:
            filters["category"] = query.split("in: categoría '")[1].split("'")[0]
        if "in: registro sanitario" in query:
            filters["sanitary_registry"] = query.split("in: registro sanitario '")[1].split("'")[0]
        if "in: proveedor" in query:
            filters["provider"] = query.split("in: proveedor '")[1].split("'")[0]
        if not any(key in query for key in ["in: marca", "in: categoría", "in: registro sanitario", "in: proveedor"]):
            filters["general"] = query
        return filters
