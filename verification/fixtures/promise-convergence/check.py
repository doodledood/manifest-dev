from display import label, net_after_fee

assert label("Hello").strip() == "Hello"
for cents in (2, 100, 1000):
    for fee in (0, 1, 2):
        assert net_after_fee(cents, fee) == cents - fee
print("readable labels and exact fees")
