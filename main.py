import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description
import matplotlib.pyplot as plt


class CSV:
  # class variable - associated with the class itself
  CSV_FILE = "finance_data.csv" 
  COLUMNS = ["date", "amount", "category", "description"]
  FORMAT = "%d-%m-%Y"

  @classmethod # class method declarator - this will have access to the class itself but not on the instance of the class
  # INITIALIZE CSV file
  def initialize_csv(cls):
    try:
      pd.read_csv(cls.CSV_FILE)
    except FileNotFoundError:
      df = pd.DataFrame(columns=cls.COLUMNS)
      df.to_csv(cls.CSV_FILE, index=False)

  @classmethod
  # ADD entry to CSV file
  def add_entry(cls, date, amount, category, description):
    # create entry - store the data in a python dictionary
    new_entry = {
      "date": date,
      "amount": amount,
      "category": category,
      "description": description
    }
    # a means append to the dictionary
    # WITH means context manager - automatically handles closing the file after the block of code is executed
    with open(cls.CSV_FILE, "a", newline="") as csvfile: 
      # CSV Writer - take a dictionary and write to a CSV file
      writer =  csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
      writer.writerow(new_entry)
    print("Entry added successfully!")

  @classmethod
  def get_transactions(cls, start_date, end_date):
      df = pd.read_csv(cls.CSV_FILE)
      df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
      start_date = datetime.strptime(start_date, CSV.FORMAT)
      end_date = datetime.strptime(end_date, CSV.FORMAT)

      mask = (df["date"] >= start_date) & (df["date"] <= end_date)
      # return a new filtered dataframe where the date is within the range
      filtered_df = df.loc[mask]

      if filtered_df.empty:
        print("No transactions found within the specified date range.")
      else:
        print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}:")
        print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}))

        total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
        total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
        print("\nSummary:")
        print(f"Total Income: P{total_income:.2f}")
        print(f"Total Expense: P{total_expense:.2f}")
        print(f"Net Income: P{(total_income - total_expense):.2f}")

      return filtered_df

def add():
  CSV.initialize_csv()
  date = get_date(
    "Enter transaction date (DD-MM-YYYY) or leave it blank for today's date: ",
    allow_default=True
  )
  amount = get_amount()
  category = get_category()
  description = get_description()
  CSV.add_entry(date, amount, category, description)


def plot_transactions(df):
  # allows to find different rows and entries using the date column
  df.set_index("date", inplace=True)

  # D = daily frequency
  income_df = (
    df[df["category"] == "Income"]
    .resample("D")
    .sum()
    .reindex(df.index, fill_value=0)
  ) 

  expense_df = (
    df[df["category"] == "Expense"]
    .resample("D")
    .sum()
    .reindex(df.index, fill_value=0)
  ) 

  # setup screen for the graph
  plt.figure(figsize=(10, 5))
  plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
  plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
  plt.xlabel("Date")
  plt.ylabel("Amount")
  plt.title("Income vs Expense")
  plt.legend()
  plt.grid(True)
  plt.show()

def main():
  while True:
    print("\nTrackFin\n")
    print("1. Add new transaction")
    print("2. View transactions")
    print("3. Exit")
    choice = input("Enter choice (1-3): ")

    if choice == "1":
      add()
    elif choice == "2":
      start_date = get_date("Enter start date (DD-MM-YYYY): ")
      end_date = get_date("Enter end date (DD-MM-YYYY) or leave it blank for today's date: ", allow_default=True)
      df = CSV.get_transactions(start_date, end_date)
      if input("Do you want to see the plot of transactions? (Y/N): ").upper() == "Y":
        plot_transactions(df)
    elif choice == "3":
      print("Exiting program...")
      break
    else:
      print("Invalid choice. Please enter a number from 1-3.")


if __name__ == "__main__":
  main()
      