from mlxtend.frequent_patterns import apriori, association_rules
import pandas as pd
import numpy as np

def market_basket(df, min_support=0.02, min_lift=1, min_invoices=5):
    """
    Perform market basket analysis with boolean DataFrame
    """

    basket = df.groupby(['InvoiceNo', 'Description'])['Quantity'].sum().unstack().fillna(0)

    basket = basket.map(lambda x: x > 0)

    print(f"Initial items: {basket.shape[1]}")
    item_counts = basket.sum()
    valid_items = item_counts[item_counts >= min_invoices].index
    basket = basket[valid_items]
    print(f"Items after filtering (min {min_invoices} invoices): {basket.shape[1]}")

    basket = basket[basket.sum(axis=1) > 0]
    print(f"Invoices after filtering: {basket.shape[0]}")

    if basket.shape[1] < 2:
        print("Warning: Not enough items for association rules")
        return pd.DataFrame()

    print(f"DataFrame dtype: {basket.dtypes.unique()}")

    try:
        frequent = apriori(basket, min_support=min_support, use_colnames=True)
        
        if len(frequent) == 0:
            print(f"No frequent itemsets found with min_support={min_support}")
            return pd.DataFrame()

        rules = association_rules(frequent, metric="lift", min_threshold=min_lift)
        
        if len(rules) == 0:
            print(f"No association rules found with min_lift={min_lift}")
            return pd.DataFrame()

        rules = rules.sort_values('lift', ascending=False)

        result = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].copy()

        result['antecedents'] = result['antecedents'].apply(lambda x: ', '.join(list(x)))
        result['consequents'] = result['consequents'].apply(lambda x: ', '.join(list(x)))
        
        return result
        
    except Exception as e:
        print(f"Error in market basket analysis: {e}")
        return pd.DataFrame()