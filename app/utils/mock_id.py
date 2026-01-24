import uuid

def generate_mock_id():
    rand = uuid.uuid4()
    return {
        "order_id" : f"MOCK-OD-{rand}",
        "payment_id" : f"MOCK-PY-{rand}",
        "signature_id" : f"MOCK-SI-{rand}",
    }