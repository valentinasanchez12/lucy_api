import uvicorn

if __name__ == '__main__':
    uvicorn.run('lucy:app', host='0.0.0.0', port=8080, reload=True, access_log=True, log_level='debug')
