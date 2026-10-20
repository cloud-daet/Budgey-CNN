from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/v1", tags=["arima"])


@router.post("/forecast")
def forecast():
    # Postponed until the CNN matching has been tested.
    # Planned: receive weekly spending totals from the app, fit the modified
    # ARIMA, return the forecast. Stateless like everything else.
    raise HTTPException(501, "Forecasting is not implemented yet")
