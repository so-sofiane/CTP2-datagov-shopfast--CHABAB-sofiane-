"""CTP 2 - Exercise 4: replay the 'cents' incident.
A naive suite (not null / unique / allowed values) PASSES on payments_batch_2.csv although every amount is 100x too big.
Only value-range and distribution expectations catch it.
Run from the 02_CTP2 folder:  python gx_payments.py
"""
import pandas as pd
import great_expectations as gx

KIT = "../shopfast-kit/data/"
files = {"payments (history)": KIT + "payments.csv", "payments_batch_2 (new)": "payments_batch_2.csv"}

context = gx.get_context(mode="file")
source = context.data_sources.add_or_update_pandas("shopfast_payments")
asset = source.add_dataframe_asset(name="payments")
batch_def = asset.add_batch_definition_whole_dataframe("whole")
E = gx.expectations

naive = [E.ExpectColumnValuesToNotBeNull(column="payment_id"), E.ExpectColumnValuesToBeUnique(column="payment_id"),
         E.ExpectColumnValuesToNotBeNull(column="amount"), E.ExpectColumnValuesToBeInSet(column="currency", value_set=["EUR"]),
         E.ExpectColumnValuesToBeInSet(column="method", value_set=["card", "paypal", "apple_pay", "bank_transfer"])]
smart = naive + [
    # Accuracy, per value: each payment between 0 and 5,000 EUR (history max = 1,400 EUR)
    E.ExpectColumnValuesToBeBetween(column="amount", min_value=0, strict_min=True, max_value=5000),
    # Accuracy, distribution: mean and median of a batch stay in a normal range (history mean 236, median 184)
    E.ExpectColumnMeanToBeBetween(column="amount", min_value=50, max_value=1000),
    E.ExpectColumnMedianToBeBetween(column="amount", min_value=50, max_value=1000),
]

def run(name, expectations, df):
    suite = context.suites.add_or_update(gx.ExpectationSuite(name=name))
    for e in expectations: suite.add_expectation(e.copy() if hasattr(e, "copy") else e)
    suite.save()
    return batch_def.get_batch(batch_parameters={"dataframe": df}).validate(suite)

for label, path in files.items():
    df = pd.read_csv(path, dtype=str); df["amount_txt"] = df["amount"]; df["amount"] = pd.to_numeric(df["amount"])
    for suite_name, exps in [("naive_payments", naive), ("smart_payments", smart)]:
        res = run(suite_name, exps, df)
        failed = [r.expectation_config.type for r in res.results if not r.success]
        print(f"{label:<24} {suite_name:<15} success={res.success}  failed={failed}")