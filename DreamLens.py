import gradio as gr
import requests
from volcengine import visual
from volcengine.visual.VisualService import VisualService
from volcenginesdkarkruntime import Ark

# Initialize VisualService and Ark client
visual_service = VisualService()
client = Ark(api_key="bc5ae3d3-3423-488a-87e9-8e02d56de50e")

# Set Access Key and Secret Key for VisualService (replace with your credentials)
visual_service.set_ak('AKLTNTY3NDgyMmViNTFmNGIzMThmNWY5MGViMDk1Y2IwNTg')
visual_service.set_sk('TVdGaFl6RmlaVEl4WmprMU5EazJNRGxoTURZMlpXUTVOV05sTTJRMk9XSQ==')

# Additional prompt and dream interpretation instructions
additional_prompt = '''
Please generate a single, concise image generation instruction focused on capturing a visually striking, static scene based on the input text. The output should meet the following requirements:

1. Scene Extraction and Simplification: Identify and isolate only one primary, vivid, and visually descriptive moment or scene from the input text. Ensure this selected scene is self-contained and can be visually represented without any need for dialogue or continuity in action.

2. Avoid First-Person References: If the input text includes first-person pronouns like "I" or "my," convert these into third-person descriptors to maintain clarity for the image generation model. For example, change "I am standing in a field" to "A person stands in a field."

3. Focus on Scene and Static Details: Provide a detailed description emphasizing the setting, lighting, character poses, attire, and any other static elements. Avoid any description that suggests movement, dialogue, or a sequence of actions. This includes:
   Scene Details: Describe the environment, lighting, and any static background elements.
   Character Details: Specify the character's attire, facing direction, and posture (e.g., "sitting," "standing with arms crossed") without any hint of continuous action.

4. No Dialogues or Dynamic Descriptions: Ensure the prompt does not contain any dialogue or dynamic elements. The description should strictly represent a single, frozen moment in time.

5. Detailed Visual Descriptions: Include specific details about the main objects, characters, background, light, and emotional tone, enabling the image generation model to accurately capture the scene’s intended look and feel.

6. Emotion and Atmosphere: If the scene conveys a particular emotion or atmosphere (e.g., “lonely,” “peaceful,” “tense”), use precise words to reflect this. For example, a desolate scene might use "lonely" or "bleak" to describe the mood.

7. Single, Cohesive Description: Provide a single, complete, and cohesive description that fully represents the selected scene, focusing on visual clarity and descriptive accuracy without extraneous information. For instance:
   "A solitary figure stands on a grassy hill under a dark, overcast sky, looking out toward the distant mountains. The person wears a long, hooded cloak, and the wind blows softly, ruffling the cloak around them. The atmosphere is somber, with muted colors and a soft, diffused light casting a grayish tone over the landscape."

This prompt should ensure the generated image precisely matches the selected scene, providing a vivid and clear representation based on the description alone.
'''

dream_prompt = '''
You are a compassionate and skilled psychological counselor. Please interpret the following dream with warmth and empathy, focusing on uncovering the emotions and meanings embedded in the dream without offering specific guidance, suggestions, or real-life advice.
Dream description: {dream_text}

1. Begin by identifying any emotions that may be hidden within the dream, paying attention to the setting, symbols, and any recurring themes. Explain how these elements might connect to the dreamer's subconscious feelings or real-life concerns, but do not extend beyond the scope of interpretation into practical suggestions or advice.

2. If there are symbolic elements in the dream, such as objects, people, or places, gently interpret what these symbols might represent in the dreamer's life or inner world, while keeping the focus solely on understanding rather than resolving or advising.

Please ensure that the interpretation remains a descriptive, empathetic analysis of the dream content without providing any form of guidance or life advice. Maintain a caring, understanding, and supportive tone to help the user gain insight into the dream's meaning without suggesting further action.
'''

personalguidance_prompt = '''
You are a compassionate and experienced psychological counselor. Please interpret the following dream with a warm, empathetic approach, and provide specific, actionable guidance for how the dreamer might address their subconscious feelings in daily life.
Dream description: {personalguide_text}

1. Make specific suggestions on emotion management, help users identify emotional triggers, and provide simple emotion management methods.

2. Put forward specific suggestions for exploring potential self-expectations, help users think about their real-life needs and values, and put forward some small real-life goals, and gradually approach the life state that they desire in their hearts.

3. Provide 2-3 specific real-life action suggestions, such as emotion management, life goal setting, or health advice, based on the dream theme, to help users make tangible improvements in their daily lives.

Please ensure that your interpretation and guidance are compassionate, easy to understand, and supportive, helping the dreamer feel emotionally understood, clear-minded, and motivated toward positive action.
'''

