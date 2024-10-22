# import gradio as gr

# def page1_function(input_text):
#     return f"这是页面 1，你输入了: {input_text}"

# def page1_function1(input_text):
#     return f"这是页面 1-1，你输入了: {input_text}"

# def page2_function(input_text):
#     return f"这是页面 2，你输入了: {input_text}"

# def page3_function(input_text):
#     return f"这是页面 3，你输入了: {input_text}"

# # 使用 Blocks 来构建多个页面
# with gr.Blocks() as demo:
#     # 创建 Tabs 组件
#     with gr.Tabs():
#         # 第一个页面
#         with gr.Tab("页面 1"):
#             # 添加页面描述
#             gr.Markdown("### 这是页面 1 的描述\n 请在下方输入内容并点击提交。")
#             input_text1 = gr.Textbox(label="输入文本")
#             output1 = gr.Textbox(label="输出")
#             button1 = gr.Button("提交")
#             button1.click(page1_function, inputs=input_text1, outputs=output1)

#             gr.Markdown("### 这是页面 1-1 的描述\n 输入数字并点击提交。")
#             input_text2 = gr.Textbox(label="输入数字")
#             output2 = gr.Textbox(label="输出2")
#             button2 = gr.Button("提交")
#             button2.click(page1_function1, inputs=input_text2, outputs=output2)
        
#         # 第二个页面
#         with gr.Tab("页面 2"):
#             gr.Markdown("### 这是页面 2 的描述\n 请在下方输入内容并点击提交。")
#             input_text2 = gr.Textbox(label="输入文本")
#             output2 = gr.Textbox(label="输出")
#             button2 = gr.Button("提交")
#             button2.click(page2_function, inputs=input_text2, outputs=output2)
        
#         # 第三个页面
#         with gr.Tab("页面 3"):
#             gr.Markdown("### 这是页面 3 的描述\n 请输入文本并提交。")
#             input_text3 = gr.Textbox(label="输入文本")
#             output3 = gr.Textbox(label="输出")
#             button3 = gr.Button("提交")
#             button3.click(page3_function, inputs=input_text3, outputs=output3)

# # 运行 Gradio 应用
# demo.launch()



import gradio as gr

# 定义函数
def greet1(name, age):
    return f"你好 {name}, 你看起来 {age} 岁！"

def greet2(name, age):
    return f"你好 {name}, 你看起来 {age} 岁！"

def farewell1(name):
    return f"再见 {name}, 希望很快再见到你！"

def farewell2(name):
    return f"再见 {name}, 希望很快再见到你！"

# 使用 Blocks 来构建多个页面
with gr.Blocks() as demo:
    
    # 添加全局居中的标题
    gr.Markdown(
        """<div style='text-align: center; font-size: 24px; font-weight: bold;'>
        这是一个大标题，显示在所有标签页上方
        </div>"""
    )
    
    # 创建 Tabs 组件
    with gr.Tabs():
        # 第一个页面 - 欢迎界面
        with gr.Tab("欢迎页面"):
            gr.Markdown("### 欢迎来到这个页面")
            interface1 = gr.Interface(
                fn=greet1,
                inputs=["text", "slider"],
                outputs="text",
                title="欢迎来到gradio",
                description="输入你的名字和年龄，我们会给你一个问候"
            )
            # interface1.render()  # 在当前选项卡中渲染接口

        # 第二个页面 - 再见界面
        with gr.Tab("再见页面"):
            gr.Markdown("### 这是再见页面")
            interface2 = gr.Interface(
                fn=farewell1,
                inputs="text",
                outputs="text",
                title="告别界面",
                description="输入你的名字，我们会和你道别"
            )
            # interface2.render()  # 在当前选项卡中渲染另一个接口

# 运行 Gradio 应用
demo.launch()
