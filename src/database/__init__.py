from typing import List, Union

from .connectionDatabase import ConnectionDatabase
from .operationsDatabase import OperationsDatabase

operations = OperationsDatabase()
conn = ConnectionDatabase().get_connection
