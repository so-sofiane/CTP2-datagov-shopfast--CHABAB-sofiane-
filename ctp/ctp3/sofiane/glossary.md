{% docs gross_revenue %}
**Gross revenue (EUR)** - total amount paid by the customer for an order, VAT included, shipping included, before refunds.
Owner: Head of Sales - Steward: Karim Benali - Status: approved (2026-11-10)
{% enddocs %}

{% docs net_revenue %}
**Net revenue (EUR)** - what the customer paid for non-cancelled orders, minus refunds, excluding VAT (divided by 1.20). Shipping fees included.
Formula: (sum paid - refunds) / 1.20. Example: EUR 120 paid, no refund -> EUR 100.
Owner: Paul Girard (Head of Finance) - Steward: Karim Benali - Status: approved (2026-11-25)
{% enddocs %}

{% docs active_customer %}
**Active customer** - a customer account with at least one non-cancelled order in the last 12 months.
Need a 6-month view? Use "recently active customer (6 months)", a separate term for Sales.
Owner: Paul Girard (Head of Finance) - Steward: Karim Benali - Status: approved (2026-11-25)
{% enddocs %}

{% docs churned_customer %}
**Churned customer** - a customer who has ordered before but has no non-cancelled order in the last 12 months.
Example: last order on 2025-09-01 -> churned on 2026-11-25.
Owner: Paul Girard (Head of Finance) - Steward: Karim Benali - Status: approved (2026-11-25)
{% enddocs %}

{% docs customer %}
**Customer** - one customer account on ShopFast, identified by customer_id. Counts accounts, not people.
Owner: Sara Martin (Head of Sales) - Steward: Karim Benali - Status: approved (2026-11-25)
{% enddocs %}

{% docs order %}
**Order** - one purchase placed by a customer, whatever its status (pending, shipped, delivered, cancelled, returned).
Owner: Sara Martin (Head of Sales) - Steward: Karim Benali - Status: approved (2026-11-25)
{% enddocs %}