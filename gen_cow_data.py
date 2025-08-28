import random
from datetime import datetime, timedelta

start = datetime.fromisoformat("2025-07-30T08:00:00")
with open("cow_samples.txt", "w", encoding="utf-8") as f:
    f.write("cow_id\ttimestamp\tlat\tlon\ttemperature\tfrequency\tsent\n")
    for cow in range(1, 26):
        lat = round(41.3800 + cow * 0.00005, 6)
        lon = round(1.2000 + cow * 0.00006, 6)
        for i in range(18):  # 3 hours, every 10 mins
            time = start + timedelta(minutes=i * 10)
            temp = round(random.uniform(38.0, 41.0), 1)
            freq = random.randint(45, 100)
            f.write(f"{cow:03}\t{time.isoformat()}Z\t{lat}\t{lon}\t{temp}\t{freq}\t1\n")