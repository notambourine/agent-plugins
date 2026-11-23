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

<!-- _class: dense -->

<p class="eyebrow">02 / Load time</p>

## ten of twelve pages got _faster_

| Page                                                                          | LCP before | LCP after |                                Change | Budget                               |
| ----------------------------------------------------------------------------- | ---------: | --------: | ------------------------------------: | ------------------------------------ |
| /                                                                             |      7.9 s |     4.6 s | <span class="down good">-41.8%</span> | <span class="pass">Pass</span>       |
| /products/merino-crew-neck-sweater                                            |      8.4 s |     5.0 s | <span class="down good">-40.5%</span> | <span class="pass">Pass</span>       |
| /cart                                                                         |      9.2 s |     6.2 s | <span class="down good">-32.6%</span> | <span class="fail">Fail</span>       |
| /collections/womens-outerwear/waterproof-jackets-and-shells?sort=best-selling |      8.8 s |     5.4 s | <span class="down good">-38.6%</span> | <span class="warn">Needs work</span> |
| /collections/mens                                                             |      8.1 s |     4.9 s | <span class="down good">-39.5%</span> | <span class="pass">Pass</span>       |
| /collections/sale                                                             |      8.6 s |     5.2 s | <span class="down good">-39.5%</span> | <span class="warn">Needs work</span> |
| /search                                                                       |      6.4 s |     4.4 s | <span class="down good">-31.3%</span> | <span class="pass">Pass</span>       |
| /account/login                                                                |      5.1 s |     3.9 s | <span class="down good">-23.5%</span> | <span class="pass">Pass</span>       |
| /pages/size-guide                                                             |      4.8 s |     4.8 s |        <span class="flat">0.0%</span> | <span class="pass">Pass</span>       |
| /pages/store-locator                                                          |      5.8 s |     6.0 s |     <span class="up bad">+3.4%</span> | <span class="warn">Needs work</span> |
| /blog/how-to-layer                                                            |      5.6 s |     4.1 s | <span class="down good">-26.8%</span> | <span class="pass">Pass</span>       |
| /checkout                                                                     |      7.2 s |     5.0 s | <span class="down good">-30.6%</span> | <span class="pass">Pass</span>       |

<p class="eyebrow">Lighthouse mobile LCP, before and after 30 September 2026, against a 5.0 s budget</p>

---

<!-- _class: stats -->

<p class="eyebrow">02 / Load time</p>

## the release in _six_ numbers

- **4x**
  lighter mobile pages, 206 MB to 48 MB
- **5.0 s**
  product LCP, <span class="down good">-40.5%</span> from 8.4 s
- **0**
  layout shift on every audited page
- **10**
  of 12 audited pages got faster
- **8**
  pages inside the 5.0 s budget
- **1**
  page still fails: the cart at 6.2 s

<p class="eyebrow">Lighthouse mobile, before and after 30 September 2026</p>

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

<!-- _class: shot -->

<p class="eyebrow">03 / Next quarter</p>

## the check, _full_ width

![The budget check](../logo/export/lockup-2048.png)

_The same check, as the reviewer sees it._

---

<!-- _class: compare -->

<p class="eyebrow">03 / Next quarter</p>

## the check on _both_ screens

- ![The budget check on desktop](../logo/export/lockup-1024.png)
  Desktop
- ![The budget check on a phone](../logo/export/monogram-1024.png)
  Phone

<p class="eyebrow">Captured 15 October 2026</p>

---

<p class="eyebrow">04 / Decisions</p>

## what we need _today_

1. Approve removing the reviews widget from the cart
2. Name an owner for the page-weight budget
3. Confirm the November release window

[Start a conversation](https://notambourine.com/tom)
