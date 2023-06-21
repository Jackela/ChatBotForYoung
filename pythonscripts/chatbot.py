import openai
import time
import os
import json
from typing import List, Union, Dict, Optional
import requests


def initialize_api_key():
    ##read api key from env
    openai.api_key = os.environ["OPENAI_API_KEY"]

initialize_api_key()

instruct_model = ["ada", "babbage", "curie", "davinci"]
default_max_tokens=1000 ## need further configuration
default_text_model = "text-davinci-003" ## default text model
default_chat_model = "gpt-3.5-turbo" ## default chat model
default_audio_model = "whisper-1"
# use "model" instead of "engine" !!!!!!!!!!!!!
def create_text_completion(message:str, model:str=None, prompt_text:str=None, suffix:Optional[str]=None, max_tokens:int=None,  temperature:float=None, 
        top_p:float=None, n:int=None, stream:bool = None, logprobs:int=None, echo:bool=None, stop:Union[str, List[str]]=None, presence_penalty:float=None,
        frequency_penalty:float=None, best_of:int=None, logit_bias:Dict[str, float]=None, user:str=None) -> str:

    params = {
        "model": model or default_text_model,
        "prompt": prompt_text or f"Conversation with OpenAI ChatBot:\nUser: {message}\nAI:",
        "max_tokens": max_tokens or default_max_tokens
    }
    if suffix is not None:
        params["suffix"] = suffix

    if top_p is not None:
        params["top_p"] = top_p

    if logprobs is not None:
        params["logprobs"] = logprobs

    if echo is not None:
        params["echo"] = echo

    if presence_penalty is not None:
        params["presence_penalty"] = presence_penalty

    if frequency_penalty is not None:
        params["frequency_penalty"] = frequency_penalty

    if best_of is not None:
        params["best_of"] = best_of

    if n is not None:
        params["n"] = n

    if stream is not None:
        params["stream"] = stream

    if stop is not None:
        params["stop"] = stop

    if temperature is not None:
        params["temperature"] = temperature

    if logit_bias is not None:
        params["logit_bias"] = logit_bias

    if user is not None:
        params["user"] = user

    response = openai.Completion.create(**params)

    if response.choices:
        return response.choices[0].text.strip()
    else:
        return ""

def create_chat_completion(content: str, role: str = "user", name: Optional[str] = None,
            model: str = None, max_tokens: int = None, temperature: float = None,
            top_p: float = None, n: int = None, stream: bool = None,
            stop: Union[str, List[str]] = None, presence_penalty: float = None,
            frequency_penalty: float = None, logit_bias: Dict[str, float] = None,
            user: str = None) -> str:
    
    params = {
        "model": model or default_chat_model,
        "messages": [{"role": role, "content": content}],
        "max_tokens": max_tokens or default_max_tokens
    }
    
    if name is not None:
        params["messages"][0]["name"] = name
        
    if temperature is not None:
        params["temperature"] = temperature
        
    if top_p is not None:
        params["top_p"] = top_ppip
        
    if n is not None:
        params["n"] = n
        
    if stream is not None:
        params["stream"] = stream
        
    if stop is not None:
        params["stop"] = stop
        
    if presence_penalty is not None:
        params["presence_penalty"] = presence_penalty
        
    if frequency_penalty is not None:
        params["frequency_penalty"] = frequency_penalty
        
    if logit_bias is not None:
        params["logit_bias"] = logit_bias
        
    if user is not None:
        params["user"] = user
        
    response = openai.ChatCompletion.create(**params)
    
    if response.choices:
        return response.choices[0].message.content
    else:
        return ""


## text-davinci-edit-001 or code-davinci-edit-001
## or use list_edit_model_ids() to get list of models
def create_text_edit(model, message: str, instruction: str):
    if model in list_edit_model_ids():
        response = openai.Edit.create(
            model=model,
            input=message,
            instruction=instruction
        )
        return response.choices[0]
    return False

# image:str is file encoded in base64
def create_image(prompt: str, image_number: int = 1, size: str = "1024x1024", response_format: str = "url"):
    response = openai.Image.create(
        prompt=prompt,
        n=image_number,
        size=size,
        response_format=response_format
    )
    return response.data[0].url

def create_image_edit(prompt: str, image: str, mask: str = None, image_number: int = 1, size: str = "1024x1024", response_format: str = "url"):
    response = openai.Image.create_edit(
        image=image,
        mask=mask,
        prompt=prompt,
        n=image_number,
        size=size,
        response_format=response_format)
    return response.data

