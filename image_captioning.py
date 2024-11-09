import cv2
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

def capture_image():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        img_path = "captured_image.jpg"
        cv2.imwrite(img_path, frame)
        cam.release()
        return img_path
    else:
        cam.release()
        raise Exception("Failed to capture image.")

def describe_scene(image_path):
    # Load processor and model
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    
    # Load and process the image
    image = Image.open(image_path).convert("RGB")
    
    # Generate description with padding enabled
    inputs = processor(images=image, return_tensors="pt", padding=True)
    out = model.generate(**inputs)
    
    # Decode the output
    description = processor.decode(out[0], skip_special_tokens=True)
    return description
