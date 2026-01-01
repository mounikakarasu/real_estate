import joblib
import pandas as pd

model = joblib.load('lead_scoring_model.joblib')

# Define leads (Budget, Clicks, Days)
good_lead = pd.DataFrame([[1500000, 15, 5]], columns=['budget', 'email_clicks', 'days_on_market'])
bad_lead = pd.DataFrame([[300000, 0, 100]], columns=['budget', 'email_clicks', 'days_on_market'])

print(f"Good Lead Success Probability: {model.predict_proba(good_lead)[0][1] * 100:.1f}%")
print(f"Bad Lead Success Probability:  {model.predict_proba(bad_lead)[0][1] * 100:.1f}%")