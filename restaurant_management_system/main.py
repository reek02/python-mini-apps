import customtkinter as ctk

# Initialize customtkinter
ctk.set_appearance_mode("light")  # Modes: "light" (default), "dark"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "dark-blue", "green"

menu = {
    'Pizza': 40,
    'Pasta': 50,
    'Burger': 60,
    'Salads': 70,
    'Coffee': 80,
    'Sandwich': 30,
    'Tea': 20,
    'Juice': 25,
    'Fries': 35,
    'Ice Cream': 45 
}

# Function to add item to order
def add_item():
    item = entry_item.get()
    if item in menu:
        order_total.set(order_total.get() + menu[item])
        order_items.append(item)
        textbox_order.insert(ctk.END, item + "\n")
        label_status.configure(text=f"Added {item} to your order.")
    else:
        label_status.configure(text=f"{item} is not available.")
    entry_item.delete(0, ctk.END)

# Create the main window
root = ctk.CTk()
root.title("QuickEats")
root.geometry("600x400")

# Create widgets
label_title = ctk.CTkLabel(root, text="Welcome to QuickEats", font=("Helvetica", 16))
label_menu = ctk.CTkLabel(root, text="Menu:\nPizza : Rs40\nPasta : Rs50\nBurger : Rs60\nSalads : Rs70\nCoffee : Rs80", justify=ctk.LEFT)
entry_item = ctk.CTkEntry(root, placeholder_text="Enter food item")
button_add = ctk.CTkButton(root, text="Add to Order", command=add_item)
label_status = ctk.CTkLabel(root, text="")
textbox_order = ctk.CTkTextbox(root, height=100)
label_total = ctk.CTkLabel(root, text="Total Amount: Rs 0")

# Variables
order_total = ctk.IntVar(value=0)
order_items = []

# Update total amount label
def update_total():
    label_total.configure(text=f"Total Amount: Rs{order_total.get()}")

# Bind total update to changes in order_total
order_total.trace_add("write", lambda *args: update_total())

# Layout widgets
label_title.pack(pady=10)
label_menu.pack(pady=10)
entry_item.pack(pady=10)
button_add.pack(pady=10)
label_status.pack(pady=10)
textbox_order.pack(pady=10, fill=ctk.BOTH, expand=True)
label_total.pack(pady=10)

# Run the main loop
root.mainloop()

