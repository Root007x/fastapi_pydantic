from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from pydantic import BaseModel


app = FastAPI()


class Text(BaseModel):
    text : str


@app.post("/upload_pdf")
async def upload_pdf(file : UploadFile = File(...), text : str = Form(...)):
    
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF files are allowed."
        )

    pdf_file = await file.read()
    current_text = Text(text=text)
    
    return {"file_size" : len(pdf_file), "String" : current_text}
    
    