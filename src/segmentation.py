def assign_segment(row):
    
    if row['R_Score'] >= 4 and row['F_Score'] >= 4 and row['M_Score'] >= 4:
        return "Champions"
    
    elif row['F_Score'] >= 4:
        return "Loyal Customers"
    
    elif row['R_Score'] >= 3 and row['F_Score'] >= 3:
        return "Potential Loyalists"
    
    elif row['R_Score'] <= 2 and row['F_Score'] >= 3:
        return "At Risk"
    
    elif row['R_Score'] <= 2 and row['F_Score'] <= 2:
        return "Hibernating"
    
    else:
        return "Others"