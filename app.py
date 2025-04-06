from google import genai
from google.genai import types
import gradio as gr
import pathlib

api_file = open("api.txt", "r")
api_key = api_file.readline()
api_file.close()
client = genai.Client(api_key=api_key)

def process(input, files):
    try:
        pretense = """
            Create a schedule for a student given the syllabi of their classes and additional information. 
            If not corrected, assume that the school follows a semester format.
            Assume that the student does not have any other obligations aside from the information in the syllabi and the additional information.
            Allocate time to complete assignments and projects as well as regularly study for exams that are mentioned in the given syllabi.
            Provide two outputs: text describing the schedule and an .ics file with events scheduled for each assignment/project/exam mentioned in the syllabi.
        """
        if not files:
            return "Please upload a syllabus"
        
        context = [pretense]
        print(input)
        if input:
            context.append(input)

        # Handle file uploads properly
        for file in files:
            file_path = pathlib.Path(file)
            context.append(types.Part.from_bytes(data=file_path.read_bytes(), mime_type="application/pdf"))

        response = client.models.generate_content(
            model="gemini-1.5-pro", contents=context
        )

        return response.text
    except:
        return "An error occurred. Please try again."

with gr.Blocks() as demo:
    gr.Markdown("""# Get your FirstWeek""")
    files = gr.File(file_count="multiple", label="Upload Syllabi", file_types=[".pdf"])
    prompt = gr.Textbox(label="Additional Information")
    submit_btn = gr.Button("Get Schedule")
    output = gr.Textbox(label="Your Schedule")
    submit_btn.click(fn=process, inputs=[prompt, files], outputs=output)

demo.launch()
