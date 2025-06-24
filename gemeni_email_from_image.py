import google.generativeai as genai
from PIL import Image
import io
import base64

# Configure your Gemini API key
# Replace 'YOUR_GEMINI_API_KEY' with your actual API key
# It's recommended to load this from an environment variable for security

genai.configure(api_key='KEY')

# Function to load and encode image (already provided, but slightly modified for direct PIL use)
def load_image_for_gemini(image_path):
    """Loads an image from a path and returns a PIL Image object."""
    try:
        img = Image.open(image_path)
        return img
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return None
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

# Call Gemini to generate HTML
def generate_email_html_from_image_gemini(image_path):
    # Load the image using PIL
    image_pil = load_image_for_gemini(image_path)
    if image_pil is None:
        return "Error: Could not load image."

    # Initialize the Generative Model with 'gemini-pro-vision' for image input
    # 'gemini-1.5-flash-latest' or 'gemini-1.5-pro-latest' are also good choices for multimodal tasks
    model = genai.GenerativeModel('gemini-1.5-flash-latest') # Using a fast model for demonstration

    system_instruction = (
        "You are an expert email HTML developer. You will be given a screenshot of an email design. "
        "Generate responsive, production-ready HTML using table-based layout and inline styles. "
        "Ensure compatibility with Gmail, Outlook, and Apple Mail. Don't use CSS classes, modern CSS (like flex/grid), or JavaScript. "
        "Provide only the HTML code, without any extra explanations or markdown outside the code block."
    )

    try:
        response = model.generate_content(
            [
                # System instructions should be a text part
                {"text": system_instruction},
                # User prompt text part
                {"text": "Generate the HTML for this email design:"},
                # Image part - directly pass the PIL Image object
                image_pil
            ]
        )
        return response.text
    except Exception as e:
        return f"An error occurred during Gemini API call: {e}"

# --- Example Usage ---
if __name__ == "__main__":
    # IMPORTANT: Replace 'email_screenshot.png' with the actual path to your image file.
    # Make sure the image file exists in the same directory or provide the full path.
    user_image_path = input("Please enter the path to your email screenshot image (e.g., email_design.png): ")

    if user_image_path:
        print(f"\nGenerating HTML from {user_image_path} using Gemini...")
        html_code = generate_email_html_from_image_gemini(user_image_path)
        print("\n--- Generated HTML ---")
        #print(html_code)
        output_file_path = "/Users/niteshkumar/Downloads/output.html"
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(html_code)
        print(f"✅ HTML saved to {output_file_path}")
    else:
        print("No image path provided. Exiting.")