# System content for generating image prompts
system_content_prompt = "Generate English prompts only. You are a professional prompt generator. " + additional_prompt

# System content for generating psychological interpretation of dreams in Chinese
system_content_analysis = "You are a psychologist. Please provide a psychological interpretation of the user's dream in Chinese based on common dream analysis theories, using clear and concise language." + dream_prompt

# System content for generating real-life guidance in Chinese with emotional warmth and natural paragraph format
system_content_personalguidance = "You are a psychologist. Please provide practical, real-life suggestions in Chinese based on the user's dreams to help the user reflect on their inner emotions and potential needs. Avoid using symbols or lists, and use a natural, emotional, and caring tone." + personalguidance_prompt 

# Function to generate prompt, analysis, and guidance, and to fetch generated image URL
def generate_prompt(dream_description):
    # Call model to generate image prompt
    prompt_completion = client.chat.completions.create(
        model="ep-20241011190041-vm752",
        messages=[
            {"role": "system", "content": system_content_prompt},
            {"role": "user", "content": dream_description}
        ]
    )
    prompt_result = str(prompt_completion.choices[0].message.content)
    print(prompt_result)
    return prompt_result

def generate_analysis(dream_description):
    # Call model to generate dream analysis
    analysis_completion = client.chat.completions.create(
        model="ep-20241011190041-vm752",
        messages=[
            {"role": "system", "content": system_content_analysis},
            {"role": "user", "content": dream_description}
        ]
    )
    analysis_result = analysis_completion.choices[0].message.content
    return analysis_result

def generate_guidance(dream_description):
    # Call model to generate personal guidance
    personalguidance_completion = client.chat.completions.create(
        model="ep-20241011190041-vm752",
        messages=[
            {"role": "system", "content": system_content_personalguidance},
            {"role": "user", "content": dream_description}
        ]
    )
    personalguidance_result = personalguidance_completion.choices[0].message.content
    return personalguidance_result

def generate_image(prompt_result):
    # Define the parameters for image generation
    print('call prompt result'+prompt_result)
    form = {
        "req_key": "high_aes_general_v20_L",
        "prompt": prompt_result,
        "model_version": "general_v2.0_L",
        "req_schedule_conf": "general_v20_9B_rephraser",
        "seed": -1,
        "scale": 3.5,
        "ddim_steps": 16,
        "width": 512,
        "height": 512,
        "use_sr": True,
        "return_url": True,
    }

    # Generate image using VisualService
    resp = visual_service.cv_process(form)
    image_url = resp['data']['image_urls'][0]

    # Download image from URL
    image_data = requests.get(image_url).content
    image_path = 'generated_image.jpg'
    with open(image_path, 'wb') as file:
        file.write(image_data)
    return image_path

# Create Gradio interface
def main():
    with gr.Blocks() as demo:
        gr.Markdown("### Dream Analysis and Image Generation")

        # Input box for user to enter dream description
        dream_input = gr.Textbox(label="Describe your dream", placeholder="Enter your dream description here...", lines=5)

        # Output boxes to display generated prompt, psychological analysis, and personal guidance
        prompt_output = gr.Textbox(label="Generated Image Prompt")
        analysis_output = gr.Textbox(label="Dream Analysis")
        personalguidance_output = gr.Textbox(label="Personal Guidance")

        # Image output to display generated image
        image_output = gr.Image(label="Generated Image")

        # Step 1: Generate prompt
        step_1_button = gr.Button("Generate Image Prompt")
        step_1_button.click(generate_prompt, inputs=[dream_input], outputs=[prompt_output])

        # Step 2: Generate dream analysis
        step_2_button = gr.Button("Generate Dream Analysis")
        step_2_button.click(generate_analysis, inputs=[dream_input], outputs=[analysis_output])

        # Step 3: Generate personal guidance
        step_3_button = gr.Button("Generate Personal Guidance")
        step_3_button.click(generate_guidance, inputs=[dream_input], outputs=[personalguidance_output])

        # Step 4: Generate Image
        step_4_button = gr.Button("Generate Image")
        step_4_button.click(generate_image, inputs=[prompt_output], outputs=[image_output])

    demo.launch(debug=True,share=True)

if __name__ == "__main__":
    main()
