import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from shakti.utils.constants import GOOGLE_APPLICATION_CREDENTIALS
from shakti.utils.utilities import get_env_creds

db = None


def initialize_db():
    global db
    get_env_creds()
    if not db:
        firebase_admin.initialize_app()
        db = firestore.client()
    return db
