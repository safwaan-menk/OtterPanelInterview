import pandas as pd
import numpy as np

def clean_taco_data(df):
   # Drop 100% null columns - remove unusable data
   null_counts = df.isnull().sum()
   dropped_cols = null_counts[null_counts == len(df)].index
   df = df.drop(columns=dropped_cols)

   # Fill financial nulls first to ensure accurate calculations
   financial_cols = ['discount', 'adjustment', 'commission', 'tip', 'delivery_fee', 'subtotal']
   df[financial_cols] = df[financial_cols].fillna(0)

   # Calculate net_payout and margins
   df['net_payout'] = df['net_payout'].fillna(
       df['subtotal'] + df['discount'] + df['adjustment'] + df['commission'] + df['tip'] + df['delivery_fee']
   )
   df['profit_margin'] = (df['net_payout'] / df['subtotal']) * 100

   # Handle timestamps and add delivery metrics
   time_cols = ['created_at', 'ordered_at', 'accepted_at', 'cooked_at', 'courier_arrived_at']
   for col in time_cols:
       if col in df.columns:
           df[col] = pd.to_datetime(df[col], errors='coerce')
           
   # Add operational KPIs
   df['order_completion'] = df['status'].map({'completed': 1, 'cancelled': 0}).fillna(0)
   df['total_processing_time'] = (df['courier_arrived_at'] - df['accepted_at']).dt.total_seconds() / 60
   df['acceptance_to_cooking'] = (df['cooked_at'] - df['accepted_at']).dt.total_seconds() / 60
   df['cooking_to_delivery'] = (df['courier_arrived_at'] - df['cooked_at']).dt.total_seconds() / 60

   # Add customer experience metrics
   df['order_rating'] = df['order_rating'].fillna(df['order_rating'].median())
   df['has_issues'] = df['order_issue_count'].notna().astype(int)
   
   # Add platform performance
   df['platform_orders'] = df.groupby('delivery platform')['order_id'].transform('count')
   df['platform_revenue'] = df.groupby('delivery platform')['subtotal'].transform('sum')

   return df

df = pd.read_csv('dataset.csv')
cleaned_df = clean_taco_data(df)
cleaned_df.to_csv('cleaned_taco_final.csv', index=False)
