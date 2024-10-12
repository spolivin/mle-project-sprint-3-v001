import argparse
import time

import requests

# Fixing the number of requests to be sent
REQUESTS_NUMBER = 30

# Creating an additional argument (port to which to send requests)
parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int)
args = parser.parse_args()

# Sequence of POST-requests to API
for i in range(0, REQUESTS_NUMBER):
    # Iteratively choosing different feature values
    data = {
        "building_type_int": i + 1,
        "latitude": 55 + i,
        "longitude": 33 + i + 9,
        "ceiling_height": 2 + i,
        "flats_count": 2 + i,
        "floors_total": 10 + i,
        "has_elevator": True,
        "floor": 2 + i,
        "kitchen_area": 10 + i + 1,
        "living_area": 20 + i + 4,
        "rooms": i + 1,
        "is_apartment": True,
        "total_area": 30 + i,
    }

    # Sending a POST-request
    server_response = requests.post(
        url=f"http://localhost:{args.port}/api/price/?flat_id={i}",
        json=data,
    )
    # Displaying server response
    print(
        f"Request #{i + 1}: response={server_response.text}, status={server_response.status_code}\n"
    )

    # Making a 30 sec pause halfway through the requests loop
    if i == (REQUESTS_NUMBER // 2) - 1:
        time.sleep(30)

    # Making a 2 sec pause after each request
    time.sleep(2)
