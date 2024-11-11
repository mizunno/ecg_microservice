from fastapi.routing import APIRouter
from adapters.api.schemas import ECGRequest
from starlette.status import HTTP_201_CREATED

router = APIRouter(
    prefix="/ecg",
    tags=["ecg"],
)


@router.get("/")
async def read_ecg():
    return {"ecg": "ECG data"}


@router.post("/")
async def create_ecg(ecg: ECGRequest, status_code=HTTP_201_CREATED):
    return {"ecg": ecg}
