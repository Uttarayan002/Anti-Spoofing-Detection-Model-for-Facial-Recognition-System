# Anti-Spoofing Detector for Facial Recognition System
*"The best way to enhance security is through facial recognition."*
## Description
Anti-spoofing techniques aim to differentiate between live (genuine) and fake (spoofed) facial inputs. The development of robust anti-spoofing detectors is vital for the security and efficacy of facial 
recognition systems. By preventing unauthorized access and reducing false acceptance rates, these systems can achieve higher reliability and usertrust. Enhanced anti-spoofing measures ensure that facial 
recognition technology can be safely deployed in sensitive and high-security environments, such as financial institutions, government facilities, and personal devices. The domain of anti-spoofing in facial 
recognition encompasses the intersection of computer vision, machine learning, and cybersecurity. It addresses critical challenges posed by spoofing attacks, aiming to fortify facial recognition systems 
against fraudulent activities and ensure secure and reliable biometric authentication.

## Dependencies
Check it out before any further procedure -> 

## Installation
There are few tools that needed to be installed before proceeding.                                                                                                                                              
Install the latest version of 'python' which is 3.12.0.                                                                                                                                                
Tools/Libraries:                                                                                                                                                                                                
 cvzone: pip install cvzone                                                                                                                                                                           
 face_recognition: pip install face-recognition                                                                                                                                                                
  tkinter: pip install tk                                                                                                                                                                                          
   cv2: pip install opencv-python

## Usage 

The Usage part should cover:

- Data Preparation (how to preprocess data)
Collect your own data by taking pictures of several live entities/human being as well as video Captured them and store it into collection of data set file. Also create a folder  for fake images which are
pictures of which is captured from videos and other devices, but not the liveimages.                                                                                                                       
Folders: python data/data_collection.py and python data/data.yaml
  
- Training the Model->
run the main file : `python src/main.py` --epochs 3                                                                                                                                          
 - Evaluation/Inference:                                                                                                                                                                                         
  Test the model:  `python yolo_test.py`


## Dataset
There are no particular datasets for this project. It can be made by your own self. Just.
For the dataset of this project, you need to collect the real-time images of your own, relatives, friends and other people near around you. On the other hand, you will collect the fake images, from any screen devices like laptop, mobile or tv screen and anything which will consider as fake. After that  you need to create two folders like live images and for the fake images,  for the live images folder you will store the live images of yourself and other live human being. And on the fake folder you will store fake images which are the images of the any other person from your screen device, but not the live person.

