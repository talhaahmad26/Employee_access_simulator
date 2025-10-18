from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, date
from .models import Room, AccessLog
from .serializers import BulkCheckSerializer


@api_view(['POST'])
def check_bulk(request):
    serializer = BulkCheckSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    items = serializer.validated_data['data']
    today = date.today()

    # Preload rooms for quick lookup
    room_names = set(item['room'] for item in items)
    rooms = {r.name: r for r in Room.objects.filter(name__in=room_names)}

    results = []
    last_access = {}  # (emp_id, room_name) → last access datetime (today only)

    for item in items:
        emp_id = item['id']
        lvl = item['access_level']
        room_name = item['room']
        req_time_str = item['request_time']

        try:
            req_time = datetime.strptime(req_time_str, "%H:%M")
        except ValueError:
            results.append({
                "id": emp_id,
                "access_level": lvl,
                "request_time": req_time_str,
                "room": room_name,
                "status": "Denied",
                "reason": f"Invalid time format: {req_time_str}"
            })
            continue

        # Define room rules
        room_rules = {
            "Vault": {"level": 3, "cooldown": 15},
            "ServerRoom": {"level": 2, "cooldown": 10},
            "R&D Lab": {"level": 1, "cooldown": 5}
        }

        # Default response (will be updated if granted)
        response_data = {
            "id": emp_id,
            "access_level": lvl,
            "request_time": req_time_str,
            "room": room_name
        }

        # Check room validity
        if room_name not in room_rules:
            response_data.update({
                "status": "Denied",
                "reason": "Invalid room"
            })
        else:
            rule = room_rules[room_name]
            required_level = rule["level"]
            cooldown = rule["cooldown"]

            # Check access level
            if lvl < required_level:
                response_data.update({
                    "status": "Denied",
                    "reason": "Below required access level"
                })
            else:
                # Cooldown check
                key = (emp_id, room_name)
                if key in last_access:
                    last_time = last_access[key]
                    diff = (req_time - last_time).total_seconds() / 60
                    if diff < cooldown:
                        response_data.update({
                            "status": "Denied",
                            "reason": f"Cooldown active ({int(diff)} min since last access)"
                        })
                    else:
                        response_data.update({
                            "status": "Granted",
                            "reason": f"Access granted to {room_name}"
                        })
                        last_access[key] = req_time
                else:
                    response_data.update({
                        "status": "Granted",
                        "reason": f"Access granted to {room_name}"
                    })
                    last_access[key] = req_time

        # ✅ Save every attempt in AccessLog (granted or denied)
        try:
            room_obj = rooms.get(room_name)
            if room_obj:
                AccessLog.objects.create(
                    employee_id=emp_id,
                    room=room_obj,
                    access_time=req_time.time(),
                    status=response_data["status"],
                    reason=response_data["reason"]
                )
        except Exception as e:
            print(f" Failed to save log for {emp_id} - {room_name}: {e}")

        # Append to results
        results.append(response_data)

    return Response({"results": results}, status=status.HTTP_200_OK)
