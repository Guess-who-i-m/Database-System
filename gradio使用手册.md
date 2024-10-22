# gradio使用手册
## 使用之前
首先安装gradio包
```bash
pip install gradio
```

## 快速入门
gradio可以包装任何python函数成为易于使用的用户界面。
```python
demo = gr.Interface(
    fn=<要用来展示的函数>,
    inputs=<输入的gradio组件类型，数量需要和函数的输入值数量匹配>,
    outputs=<输出的gradio组件类型，数量需要和函数的返回值数量匹配>
)
```

输入可以是以下类型之一:
- gr.inputs.Text：文本输入
- gr.inputs.Image：图像输入
- gr.inputs.Number：数字输入
- gr.inputs.Dataframe：数据框输入
- 等等

输出也可以是以下类型之一：
- gr.outputs.Text：文本输出
- gr.outputs.Image：图像输出
- gr.outputs.Number：数字输出
- gr.outputs.Label：标签输出

下面是一个最简单的使用案例
```python
input_text = gr.input.Text()    # 这是一个类
output_text = gr.output.Text()

def predict_function(input_text):
    # 一堆函数处理逻辑
    return f"你输入的时{input_text}"

# 将处理函数与gradio接口相连
demo = gr.Interface(
    fn = predict_function,
    inputs = input_text,
    outputs = output_text
)

demo.launch
```



## 