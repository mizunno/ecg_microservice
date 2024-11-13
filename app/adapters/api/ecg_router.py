from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from adapters.api.schemas import (
    ECGRequestSchema,
    ECGResponseSchema,
    LeadSchema,
    ECGInsightResponseSchema,
)
from services.ecg_service import ECGService
from adapters.api.dependencies import (
    get_ecg_service,
    verify_user,
)
from adapters.database.models import User


router = APIRouter(
    prefix="/ecg",
    tags=["ecg"],
)


@router.get(
    "/{ecg_id}", response_model=ECGResponseSchema, status_code=status.HTTP_200_OK
)
def get_ecg(
    ecg_id: str,
    current_user: User = Depends(verify_user),
    ecg_service: ECGService = Depends(get_ecg_service),
):
    """
    Endpoint to retrieve an ECG by ID.
    """

    ecg = ecg_service.get(ecg_id=ecg_id)

    if ecg is None or ecg.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ECG not found"
        )

    return {
        "ecg_id": ecg.ecg_id,
        "date": ecg.date,
        "leads": [
            LeadSchema(
                name=lead.name,
                signal=lead.signal,
                num_samples=lead.num_samples,
                zero_crossings=lead.zero_crossings,
            )
            for lead in ecg.leads
        ],
    }


@router.get(
    "/{ecg_id}/insights",
    response_model=ECGInsightResponseSchema,
    status_code=status.HTTP_200_OK,
)
def get_ecg_insights(
    ecg_id: str,
    current_user: User = Depends(verify_user),
    ecg_service: ECGService = Depends(get_ecg_service),
):
    """
    Endpoint to retrieve the insights of a particular ECG.
    """

    ecg = ecg_service.get(ecg_id=ecg_id)

    if ecg is None or ecg.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ECG not found"
        )

    return {
        "leads": [
            {"name": lead.name, "zero_crossings": lead.zero_crossings}
            for lead in ecg.leads
        ]
    }


@router.post("", status_code=status.HTTP_201_CREATED)
def upload_ecg(
    ecg_data: ECGRequestSchema,
    current_user: User = Depends(verify_user),
    ecg_service: ECGService = Depends(get_ecg_service),
):
    """
    Endpoint to upload ECG data for processing and storage.
    """
    try:
        ecg_id = ecg_service.process(
            leads=[lead.model_dump() for lead in ecg_data.leads],
            user_id=current_user.id,
        )
        return {"ecg_id": ecg_id}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to upload ECG data") from e