def create_image_variation(image: str, image_number: int = 1, size: str = "1024x1024", response_format: str = "url"):
    response = openai.Image.create_variation(
        image=image,
        n=image_number,
        size=size,
        response_format=response_format
    )
    return response.data

def create_embedding(model,message: str):
    if model in list_embedding_model_ids():
        response = openai.Embedding.create(
            model=model,
            input=message
        )
        return response.data[0].embedding
    return False

## only "whisper-1" is available for audio related work
## audio formats: mp3, mp4, mpeg, mpga, m4a, wav, or webm
def create_audio_transcription( file:str, model:str=None, prompt:str = None, response_format:str = "json", temperature:float = 0, language:str = "zh"):
    if model in list_audio_model_ids() or model == None:  
        response = openai.Audio.transcribe(
            file = file,
            model = model or default_audio_model,
            prompt = prompt,
            response_format = response_format,
            temperature = temperature,
            language = language
        )
        return response.text
    return False

## translate into English Only
## 不支持中文（普通话）翻译成英文 （ ？）
## 支持粤语翻译英文
## 支持日文翻译中文
def create_audio_translation(file:str, model:str=None, prompt:str = None, response_format:str = "json", temperature:float = 0):
    if model in list_audio_model_ids() or model == None:  
        response = openai.Audio.translate(
            file = file,
            model = model or default_audio_model,
            prompt = prompt,
            response_format = response_format,
            temperature = temperature,
            ##language = language ## only English is supported
        )
        return response.text
    return False

def create_moderation(message:str):
    return openai.Moderation.create(
        input = message
    )
## Models compatibility
## 参考以下网址 模型对于各项功能是否适用
## https://platform.openai.com/docs/models/model-endpoint-compatibility

def list_models():
    return openai.Model.list().data

def list_model_ids():
    model_ids = [model['id']
        for model in list_models() if model['object'] == 'model']
    return model_ids

def list_text_model_ids():
    text_model_ids = [model for model in list_model_ids() if 'text' in model 
    or 'davinci' in model or 'curie' in model or 'ada' in model]
    return text_model_ids

def list_chat_model_ids():
    chat_model_ids = [model['id'] for model in list_models() if 'gpt' in model['id']]
    return chat_model_ids

def list_edit_model_ids():
    edit_model_ids = [model['id'] for model in list_models() if 'edit' in model['id']]
    return edit_model_ids

def list_embedding_model_ids():
    embedding_model_ids = [model['id'] for model in list_models() if 'embedding' in model['id']]
    return embedding_model_ids

## only "whisper-1" is available for audio related work
## modify the code if other models released
def list_audio_model_ids():
    return ["whisper-1"]

def retritve_model(model_id: str):
    return openai.Model.retrieve(model)

def change_default_model(model: str):
    model_ids = list_model_ids()
    if model in model_ids:
        defulat_model = model
        return True
    else:
        return False

def change_default_audio_model(model: str):
    model_ids = list_audio_model_ids()
    if model in model_ids:
        defulat_audio_model = model
        return True
    else:
        return False

## only for "orgnization"
def list_orgnization_files():
    return openai.File.list().data

## valid purpose: "fine-tune"
def upload_orgnization_file(file:str, purpose:str):
    return openai.File.create(file=file, purpose=purpose)  

def delete_orgnization_file(file_id:str):
    return openai.File.delete(file_id)

def retrieve_orgnization_file(file_id:str):
    return openai.File.retrieve(file_id)

def receive_orgnization_file_content(file_id:str):
    content = openai.File.download(file_id)
    return content

## fine tune
## 用于微调
## Data Formatting
## https://platform.openai.com/docs/guides/fine-tuning/data-formatting
## Token limits for GPT-3 (instrcut models: ada, babbage, curie, davinci) = 2049 tokens
## https://platform.openai.com/docs/models/gpt-3
def create_fine_tune(file_id, validation_file_id=None, model=None, n_epochs=None,
        batch_size=None, learning_rate_multiplier=None, prompt_loss_weight=None,
        compute_classification_metrics=None, classification_n_classes=None,
        classification_positive_class=None, classification_betas=None,
        suffix=None):

    params = {"training_file": file_id}
    if validation_file_id:
        params["validation_file"] = validation_file_id
        
    if model:
        params["model"] = model
        
    if n_epochs is not None:
        params["n_epochs"] = n_epochs
        
    if batch_size is not None:
        params["batch_size"] = batch_size
        
    if learning_rate_multiplier is not None:
        params["learning_rate_multiplier"] = learning_rate_multiplier
        
    if prompt_loss_weight is not None:
        params["prompt_loss_weight"] = prompt_loss_weight
        
    if compute_classification_metrics is not None:
        params["compute_classification_metrics"] = compute_classification_metrics
        
    if classification_n_classes is not None:
        params["classification_n_classes"] = classification_n_classes
        
    if classification_positive_class is not None:
        params["classification_positive_class"] = classification_positive_class
        
    if classification_betas is not None:
        params["classification_betas"] = classification_betas
        
    if suffix:
        params["suffix"] = suffix

    return openai.FineTune.create(**params)


