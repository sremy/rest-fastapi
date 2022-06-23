from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.post("/uploadfile/")
async def upload_file(file: UploadFile):
    # file is a tempfile.SpooledTemporaryFile, a file-like object
    bin_array = await file.read(-1)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(bin_array),
        "size_string": human_size(len(bin_array))
    }


@app.post("/uploadbytes/")
async def upload_bytes(file: bytes = File()):
    # With File class, all the content is read in memory by FastAPI and stored in bytes array
    # Prefer to use the UploadFile class, which stores content in memory until the spool_max_size limit,
    # passing this limit the content will be stored on disk.
    return {"content_size": len(file)}


@app.get("/")
async def main():
    content = """
<body>

<form action="/uploadfile/" enctype="multipart/form-data" method="post">
<div><input name="file" type="file" multiple></div>
<div><input type="submit"></div>
</form>

</body>
    """
    return HTMLResponse(content=content)


def human_size(bytes_count: int) -> str:
    """Given an integer size, return a short string formatted with a binary prefix """
    if bytes_count < 1024:
        return f"{bytes_count} Bytes"
    unite = 0
    suffix = "BKMGTPEZY"
    while bytes_count >= 1024:
        bytes_count /= 1024
        unite += 1
    if unite > 6:
        return "> 1024 YiP"
    return f"{bytes_count:.1f} {suffix[unite]}iB"
