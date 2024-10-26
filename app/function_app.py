import azure.functions as func
import logging
import json
from openai import OpenAI;

def validate_json_format(json_data):
    # Define the required keys
    required_keys = ['Romance', 'Comedy', 'Action', 'Sadness', 'Critically_Acclaimed']
    
    # Check if all required keys are present
    for key in required_keys:
        if key not in json_data:
            return False
    
    # Validate that all values are between 0 and 10
    for key in required_keys:
        value = json_data[key]
        if not isinstance(value, (int, float)) or value < 0 or value > 10:
            return False
    
    return True



secret_key = "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"

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
        prompt = req_body["prompt"],
        n=1,
        size="1024x1024"
        )

    #print(completion.choices[0].message.content)
    
    return func.HttpResponse(
        response.data[0].url,
        status_code=200
        )

    

@app.route(route="recommender", auth_level=func.AuthLevel.ANONYMOUS)
def recommender(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()

    if not validate_json_format(req_body): #Validar formato correcto en JSON
        return func.HttpResponse(
        "Bad Format!",
        status_code=500
        ) 
    
    #Prompt
    client = OpenAI(api_key=secret_key,) 
    return_json = {"movies": "", "imageURL": ""}
    prompt = f"""Generate a list of 5 movie recommendations based on the following category ratings (0-10):
        Romance: {req_body["Romance"]}
        Comedy: {req_body["Comedy"]}
        Action: {req_body["Action"]}
        Sadness: {req_body["Sadness"]}
        Critically Acclaimed: {req_body["Critically_Acclaimed"]}
        For each movie, provide a brief summary and number them. After the movie title provide the year it was released in parenthesis. Without introduction or conclusion and without formatting please."""
    

    #Conseguir las 5 recomendaciones
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ],
    temperature = 1
    )
    return_json["movies"] = completion.choices[0].message.content 
    #Conseguir el nombre de la primera pelicula
    index1 = return_json["movies"].find("1.")
    index2 = return_json["movies"].find("(")
    firstmovie = return_json["movies"][index1 + 2:index2]

    #Crear foto de la primera pelicula
    image_prompt = f"Create a movie poster without text of {firstmovie}."
    response = client.images.generate(
        model="dall-e-3",
        prompt = image_prompt,
        n=1,
        size="1024x1024"
        )
    
    return_json["imageURL"] = response.data[0].url

    
    json_response = json.dumps(return_json)
    return func.HttpResponse(
        json_response,
        status_code=200,
        mimetype="application/json"
        )