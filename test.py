from datetime import datetime
now = datetime.now()
time_prefix = now.strftime("%Y%m%d_%H%M%S")
print(time_prefix + "news.txt")