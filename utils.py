import os
import subprocess
import shutil
from Models.models import *
import re
import datetime
from mongo import insert_data


async def stage_files() -> list[str]:
    files = []
    # for all the files that are in the Tmp folder, append the file path to the files list
    for file in os.listdir(os.path.join(os.getcwd(), 'Tmp')):
        files.append(os.path.join(os.getcwd(), 'Tmp', file))
    return files

##This uses the EPM commandlet to grab all the file attribute information via powershell.
async def get_fileattributes(file) -> FileInfo:
    #Set the certoutput path to the Certificates folder
    certoutput = os.path.join(os.getcwd(), 'Certificates')
    #instatiate the FileInfo model
    fileinfo = FileInfo()
    epmModule = os.path.join(os.getcwd(),'EpmModules', 'EpmCmdlets.dll')  
    # epmModule = os.path.join(os.getcwd(), 'modules', 'EpmModules', 'EpmCmdlets.dll')
    hashalgorithm = "Sha256"
    result = subprocess.run(["powershell", rf"Import-Module {epmModule}; Get-fileAttributes -FilePath '{file}' -CertOutputPath {certoutput} -HashAlgorithm '{hashalgorithm}'"],capture_output=True, text=True)
    fileattributes = result.stdout
    result_dict = {}
    for line in fileattributes.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            result_dict[key.strip()] = value.strip()
    #Set the path to the certificate location
    certstore = os.path.join(certoutput, result_dict['FileName'] + ' Certificate Chain')
    #Cleanup the current file that was processed from the Tmp folder
    os.remove(file)
    #map the fileattributes to the FileInfo model
    fileinfo.FileName = result_dict['FileName']
    fileinfo.FilePath = result_dict['FilePath']
    fileinfo.FileHash = result_dict['FileHash']
    fileinfo.HashAlgorithm = result_dict['HashAlgorithm']
    fileinfo.ProductName = result_dict['ProductName']
    fileinfo.InternalName = result_dict['InternalName']
    fileinfo.Version = result_dict['Version']
    fileinfo.Description = result_dict['Description']
    fileinfo.CompanyName = result_dict['CompanyName']
    fileinfo.Certificates = await get_certificates(certstore)

    return fileinfo


async def get_certificates(certstore) -> list[Certificate]:
    certs = []
    #set a list to gather all the certificate paths in the certstore
    certificates = []
    # for all the certificates that are in the certstore, append the file path to the files list
    for certificate in os.listdir(certstore):
        certificates.append(os.path.join(certstore, certificate))

    for path in certificates:
        #instatiate the Certificate model
        cert = Certificate()
        #run the get_certificate function for each certificate in the certstore
        certname = subprocess.run(["powershell", f"Split-Path '{path}' -Leaf"],capture_output=True, text=True)
        path = re.sub(r'\[(\d+)\]', r'`[\1`]', path)
        encoding = subprocess.run(["powershell", f"cat '{path}'"],capture_output=True, text=True)
        cert.Name = certname.stdout.strip()
        cert.Encoding = encoding.stdout.strip()
        #append the certificate to the certs list
        certs.append(cert)
    #cleanup all the certificates in the certstore
    shutil.rmtree(certstore)
    return certs

async def process_and_insert(fileData: list[FileInfo]):
    for file in fileData:
        data = file.model_dump()
        await insert_data(data)
    return print("Data inserted successfully into the database.")




# encoding = subprocess.run(["powershell","cat 'C:\\Users\\osjimene\\Projects\\RuleCreator\\Tmp\\DigiCert Trusted G4 Code Signing RSA4096 SHA384 2021 CA1 CA-Cert Index`[2`].cer'"], capture_output=True, text=True)