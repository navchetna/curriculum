import torch
import string
from transformers import BertTokenizer, BertForMaskedLM
import time


class text_autocomplete():
    def __init__(self) -> None:
        self.bert_tokenizer = BertTokenizer.from_pretrained("bert-base-uncased", cache_dir="my_models/")
        self.bert_model = BertForMaskedLM.from_pretrained("bert-base-uncased", cache_dir="my_models/").eval()
        
    
    def decode(self, tokenizer, pred_idx, top_clean):
        ignore_tokens = string.punctuation + "[PAD]"
        tokens = []
        for w in pred_idx:
            token = "".join(tokenizer.decode(w).split())
            if token not in ignore_tokens:
                tokens.append(token.replace("##", ""))
        return "\n".join(tokens[:top_clean])

    def encode(self, tokenizer, text_sentence, add_special_tokens=True):
        text_sentence = text_sentence.replace("<mask>", tokenizer.mask_token)
        # if <mask> is the last token, append a "." so that models dont predict punctuation.
        if tokenizer.mask_token == text_sentence.split()[-1]:
            text_sentence += " ."

            input_ids = torch.tensor(
                [tokenizer.encode(text_sentence, add_special_tokens=add_special_tokens)]
            )
            mask_idx = torch.where(input_ids == tokenizer.mask_token_id)[1].tolist()[0]
        return input_ids, mask_idx

    def get_all_predictions(self, text_sentence, top_clean=5):
        # ========================= BERT =================================
        input_ids, mask_idx = self.encode(self.bert_tokenizer, text_sentence)
        start = time.time()
        with torch.no_grad():
            predict = self.bert_model(input_ids)[0]
        bert = self.decode(
            self.bert_tokenizer, predict[0, mask_idx, :].topk(top_clean).indices.tolist(), top_clean
        )
        total_time = time.time() - start
        print("Total Time Taken : ", total_time)
        return {"Predictions": bert}


    def get_prediction(self, input_text, top_k):
        try:
            input_text += " <mask>"
            res = self.get_all_predictions(input_text, top_clean=top_k)
            return res
        except Exception as error:
            print("ERROR : ", error)