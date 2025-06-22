# Anti-Spoofing Detector Model for Facial Recognition System (May 2024 - Jul 2024)
*"The best way to enhance security is through facial recognition."*
____________________________________________________________________________________________________________________________________________________________________________________________________

# Project Overview
Anti-spoofing techniques aim to differentiate between live (genuine) and fake (spoofed) facial inputs. The development of robust anti-spoofing detectors is vital for the security and efficacy of facial 
recognition systems. By preventing unauthorized access and reducing false acceptance rates, these systems can achieve higher reliability and usertrust. Enhanced anti-spoofing measures ensure that facial 
recognition technology can be safely deployed in sensitive and high-security environments, such as financial institutions, government facilities, and personal devices. The domain of anti-spoofing in facial 
recognition encompasses the intersection of computer vision, machine learning, and cybersecurity. It addresses critical challenges posed by spoofing attacks, aiming to fortify facial recognition systems 
against fraudulent activities and ensure secure and reliable biometric authentication.
____________________________________________________________________________________________________________________________________________________________________________________________________

# Project Goal 
This project aims to develop a robust, deep learning-based anti-spoofing detector to enhance the security of facial recognition systems. By leveraging YOLOv8 and OpenCV, the model:

- Accurately distinguishes between live faces and spoofing attempts (e.g., printed photos, digital screens, or masks).

- Reduces false acceptance rates (FAR) and prevents unauthorized access in high-security environments (e.g., banking, government, or personal devices).

- Achieves >99% accuracy while ensuring seamless integration with existing facial recognition pipelines.

**Key Objectives**

1. Improve biometric security by detecting sophisticated spoofing attacks.

2. Optimize real-time performance for practical deployment.

3. Maintain user convenience without compromising authentication rigor.
 
# Installation and Set-up
## Dependencies
Check it out before any further procedure -> [requirements](https://github.com/Uttarayan002/Anti-Spoofing-Detector-for-Facial-Recognition-System/blob/main/requirement.txt.txt)

## Python Packages Used
There are few tools that needed to be installed before proceeding.                                                                                                                                              
Install the latest version of 'python' which is 3.12.0.                                                                                                                                                
Tools/Libraries:                                                                                                                                                                                                
- cvzone: `pip install cvzone`                                                                                                                                                                           
- face_recognition: `pip install face-recognition`
- tkinter: `pip install tk`                                                                                                                                                                                  -
- cv2: `pip install opencv-python`
________________________________________________________________________________________________________________________________________________________________________________
# Data 
We collected our own Datasets for this project.
**Source Data**
Relevant Data are collected by generated specific scripts which eventually leads to automate the data collection and labelling process. It is recommended to everyone if you are using real world applications use your own datasets in your own environment. Collect from different human being with various face shapes & structures, distinct outfits and different places. All you need a few and solid lines of script aand  webcam.ive person.
                                                                                                                       
Folders: python data/data_collection.py and python data/data.yaml
________________________________________________________________________________________________________________________________________________________________________________

# Results and evaluation                                                                                                                                     
Evaluation/Inference:                                                                                                                                                                                     Test the model:  `python yolo_test.py`

## Results
Achieved *high model accuracy* by epoch 3, demonstrating strong early convergence.

| Metric        | Achieve       |
| ------------- | ------------- |
| Precision     | 0.99458       |
| Recall        | 0.999         |
| mAP           | 0.99192       |

![confusion_matrix](https://github.com/user-attachments/assets/b67b1bb3-16a8-4c91-b86e-fcc2295636e7)

## How it will WORK!!
![spoof detection (real)](https://github.com/user-attachments/assets/23fc3856-8b15-4e5d-9618-13ae1e832839) ![spoof detection (fake)2](https://github.com/user-attachments/assets/72302ee0-8b1b-421b-8504-ff39a76b6284)
________________________________________________________________________________________________________________________________________________________________________________

# Future Work 
- Although this project aims to differentiate between liveliness and the spooked detection, which helps to secure any authentic data from the third party or unknown sources.
- We also aim to leverage by integrate with the cloud computing which helps in the real time production level, or industrial level.

# License
[MIT](https://github.com/Uttarayan002/Anti-Spoofing-Detector-for-Facial-Recognition-System?tab=MIT-1-ov-file)

# Contributor
Rik Singha Mahapatra
Sanu Manna

## Note
This project was originally completed in July 2024 as part of our core course.
I uploaded it to GitHub to archive the work and share it publicly.

## Contacts
Author: Uttarayan Haldar | [LinkedIn](https://www.linkedin.com/in/uttarayan-haldar/)
