UVICORN_SERVER_PORT="${1}"
FLAT_ID="${2}"

curl -X 'POST' \
  http://localhost:"$UVICORN_SERVER_PORT"/api/price/?flat_id="$FLAT_ID" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "building_type_int": 2,
  "latitude": 55,
  "longitude": 33,
  "ceiling_height": 2,
  "flats_count": 200,
  "floors_total": 100,
  "has_elevator": true,
  "floor": 30,
  "kitchen_area": 1,
  "living_area": 10,
  "rooms": 2,
  "is_apartment": false,
  "total_area": 90
}'