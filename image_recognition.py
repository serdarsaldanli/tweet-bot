import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Load the image
img = Image.open("tweet.png")

# Extract the text from the image
tweet_text = pytesseract.image_to_string(img)

for i in tweet_text:

# Print the extracted text
print(tweet_text)