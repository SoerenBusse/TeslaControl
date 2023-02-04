import logging
import secrets

import teslapy
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status
from starlette.responses import Response
from teslapy import Tesla, Vehicle

from app.config.settings import settings
from app.state.WakeupState import WakeupState
from app.utils import Utils

logger = logging.getLogger(__name__)

app = FastAPI()
security = HTTPBasic()
tesla = Tesla(settings.tesla_account_email, authenticator=None)

# Store wheter a wakeup is currently running
# Because we're only using a single worker it's save to store it in a variable
wakeup_state = WakeupState()


def authorize(credentials: HTTPBasicCredentials = Depends(security)):
    username_bytes = credentials.username.encode("utf8")
    password_bytes = credentials.password.encode("utf8")

    correct_username = secrets.compare_digest(username_bytes, settings.api_username.encode("utf8"))
    correct_password = secrets.compare_digest(password_bytes, settings.api_password.encode("utf8"))

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username


def fetch_vehicle() -> Vehicle:
    if not tesla.authorized:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Tesla API not authorized. You've to run the login script before using the service"
        )

    vehicles = tesla.vehicle_list()
    vehicle: Vehicle = next((vehicle for vehicle in vehicles if vehicle["vin"] == settings.vehicle_vin), None)

    if vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"No vehicle with VIN {settings.vehicle_vin} in user account {settings.tesla_account_email} found"
        )

    return vehicle


@app.post("/open-charge-port")
async def open_charge_port(_=Depends(authorize), vehicle: Vehicle = Depends(fetch_vehicle)):
    # Only execute command if there's no wake up currently running
    if wakeup_state.wakeup_running:
        return Response(status_code=status.HTTP_202_ACCEPTED)

    # Call open charge port command. Sadly teslapy is not async
    try:
        logger.info("Wakeup vehicle")
        wakeup_state.wakeup_running = True
        await Utils.wake_up_vehicle_async(vehicle)

        logger.error("Open charge port")
        vehicle.command("CHARGE_PORT_DOOR_OPEN")
    except (teslapy.HTTPError | teslapy.VehicleError) as e:
        message = f"Error while opening charge port: ${str(e)}"

        logger.error(message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message
        )
    finally:
        logger.info("Disable wakeup")
        wakeup_state.wakeup_running = False

    return Response(status_code=status.HTTP_204_NO_CONTENT)
