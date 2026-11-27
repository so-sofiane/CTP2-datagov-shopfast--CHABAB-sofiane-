1. What breaks: source payments.amount switches from euros to cents (x100), so stg_payments, fct_orders and dim_customers show amounts 100x too high, with no failing test.
2. Exposures hit: sales_dashboard (CEO revenue), finance_monthly_revenue (monthly closing) and churn_prediction_model (customer spend features).
3. Owners to warn: Sara Martin (Sales, dashboard + stg_customers), the Finance team/CFO (report), Karim Benali (steward, ML model).
4. Test to add: on stg_payments.amount, an accepted range (e.g. 0 to 10,000 EUR) + convert cents/100 in stg_payments before deploying.
5. Who approves: the payments data owner (Finance/CFO), after sign-off from the 3 exposure owners; no deploy before the fix is merged.