import time

start_time1 = time.time()
with open('comedy_url.py', 'r') as file:
    code = file.read()
    exec(code)

end_time1 = time.time()
execution_time1 = end_time1 - start_time1


start_time2 = time.time()
with open('comedy_scrape.py', 'r') as file:
    code = file.read()
    exec(code)

end_time2 = time.time()
execution_time2 = end_time2 - start_time2

print(f"Execution time for exec(): {execution_time1:.4f} seconds")
print(f"Execution time for exec(): {execution_time2:.4f} seconds")
