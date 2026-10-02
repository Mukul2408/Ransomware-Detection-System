# Ransomware-Detection-System
Ransomware can modify, rename, and encrypt a large number of files within a very short period of time, making early detection extremely important. This project explores a simple approach to detecting ransomware by focusing on its behavior rather than trying to identify specific ransomware variants through signatures.

The system continuously monitors a selected folder for file-system activity using Python's Watchdog library. Events such as file creation, modification, deletion, and renaming are collected and passed through the detection pipeline. Instead of treating every individual event as a threat, the system looks for unusual bursts of activity within a short sliding time window. It also uses file entropy to identify sudden changes that may indicate that a file's contents have been encrypted.

These different signals are converted into a risk score, which is then used by a simple state machine to classify the current situation as Safe, Suspicious, or Confirmed Threat. This keeps the detection process structured and makes it easier to understand how the system reaches a decision.

A Tkinter-based dashboard provides a live view of the detected file activity and the current threat state, while SQLite is used to maintain a record of important events and risk scores. The project also includes a separate attack-simulation utility that safely reproduces ransomware-like file activity in a dedicated test folder, allowing the complete detection pipeline to be demonstrated without using real malicious software.

Overall, this project brings together file-system monitoring, threading, queues, entropy analysis, risk scoring, state machines, GUI development, and database logging into one practical cybersecurity project.
