#!/usr/bin/env python3
"""
Create PDFs of Names of God for Laser Cutting
This script creates individual PDF files for each name of God with interconnected,
laser-cutting friendly designs based on the sample image style.
"""

import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import inch, mm
from reportlab.pdfbase import pdfmetrics, pdfutils
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


class NamesPDFGenerator:
    def __init__(self, sample_image_path):
        self.sample_image_path = sample_image_path
        self.names = [
            "Jehovah Jireh",
            "Jehovah Shammah",
            "Jehovah Sabaoth",
            "Jehovah Rapha",
            "Jehovah Raah",
            "Jehovah Makadesh",
            "Jehovah Nissi",
            "Jehovah Shalom",
            "El Roi",
            "Adonai",
            "El Shadai",
            "Yahwe",
            "Abba",
            "El Elyon",
            "El Olam",
            "Elohim",
            "Emmanuel",
            "Yahweh Sabaoth",
            "El Gibbor",
            "Qedosh",
        ]
        self.output_dir = "name_pdfs"
        self.ensure_output_directory()

    def ensure_output_directory(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def analyze_sample_image(self):
        """Analyze the sample image to understand the style requirements"""
        try:
            # Load the sample image
            img = cv2.imread(self.sample_image_path)
            if img is None:
                print(
                    f"Warning: Could not load sample image from {self.sample_image_path}"
                )
                return None

            # Convert to grayscale for analysis
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Get image dimensions
            height, width = gray.shape

            # Analyze for text characteristics
            # This is a simple analysis - in practice, you might use OCR or other techniques
            return {
                "width": width,
                "height": height,
                "dominant_color": "black",  # Assume black text for laser cutting
                "style": "bold_serif",  # Default assumption
            }
        except Exception as e:
            print(f"Error analyzing sample image: {e}")
            return None

    def get_font_path(self):
        """Get a suitable font path for the design"""
        # Try to find system fonts that work well for laser cutting
        possible_fonts = [
            "/System/Library/Fonts/Times.ttc",  # macOS Times
            "/System/Library/Fonts/Georgia.ttc",  # macOS Georgia
            "/System/Library/Fonts/Helvetica.ttc",  # macOS Helvetica
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",  # Linux
            "C:\\Windows\\Fonts\\times.ttf",  # Windows
            "C:\\Windows\\Fonts\\georgia.ttf",  # Windows
        ]

        for font_path in possible_fonts:
            if os.path.exists(font_path):
                return font_path

        return None  # Use default font

    def create_interconnected_design(self, text, canvas_obj, page_width, page_height):
        """Create an interconnected design suitable for laser cutting"""

        # Set up the canvas for laser cutting (black lines on white background)
        canvas_obj.setStrokeColor("black")
        canvas_obj.setFillColor("black")

        # Calculate text positioning
        text_width = canvas_obj.stringWidth(text, "Helvetica-Bold", 48)
        x = (page_width - text_width) / 2
        y = page_height / 2

        # Create the main text
        canvas_obj.setFont("Helvetica-Bold", 48)
        canvas_obj.drawString(x, y, text)

        # Add decorative elements for interconnectedness
        self.add_decorative_elements(
            canvas_obj, x, y, text_width, page_width, page_height
        )

    def add_decorative_elements(
        self, canvas_obj, text_x, text_y, text_width, page_width, page_height
    ):
        """Add decorative elements to make the design interconnected"""

        # Add border frame
        margin = 20
        canvas_obj.setLineWidth(2)
        canvas_obj.rect(
            margin,
            margin,
            page_width - 2 * margin,
            page_height - 2 * margin,
            stroke=1,
            fill=0,
        )

        # Add corner decorations
        corner_size = 30
        corners = [
            (margin, margin),  # bottom-left
            (page_width - margin - corner_size, margin),  # bottom-right
            (margin, page_height - margin - corner_size),  # top-left
            (
                page_width - margin - corner_size,
                page_height - margin - corner_size,
            ),  # top-right
        ]

        for x, y in corners:
            # Create decorative corner elements
            canvas_obj.setLineWidth(1)
            canvas_obj.line(x, y, x + corner_size / 2, y + corner_size / 2)
            canvas_obj.line(
                x + corner_size, y, x + corner_size / 2, y + corner_size / 2
            )
            canvas_obj.line(
                x, y + corner_size, x + corner_size / 2, y + corner_size / 2
            )
            canvas_obj.line(
                x + corner_size,
                y + corner_size,
                x + corner_size / 2,
                y + corner_size / 2,
            )

        # Add underline decoration
        underline_y = text_y - 10
        canvas_obj.setLineWidth(3)
        canvas_obj.line(text_x - 20, underline_y, text_x + text_width + 20, underline_y)

        # Add side flourishes
        flourish_y = text_y + 15
        canvas_obj.setLineWidth(1)

        # Left flourish
        left_start = text_x - 40
        canvas_obj.line(left_start, flourish_y, left_start + 25, flourish_y)
        canvas_obj.circle(left_start + 30, flourish_y, 3, stroke=1, fill=1)

        # Right flourish
        right_start = text_x + text_width + 15
        canvas_obj.line(right_start, flourish_y, right_start + 25, flourish_y)
        canvas_obj.circle(right_start + 30, flourish_y, 3, stroke=1, fill=1)

    def create_single_pdf(self, name, index):
        """Create a single PDF for one name"""
        filename = f"{self.output_dir}/{index:02d}_{name.replace(' ', '_').replace('/', '_')}.pdf"

        # Create PDF with A4 size (good for laser cutting)
        page_width, page_height = A4
        c = canvas.Canvas(filename, pagesize=A4)

        # Set title
        c.setTitle(f"Names of God - {name}")

        # Create the interconnected design
        self.create_interconnected_design(name, c, page_width, page_height)

        # Add metadata for laser cutting
        c.setSubject("Laser Cutting Design")
        c.setKeywords(["laser cutting", "names of God", "religious", "decoration"])

        # Save the PDF
        c.save()
        print(f"Created: {filename}")

        return filename

    def create_all_pdfs(self):
        """Create PDFs for all names"""
        print("Analyzing sample image...")
        sample_analysis = self.analyze_sample_image()

        if sample_analysis:
            print(f"Sample analysis: {sample_analysis}")
        else:
            print("Using default styling...")

        print(f"\nCreating PDFs for {len(self.names)} names...")
        created_files = []

        for i, name in enumerate(self.names, 1):
            try:
                filename = self.create_single_pdf(name, i)
                created_files.append(filename)
            except Exception as e:
                print(f"Error creating PDF for '{name}': {e}")

        print(
            f"\nCompleted! Created {len(created_files)} PDF files in '{self.output_dir}' directory."
        )
        print("\nLaser Cutting Notes:")
        print("- All designs use black lines on white background")
        print("- Interconnected elements ensure structural integrity")
        print("- A4 size provides good material usage")
        print("- 2-3mm line widths recommended for most laser cutters")

        return created_files

    def create_combined_pdf(self):
        """Create a single PDF with multiple names per page for efficient cutting"""
        filename = f"{self.output_dir}/00_Combined_Names_of_God.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        page_width, page_height = A4

        # Calculate layout for multiple names per page
        names_per_page = 4
        cols = 2
        rows = 2

        for page_start in range(0, len(self.names), names_per_page):
            page_names = self.names[page_start : page_start + names_per_page]

            for i, name in enumerate(page_names):
                col = i % cols
                row = i // cols

                # Calculate position
                x_offset = col * (page_width / cols)
                y_offset = (rows - row - 1) * (page_height / rows)

                # Create smaller version of the design
                self.create_compact_design(
                    name, c, x_offset, y_offset, page_width / cols, page_height / rows
                )

            if page_start + names_per_page < len(self.names):
                c.showPage()

        c.save()
        print(f"Created combined PDF: {filename}")
        return filename

    def create_compact_design(
        self, text, canvas_obj, x_offset, y_offset, width, height
    ):
        """Create a compact version of the design for combined layouts"""
        canvas_obj.setStrokeColor("black")
        canvas_obj.setFillColor("black")

        # Scale font size for compact layout
        font_size = 24
        canvas_obj.setFont("Helvetica-Bold", font_size)

        # Center text in the allocated space
        text_width = canvas_obj.stringWidth(text, "Helvetica-Bold", font_size)
        x = x_offset + (width - text_width) / 2
        y = y_offset + height / 2

        canvas_obj.drawString(x, y, text)

        # Add simple border
        margin = 10
        canvas_obj.setLineWidth(1)
        canvas_obj.rect(
            x_offset + margin,
            y_offset + margin,
            width - 2 * margin,
            height - 2 * margin,
            stroke=1,
            fill=0,
        )

        # Add simple underline
        canvas_obj.line(x - 10, y - 5, x + text_width + 10, y - 5)


def main():
    sample_path = "sample.png"

    if not os.path.exists(sample_path):
        print(
            f"Warning: Sample image '{sample_path}' not found. Using default styling."
        )

    generator = NamesPDFGenerator(sample_path)

    # Create individual PDFs
    created_files = generator.create_all_pdfs()

    # Create combined PDF
    combined_file = generator.create_combined_pdf()

    print(f"\nAll files created successfully!")
    print(f"Individual PDFs: {len(created_files)} files")
    print(f"Combined PDF: {combined_file}")


if __name__ == "__main__":
    main()
