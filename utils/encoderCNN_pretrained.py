from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights
from torchvision.io.image import read_image
from torch import nn
from PIL import Image


class EncoderCNN(nn.Module):
    """
    Encoder inputs images and returns features, their boxes and embeddings.
    """
    
    def __init__(self):
        super(EncoderCNN, self).__init__()
        
        self.weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
        
        self.model = fasterrcnn_resnet50_fpn_v2(weights=self.weights, pretrained=True) 
        
        self.model.eval()
        
        self.coco_instances = ['__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 
                          'fire hydrant', 'N/A', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 
                          'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 
                          'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 
                          'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 
                          'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table', 'N/A', 'N/A', 'toilet', 
                          'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 
                          'N/A', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']

                
    def get_prediction(self, image, threshold):
        """
        get_prediction
            parameters:
            - image - the actual raw image read from the torchvision 'read_image' function
            - threshold - threshold value for prediction score
            method:
            - Image is obtained from the image path
            - the image is converted to image tensor using PyTorch's Transforms
            - image is passed through the model to get the predictions
            - class, box coordinates are obtained, but only prediction score > threshold are chosen.
        
            returns: 
                -
        """
        transform = self.weights.transforms()
        img = transform(image)
        pred = self.model([img])
        pred_class = pred[0]['labels']
        pred_boxes = pred[0]['boxes'].detach()
        pred_score = list(pred[0]['scores'].detach().numpy())
        pred_t = [pred_score.index(x) for x in pred_score if x>threshold][-1]
        pred_boxes = pred_boxes[:pred_t+1]
        pred_score = pred_score[:pred_t+1]
        
        return  img, pred_boxes, pred_score, self.weights

   