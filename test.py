from datetime import datetime

curr = datetime.now()

req_format = datetime.strftime(curr, "%m/%d/%Y")

print(curr)