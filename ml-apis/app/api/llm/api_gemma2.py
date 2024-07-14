from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
import torch
import os


class ApiGemma2Request(BaseModel):
    text: str

model_name='google/gemma-2-9b'
access_token = os.getenv("HF_ACCESS_TOKEN", "")
if access_token:
    login(token=access_token)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        torch_dtype=torch.bfloat16
    )

def handle(request: ApiGemma2Request):
    text = request.text

    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    try:
        result_text = process_text(text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"out_text": result_text}

def process_text(text: str) -> str:
    # テキストをトークン化
    input_ids = tokenizer(text, return_tensors="pt")
    # モデルを使ってテキストを生成
    outputs = model.generate(**input_ids,
        max_length=200,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        repetition_penalty=1.2,
        do_sample=False,
        #temperature=1.0,
    )
    result_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f'input:[{text}] output:[{result_text}]', flush=True)
    return result_text