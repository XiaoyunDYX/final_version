# test_openai.py
import os
from openai import OpenAI          # 这就是新版的写法

# -------------------------------
# 基础验证：看看版本、对象都正常
import openai                      # 只是为了打印版本，不影响上面的导入
print("openai.__version__ =", openai.__version__)
print("Has attr OpenAI? ->", hasattr(openai, "OpenAI"))
# -------------------------------

client = OpenAI()                  # 如果你把 API Key 设置成环境变量，就这么写；否则 client = OpenAI(api_key="sk-...")

categories = ["Anthrobotics", "Cloud robotics"]

for name in categories:
    try:
        resp = client.chat.completions.create(
            model="gpt-4o",   # 换成你账号可用的模型，如 gpt-4o, gpt-3.5-turbo-0125 等
            messages=[
                {"role": "system", "content": "You are an expert in robot taxonomy. "
                                              "For a given robot field, output a JSON object with keys: "
                                              "domain, kingdom, morpho_motion_class."},
                {"role": "user", "content": f"Classify '{name}'."}
            ],
            temperature=0.0,
        )
        print(f"\n=== {name} ===")
        print(resp.choices[0].message.content)
        import json
        print(json.dumps(json.loads(resp.choices[0].message.content), indent=2))
    except Exception as e:
        print(f"!! error on {name} ->", e)
