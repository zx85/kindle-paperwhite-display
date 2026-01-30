import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from kindleDisplay import app

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5050)
#    app.run(host='0.0.0.0')
