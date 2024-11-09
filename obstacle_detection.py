from PIL import Image
import torch

def provide_supportive_guidance(image_path):
    # Load YOLO model
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    
    # Load and analyze the image
    image = Image.open(image_path)
    results = model(image)
    
    # Retrieve detected objects and positions
    detections = results.pandas().xyxy[0]  # DataFrame of detections
    object_counts = detections['name'].value_counts().to_dict()
    
    # Environment description
    if "person" in object_counts and object_counts["person"] > 5:
        environment_desc = "You are in a crowded area with several people around."
    elif "car" in object_counts or "bus" in object_counts:
        environment_desc = "You are near a street with vehicles present."
    else:
        environment_desc = "This appears to be a quieter environment with few objects around."
    
    # Summarize detected objects
    object_summary = ", ".join([f"{count} {obj}(s)" for obj, count in object_counts.items()])
    guidance = f"{environment_desc}\n\nThere are {object_summary} in view.\n"
    
    # Split image into regions and count objects in each
    image_width, _ = image.size
    left_region = image_width * 0.33
    right_region = image_width * 0.66
    
    left_count = detections[detections['xmax'] <= left_region].shape[0]
    center_count = detections[(detections['xmax'] > left_region) & (detections['xmax'] <= right_region)].shape[0]
    right_count = detections[detections['xmax'] > right_region].shape[0]
    
    # Determine the best path based on obstacle counts
    if left_count < center_count and left_count < right_count:
        path_suggestion = "The left side seems the clearest. Moving to the left may be safest."
    elif right_count < center_count and right_count < left_count:
        path_suggestion = "The right side appears to be the clearest. Moving to the right is recommended."
    elif center_count < left_count and center_count < right_count:
        path_suggestion = "You may proceed straight as the path forward seems the clearest."
    else:
        path_suggestion = "Please proceed with caution, as there are obstacles on all sides."
    
    guidance += f"{path_suggestion}\n"
    
    # Additional movement suggestions based on detected objects
    if "car" in object_counts or "bus" in object_counts:
        guidance += "Be cautious of nearby vehicles.\n"
    elif "person" in object_counts:
        if object_counts["person"] <= 3:
            guidance += "A few people are nearby. You may proceed forward with caution.\n"
        else:
            guidance += "There are several people in your path. Move carefully and consider a slower pace.\n"
    else:
        guidance += "The way ahead appears clear. You may proceed forward.\n"
    
    return guidance
