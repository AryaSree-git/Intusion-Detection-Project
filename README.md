# AI-Based Intrusion Detection and Alert System

## Project Overview

The **AI-Based Intrusion Detection and Alert System** is a computer vision-based security application designed to identify unauthorized human presence in restricted areas and provide immediate alerts to authorized personnel.

The system uses a camera module to monitor a designated area and applies **YOLOv8 object detection** to identify people entering the monitored region. When a person is detected, the system captures their image, activates an alarm, and sends an email notification containing the captured photograph to the authorized person.

This project aims to improve security monitoring through automated detection and real-time alert mechanisms, reducing the need for continuous manual supervision.

## Key Features

- **Human Detection:** Detects people using the YOLOv8 object detection model.
- **Camera-Based Monitoring:** Continuously monitors the designated area through a camera module.
- **Image Capture:** Automatically captures a photograph when a person is detected.
- **Email Notifications:** Sends an alert email with the captured image to the authorized recipient.
- **Alarm Activation:** Triggers an alarm when a person is detected in the monitored area.
- **Automated Monitoring:** Combines detection, image capture, email notification, and alarm activation into one workflow.

## System Workflow

1. The camera module continuously captures video from the monitored area.
2. The video frames are processed using Python and OpenCV.
3. YOLOv8 analyzes the frames to detect human presence.
4. When a person is detected, the system captures an image.
5. An alarm is activated to indicate the detected presence.
6. An email notification containing the captured image is sent to the authorized person.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| YOLOv8 | Human/object detection |
| OpenCV | Video capture and image processing |
| Camera Module | Live video monitoring |
| SMTP / Email Integration | Sending email alerts with captured images |

## Project Architecture

**Camera Input → OpenCV Frame Processing → YOLOv8 Detection → Person Detected → Image Capture → Alarm Activation + Email Notification**

## Applications

- Restricted laboratory areas
- College and institutional security
- Office premises
- Server rooms and data centers
- Warehouses and storage facilities
- Private and restricted-access zones

## Future Enhancements

- Integration with IoT-based security devices.
- Cloud-based image storage and monitoring.
- Mobile application for instant security notifications.
- Multiple-camera surveillance support.
- Person tracking and detection-zone configuration.
- Integration with access-control systems.
- Improved alert handling to reduce repeated notifications.

## Project Objective

The main objective is to develop an automated security system that detects human presence in restricted areas and immediately notifies authorized personnel through visual evidence and an alarm mechanism.

## Note

This project is intended as a prototype for automated intrusion monitoring. Detection performance depends on camera placement, lighting conditions, model configuration, and the environment in which it is deployed.