# Quick fix for translation speed issues
# Run this in your backend directory

echo "Installing missing dependencies for faster translation..."

# Install accelerate for better model loading
pip install accelerate>=0.26.0

# Install additional optimization packages
pip install optimum[onnxruntime]

echo "Dependencies installed! The server should now load the model properly."
echo "If you still see errors, the fallback translation system will work instantly."
