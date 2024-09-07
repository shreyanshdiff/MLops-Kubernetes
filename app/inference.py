import pandas as pd
import joblib
import redis
import hashlib
import json

model = joblib.load('Machine_Failure_classification.pkl')

redis_client = redis.StrictRedis(host='localhost' , port = 6379 , db = 0 , decode_responses=True)

def hash_input(input_data):
    """Generate a hash for the input and use it as a redis key"""
    input_str = json.dumps(input_data , sort_keys = True)
    return hashlib.sha256(input_str.encode()).hexdigest()

def get_prediction(input_data):
    """Get prediction from redis or calculate if not cached"""
    
    key = hash_input(input_data)
    cached_result = redis_client.get(key)
    
    if cached_result:
        print("cache hit!")
        return json.loads(cached_result)
    else:
        input_df = pd.DataFrame([input_data])
        prediction = model.predict(input_df)
        
        result = 'Failure' if prediction[0] == 1 else 'No Failure'
        
        redis_client.set(key , json.dumps(result))
        print("cache miss")
        return result
if __name__ == '__main__':
    print("Running inference script...")
    input_data = {
        'footfall': 31,
        'tempMode': 17,
        'AQ': 7,
        'USS': 6,
        'CS': 5,
        'VOC':5,
        'RP': 24,
        'IP': 4,
        'Temperature':1


    }

    result = get_prediction(input_data)
    print("Prediction:", result)
    