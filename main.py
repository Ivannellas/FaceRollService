from fastapi import FastAPI, File, UploadFile
import face_recognition
import numpy as np

app = FastAPI()

# In-memory storage of employee face encodings
# In production, load from database
employee_encodings = {}  # {employee_id: encoding}

@app.post("/face/register/{employee_id}")
async def register_face(employee_id: int, file: UploadFile = File(...)):
    image = face_recognition.load_image_file(file.file)
    encodings = face_recognition.face_encodings(image)

    if not encodings:
        return {"success": False, "message": "No face detected"}

    employee_encodings[employee_id] = encodings[0].tolist()  # convert to list for JSON
    return {"success": True, "message": f"Face registered for employee {employee_id}"}

@app.post("/face/verify")
async def verify_face(file: UploadFile = File(...)):
    image = face_recognition.load_image_file(file.file)
    unknown_encodings = face_recognition.face_encodings(image)

    if not unknown_encodings:
        return {"success": False, "message": "No face detected"}
    
    unknown_encoding = unknown_encodings[0]

    for emp_id, enc in employee_encodings.items():
        known_encoding = np.array(enc)
        results = face_recognition.compare_faces([known_encoding], unknown_encoding)
        if results[0]:
            distance = face_recognition.face_distance([known_encoding], unknown_encoding)[0]
            return {"success": True, "employee_id": emp_id, "distance": float(distance)}

    return {"success": False, "message": "Face not recognized"}