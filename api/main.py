from fastapi import FastAPI, File, UploadFile
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf

app = FastAPI()

MODEL = tf.keras.models.load_model("../models/1")
CLASS_NAME =['HYUNDAI_CRETA',
 'HYUNDAI_VENUE',
 'HYUNDAI_VERNA',
 'KIA_SELTOS',
 'MAHINDRA_BOLERO',
 'MAHINDRA_SCORPIO',
 'MAHINDRA_THAR',
 'MAHINDRA_XUV700',
 'MARUTI_BALENO',
 'MARUTI_BREZZA',
 'MARUTI_CIAZ',
 'MARUTI_DZIRE',
 'MARUTI_ERTIGA',
 'MARUTI_SWIFT',
 'TATA_HARRIER',
 'TATA_NEXON',
 'TATA_PUNCH',
 'TOYOTA_FORTUNER']

@app.get("/ping")
async def ping():
    return "Hello i am alive"


def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image


@app.post("/predict")
async def predict(
        file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)

    prediction = MODEL.predict(img_batch)

    predicted_class = CLASS_NAME[np.argmax(prediction[0])]
    confidence = np.max(prediction[0])

    return{
        "class": predicted_class,
        "confidence": float(confidence)
    }


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=4500)
