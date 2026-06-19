import sys
import traceback

print("DEBUG: Starting application...", file=sys.stderr)

try:
    print("DEBUG: Importing GUI...", file=sys.stderr)
    from gui.app import PredictiveTextGUI
    print("DEBUG: GUI imported successfully", file=sys.stderr)
    
    print("DEBUG: Creating GUI instance...", file=sys.stderr)
    app = PredictiveTextGUI()
    print("DEBUG: GUI instance created", file=sys.stderr)
    
    print("DEBUG: Running GUI...", file=sys.stderr)
    app.run()
    print("DEBUG: GUI finished", file=sys.stderr)
    
except Exception as e:
    print(f"DEBUG: ERROR - {e}", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)
