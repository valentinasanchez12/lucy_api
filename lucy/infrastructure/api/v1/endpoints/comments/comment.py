import uuid

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from lucy.application.use_case.comment.comment_use_case import CommentUseCase
from lucy.domain.models.comments import Comments
from lucy.domain.models.product import Product
from lucy.infrastructure.repositories.pg_repositories.pg_comment_repository import PGCommentRepository


async def save(request: Request):
    try:
        data = await request.json()
        required_fields = ["comment", "product_uuid"]

        # Validar campos requeridos
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return JSONResponse(
                status_code=422,
                content={
                    "data": None,
                    "success": False,
                    "response": f"Missing Parameters: {', '.join(missing_fields)}"
                }
            )

        product_id = data["product_uuid"]
        comment = Comments(
            _uuid=uuid.uuid4(),
            _comment=data["comment"]
        )

        use_case = CommentUseCase(repository=PGCommentRepository())
        saved_comment = await use_case.create(comment, product_id)

        if saved_comment:
            return JSONResponse(
                status_code=201,
                content={
                    "data": saved_comment,
                    "success": True,
                    "response": "Comment created successfully."
                }
            )
        else:
            return JSONResponse(
                status_code=400,
                content={
                    "data": None,
                    "success": False,
                    "response": "Unable to create comment."
                }
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "data": None,
                "success": False,
                "response": f"Internal Server Error: {str(e)}"
            }
        )


async def get_comments_by_product(request: Request):
    try:
        product_id = request.path_params.get("product_id")
        if not product_id:
            return JSONResponse(
                status_code=400,
                content={
                    "data": None,
                    "success": False,
                    "response": "Product ID is required."
                }
            )

        use_case = CommentUseCase(repository=PGCommentRepository())
        comments = await use_case.get_by_product_id(product_id)

        return JSONResponse(
            status_code=200,
            content={
                "data": comments,
                "success": True,
                "response": "Comments retrieved successfully."
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "data": None,
                "success": False,
                "response": f"Internal Server Error: {str(e)}"
            }
        )


routes = [
    Route('/', endpoint=save, methods=['POST']),
    Route('/{product_id}', endpoint=get_comments_by_product, methods=['GET']),
]
