import customtkinter as ctk
from fpdf import FPDF  # pip install fpdf

# Initialize customtkinter
ctk.set_appearance_mode("dark")  # Modes: "light", "dark"
ctk.set_default_color_theme("blue")  # Themes: "blue", "dark-blue", "green"

# Menu dictionary
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

# Create the main window first
root = ctk.CTk()
root.title("QuickEats")
root.geometry("800x600")

# Now initialize variables with the root as master
order_total = ctk.IntVar(master=root, value=0)
order_items = {}  # Dictionary mapping item -> quantity

def update_order_display():
    """Refresh the order summary textbox and total amount label."""
    textbox_order.configure(state="normal")
    textbox_order.delete("0.0", ctk.END)
    for item, qty in order_items.items():
        item_total = menu[item] * qty
        textbox_order.insert(ctk.END, f"{item} x {qty} - ₹{item_total}\n")
    textbox_order.configure(state="disabled")
    label_total.configure(text=f"Total Amount: ₹{order_total.get()}")

def add_item(item, qty_entry):
    """Add the specified item with given quantity to the order."""
    try:
        qty = int(qty_entry.get())
        if qty <= 0:
            label_status.configure(text="Quantity must be positive.")
            return
    except ValueError:
        label_status.configure(text="Invalid quantity.")
        return
    # Update order_items dictionary
    if item in order_items:
        order_items[item] += qty
    else:
        order_items[item] = qty
    # Update total amount
    current_total = order_total.get()
    order_total.set(current_total + menu[item] * qty)
    label_status.configure(text=f"Added {qty} x {item} to your order.")
    # Reset quantity entry to default "1"
    qty_entry.delete(0, ctk.END)
    qty_entry.insert(0, "1")
    update_order_display()

def clear_order():
    """Clear the current order."""
    order_items.clear()
    order_total.set(0)
    textbox_order.configure(state="normal")
    textbox_order.delete("0.0", ctk.END)
    textbox_order.configure(state="disabled")
    label_total.configure(text="Total Amount: ₹0")
    label_status.configure(text="Order cleared.")

def generate_pdf():
    """Generate a PDF file including order details."""
    pdf = FPDF()
    pdf.add_page()
    # Ensure "DejaVuSans.ttf" is in the same directory or update the path.
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=16)
    pdf.cell(200, 10, txt="QuickEats Order Details", ln=1, align="C")
    pdf.ln(10)
    pdf.set_font("DejaVu", size=12)
    for item, qty in order_items.items():
        line = f"{item} x {qty} - ₹{menu[item] * qty}"
        pdf.cell(200, 10, txt=line, ln=1)
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Total Amount: ₹{order_total.get()}", ln=1)
    pdf.output("order_details.pdf")



def place_order():
    """Simulate placing the order and generate PDF."""
    if order_total.get() > 0:
        generate_pdf()
        label_status.configure(text="Order placed! PDF generated as 'order_details.pdf'.")
        clear_order()
    else:
        label_status.configure(text="No items in order.")

# Layout the UI with a grid: left for menu, right for order summary/actions
left_frame = ctk.CTkFrame(root)
left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
right_frame = ctk.CTkFrame(root)
right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Left Frame: Menu Items
label_menu_title = ctk.CTkLabel(left_frame, text="Menu", font=("Helvetica", 18))
label_menu_title.pack(pady=10)

# For each menu item, create a row with name, price, quantity entry, and an Add button.
for item, price in menu.items():
    item_frame = ctk.CTkFrame(left_frame)
    item_frame.pack(pady=5, fill="x", padx=10)
    
    label_item = ctk.CTkLabel(item_frame, text=f"{item} - ₹{price}", anchor="w")
    label_item.pack(side="left", padx=5)
    
    qty_entry = ctk.CTkEntry(item_frame, width=50)
    qty_entry.insert(0, "1")
    qty_entry.pack(side="left", padx=5)
    
    btn_add = ctk.CTkButton(item_frame, text="Add", 
                            command=lambda item=item, qty_entry=qty_entry: add_item(item, qty_entry))
    btn_add.pack(side="left", padx=5)

# Right Frame: Order Summary and Actions
label_order_title = ctk.CTkLabel(right_frame, text="Your Order", font=("Helvetica", 18))
label_order_title.pack(pady=10)

textbox_order = ctk.CTkTextbox(right_frame, height=200)
textbox_order.pack(pady=10, fill="both", expand=True)
textbox_order.configure(state="disabled")

label_total = ctk.CTkLabel(right_frame, text="Total Amount: ₹0", font=("Helvetica", 16))
label_total.pack(pady=10)

# Order Action Buttons
action_frame = ctk.CTkFrame(right_frame)
action_frame.pack(pady=10, fill="x", padx=10)

btn_clear = ctk.CTkButton(action_frame, text="Clear Order", command=clear_order)
btn_clear.pack(side="left", padx=10)

btn_place = ctk.CTkButton(action_frame, text="Place Order", command=place_order)
btn_place.pack(side="left", padx=10)

# Status Label (across the bottom)
label_status = ctk.CTkLabel(root, text="", font=("Helvetica", 14))
label_status.grid(row=1, column=0, columnspan=2, pady=10)

root.mainloop()
