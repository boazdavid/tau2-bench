import os
from typing import Optional

from tau2.domains.airline.data_model import FlightDB
from tau2.domains.airline.tools import AirlineTools
from tau2.domains.airline.utils import AIRLINE_DB_PATH, AIRLINE_POLICY_PATH
from tau2.environment.environment import Environment
from rt_toolguard import guard_methods

def get_guarded_environment(
    db: Optional[FlightDB] = None,
    solo_mode: bool = False,
) -> Environment:
    if solo_mode:
        raise ValueError("Airline domain does not support solo mode")
    if db is None:
        db = FlightDB.load(AIRLINE_DB_PATH)
    tools = AirlineTools(db)
    
    # guards_path = "../gen_policy_validator/eval/airline/GT_tau2" #TODO env var
    guards_path = os.getenv("TOOLGUARDS_PATH")
    if guards_path:
        tools = guard_methods(tools, guards_path)

    with open(AIRLINE_POLICY_PATH, "r") as fp:
        policy = fp.read()
    return Environment(
        domain_name="airline",
        policy=policy,
        tools=tools,
    )