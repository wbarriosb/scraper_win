import pandas as pd
from sodapy import Socrata
import constants as cons

def run_api():
    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    MyAppToken= cons.TOKEN
    client = Socrata("www.datos.gov.co", MyAppToken)

    # Example authenticated client (needed for non-public datasets):
    # client = Socrata(www.datos.gov.co,
    #                  MyAppToken,
    #                  userame="user@example.com",
    #                  password="AFakePassword")

    # First 2000 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    # results = client.get("3t73-n4q9", limit=2000)
    results = client.get("3t73-n4q9", limit= cons.REGS_LIMIT)

    # Convert results to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    return results_df

if __name__=='__main__':
    df= run_api()
    print(df.head(5))