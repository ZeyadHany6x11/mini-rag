# mini-rag

This is a minimal implementation of the RAG model for question answering.

## Requirements

- Python 3.8 or later

#### Install Python using MiniConda

1) Download and install MiniConda from [here](https://docs.anaconda.com/free/miniconda/#quick-command-line-install)
2) Create a new environment using the following command:
```bash
$ conda create -n mini-rag python=3.8
```
3) Activate the environment:
```bash
$ conda activate mini-rag
```

### (Optional) Setup you command line interface for better readability

```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

## Installation

### Install the required packages

```bash
$ pip install -r src/requirements.txt
```

### Setup the environment variables

```bash
$ cp src/.env.example src/.env
```

Set the values in `src/.env`. The upload settings control the allowed MIME types, maximum file size, and read chunk size.

## Run the FASTAPI Server 

```bash 
$ cd src
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

Run the server from `src` so it can load `src/.env` and the local modules.

## API Endpoints

### Welcome

```http
GET http://127.0.0.1:5000/api/v1/
```

### Upload a file

Send a multipart form request with the file field named `file`:

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/data/upload/1" \
  -F "file=@path/to/document.pdf"
```

The upload endpoint accepts the MIME types listed in `FILE_ALLOWED_TYPES` and files up to `FILE_MAX_SIZE` MB. It saves accepted files under `src/assets/files/<project_id>/` with a generated filename. This endpoint validates and stores files; document parsing and indexing are not implemented yet.

## POSTMAN Collection 

[Download the POSTMAN collection](src/assets/Mini-Rag-App.postman_collection.json)
