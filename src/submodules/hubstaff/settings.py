import os

from pydantic import BaseSettings


class HubStaffSettings(BaseSettings):
    HUBSTAFF_CLIENT_ID: str = os.environ['HUBSTAFF_CLIENT_ID']
    HUBSTAFF_SECRET_KEY: str = os.environ['HUBSTAFF_SECRET_KEY']


hub_staff_settings = HubStaffSettings()
