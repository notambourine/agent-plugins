---
marp: true
theme: nt
paginate: true
footer: Ecommerce retailer / Site speed review
---

<!-- _class: lead -->

<p class="eyebrow">Site speed review</p>

# pages that load _lighter_

What the September release changed, and what ships next.

<p class="eyebrow">October 2026</p>

---

<p class="eyebrow">Agenda</p>

## four things to _decide_

1. Results from the September release
2. Where load time still goes
3. What ships next quarter
4. Decisions we need today

---

<!-- _class: divider -->

<p class="eyebrow">01 / Results</p>

# the _results_

---

<!-- _class: stats -->

<p class="eyebrow">01 / Results</p>

## mobile pages got _4x_ lighter

- **4x**
  lighter mobile pages, 206 MB to 48 MB across audited pages
- **5 s**
  mobile LCP, down from 8.4
- **0**
  layout shift on every audited page

<p class="eyebrow">Lighthouse, before and after 30 September 2026</p>

---

<p class="eyebrow">02 / Load time</p>

## the cart is still the _slowest_ page

Cart LCP fell from 9.2 s to 6.2 s on mobile. It still trails every other page by more than a second.

- Third-party scripts block first render
- Product images ship at desktop size
- The promo banner shifts after load

<p class="eyebrow">Mobile cart, median of five runs</p>

---

<p class="eyebrow">02 / Load time</p>

## every page _faster_, cart last

| Page    | Mobile LCP before | Mobile LCP after |
| ------- | ----------------- | ---------------- |
| Home    | 7.9 s             | 4.6 s            |
| Product | 8.4 s             | 5.0 s            |
| Cart    | 9.2 s             | 6.2 s            |

<p class="eyebrow">Lighthouse mobile, audited pages</p>

---

<!-- _class: split -->

<p class="eyebrow">03 / Next quarter</p>

## what ships _next_

- Defer the reviews widget
- Resize product images at the edge
- Reserve space for the promo banner
- Preload the cart's hero font
- Drop the unused A/B script
- Budget page weight in CI

---

<!-- _class: quote -->

> Checkout feels instant now. Support tickets about the cart stopped.
>
> _Head of ecommerce_

---

![bg right:40% contain](../logo/export/mark-1024.png)

<p class="eyebrow">03 / Next quarter</p>

## one budget, _enforced_

CI fails a pull request that adds page weight past the budget. The number stays where this release put it.

---

<p class="eyebrow">03 / Next quarter</p>

## the budget _check_

![w:420](../logo/export/lockup-1024.png)

_A failing check on a pull request that adds 400 KB._

---

<p class="eyebrow">04 / Decisions</p>

## what we need _today_

1. Approve removing the reviews widget from the cart
2. Name an owner for the page-weight budget
3. Confirm the November release window

[Start a conversation](https://notambourine.com/tom)
