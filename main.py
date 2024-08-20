import os
import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import requests
from PIL import Image, ImageTk
from io import BytesIO
import webbrowser
import mplcursors
import threading


# Function to set the date range based on the number of months
def set_date_range(months):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30 * months)
    start_entry.delete(0, tk.END)
    start_entry.insert(0, start_date.strftime("%Y-%m-%d"))
    end_entry.delete(0, tk.END)
    end_entry.insert(0, end_date.strftime("%Y-%m-%d"))


# Function to fetch and plot stock data
def fetch_and_plot():
    ticker = ticker_entry.get().upper()
    start_date = start_entry.get()
    end_date = end_entry.get()

    def fetch_data():
        try:
            # Start the loading indicator
            progress_bar.grid(row=0, column=0, sticky="ew")
            progress_bar.start()

            # Input validation
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")

            stock_data = yf.download(ticker, start=start_date, end=end_date)
            if stock_data.empty:
                messagebox.showerror("Error", f"No data found for {ticker}.")
                return

            # Clear the previous plot
            for widget in plot_frame.winfo_children():
                widget.destroy()

            # Plotting the data with a darker and sharper style
            plt.style.use('dark_background')  # Dark background style
            fig, ax = plt.subplots(figsize=(8, 6))  # Initial size
            ax.plot(stock_data.index, stock_data['Close'], color='cyan', linewidth=2)

            ax.set_title(f"{ticker} Closing Prices", color='white')
            ax.set_xlabel("Date", color='white')
            ax.set_ylabel("Close Price", color='white')

            ax.grid(True, color='gray', linestyle='--')
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')

            # Adding hover functionality to display data points
            cursor = mplcursors.cursor(ax, hover=True)
            def on_hover(sel):
                y_price = sel.target[1]
                sel.annotation.arrow_patch.set_color('white')  # Change arrow color to white
                sel.annotation.set_text(f"${y_price:.2f}\n")  # Display only price

            cursor.connect("add", on_hover)

            # Embedding the plot in the tkinter GUI
            canvas = FigureCanvasTkAgg(fig, master=plot_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

            # Configure resizing
            plot_frame.grid_rowconfigure(0, weight=1)
            plot_frame.grid_columnconfigure(0, weight=1)

            # Fetch and display news stories
            fetch_news(ticker)

        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch data: {str(e)}")
        finally:
            # Stop the loading indicator
            progress_bar.stop()
            progress_bar.grid_forget()

    thread = threading.Thread(target=fetch_data)
    thread.daemon = True
    thread.start()

# Function to fetch news stories
def fetch_news(ticker):
    def fetch_news_data():
        news_frame.grid_forget()
        news_frame.grid(row=1, column=0, sticky="nsew")
        for widget in news_frame.winfo_children():
            widget.destroy()

        # Fetch news from the API
        news_api_url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey=d1bdbb9069e6456a94211d034d0a9430"
        response = requests.get(news_api_url)
        if response.status_code == 200:
            news_data = response.json()
            if news_data.get("status") == "ok":
                for article in news_data.get("articles", []):
                    title = article.get("title")
                    description = article.get("description")
                    image_url = article.get("urlToImage")
                    url = article.get("url")

                    # Create a frame for each news article
                    article_frame = ttk.Frame(news_frame, padding="5")
                    article_frame.grid(sticky="ew", padx=5, pady=5)

                    # Display the image if available
                    if image_url:
                        try:
                            image_response = requests.get(image_url)
                            if image_response.status_code == 200:
                                image_data = image_response.content
                                try:
                                    image = Image.open(BytesIO(image_data))
                                    image = image.resize((100, 100), Image.LANCZOS)
                                    photo = ImageTk.PhotoImage(image)
                                    image_label = ttk.Label(article_frame, image=photo)
                                    image_label.image = photo  # Keep a reference to avoid garbage collection
                                    image_label.grid(row=0, column=0, padx=5)
                                    # Fix reference issue by using a closure
                                    image_label.bind("<Button-1>", lambda e, url=url: webbrowser.open_new(url))
                                except Exception as e:
                                    print(f"Failed to open image: {e}")
                            else:
                                print(f"Failed to fetch image. Status code: {image_response.status_code}")
                        except Exception as e:
                            print(f"Failed to load image: {e}")

                    # Display the title and description
                    text_frame = ttk.Frame(article_frame)
                    text_frame.grid(row=0, column=1, sticky="ew")
                    ttk.Label(text_frame, text=title, font=("Helvetica", 12, "bold")).grid(row=0, column=0, sticky="w", padx=5)
                    ttk.Label(text_frame, text=description, wraplength=300).grid(row=1, column=0, sticky="w", padx=5)
            else:
                messagebox.showerror("Error", "Failed to fetch news stories.")
        else:
            messagebox.showerror("Error", f"Failed to fetch news stories. Status code: {response.status_code}")

    thread = threading.Thread(target=fetch_news_data)
    thread.daemon = True
    thread.start()

# Function to handle window close event
def on_closing():
    root.destroy()

# Creating the main window
root = tk.Tk()
root.title("Stock Analyzer")
root.geometry("800x1000")  # Portrait orientation with more space

# Bind the window close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Frame for input controls
input_frame = ttk.Frame(root, padding="10")
input_frame.grid(row=0, column=0, sticky="ew")

# Ticker input
ttk.Label(input_frame, text="Stock Ticker:").grid(row=0, column=0, padx=5)
ticker_entry = ttk.Entry(input_frame)
ticker_entry.grid(row=0, column=1, padx=5)

# Start date input
ttk.Label(input_frame, text="Start Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5)
start_entry = ttk.Entry(input_frame)
start_entry.grid(row=1, column=1, padx=5)

# End date input
ttk.Label(input_frame, text="End Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5)
end_entry = ttk.Entry(input_frame)
end_entry.grid(row=2, column=1, padx=5)

# Date range buttons
ttk.Button(input_frame, text="1 Month", command=lambda: set_date_range(1)).grid(row=3, column=0, padx=5, pady=5)
ttk.Button(input_frame, text="2 Months", command=lambda: set_date_range(2)).grid(row=3, column=1, padx=5, pady=5)
ttk.Button(input_frame, text="3 Months", command=lambda: set_date_range(3)).grid(row=3, column=2, padx=5, pady=5)

# Fetch button
fetch_button = ttk.Button(input_frame, text="Fetch Data", command=fetch_and_plot)
fetch_button.grid(row=4, column=0, columnspan=3, pady=5)

# Frame for the plot
plot_frame = ttk.Frame(root)
plot_frame.grid(row=1, column=0, sticky="nsew")

# Scrollable frame for news stories
scroll_canvas = tk.Canvas(root)
scroll_canvas.grid(row=2, column=0, sticky="nsew")

scrollbar = ttk.Scrollbar(root, orient="vertical", command=scroll_canvas.yview)
scrollbar.grid(row=2, column=1, sticky="ns")

scroll_frame = ttk.Frame(scroll_canvas)
scroll_frame.bind(
    "<Configure>",
    lambda e: scroll_canvas.configure(
        scrollregion=scroll_canvas.bbox("all")
    )
)
scroll_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
scroll_canvas.configure(yscrollcommand=scrollbar.set)

news_frame = ttk.Frame(scroll_frame)
news_frame.grid(sticky="nsew")

# Progress bar for loading indicator
progress_bar = ttk.Progressbar(input_frame, mode='indeterminate')

# Configure resizing
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
scroll_frame.grid_rowconfigure(0, weight=1)
scroll_frame.grid_columnconfigure(0, weight=1)

# Running the main loop
root.mainloop()