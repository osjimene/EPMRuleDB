from fastapi import FastAPI, UploadFile, File
from Models.models import FileInfo
from Modules.utils import stage_files, get_fileattributes, process_and_insert
from Modules.mongo import insert_data, collection
from Schema.schemas import list_serial, individual_serializer
import json
import os
from typing import List



app = FastAPI(max_upload_size=1024*1024*1024)  # 1GB

@app.get("/")
async def root():
    return {"message": "This is the root of your endpoint."}



@app.post("/processfiles/")
async def process_files() -> str:
    files = await stage_files()
    rules = []
    if files:
        for file in files:
            fileinfo = await get_fileattributes(file)
            rules.append(fileinfo)
            # return rules
        await process_and_insert(rules)
        return (f"{len(rules)} files have been processed successfully.")
        # return("The following Rules have been processed successfully:\n " + str(rules))
    return ("There are currently no staged files to process.")


@app.get("/getrecentdata/")
async def get_recent_data(num_records: int = 10):
    FileParams = list_serial(collection.find().sort("_id", -1).limit(num_records))
    return FileParams

@app.post("/insertdata/")
async def insert(fileData: List[FileInfo]):
    for file in fileData:
        data = file.model_dump()
        await insert_data(data)
    return print("Data inserted successfully into the database.")


@app.post("/uploadfile/")
async def create_upload_file(files: List[UploadFile] = File(...)):
    response = []
    for file in files:
        if file.filename.endswith('.exe'):
            fileData = file.file.read()
            #if os.path.join(os.getcwd(), 'Tmp') does not exist, create it
            if not os.path.exists(os.path.join(os.getcwd(), 'Tmp')):
                os.makedirs(os.path.join(os.getcwd(), 'Tmp'))
            with open(os.path.join(os.getcwd(), 'Tmp', file.filename), "wb") as buffer:
                buffer.write(fileData)
            response.append({"info": f"File {file.filename} has been uploaded and processed successfully."})
        else:
            response.append({"error": f"File {file.filename} is not an executable file. Please upload an executable file only for metadata extraction."})
    return response
