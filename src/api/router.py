"""Configure API routing."""

import fastapi

from src.api.endpoints import get_transcript
from src.config import settings

router = fastapi.APIRouter(responses={404: {"description": "Not found"}})
router.include_router(get_transcript.router)
