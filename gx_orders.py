"""CTP 2 - Exercise 3: expectation suite for ShopFast orders (GX Core 1.x).
Run from the 02_CTP2 folder:  python gx_orders.py
"""
import pandas as pd
import great_expectations as gx

KIT = "../shopfast-kit/data/"
orders = pd.read_csv(KIT + "orders.csv", dtype=str)
customers = pd.read_csv(KIT + "customers.csv", dtype=str)
orders["total_amount_eur"] = pd.to_numeric(orders["total_amount_eur"], errors="coerce")
orders["order_date_dt"] = pd.to_datetime(orders["order_date"], format="%Y-%m-%d", errors="coerce")

context = gx.get_context(mode="file")
source = context.data_sources.add_or_update_pandas("shopfast")
asset = source.add_dataframe_asset(name="orders")
batch_def = asset.add_batch_definition_whole_dataframe("all_orders")

suite = context.suites.add_or_update(gx.ExpectationSuite(name="orders_suite"))
E = gx.expectations
for e in [
    E.ExpectTableRowCountToBeBetween(min_value=1000, max_value=100000),
    E.ExpectColumnValuesToNotBeNull(column="order_id"),
    E.ExpectColumnValuesToBeUnique(column="order_id"),
    # TODO 1 - Completeness: every order belongs to a customer
    E.ExpectColumnValuesToNotBeNull(column="customer_id"),
    # TODO 2 - Consistency (foreign key): the customer must exist in customers.csv
    E.ExpectColumnValuesToBeInSet(column="customer_id", value_set=set(customers["customer_id"].dropna())),
    # TODO 3 - Completeness + Validity: order_date filled and in YYYY-MM-DD
    E.ExpectColumnValuesToNotBeNull(column="order_date"),
    E.ExpectColumnValuesToMatchRegex(column="order_date", regex=r"^\d{4}-\d{2}-\d{2}$"),
    # TODO 4 - Accuracy: no order in the future
    E.ExpectColumnValuesToBeBetween(column="order_date_dt", max_value=pd.Timestamp.today()),
    # TODO 5 - Validity: status from the agreed list (business decision: 5 lifecycle states)
    E.ExpectColumnValuesToBeInSet(column="status", value_set=["pending", "shipped", "delivered", "cancelled", "returned"]),
    # TODO 6 - Validity: channel and shipping_country, values taken from value_counts() on the data
    E.ExpectColumnValuesToBeInSet(column="channel", value_set=["web", "mobile_app", "marketplace"]),
    E.ExpectColumnValuesToBeInSet(column="shipping_country", value_set=["FR", "DE", "BE", "ES"]),
    # TODO 7 - Accuracy: amount > 0 and below 10,000 EUR (no single order is that big)
    E.ExpectColumnValuesToBeBetween(column="total_amount_eur", min_value=0, strict_min=True, max_value=10000),
]:
    suite.add_expectation(e)
suite.save()

vd = context.validation_definitions.add_or_update(gx.ValidationDefinition(name="orders_validation", data=batch_def, suite=suite))
checkpoint = context.checkpoints.add_or_update(gx.Checkpoint(name="orders_checkpoint", validation_definitions=[vd],
                                                             actions=[gx.checkpoint.UpdateDataDocsAction(name="docs")]))
result = checkpoint.run(batch_parameters={"dataframe": orders})

print("\nSuite passed:", result.success)
for vr in result.run_results.values():
    for r in vr.results:
        cfg = r.expectation_config
        print(f"{'PASS' if r.success else 'FAIL'}  {cfg.type:<45} {cfg.kwargs.get('column', ''):<18} unexpected={r.result.get('unexpected_count', '-')}")
print("\nOpen the report: gx/uncommitted/data_docs/local_site/index.html")