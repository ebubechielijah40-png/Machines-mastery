"""Print semantic argument boundaries, never execute their contents."""
import json,sys
print(json.dumps(sys.argv[1:]))
