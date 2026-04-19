import gradio as gr
from self_correct import run_with_correction

def query_handler(user_query: str):
    if not user_query.strip():
        return "Please enter a question.", gr.update(visible=False)

    result = run_with_correction(user_query)

    if result["success"]:
        sql_display = f"```sql\n{result['sql']}\n```\n_(resolved in {result['attempts']} attempt(s))_"
        headers = result["columns"]
        rows = [list(r) for r in result["rows"]]
        table_data = [headers] + rows if rows else [headers]
        return sql_display, gr.update(value=table_data, visible=True)
    else:
        error_msg = f"Failed after {result['attempts']} attempts.\n\nLast error: {result['error']}"
        return error_msg, gr.update(visible=False)

with gr.Blocks(title="Text-to-SQL Agent") as demo:
    gr.Markdown("# Text-to-SQL Agent\nPowered by Gemini 2.5 Flash")
    with gr.Row():
        query_input = gr.Textbox(
            label="Ask a question about your data",
            placeholder="e.g. Show me the top 5 customers by total order value",
            lines=2,
        )
    submit_btn = gr.Button("Run Query", variant="primary")
    sql_output = gr.Markdown(label="Generated SQL")
    table_output = gr.Dataframe(label="Results", visible=False, wrap=True)

    submit_btn.click(
        fn=query_handler,
        inputs=[query_input],
        outputs=[sql_output, table_output],
    )

demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
