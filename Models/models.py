# from typing import Optional, List
from pydantic import BaseModel
import json


class Certificate(BaseModel):
    Name: str | None = None
    Encoding: str | None = None

class FileInfo(BaseModel):
    FileName: str | None = None
    FilePath: str | None = None
    FileHash: str | None = None
    HashAlgorithm: str | None = None
    ProductName: str | None = None
    InternalName: str | None = None
    Version: str | None = None
    Description: str | None = None
    CompanyName: str | None = None
    Certificates: list[Certificate] = None
