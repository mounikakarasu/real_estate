import pandas as pd
import numpy as np

# CONFIG
NUM_SAMPLES = 1000

def generate_leads():
    data = []
    
    for _ in range(NUM_SAMPLES):
        # 1. Random Features
        budget = np.random.randint(200000, 2000000)
        email_clicks = np.random.randint(0, 20)
        days_on_market = np.random.randint(1, 180)
        
        # 2. The Logic (The "Signal" we want AI to find)
        # High budget & clicks increase score; long days on market decrease it.
        score = (budget / 2000000) * 40 + (email_clicks * 3) - (days_on_market * 0.1)
        score += np.random.normal(0, 5) # Add noise so it's not perfect
        
        # 3. Target (1 = Sold, 0 = Lost)
        converted = 1 if score > 50 else 0
        
        data.append({
            'budget': budget,
            'email_clicks': email_clicks,
            'days_on_market': days_on_market,
            'converted': converted
        })

    df = pd.DataFrame(data)
    df.to_csv('training_data.csv', index=False)
    print(f"Generated {NUM_SAMPLES} synthetic leads.")

if __name__ == "__main__":
    generate_leads()