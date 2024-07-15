import customtkinter as ctk

# Initialize customtkinter
ctk.set_appearance_mode("dark")  # Modes: "light" (default), "dark"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (default), "dark-blue", "green"

# Function to calculate the output
def calculate_payment():
    try:
        rent = int(entry_rent.get())
        food = int(entry_food.get())
        electricity_spent = int(entry_electricity_spent.get())
        charge_per_unit = int(entry_charge_per_unit.get())
        persons = int(entry_persons.get())

        total_electricity_bill = electricity_spent * charge_per_unit
        output = (food + rent + total_electricity_bill) // persons

        label_result.configure(text=f"Each person will pay = {output} Rs.")
    except ValueError:
        label_result.configure(text="Please enter valid numbers.")

# Create the main window
root = ctk.CTk()
root.title("Rent Calculator")
root.geometry("400x500")

# Create widgets
label_title = ctk.CTkLabel(root, text="Rent Calculator", font=("Helvetica", 16), text_color="white")
entry_rent = ctk.CTkEntry(root, placeholder_text="Enter your hostel / flat rent", width=300)
entry_food = ctk.CTkEntry(root, placeholder_text="Enter the amount of food ordered", width=300)
entry_electricity_spent = ctk.CTkEntry(root, placeholder_text="Enter the total amount of electricity spent", width=300)
entry_charge_per_unit = ctk.CTkEntry(root, placeholder_text="Enter the amount of charge per unit", width=300)
entry_persons = ctk.CTkEntry(root, placeholder_text="Enter the number of persons living in room / flat", width=300)
button_calculate = ctk.CTkButton(root, text="Calculate", command=calculate_payment)
label_result = ctk.CTkLabel(root, text="", text_color="grey")

# Layout widgets
label_title.pack(pady=10)
entry_rent.pack(pady=10)
entry_food.pack(pady=10)
entry_electricity_spent.pack(pady=10)
entry_charge_per_unit.pack(pady=10)
entry_persons.pack(pady=10)
button_calculate.pack(pady=20)
label_result.pack(pady=10)

# Run the main loop
root.mainloop()

