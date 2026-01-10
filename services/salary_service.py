from services.sheets_shifts import get_shifts, get_revenue
from services.sheet_month_setting import get_month_setting
from services.sheets_penalties import get_penalties

# смена 
SHIFT_PAY = 1000  # за одну смену
# категория
CATEGORY_PAY = {
    1: 300,  # 🥇
    2: 200,  # 🥈
    3: 0     # 🥉
}
# выручка
REVENUE_THRESHOLDS = [
    (5000, 50), (7500, 100), (10000, 150), (15000, 200),
    (20000, 250), (25000, 300), (30000, 350), (35000, 400),
    (40000, 450), (45000, 600), (50000, 750), (55000, 900),
    (60000, 1050), (65000, 1200), (70000, 1350), (75000, 1500),
    (80000, 1650), (85000, 1800), (90000, 1950), (95000, 2100),
    (100000, 2250)
]
# План
PLAN_BONUS = [
    (95, 55.5), (100, 111), (105, 166.5), (110, 222),
    (115, 277.5), (120, 333)
]

def revenue_bonus(revenue):
    if revenue < 5000:
        return 0
    for i in range(len(REVENUE_THRESHOLDS)-1):
        rev_low, pay_low = REVENUE_THRESHOLDS[i]
        rev_high, pay_high = REVENUE_THRESHOLDS[i+1]
        if revenue < rev_high:
            return pay_low + (revenue - rev_low) * (pay_high - pay_low) / (rev_high - rev_low)
    return REVENUE_THRESHOLDS[-1][1]

def plan_bonus(plan_percent):
    if plan_percent is None:
        return 0

    plan_percent = int(plan_percent)

    for perc, bonus in reversed(PLAN_BONUS):
        if plan_percent >= perc:
            return bonus
    return 0


def calculate_salary(user_id, month_key):
    #Смены
    shifts = get_shifts(user_id, month_key)
    revenues = get_revenue(user_id, month_key)
    shifts_count = len(shifts)
    shift_pay = shifts_count * SHIFT_PAY
    

    setting = get_month_setting(user_id, month_key)
    category = setting.get("category", 3)
    plan_percent = setting.get("plan")

    category_bonus = shifts_count * CATEGORY_PAY.get(category, 0)

    total_revenue = sum(revenues)
    revenue_bonus_value = sum(revenue_bonus(r) for r in revenues)
   

    plan_bonus_per_shift = plan_bonus(plan_percent)
    plan_bonus_total = shifts_count * plan_bonus_per_shift

    penalties = get_penalties(user_id, month_key)
    penalties_total = sum(p["amount"] for p in penalties)



    total = (
        shift_pay
        + category_bonus
        + revenue_bonus_value
        + plan_bonus_total
        - penalties_total
    )
    
    return {
        "shifts_count": shifts_count,
        "shift_pay": shift_pay,
        "category" : category, 
        "category_bonus": category_bonus,
        "revenue_bonus": revenue_bonus_value,
        "plan_percent": plan_percent,
        "plan_bonus_total": plan_bonus_total,
        "penalties": penalties,
        "penalties_total": penalties_total,
        "total": total
    }