def list_fine_tunes():
    fine_tunes = openai.FineTune.list().data
    return fine_tunes

def list_fine_tune_events(fine_tune_id):
    fine_tune_events = openai.FineTune.list_events(fine_tune_id).data
    return fine_tune_events

def retrieve_fine_tune_model(fine_tune_id):
    fine_tune_model = openai.FineTune.retrieve(fine_tune_id)
    return fine_tune_model

def retrieve_fine_tune_model_config(fine_tune_id):
    fine_tune_model = retrieve_fine_tune_model(fine_tune_id)
    return fine_tune_model

def cancel_fine_tune(fine_tune_id):
    return openai.FineTune.cancel(fine_tune_id)

## fine_tune_model example: curie:ft-acmeco-2021-03-03-21-44-20
def delete_fine_tune_model(model):
    return openai.Model.delete(model)

prompt = "Classify whether the following input text is asking for chat or asking for AI-generated Image:"
def clarify_message(message: str):

    # Define the OpenAI API parameters
    parameters = {
        "prompt": prompt,
        "temperature": 0.5,
        "max_tokens": 1,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }

    # Call the OpenAI API to generate a response
    response = openai.Completion.create(
        engine=default_text_model,
        prompt=prompt+message,
        max_tokens=100
    )

    # Extract the generated text
    model_output = response.choices[0].text.strip()
    clarified_type = None
    # Determine if the input text was classified as a "chat" or "image" message
    if "chat" in model_output.lower():
        clarified_type = "chat"
    elif "image" in model_output.lower():
        clarified_type = "image"
    else: ## unexcepted result
        clarified_type = model_output
    return clarified_type

def response_to_user(message: str, temperature: float):

    ##for test
    print("response_to_user called with message:", message, "and temperature:", temperature)
    clarified_type = clarify_message(message)
    ## return response:str as text if it is a chat
    ## return response:str as url if it is a image
    if clarified_type == "chat":
        response = create_chat_completion(content=message, temperature=temperature)## shallow copy
        return response
    elif clarified_type == "image":
        response = create_image(prompt=message)
        return response

##客服接口 发送图片消息
def send_image(prompt: str, user_id: str):
    access_token = accesstoken.get_current_access_token()  # 获取 access_token
    """
    image_url = create_image(prompt=prompt)
    filepath = imageutils.url_to_image(url=image_url)
    print("image created.")
    media_id = imageutils.upload_image(access_token, filepath)
    """
    url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=' + access_token
    headers = {'content-type': 'application/json', 'charset': 'utf-8'}
    """
    data = {
        'touser': user_id,
        'msgtype': 'image',
        'image': {
        'media_id': media_id
        }
    }
        """
    data = {
        'touser': user_id,
        'msgtype': 'text',
        "text": {
            'content': "test"
        }
    }
    print(data)
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print('图片已发送！')
    else:
        print('发送失败！')
## for testing
def get_default_model():
    return default_model

def get_default_audio_model():
    return default_audio_model

def get_all_orgnization_file_ids():
    file_list = list_orgnization_files()
    file_ids = [file_dict['id'] for file_dict in file_list]
    return file_ids

def delete_all_orgnization_files():
    file_ids = get_all_orgnization_file_ids()
    for file_id in file_ids:
        delete_orgnization_file(file_id)
    return True

def get_all_fine_tune_models():
    model_list = list_fine_tunes()
    models = [model_dict["fine_tuned_model"] for model_dict in model_list]
    return models

def delete_all_fine_tune_models():
    models = get_all_fine_tune_models()
    for model in models:
        delete_fine_tune_model(model)
    return True

def func1():
    print("func1")
    t = threading.Thread(target=func2)
    t.start()
    print("func1")
    # create and start a new thread to run func2

def func2():
    time.sleep(10)
    print("func2")

if __name__ == "__main__":
    print(response_to_user("test", 0.8))
