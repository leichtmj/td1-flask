# Import required modules
from flask import Flask , render_template , request
from src.detect import process_image

# Create flask instance
app = Flask ( __name__ )

# Main route
@app.route ('/')
def index():
    return render_template ('index.html')

# API endpoint for image upload
@app.route ('/api/upload', methods =[ 'POST '])
def upload () :
    # Receive the file from the client
    file = request.files['file']
    # Save to temp folder
    filepath = f'static/temp/{ file . filename }'
    file.save( filepath )
    
    # Process image after upload
    process_image( filepath )
    # Return server url to client
    return f"{ request.url_root }{ filepath }"

# Run web server
if __name__ == '__main__ ':
    # Set debug true to load reload server auto on changes
    app.run( debug = True )