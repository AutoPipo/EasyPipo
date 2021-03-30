
import random, datetime, os

        
def get_job_id():
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    job_id = nowTime + str(random.randint(11 , 999999))
    return job_id