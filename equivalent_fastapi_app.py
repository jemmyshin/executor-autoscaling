from fastapi import FastAPI, Response
import asyncio
from jina.serve.runtimes.gateway.models import (
    JinaEndpointRequestModel,
    JinaRequestModel,
    JinaResponseModel,
)
from jina import __version__

app = FastAPI(
    title='My Jina Service',
    description='This is my awesome service. You can set `title` and `description` in your `Flow` or `Gateway` '
                   'to customize the title and description.',
    version=__version__,
)

PROCESS_TIME = 1


@app.post(
    path='/post',
    response_model=JinaResponseModel,
    # do not add response_model here, this debug endpoint should not restricts the response model
)
async def post(
        body: JinaEndpointRequestModel, response: Response
):  # 'response' is a FastAPI response, not a Jina response
    # The above comment is written in Markdown for better rendering in FastAPI
    await asyncio.sleep(PROCESS_TIME)
    result = body.dict()  # type: Dict
    return result

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=52000, log_level="info")