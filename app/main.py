from fastapi import FastAPI,File,UploadFile,HTTPException
from app.schema.upload_schema import UploadResponse
from app.services.upload_service import save_file
import uvicorn
app = FastAPI()


@app.get("/home")
def func():
    return {"message": "welcome to DocuParse project"}



@app.post("/uploadfile", response_model=UploadResponse)
async def create_upload_file(file: UploadFile = File(...)):
    file_info = await save_file(file)
    return UploadResponse(**file_info)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

