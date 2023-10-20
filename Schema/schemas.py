

def individual_serializer(FileInfo) -> dict:
    return {
        "id": str(FileInfo["_id"]),
        "FileName": FileInfo["FileName"],
        "FilePath": FileInfo["FilePath"],
        "FileHash": FileInfo["FileHash"],
        "HashAlgorithm": FileInfo["HashAlgorithm"],
        "ProductName": FileInfo["ProductName"],
        "InternalName": FileInfo["InternalName"],
        "Version": FileInfo["Version"],
        "Description": FileInfo["Description"],
        "CompanyName": FileInfo["CompanyName"],
        "Certificates": FileInfo["Certificates"],
    }

def list_serial(FileInfo) -> list:
    return [individual_serializer(FileInfo) for FileInfo in FileInfo]