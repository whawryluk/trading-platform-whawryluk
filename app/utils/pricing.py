def calculate_price(symbol: str, quantity: float) -> float:
	base_prices = {"EURUSD": 1.2, "GBPUSD": 1.35, "PLNUSD": 0.25, "AAPL": 10}
	base_price = base_prices.get(symbol.upper(), 1.0)
	return base_price * quantity