#!/bin/bash
# Quick setup script for development environment

echo "=========================================="
echo "Student Management System - Backend Setup"
echo "=========================================="
echo ""

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "❌ Conda is not installed. Please install Miniconda or Anaconda first."
    exit 1
fi

echo "✓ Conda found"
echo ""

# Create conda environment
echo "Creating conda environment 'student_mgmt'..."
conda create -n student_mgmt python=3.11 -y

if [ $? -ne 0 ]; then
    echo "❌ Failed to create conda environment"
    exit 1
fi

echo "✓ Conda environment created"
echo ""

# Activate environment
echo "To continue setup, please run:"
echo ""
echo "  conda activate student_mgmt"
echo "  pip install -r requirements.txt"
echo "  python scripts/init_db.py"
echo ""
echo "This will:"
echo "  1. Install all Python dependencies"
echo "  2. Create database tables"
echo "  3. Create admin user (username: admin, password: admin123)"
