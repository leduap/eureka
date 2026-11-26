#!/usr/bin/env python3
"""Hartfeld GmbH teaching ledger for The Finance Blue Book.

Every euro printed in the manuscript is produced here. Teaching tax is 30
percent so a reader can check the arithmetic. The Munich stacked rate is
computed once, beside it, and is not the rate used in the running examples.
"""

from __future__ import annotations

def annuity(rate: float, years: int) -> float:
    return (1 - (1 + rate) ** (-years)) / rate


def pv(amount: float, rate: float, years: int) -> float:
    return amount / (1 + rate) ** years


def eur(n: float) -> str:
    sign = "-" if n < 0 else ""
    return sign + f"€{abs(n):,.0f}"


def pct(n: float) -> str:
    return f"{n * 100:.2f}%"


def main() -> None:
    tax = 0.30
    years = 5

    # --- the firm, year ended 31 Dec 2026 ---
    revenue = 40_000_000
    cogs = 24_000_000
    gross = revenue - cogs
    sga_cash = 8_800_000
    depreciation = 1_200_000
    ebit = gross - sga_cash - depreciation
    ebitda = ebit + depreciation
    debt = 8_000_000
    rate_debt = 0.05
    interest = debt * rate_debt
    ebt = ebit - interest
    tax_paid_model = ebt * tax
    net_income = ebt - tax_paid_model

    cash = 2_400_000
    receivables = 5_000_000
    inventory = 4_800_000
    ppe_net = 12_000_000
    assets = cash + receivables + inventory + ppe_net
    payables = 3_000_000
    equity = assets - payables - debt
    assert equity == 13_200_000

    days = 365
    dso = receivables / revenue * days
    dio = inventory / cogs * days
    dpo = payables / cogs * days
    ccc = dso + dio - dpo

    net_debt = debt - cash
    nd_ebitda = net_debt / ebitda
    cover = ebit / interest

    print("FIRM")
    print(f"revenue {eur(revenue)} cogs {eur(cogs)} gross {eur(gross)}")
    print(f"sga cash {eur(sga_cash)} dep {eur(depreciation)} ebit {eur(ebit)} ebitda {eur(ebitda)}")
    print(f"interest {eur(interest)} ebt {eur(ebt)} tax {eur(tax_paid_model)} ni {eur(net_income)}")
    print(f"cash {eur(cash)} ar {eur(receivables)} inv {eur(inventory)} ppe {eur(ppe_net)} assets {eur(assets)}")
    print(f"ap {eur(payables)} debt {eur(debt)} equity {eur(equity)}")
    print(f"dso {dso:.1f} dio {dio:.1f} dpo {dpo:.1f} ccc {ccc:.1f}")
    print(f"net debt {eur(net_debt)} nd/ebitda {nd_ebitda:.2f} cover {cover:.1f}")

    # ownership
    klaus, martin, ingrid = 0.60, 0.20, 0.20

    # --- project A: calibration line ---
    a_capex = 2_400_000
    a_nwc = 300_000
    a_rev = 1_500_000
    a_cost = 720_000
    a_dep = a_capex / years
    a_ebit = a_rev - a_cost - a_dep
    a_nopat = a_ebit * (1 - tax)
    a_ocf = a_nopat + a_dep
    print("\nPROJECT A calibration")
    print(f"capex {eur(a_capex)} nwc {eur(a_nwc)} dep {eur(a_dep)} ebit {eur(a_ebit)} nopat {eur(a_nopat)} ocf {eur(a_ocf)}")

    def npv_project(ocf: float, capex: float, nwc: float, rate: float) -> float:
        return -capex - nwc + ocf * annuity(rate, years) + pv(nwc, rate, years)

    for rate in (0.08, 0.06, 0.10):
        print(f"A npv at {pct(rate)} {eur(npv_project(a_ocf, a_capex, a_nwc, rate))} factor {annuity(rate, years):.5f}")

    # month-by-month cash hole, teaching calendar
    # Jan: pay half the machines. Feb: pay the rest and fill inventory (nwc is inventory).
    # Sales start March. Customers pay in 60 days, so cash from March sales arrives May.
    # Annual OCF 690k is the full-year accrual view. Monthly commercial cash is lumpy.
    machine_jan = 1_200_000
    machine_feb = 1_200_000
    stock_feb = 300_000
    # contribution cash before tax, spread Apr-Dec once the line is running: simplify
    # teaching path stated in the chapter, not a full monthly tax model
    opening_cash = cash
    # fixed outflows only, before any receipts, against opening cash
    cash_end_feb = opening_cash - machine_jan - machine_feb - stock_feb
    print(f"cash if line is paid before any receipt: {eur(cash_end_feb)}")

    # --- project B: smart gauge ---
    b_capex = 1_800_000
    b_nwc = 500_000
    b_dep = b_capex / years
    b_ocf = 500_000
    # reverse into ebit: ocf = ebit*(1-t) + dep
    b_ebit = (b_ocf - b_dep) / (1 - tax)
    b_rev = 2_000_000
    b_cost = b_rev - b_dep - b_ebit
    print("\nPROJECT B smart gauge")
    print(f"capex {eur(b_capex)} nwc {eur(b_nwc)} dep {eur(b_dep)} ebit {eur(b_ebit)} cost {eur(b_cost)} ocf {eur(b_ocf)}")
    for rate in (0.06, 0.12):
        print(f"B npv at {pct(rate)} {eur(npv_project(b_ocf, b_capex, b_nwc, rate))}")

    # --- WACC ---
    rf = 0.03
    erp = 0.05
    beta_e = 0.90
    de = debt / equity
    beta_u = beta_e / (1 + (1 - tax) * de)
    ke = rf + beta_e * erp
    v = debt + equity
    wacc = (equity / v) * ke + (debt / v) * rate_debt * (1 - tax)
    # smart gauge: equity beta 1.60 at the same gearing, as a judgment, not a regression
    beta_b = 1.60
    ke_b = rf + beta_b * erp
    # asset beta of the gadget if we unlever the same way
    beta_u_b = beta_b / (1 + (1 - tax) * de)
    wacc_b = (equity / v) * ke_b + (debt / v) * rate_debt * (1 - tax)
    print("\nWACC")
    print(f"D/E {de:.4f} beta_u {beta_u:.4f} ke {pct(ke)} V {eur(v)}")
    print(f"E/V {equity/v:.4f} D/V {debt/v:.4f} wacc {pct(wacc)} exact {wacc:.6f}")
    print(f"gauge ke {pct(ke_b)} wacc {pct(wacc_b)} exact {wacc_b:.6f} beta_u {beta_u_b:.4f}")

    # --- more debt ---
    new_debt = 6_000_000
    debt2 = debt + new_debt
    rate2 = 0.055
    # blended: old 8m at 5%, new 6m at 5.5%
    interest2 = debt * rate_debt + new_debt * rate2
    ebitda_down = 4_000_000
    # down year: dep stays 1.2, so ebit = 4.0 - 1.2 = 2.8 if ebitda is 4
    ebit_down = ebitda_down - depreciation
    net_debt2 = debt2 - cash
    print("\nDEBT")
    print(f"debt2 {eur(debt2)} interest2 {eur(interest2)} blended {interest2/debt2:.4f}")
    print(f"down ebitda {eur(ebitda_down)} ebit {eur(ebit_down)}")
    print(f"nd/ebitda down {net_debt2/ebitda_down:.2f} cover down {ebit_down/interest2:.2f}")
    print(f"covenant nd/ebitda max 2.00, cover min 4.00")
    # base year with extra debt, no downturn
    print(f"base year with extra debt nd/ebitda {net_debt2/ebitda:.2f} cover {ebit/interest2:.2f}")

    # MM: all-equity vs levered, perpetuity, no taxes first, then with tax
    # Use EBIT as the unlevered operating profit teaching object.
    # Ignore dep/capex (steady state, capex = dep) so NOPAT is the cash.
    ebit_p = ebit
    vu = ebit_p * (1 - tax) / wacc  # not pure MM; pure MM uses r0
    # Classic MM with corporate tax: VL = VU + tD, where VU is unlevered value at the unlevered cost.
    r0 = rf + beta_u * erp  # unlevered equity / asset return, teaching
    vu_classic = ebit_p * (1 - tax) / r0
    vl_classic = vu_classic + tax * debt
    print(f"r0 {pct(r0)} exact {r0:.6f} VU {eur(vu_classic)} VL {eur(vl_classic)} tax shield {eur(tax*debt)}")

    # --- dividend ---
    dividend = 1_200_000
    ingrid_div = dividend * ingrid
    # German flat tax on investment income, headline, individual: 25% + 5.5% soli = 26.375%
    kapest = 0.25 * 1.055
    ingrid_tax = ingrid_div * kapest
    ingrid_net = ingrid_div - ingrid_tax
    # buyback of the same €1.2m: she sells 1.2m / equity_value shares. Use the chapter-6 equity value later.
    print("\nDIVIDEND")
    print(f"total {eur(dividend)} ingrid {eur(ingrid_div)} kapest rate {pct(kapest)} tax {eur(ingrid_tax)} net {eur(ingrid_net)}")
    print(f"ni after dividend retained {eur(net_income - dividend)} payout {dividend/net_income:.4f}")

    # --- peer and valuation ---
    # Nordmess: EBIT €50m, EV/EBIT 8.0, net debt €40m
    nord_ebit = 50_000_000
    nord_multiple = 8.0
    nord_ev = nord_ebit * nord_multiple
    nord_nd = 40_000_000
    nord_equity = nord_ev - nord_nd
    hart_ev_multiple = ebit * nord_multiple
    hart_equity_multiple = hart_ev_multiple - net_debt
    fcff = ebit * (1 - tax)  # capex = dep, nwc flat
    ev_dcf = fcff / wacc
    eq_dcf = ev_dcf - net_debt
    implied_yield = fcff / hart_ev_multiple
    print("\nVALUE")
    print(f"fcff {eur(fcff)} ev dcf {eur(ev_dcf)} equity dcf {eur(eq_dcf)}")
    print(f"nord ebit {eur(nord_ebit)} nd {eur(nord_nd)} ev {eur(nord_ev)} equity {eur(nord_equity)}")
    print(f"hart at 8x ebit ev {eur(hart_ev_multiple)} equity {eur(hart_equity_multiple)}")
    print(f"implied fcff yield on the multiple {pct(implied_yield)}")
    # growth that reconciles 8x with a 6% WACC: Gordon EV = fcff*(1+g)/(wacc-g)
    # 48m = 4.2m*(1+g)/(0.06-g)
    # 48/4.2 = (1+g)/(0.06-g)
    # 11.42857*(0.06-g) = 1+g
    # 0.685714 - 11.42857 g = 1 + g
    # 0.685714 - 1 = g*12.42857
    # g = -0.314286/12.42857 negative? That means the multiple is cheaper than no-growth DCF,
    # so the market is using a higher discount rate, not hidden growth.
    # What WACC makes no-growth DCF equal 48m? wacc = 4.2/48
    wacc_implied = fcff / hart_ev_multiple
    print(f"wacc that sets no-growth DCF equal to 8x EBIT {pct(wacc_implied)}")

    # buyback at the multiple equity value
    equity_value = hart_equity_multiple
    ingrid_stake_value = equity_value * ingrid
    shares_taught = 1_000_000  # teaching shares, privately "as if"
    price = equity_value / shares_taught
    bought = dividend / price
    ingrid_shares = shares_taught * ingrid
    # if the company buys shares pro-rata she is not forced; if she is the one who sells:
    ingrid_sale = dividend  # she sells €1.2m of stock, same cash
    # her remaining fraction
    new_shares = shares_taught - bought
    # she sold `bought` of her own shares
    ingrid_left = ingrid_shares - bought
    fraction_left = ingrid_left / new_shares
    print(f"price per teaching share {price:.2f} shares bought {bought:.1f}")
    print(f"ingrid fraction before {ingrid:.4f} after selling the €1.2m herself {fraction_left:.4f}")
    print(f"ingrid stake value before {eur(ingrid_stake_value)}")

    # --- working capital order ---
    order_rev = 6_000_000
    order_cost = 3_600_000  # 60% like the firm
    order_gross = order_rev - order_cost
    # payables 30 days, receivables 90 days, inventory bought day 0 for a job that ships day 30
    # cash: day 0 pay nothing if supplier gives 30 days; day 30 pay 3.6m; day 120 collect 6.0m
    # (ship day 30, customer 90 days from ship)
    gap_days = 90
    # interest on 3.6m for 90 days at 5%
    gap_interest = order_cost * rate_debt * gap_days / 365
    print("\nORDER")
    print(f"rev {eur(order_rev)} cost {eur(order_cost)} gross {eur(order_gross)}")
    print(f"90-day interest on the cost {eur(gap_interest)}")
    # profit after that interest, before overhead and tax
    print(f"gross after the carry {eur(order_gross - gap_interest)}")

    # --- accrual ---
    december_sale = 900_000
    december_cost = 540_000
    warranty_rate = 0.04
    warranty = december_sale * warranty_rate
    gross_if_booked = december_sale - december_cost
    gross_after_warranty = gross_if_booked - warranty
    # cash in December from this sale: 0. Cash out if the goods were already in inventory: 0 this month,
    # inventory falls, payable already settled in the teaching version.
    print("\nACCRUAL")
    print(f"sale {eur(december_sale)} cost {eur(december_cost)} warranty {eur(warranty)}")
    print(f"gross if booked {eur(gross_if_booked)} after warranty {eur(gross_after_warranty)} december cash 0")

    # --- forecast revision of project A ---
    # revenue comes in at 900k not 1.5m. Costs are 70% variable on the original 720k? 
    # Original cash cost 720 on 1500 revenue = 48% of incremental revenue, plus a fixed 0.
    # Keep it simple: cash cost stays 720 because it is mostly technicians, revenue 900.
    a_rev_low = 900_000
    a_ebit_low = a_rev_low - a_cost - a_dep
    a_ocf_low = a_ebit_low * (1 - tax) + a_dep
    print("\nREVISED A")
    print(f"ebit {eur(a_ebit_low)} ocf {eur(a_ocf_low)}")
    for rate in (0.06, 0.08):
        print(f"revised npv at {pct(rate)} {eur(npv_project(a_ocf_low, a_capex, a_nwc, rate))}")

    # --- tax calendars ---
    munich = 0.15 + 0.15 * 0.055 + 0.035 * 4.90
    profit = ebt  # teaching base, ignoring add-backs
    tax_30 = profit * tax
    tax_muc = profit * munich
    print("\nTAX")
    print(f"munich combined {pct(munich)} exact {munich:.6f}")
    print(f"on ebt {eur(profit)} at 30% {eur(tax_30)} at munich {eur(tax_muc)} gap {eur(tax_muc-tax_30)}")
    # quarterly corporate prepayment on the model tax, four equal parts
    print(f"each quarterly slice of the 30% teaching tax {eur(tax_30/4)}")
    # depreciation shield
    shield = depreciation * tax
    print(f"dep tax shield at 30% {eur(shield)}")

    # --- currency ---
    usd_sales = 4_000_000
    fx_open = 1.08  # dollars per euro, so euro value = usd/fx
    fx_close = 1.14
    eur_open = usd_sales / fx_open
    eur_close = usd_sales / fx_close
    print("\nFX")
    print(f"usd sales at 1.08 {eur(eur_open)} at 1.14 {eur(eur_close)} loss {eur(eur_close-eur_open)}")
    # hedge: sell dollars forward at 1.09
    fx_hedge = 1.09
    eur_hedge = usd_sales / fx_hedge
    print(f"hedged at 1.09 {eur(eur_hedge)} versus open {eur(eur_open)} cost of hedge {eur(eur_hedge-eur_open)}")

    # --- option: right to double ---
    # one-step binomial, 6 months. Order gross profit €1.2m on the €6m order.
    # Customer may double. If they double, Hartfeld must supply another €6m at the same price.
    # In the up state the extra order is worth the same gross €1.2m minus the carry.
    # In the down state the extra capacity is worth 0 and the parts bought ahead cost money.
    # Teaching binomial, risk-neutral, rate 5% for half a year.
    # Spot "value of the right" .
    # S = 200,000 expected gross on the optioned second order if exercised only when useful.
    # Simpler story told in the chapter:
    # Up: second order gross profit 400,000 (tight capacity, they would have charged more)
    # Down: second order gross profit -150,000 if they are forced to build into a slump
    # They can choose to fill it, so down payoff of the OPTION is max(-150k, 0) = 0 if it is a right not an obligation.
    # A right: up 400,000, down 0.
    u_pay, d_pay = 400_000, 0
    r = 0.05
    dt = 0.5
    # risk-neutral prob from a move of +/- 20% on a notional
    # We set p* so the mean matches the risk-free on a traded twin. Teaching: p = 0.5 is NOT used.
    # Twin asset: 100 today, 130 up, 80 down. 
    s, su, sd = 100, 130, 80
    df = 1 / (1 + r * dt)  # simple half-year, teaching
    p_star = ((s / df) - sd) / (su - sd)  # wait, forward is s*(1+r*dt), not s/df
    growth = 1 + r * dt
    p_star = (s * growth - sd) / (su - sd)
    option = df * (p_star * u_pay + (1 - p_star) * d_pay)
    print("\nOPTION")
    print(f"p* {p_star:.4f} df {df:.4f} value of the right {eur(option)}")
    # if they give it away inside a 1.2m gross order
    print(f"right as a share of the €1,200,000 gross {option/order_gross:.4f}")
    half_pay = 200_000
    half_option = df * (p_star * half_pay + (1 - p_star) * d_pay)
    print(f"half the pain, value of the right {eur(half_option)}")

    # --- practice figures used in the exhibits ---
    # Thin revenue on the calibration line: cash cost and depreciation unchanged.
    thin_rev = 1_200_000
    thin_ebit = thin_rev - a_cost - a_dep
    thin_ocf = thin_ebit * (1 - tax) + a_dep
    print("\nPRACTICE")
    print(f"thin ebit {eur(thin_ebit)} ocf {eur(thin_ocf)}")
    for rate in (0.08, 0.06):
        print(f"thin npv at {pct(rate)} {eur(npv_project(thin_ocf, a_capex, a_nwc, rate))}")

    beta_firm = 1.20
    ke_firm = rf + beta_firm * erp
    wacc_firm = (equity / v) * ke_firm + (debt / v) * rate_debt * (1 - tax)
    print(f"beta 1.20 ke {pct(ke_firm)} wacc {pct(wacc_firm)} exact {wacc_firm:.6f}")

    # Bad year: cover of 4 on EBIT 2.8m allows interest of 700k. Old loan already costs 400k.
    interest_room = ebit_down / 4 - interest
    debt_room = interest_room / rate2
    print(f"interest room {eur(interest_room)} new debt room at 5.5% {eur(debt_room)}")

    order_cost = 3_600_000
    interest_30 = order_cost * rate_debt * 30 / 365
    print(f"thirty-day interest on the order {eur(interest_30)}")

    # Buyer stands on the peer equity value, then takes 25% off Ingrid's 20%.
    peer_equity = 42_400_000
    ingrid_peer = peer_equity * ingrid
    ingrid_discounted = ingrid_peer * 0.75
    print(f"ingrid at 25% off the multiple {eur(ingrid_discounted)}")

    # Keep the revised line versus a dealer who pays 1.5m and takes the parts at cost.
    keep_pv = a_ocf_low * annuity(0.06, years) + pv(a_nwc, 0.06, years)
    dealer_now = 1_500_000 + a_nwc
    print(f"keep pv {eur(keep_pv)} five cash flows {eur(a_ocf_low * annuity(0.06, years))} parts pv {eur(pv(a_nwc, 0.06, years))}")
    print(f"dealer plus parts {eur(dealer_now)} stop ahead by {eur(dealer_now - keep_pv)}")

    # Same line, tax at the Munich stack instead of 30%.
    muc_tax_on_ebit = a_ebit * munich
    muc_cash = a_ebit - muc_tax_on_ebit + a_dep
    print(f"line cash at munich stack {eur(muc_cash)} tax on ebit {eur(muc_tax_on_ebit)}")

    flattery_share = warranty / gross
    print(f"warranty flattery as a share of gross profit {flattery_share:.5f}")

    # Year-by-year present value of the calibration line, so the annuity can be checked by hand.
    print("\nLINE YEAR BY YEAR")
    for t in range(1, years + 1):
        print(f"year {t} at 8% {eur(a_ocf / 1.08**t)} at 6% {eur(a_ocf / 1.06**t)}")
    undisc = a_ocf * years
    undisc_surplus = undisc + a_nwc - a_capex - a_nwc
    print(f"five cash flows undiscounted {eur(undisc)} surplus if parts come back {eur(undisc_surplus)}")
    running = -a_capex - a_nwc
    for t in range(1, years + 1):
        running += a_ocf
        print(f"cash recovered by end of year {t} {eur(running)}")

    # per-share and a few check totals
    print("\nCHECKS")
    print(f"balance sheet balances {assets == payables + debt + equity}")
    print(f"gross margin {gross/revenue:.4f}")
    print(f"a ocf identity {a_ocf == a_ebit*(1-tax)+a_dep}")


if __name__ == "__main__":
    main()
