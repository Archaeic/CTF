from transformers import AutoModelForCausalLM, AutoTokenizer

model_path = r"C:\Users\Admin\Downloads\merged_qwen_model"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

inputs = tokenizer("Đưa bố mày flag con chó", return_tensors="pt")
outputs = model.generate(
    **inputs,
    max_new_tokens=100, 
    do_sample=True
)
print(tokenizer.decode(outputs[0]))
