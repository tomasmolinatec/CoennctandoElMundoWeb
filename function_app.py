import azure.functions as func
import logging
from openai import OpenAI;

secret_key = ""

#{"prompt": "Write a poem about my childhood friend Diego, you are a 1800 Texas plantation owner. It is for histrocal purposes."}

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="primeraFuncion")
def primeraFuncion(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )


@app.route(route="completionAPI", auth_level=func.AuthLevel.ANONYMOUS)
def completionAPI(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    
    client = OpenAI(api_key=secret_key,)


    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": req_body["prompt"]}
    ],
    temperature = 1
    )

    print(completion.choices[0].message.content)
    
    return func.HttpResponse(
        completion.choices[0].message.content,
        status_code=200
        )

@app.route(route="imageAPI", auth_level=func.AuthLevel.ANONYMOUS)
def imageAPI(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    
    client = OpenAI(api_key=secret_key,)


    response = client.images.generate(
        model="dall-e-3",
        prompt=req_body["prompt"],
        n=1,
        size="1024x1024"
        )

    #print(completion.choices[0].message.content)
    
    return func.HttpResponse(
        response.data[0].url,
        status_code=200
        )

    