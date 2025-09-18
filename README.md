# 🎬 Background Replacer - Green Screen Tool

A powerful, user-friendly Python application for replacing backgrounds and removing green/blue screens from images with professional results.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## ✨ Features

### 🎨 **Beautiful Interface**
- Modern dark-themed GUI with professional design
- Tabbed interface for easy navigation
- Real-time preview of all processing steps
- Responsive image display with automatic scaling

### 🔧 **Advanced Processing**
- **HSV Color Range Control**: Fine-tune hue, saturation, and value ranges for precise color targeting
- **Smart Smoothing**: Multiple noise reduction and edge refinement options
- **Morphological Operations**: Erosion and dilation for clean mask edges
- **Gaussian Blending**: Smooth, natural-looking edges in final results

### 🚀 **User-Friendly Features**
- **Quick Presets**: One-click green screen and blue screen configurations
- **Real-time Mask Preview**: See exactly what will be removed before processing
- **Multiple View Modes**: Original, background, result, and mask preview tabs
- **Batch-Ready Design**: Easy to extend for multiple image processing

## 📸 Screenshots

*Coming Soon - Add screenshots of your application in action*

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Quick Install

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/background-replacer.git
   cd background-replacer
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python background_replacer.py
   ```

### Manual Installation

If you prefer to install dependencies manually:

```bash
pip install opencv-python pillow numpy
```

## 🎯 Quick Start

### Basic Usage

1. **Launch the application:**
   ```bash
   python background_replacer.py
   ```

2. **Load your images:**
   - Click "Load Original Image" and select your green/blue screen image
   - Click "Load Background Image" and choose your desired background

3. **Choose a preset or customize:**
   - Use "Green Screen" or "Blue Screen" presets for quick results
   - Or manually adjust HSV values for custom colors

4. **Process and save:**
   - Click "🔄 Process Image" to generate the result
   - Click "💾 Save Result" to save your final image

### Advanced Workflow

For best results with challenging images:

1. **Load images** as described above
2. **Check the Mask Preview** tab to see what's being detected
3. **Fine-tune HSV values:**
   - Adjust **Hue** range to target the specific color
   - Modify **Saturation** to handle color variations
   - Tweak **Value** for different lighting conditions
4. **Improve mask quality:**
   - Increase **Blur Kernel** to reduce noise
   - Use **Erosion** to shrink unwanted areas
   - Apply **Dilation** to fill in gaps
5. **Process and iterate** until satisfied with the result

## ⚙️ Configuration Options

### Color Range Controls (HSV)
| Parameter | Description | Range | Default |
|-----------|-------------|-------|---------|
| **Hue Min/Max** | Target color range | 0-179 | 35-85 (Green) |
| **Saturation Min/Max** | Color intensity range | 0-255 | 40-255 |
| **Value Min/Max** | Brightness range | 0-255 | 40-255 |

### Processing Options
| Parameter | Description | Range | Default |
|-----------|-------------|-------|---------|
| **Blur Kernel** | Noise reduction strength | 1-15 | 5 |
| **Erosion** | Mask shrinking iterations | 0-10 | 2 |
| **Dilation** | Mask expansion iterations | 0-10 | 2 |

## 🎨 Presets

### Green Screen Preset
- **Hue**: 35-85
- **Saturation**: 40-255
- **Value**: 40-255
- **Optimized for**: Standard green screens, chroma key backgrounds

### Blue Screen Preset
- **Hue**: 100-130
- **Saturation**: 50-255
- **Value**: 50-255
- **Optimized for**: Blue screens, sky replacements

## 📁 Project Structure

```
background-replacer/
│
├── background_replacer.py    # Main application file
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── LICENSE                  # MIT License
│
├── examples/                # Example images (optional)
│   ├── sample_greenscreen.jpg
│   └── sample_background.jpg
│
└── docs/                    # Additional documentation
    └── advanced_usage.md
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/amazing-feature`
3. **Commit your changes:** `git commit -m 'Add amazing feature'`
4. **Push to the branch:** `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/background-replacer.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available
```

## 🐛 Known Issues & Troubleshooting

### Common Problems

**Issue**: Images appear distorted or don't load
- **Solution**: Ensure images are in supported formats (JPG, PNG, BMP, TIFF)
- **Check**: File path doesn't contain special characters

**Issue**: Poor mask quality
- **Solution**: Adjust HSV ranges more precisely
- **Tip**: Use the mask preview tab to fine-tune settings

**Issue**: Rough edges in final result
- **Solution**: Increase blur kernel size and adjust erosion/dilation

### Performance Tips

- Use images with good lighting and clean green/blue screens
- Avoid shadows on the background screen
- Ensure consistent lighting across the subject
- Start with presets and make small adjustments

## 📋 Requirements

### System Requirements
- **OS**: Windows 10+, macOS 10.12+, or Linux
- **RAM**: 4GB minimum, 8GB recommended
- **Python**: 3.7 or higher

### Python Dependencies
```
opencv-python>=4.5.0
Pillow>=8.0.0
numpy>=1.19.0
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
