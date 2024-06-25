from pydantic import BaseModel
from transformers import BertTokenizer, BertModel
import torch

class ApiBertRequest(BaseModel):
    text: str

# モデルとトークナイザーのロード
#tokenizer = BertTokenizer.from_pretrained('cl-tohoku/bert-base-japanese-v2')
#model = BertModel.from_pretrained('cl-tohoku/bert-base-japanese-v2')
tokenizer = BertTokenizer.from_pretrained('sonoisa/sentence-bert-base-ja-mean-tokens')
model = BertModel.from_pretrained('sonoisa/sentence-bert-base-ja-mean-tokens')

def handle(request: ApiBertRequest):
    text = request.text

    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    try:
        vector = vectorize_text(text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"vector": vector}

def vectorize_text(text: str):
    # テキストをトークン化
    inputs = tokenizer(text,
        return_tensors='pt',
        max_length=512,
        padding="max_length",
        truncation=True,
    )

    # モデルを使ってテキストをベクトル化
    with torch.no_grad():
        outputs = model(**inputs)
        last_hidden_state = outputs.last_hidden_state
        cls_embedding = last_hidden_state[:, 0, :].squeeze().tolist()

    return cls_embedding