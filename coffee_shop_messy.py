#!/usr/bin/env python3
"""
Coffee Shop Ordering System
Version 7.4 - "It works, don't touch it"

Started as a simple order system. Got... complicated.
Good luck!
"""

# Global variables (added over time)
menu = {
    'latte': 4.50,
    'cappuccino': 4.25,
    'espresso': 3.50,
    'americano': 3.75,
    'mocha': 5.00
}

loyalty_accounts = {}  # {customer_name: points}
member_list = ['alice', 'bob', 'charlie']  # Members get discount
daily_sales = 0.0
order_count = 0
member_discount = 0.10
points_per_dollar = 1
free_drink_points = 100

def take_order():
    """Main order function - handles everything."""
    global daily_sales, order_count
    
    print("\n=== New Order ===")
    customer_name = input("Customer name: ").strip().lower()
    
    # Check if member
    is_member = customer_name in member_list
    if is_member:
        print(f"Welcome back, {customer_name.title()}! (Member discount applies)")
    
    # Get drink
    print("\nAvailable drinks:")
    for drink in menu:
        print(f"  - {drink.title()}")
    
    drink_name = input("Drink: ").strip().lower()
    
    # Validate drink
    if drink_name not in menu:
        print("Error: Drink not on menu")
        return
    
    base_price = menu[drink_name]
    
    # Get size
    size = input("Size (small/medium/large): ").strip().lower()
    
    # Calculate size price
    if size == 'small':
        price = base_price * 1.0
    elif size == 'medium':
        price = base_price * 1.3
    elif size == 'large':
        price = base_price * 1.6
    else:
        print("Error: Invalid size")
        return
    
    # Milk options
    milk_type = input("Milk (whole/skim/oat/almond/none): ").strip().lower()
    
    # Milk surcharge
    if milk_type == 'oat':
        price += 0.50
    elif milk_type == 'almond':
        price += 0.50
    elif milk_type == 'whole' or milk_type == 'skim' or milk_type == 'none':
        pass  # No extra charge
    else:
        print("Error: Invalid milk type")
        return
    
    # Extras
    extra_shot = input("Extra shot? (y/n): ").strip().lower()
    if extra_shot == 'y':
        price += 1.00
    
    whipped_cream = input("Whipped cream? (y/n): ").strip().lower()
    if whipped_cream == 'y':
        price += 0.75
    
    # Apply member discount
    if is_member:
        discount_amount = price * member_discount
        price = price - discount_amount
        print(f"Member discount applied: -${discount_amount:.2f}")
    
    # Total before loyalty
    print(f"\nTotal: ${price:.2f}")
    
    # Ask about loyalty points
    use_points = input("Redeem loyalty points for free drink? (y/n): ").strip().lower()
    
    if use_points == 'y':
        if customer_name not in loyalty_accounts:
            print("No loyalty account found.")
            loyalty_accounts[customer_name] = 0
        
        current_points = loyalty_accounts[customer_name]
        print(f"Current points: {current_points}")
        
        if current_points >= free_drink_points:
            # Free drink must be small
            if size != 'small':
                print("Error: Free drinks must be small size")
                return
            
            # Deduct points
            loyalty_accounts[customer_name] -= free_drink_points
            price = 0.0
            print(f"Free drink! Points remaining: {loyalty_accounts[customer_name]}")
        else:
            print(f"Not enough points. Need {free_drink_points}, have {current_points}")
    
    # Final payment
    if price > 0:
        payment = float(input(f"Payment (total ${price:.2f}): $"))
        
        if payment < price:
            print("Error: Insufficient payment")
            return
        
        change = payment - price
        if change > 0:
            print(f"Change: ${change:.2f}")
        
        # Add loyalty points (if not free drink)
        if use_points != 'y' or loyalty_accounts.get(customer_name, 0) < free_drink_points:
            points_earned = int(price * points_per_dollar)
            if customer_name not in loyalty_accounts:
                loyalty_accounts[customer_name] = 0
            loyalty_accounts[customer_name] += points_earned
            print(f"Loyalty points earned: {points_earned}")
            print(f"Total loyalty points: {loyalty_accounts[customer_name]}")
    
    # Update daily totals
    daily_sales += price
    order_count += 1
    
    # Receipt
    print("\n--- Receipt ---")
    print(f"Customer: {customer_name.title()}")
    print(f"Drink: {drink_name.title()} ({size})")
    if milk_type != 'none':
        print(f"Milk: {milk_type.title()}")
    if extra_shot == 'y':
        print("Extra shot")
    if whipped_cream == 'y':
        print("Whipped cream")
    if is_member:
        print("Member discount applied")
    print(f"Total: ${price:.2f}")
    print("Thank you!")
    print("---------------\n")


def staff_order():
    """Handle staff drinks - free but track for inventory."""
    global order_count
    
    print("\n=== Staff Order ===")
    
    # Get drink
    print("Available drinks:")
    for drink in menu:
        print(f"  - {drink.title()}")
    
    drink_name = input("Drink: ").strip().lower()
    
    if drink_name not in menu:
        print("Error: Drink not on menu")
        return
    
    # Get size  
    size = input("Size (small/medium/large): ").strip().lower()
    if size not in ['small', 'medium', 'large']:
        print("Error: Invalid size")
        return
    
    # Staff drinks always free
    price = 0.0
    order_count += 1
    
    print(f"\nStaff drink: {drink_name.title()} ({size})")
    print("Total: $0.00 (Staff)")
    print("Recorded for inventory.\n")


def daily_report():
    """Print and save daily sales report."""
    global daily_sales, order_count
    
    print("\n=== Daily Sales Report ===")
    print(f"Total orders: {order_count}")
    print(f"Total sales: ${daily_sales:.2f}")
    
    if order_count > 0:
        avg_order = daily_sales / order_count
        print(f"Average order: ${avg_order:.2f}")
    
    # Save to file
    try:
        with open('daily_sales.txt', 'a') as f:
            f.write(f"Orders: {order_count}, Sales: ${daily_sales:.2f}\n")
        print("Report saved to daily_sales.txt")
    except:
        print("Error: Could not save report")
    
    print("=========================\n")


def reset_day():
    """Reset daily counters."""
    global daily_sales, order_count
    daily_sales = 0.0
    order_count = 0
    print("Daily counters reset.\n")


def view_loyalty():
    """Show all loyalty accounts."""
    print("\n=== Loyalty Accounts ===")
    if not loyalty_accounts:
        print("No accounts yet.")
    else:
        for name, points in loyalty_accounts.items():
            print(f"{name.title()}: {points} points")
    print("========================\n")


def main_menu():
    """Main program loop."""
    while True:
        print("\n======= Coffee Shop POS =======")
        print("1. Take Order")
        print("2. Staff Order (Free)")
        print("3. Daily Report")
        print("4. View Loyalty Accounts")
        print("5. Reset Daily Counters")
        print("6. Exit")
        print("===============================")
        
        choice = input("Choice: ").strip()
        
        if choice == '1':
            take_order()
        elif choice == '2':
            staff_order()
        elif choice == '3':
            daily_report()
        elif choice == '4':
            view_loyalty()
        elif choice == '5':
            reset_day()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Error: Invalid choice")


if __name__ == '__main__':
    main_menu()