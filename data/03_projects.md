# Technical Portfolio and Software Engineering Projects

## Project 1: Emora — Multimodal Emotion Classification (Final Year Project)
- **Project Status:** Active capstone research project (currently in progress; training and model evaluation underway).
- **Core Concept:** Emora is an explainable multimodal deep learning framework designed to detect and classify children's emotional states by combining features from their drawings and accompanying written text reflections.
- **Research Focus & Hypothesis:** The central research question investigates whether fusing vision models (e.g., CNNs/Vision Transformers) and language models (e.g., BERT, RoBERTa) improves classification accuracy compared to single-modality baselines.
- **Architecture & Technical Stack:** PyTorch, Hugging Face Transformers (`bert-base-uncased`, `roberta-base`), Computer Vision models, multimodal feature fusion layers, and explainable AI (XAI) techniques like Grad-CAM for spatial region importance and token-level attribution maps.
- **Future Pipeline Extension:** Planned potential extension includes an agentic RAG (Retrieval-Augmented Generation) component for contextual interpretation if development time permits.

## Project 2: Roman Urdu to Nastaliq Urdu Transliteration Engine
- **Project Overview:** A specialized Natural Language Processing (NLP) system built to convert Roman Urdu text (Urdu written in the Latin alphabet) into standard Nastaliq script Urdu.
- **Technical Stack & Methodologies:** Python, NLP sequence-to-sequence mappings, character/token-level mapping rules, and text normalization pipelines.
- **Core Problem Solved:** Addresses phonetic variations, spelling inconsistencies, and informal transliteration patterns commonly used in digital South Asian communication to produce accurate native Urdu text output.

## Project 3: TrashSense — Waste Classification & Environmental Advisory System
- **Project Overview:** An intelligent automated waste classification system that pairs computer vision models with an LLM-driven advisory pipeline to promote proper recycling and disposal habits.
- **Technical Implementation:** Benchmarked image classification across waste categories using models like ResNet-50 and MobileNetV2 with 5-fold cross-validation. Integrated an LLM agentic pipeline that receives the predicted waste category and generates actionable environmental guidance for end users via a Gradio interface.

## Project 4: Personal Protective Equipment (PPE) Detection & Benchmarking System
- **Project Overview:** A deep learning computer vision system built to detect personal protective equipment (helmets, safety vests, masks) in real time to ensure workplace safety compliance.
- **Model Comparison & Benchmarking:** Trained, evaluated, and compared three distinct object detection architectures: YOLOv8n, YOLOv11n, and Faster R-CNN.
- **Deployment & Interface:** Deployed as an interactive Gradio web application capable of processing both static image inputs and dynamic video streams for real-time safety inspection.

## Project 5: File Vault — Hybrid Desktop File Encryption Utility
- **Project Overview:** A standalone desktop application built to secure sensitive local files using hybrid cryptographic mechanisms.
- **Technical Stack:** Python, Tkinter GUI, `cryptography` library.
- **Security Design:** Combines AES-256-GCM for high-performance authenticated symmetric file encryption with RSA-2048 (OAEP padding) for key management and secure key exchange.

## Project 6: TradeCraft — Skill Swapping Mobile Application
- **Project Overview:** Developed as the term project for Mobile Application Development, TradeCraft is a collaborative peer-to-peer mobile application platform designed for direct skill-trading and service swapping without monetary transactions.
- **Key Features:** Features interactive user profiles, trade proposal workflows, category tagging, and request routing.

## Project 7: Software Patch & Version Protection Utility
- **Project Overview:** Developed for the Software Requirement Engineering course, this Python-based utility manages patch delivery, verifies version integrity, and protects against unauthorized version tampering.

## Project 8: Mini Library & Book Management System (Assembly Language)
- **Project Overview:** Developed for the Computer Organization & Assembly Language course, this low-level console utility manages book records, inventory indexing, and basic search operations directly using assembly instructions.