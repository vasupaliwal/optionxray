from optionxray import Market, Option, XRay, greeks_bs, implied_vol_bs, price_bs


def main() -> None:
    option = Option(spot=100, strike=105, maturity=0.5, rate=0.01, dividend=0.0, option_type="call")
    market = Market(market_price=4.2)

    scenarios = [
        {"name": "Spot +2%", "dS_pct": 0.02},
        {"name": "Vol +3 pts", "dvol_abs": 0.03},
        {"name": "Rates +50bp", "dr_abs": 0.005},
        {"name": "Time +10d", "dT_days": 10},
    ]

    bs_price = price_bs(option, vol=0.25)
    iv = implied_vol_bs(option, market_price=market.market_price).implied_vol if market.market_price else None
    greeks = greeks_bs(option, vol=0.25)

    print(f"Black-Scholes price at 25% vol: {bs_price:.4f}")
    print(f"Implied vol from market price: {iv:.2%}" if iv is not None else "No market price provided.")
    print(f"Greeks at 25% vol: {greeks}")

    xray = XRay(option, market)
    result = xray.run(scenarios=scenarios)

    print(result.summary_text)
    if not result.scenarios_df.empty:
        print("\nScenario table:")
        print(result.scenarios_df)


if __name__ == "__main__":
    main()
