import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccount.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()


def save_message(session_id, device_id, user_msg, ai_reply):
    ref = db.collection("sessions").document(session_id)
    ref.set(
        {"last_device": device_id, "updated_at": datetime.utcnow()},
        merge=True
    )
    ref.collection("messages").add({
        "role": "user",
        "content": user_msg,
        "device": device_id,
        "ts": datetime.utcnow()
    })
    ref.collection("messages").add({
        "role": "model",
        "content": ai_reply,
        "device": "flash",
        "ts": datetime.utcnow()
    })


def get_session(session_id):
    ref = db.collection("sessions").document(session_id)
    msgs = ref.collection("messages").order_by("ts").stream()
    return [m.to_dict() for m in msgs]


def get_history(session_id):
    msgs = get_session(session_id)
    return [{"role": m["role"], "parts": [m["content"]]} for m in msgs]


def set_active_device(session_id, device_id):
    db.collection("sessions").document(session_id).set(
        {"active_device": device_id}, merge=True
    )
