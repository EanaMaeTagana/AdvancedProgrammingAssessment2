"""

WIZARDINGWORLD 

"""

# All important imports to run the application
import tkinter as tk
import requests
import random
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO

class WizardingWorld:

    # Initialize the main window and setup its properties

    def __init__(self, root):
        self.root = root  # Store the main root window
        self.root.title("WizardingWorld")  # Set the title of the window
        self.root.config(bg="black")
        self.root.geometry("900x700")  # Set the window size (900x700 pixels)
        self.root.resizable(False, False)  # Makes the window non-resizable

        # Navigation Frame
        self.nav_frame = tk.Frame(self.root, bg="black")
        self.nav_frame.pack(side="top", pady=10)  

        # List of tabs for the user to navigate
        self.tabs = ["Home", "Characters", "Books", "Spells", "Movies"]
        self.buttons = {}  # Dictionary to store each section

        # For each tab, a button is created
        for tab in self.tabs:
            # Button for switching to the corresponding tab
            button = tk.Button(self.nav_frame, text=tab, command=lambda tab=tab: self.show_frame(tab))
            button.pack(side="left", padx=10)  # Packs the buttons with padding
            self.buttons[tab] = button  # Stores the buttons in the references

        # Content frame which will hold each frames content
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill="both", expand=True)  # Make sure that the frame takes up all the available space

        # Initially show the "Home" section
        self.show_frame("Home")

    # Function to show the content for the section which the user selects
    def show_frame(self, tab):
        # Destroy any existing widgets in the frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Call the appropriate function to create the content that will appear
        if tab == "Home":
            self.create_home_section()
        elif tab == "Characters":
            self.create_character_section()
        elif tab == "Books":
            self.create_books_section()
        elif tab == "Spells":
            self.create_spells_section()
        elif tab == "Movies":
            self.create_movies_section()

    """          HOME SECTION          """

    # Creates the interface for the home section
    def create_home_section(self):

        # Background Image
        self.backgroundimage = PhotoImage(file="backgroundimage.png")
        imagelabel = Label(self.content_frame, image = self.backgroundimage)
        imagelabel.place(x=-1, y=-1)

        # Gap
        gap = tk.Label(self.content_frame, text="", fg="white", bg="black")
        gap.pack(pady=120)

        # Title 
        character_section = tk.Label(self.content_frame, text="WELCOME TO THE WIZARDING WORLD!", font=('Tahoma', 46), fg="white", bg="black")
        character_section.pack(pady=5)

        # Descriptive label
        character_label = tk.Label(self.content_frame, text="Select a section to discover all there is to know in the wizarding world of Harry Potter...", font=('Helvetica', 20), fg="white", bg="black")
        character_label.pack(pady=5)

        # Navigation frame to hold the search entry and button
        nav_frame = tk.Frame(self.content_frame)
        nav_frame.pack(side="top", pady=20)


    """          CHARACTER SECTION          """

    # Creates the user interface for the character section
    def create_character_section(self):

        # Background Image
        self.backgroundimage = PhotoImage(file="backgroundimage.png")
        imagelabel = Label(self.content_frame, image = self.backgroundimage)
        imagelabel.place(x=-1, y=-1)

        # Gap
        gap = tk.Label(self.content_frame, text="", fg="white", bg="black")
        gap.pack(pady=5)

        # Title 
        character_section = tk.Label(self.content_frame, text="CHARACTERS", font=('Tahoma', 35), fg="white", bg="black")
        character_section.pack(pady=5)

        # Descriptive label
        character_label = tk.Label(self.content_frame, text="Enter the name of a character to learn more about them...", font=('Helvetica', 20), fg="white", bg="black")
        character_label.pack(pady=5)

        # Navigation frame to hold the search entry and button
        nav_frame = tk.Frame(self.content_frame)
        nav_frame.pack(side="top", pady=20)

        # Text entry in which user will input character name
        self.search_entry = tk.Entry(nav_frame, width=50)
        self.search_entry.pack(side="left", padx=10)

        # Search button which triggers the search function
        search_button = tk.Button(nav_frame, text="Search", command=self.search_characters)
        search_button.pack(side="left")

        # Gap
        gap = tk.Label(self.content_frame, text="", fg="white", bg="black")
        gap.pack(pady=5)

        # Canvas in which the searched content will appear in
        canvas = tk.Canvas(self.content_frame, width=800, height=500, bd=0)
        canvas.pack(side="left", fill="both", expand=True)

        # Scrollbar function to view all data
        scrollbar = tk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Individual frames which the character data will be presented
        self.character_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.character_frame, anchor="nw") # Creates the window 

        # Ensures the canvas scrolls correctly with the content inside
        self.character_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Handles the search function once user triggers the search button
    def search_characters(self):
        query = self.search_entry.get() # Gets the text input of the user
        if query.strip():
            characters = self.fetch_character_data(query) # Fetches the data based on what was entered
            self.display_characters(characters) # Displays the character data in the UI
        else:
            messagebox.showwarning("Input Error", "Please enter a character name to search.") # Error handling if no input was entered

    # Fetches the character data from the API
    def fetch_character_data(self, query):

        # API request URL with the query to filter the names
        url = f"https://api.potterdb.com/v1/characters?filter[name_cont]={query}&page[size]=25"
        
        try:
            # Sends a GET request to the API
            response = requests.get(url)

            # Raises an exception of error is returned
            response.raise_for_status()

            # Parse the response data as JSON
            data = response.json()

            # Returns data
            return data['data']
        
        # Handles errors
        except requests.exceptions.RequestException as e:
            messagebox.showerror("API Error", f"Error fetching data: {e}")
            return []

    # Displays the list of characters in the graphical interface
    def display_characters(self, characters):

        # Clears any existing widgets
        for widget in self.character_frame.winfo_children():
            widget.destroy()

        # Checks if any characters were returned
        if characters:
            # Loops through each item
            for character in characters:
                # Extracts each detail (name, house, status, gender, and nationality)
                # Some are defaulted to empty string if not available
                character_name = character['attributes']['name']
                character_house = character['attributes'].get('house', '')
                character_blood_status = character['attributes'].get('blood_status', '')
                character_gender = character['attributes'].get('gender', '')
                character_nationality = character['attributes'].get('nationality', '')
                
                # Creates a frame for each character to display their details
                character_frame = tk.LabelFrame(self.character_frame, text=character_name, padx=10, pady=10, width=850, height=155)
                character_frame.pack(fill="x", padx=10, pady=5)
                character_frame.grid_propagate(False)

                # Adds labels to each detail and puts them in a grid format
                tk.Label(character_frame, text="House:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
                tk.Label(character_frame, text=character_house).grid(row=0, column=1, sticky="w", padx=5, pady=2)
                tk.Label(character_frame, text="Blood Status:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
                tk.Label(character_frame, text=character_blood_status).grid(row=1, column=1, sticky="w", padx=5, pady=2)
                tk.Label(character_frame, text="Gender:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
                tk.Label(character_frame, text=character_gender).grid(row=2, column=1, sticky="w", padx=5, pady=2)
                tk.Label(character_frame, text="Nationality:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
                tk.Label(character_frame, text=character_nationality).grid(row=3, column=1, sticky="w", padx=5, pady=2)
        
        else: # Error shown if no characters are found
            messagebox.showinfo("No Results", "No characters found matching the search.")

    """          BOOKS SECTION          """

    # Creates the book section 
    def create_books_section(self):

        # Background Image
        self.backgroundimage = PhotoImage(file="backgroundimage.png")
        imagelabel = Label(self.content_frame, image = self.backgroundimage)
        imagelabel.place(x=-1, y=-1)

        # Title
        book_section = tk.Label(self.content_frame, text="BOOKS", font=('Tahoma', 35), fg="white", bg="black")
        book_section.grid(row=0, column=0, pady=5, padx=10, sticky="nsew")

        # Description label
        books_label = tk.Label(self.content_frame, text="The seven books of the Wizarding World.", font=('Helvetica', 20), fg="white", bg="black")
        books_label.grid(row=1, column=0, pady=5, padx=10, sticky="nsew")

        # Create a frame to hold the content of the section
        self.book_frame = tk.Frame(self.content_frame)
        self.book_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Fetch and display the data
        books = self.fetch_books_data("")
        self.display_books(books)

        # Creates the 4x4 grid for the layout of the books
        self.content_frame.grid_rowconfigure(2, weight=1)  # Allows the grid to expand
        self.content_frame.grid_columnconfigure(0, weight=1)  # Makes the first column take full width

    def fetch_books_data(self, query):

        # API URL request to get the data based on the query
        url = f"https://api.potterdb.com/v1/books?filter[title_cont]={query}&page[size]=25"
        
        try:
            response = requests.get(url) # Sends the GET request

            response.raise_for_status() # Raises an exception of error is returned

            data = response.json() # Parse as a JSON response

            return data['data'] # Return the data
        
        # Response shown when faced with an error
        except requests.exceptions.RequestException as e:
            messagebox.showerror("API Error", f"Error fetching data: {e}")
            return []

    # Function to display the books
    def display_books(self, books):
        # Destroys any existing widgets within the frame
        for widget in self.book_frame.winfo_children():
            widget.destroy()

        if books:
            # Places the book data in a 4x4 grid
            for index, book in enumerate(books):
                row = index // 4  # Calculates the rows
                col = index % 4   # Calculates the columns
                
                # Gets the book title and cover image from the data taken
                book_title = book['attributes']['title']
                book_cover_url = book['attributes'].get('cover', '')

                # Creates a frame for each book
                book_frame = tk.Frame(self.book_frame, relief="solid", bd=1)
                book_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

                inner_frame = tk.Frame(book_frame)
                inner_frame.pack(expand=True)

                # Displays the book's image 
                if book_cover_url:

                    try:
                        img_data = requests.get(book_cover_url).content # Gets the image data
                        img = Image.open(BytesIO(img_data)) # Opens the image
                        img.thumbnail((80, 130)) # Resizes the image
                        img = ImageTk.PhotoImage(img) # Concerts to a Tkinter image
                        img_label = tk.Label(inner_frame, image=img) # Creates a label for the image
                        img_label.image = img # Creates a reference to the image
                        img_label.pack(pady=5) # Places the image on the screen

                    # Error if an image is failed to load
                    except Exception as e:
                        tk.Label(inner_frame, text="Image Not Available").pack(pady=5)

                # Book title
                book_title_label = tk.Label(inner_frame, text=book_title, font=('Helvetica', 16), wraplength=150, justify="center")
                book_title_label.pack(pady=5)

                # View more button
                view_button = tk.Button(inner_frame, text="View More Details", command=lambda book=book: self.open_book_details(book))
                view_button.pack(pady=5)

            # Adjusts the grid to ensure the size stays the same
            for i in range(4):
                self.book_frame.grid_columnconfigure(i, weight=1)  # Equal space for each column
                self.book_frame.grid_rowconfigure(i, weight=1)  # Equal space for each row

        # Error if no book data is found
        else:
            messagebox.showinfo("No Results", "No books found.")

    # Function for when user opens details
    def open_book_details(self, book):

        # Creates a completely new window
        details_window = tk.Toplevel(self.root)
        details_window.title(f"{book['attributes']['title']}") # Sets window title
        details_window.geometry("400x400") # Window size
        details_window.config(bg="black")
        details_window.resizable(False, False)
        content_frame = tk.Frame(details_window, bg="black")
        content_frame.pack(expand=True, fill="both", pady=40) # Adds a content frame

        # Gets the book details from the data
        book_title = book['attributes']['title']
        book_author = book['attributes'].get('author', '')
        book_pages = book['attributes'].get('pages', '')
        book_dedication = book['attributes'].get('dedication', '')
        book_release_date = book['attributes'].get('release_date', '')
        book_summary = book['attributes'].get('summary', 'No summary available.')

        # Adds a label to each and displays the book details in within the frame 
        tk.Label(content_frame, text=f"{book_title}", font=('Helvetica', 16), wraplength=380, fg="white", bg="black").pack(pady=5)
        tk.Label(content_frame, text=f"Author: {book_author}", font=('Helvetica', 12), wraplength=380, fg="white", bg="black").pack(pady=5)
        tk.Label(content_frame, text=f"Pages: {book_pages}", font=('Helvetica', 12), wraplength=380, fg="white", bg="black").pack(pady=5)
        tk.Label(content_frame, text=f"Dedication: {book_dedication}", font=('Helvetica', 12), wraplength=380, justify="left", fg="white", bg="black").pack(pady=5)
        tk.Label(content_frame, text=f"Release Date: {book_release_date}", font=('Helvetica', 12), wraplength=380, fg="white", bg="black").pack(pady=5)
        tk.Label(content_frame, text=book_summary, font=('Helvetica', 12), wraplength=380, justify="left", fg="white", bg="black").pack(pady=5)


    """          SPELLS SECTION          """

    # Creates the spells section
    def create_spells_section(self):

        # Background Image
        self.backgroundimage = PhotoImage(file="backgroundimage.png")
        imagelabel = Label(self.content_frame, image = self.backgroundimage)
        imagelabel.place(x=-1, y=-1)

        # Gap to add space in the interface
        gap = tk.Label(self.content_frame, fg="white", bg="black")
        gap.pack(pady=60)

        # Title
        spells_section = tk.Label(self.content_frame, text="LEARN A RANDOM SPELL", font=('Tahoma', 35), fg="white", bg="black")
        spells_section.pack(pady=10)

        # Descriptive label
        spells_label = tk.Label(self.content_frame, text="Click the button and learn a wizard's spell.", font=('Helvetica', 20), fg="white", bg="black")
        spells_label.pack(pady=5)

        # Label which will display the spell name
        self.spell_name_label = tk.Label(self.content_frame, text="Spell Name: ", font=('Helvetica', 16), fg="white", bg="black")
        self.spell_name_label.pack(pady=5)
        
        # Label which will display the spell category
        self.spell_category_label = tk.Label(self.content_frame, text="Category: ", font=('Helvetica', 14), fg="white", bg="black")
        self.spell_category_label.pack(pady=5)
        
        # Label which will display the spell effect
        self.spell_effect_label = tk.Label(self.content_frame, text="Effect: ", font=('Helvetica', 14), wraplength=800, fg="white", bg="black")
        self.spell_effect_label.pack(pady=10)

        # Button which triggers the random spell function
        random_spell_button = tk.Button(self.content_frame, text="Show Random Spell", command=self.display_random_spell)
        random_spell_button.pack(pady=10)

    # Function to display a random spell
    def display_random_spell(self):

        # Gets a random spell from the database
        spell = self.fetch_random_spell()

        if spell:
            # If there is data taken, each label is updated to show the details
            self.spell_name_label.config(text=f"Spell Name: {spell['name']}")
            self.spell_category_label.config(text=f"Category: {spell['category']}")
            self.spell_effect_label.config(text=f"Effect: {spell['effect']}")

        else:
            # If there was no data taken, an error message is in place of the labels
            self.spell_name_label.config(text="Spell Name: No spell data available.")
            self.spell_category_label.config(text="Category: ")
            self.spell_effect_label.config(text="Effect: ")

    # Function to get the random spell
    def fetch_random_spell(self):

        # Endpoint URL in which the data will be taken from
        url = "https://api.potterdb.com/v1/spells?page[size]=100"  
        
        try:
            # GET request sent to API
            response = requests.get(url)

            response.raise_for_status() # Exception raised

            data = response.json() # Parsed JSON response

            # If the API returns a list of spells
            spells = data['data']
            
            # A random spell is chosen from the list
            if spells:
                random_spell = random.choice(spells)
                return {
                    # The data is taken from the spell chosen
                    "name": random_spell['attributes']['name'],
                    "category": random_spell['attributes'].get('category', 'N/A'),
                    "effect": random_spell['attributes'].get('effect', 'No effect description available.')
                }
            
            # If no spells are found
            else:
                return None  
            
        # If there was an issue in getting the data
        except requests.exceptions.RequestException as e:
            messagebox.showerror("API Error", f"Error fetching spell data: {e}")
            return None

    """          MOVIE SECTION          """

    # Creates the movie section
    def create_movies_section(self):

        # Background Image
        self.backgroundimage = PhotoImage(file="backgroundimage.png")
        imagelabel = Label(self.content_frame, image = self.backgroundimage)
        imagelabel.place(x=-1, y=-1)
        
        # Gap to create space between the content
        gap = tk.Label(self.content_frame, fg="white", bg="black")
        gap.pack(pady=40)

        # Title
        movies_section = tk.Label(self.content_frame, text="MOVIES", font=('Tahoma', 35), fg="white", bg="black")
        movies_section.pack(pady=10)

        # Descriptive label
        spells_section = tk.Label(self.content_frame, text="Choose a movie to reveal more.", font=('Helvetica', 20), fg="white", bg="black")
        spells_section.pack(pady=5)

        # Frame for the section's content
        self.movie_frame = tk.Frame(self.content_frame, bg="black")
        self.movie_frame.pack(pady=10)

        # Listbox to store all the movies
        self.movie_listbox = tk.Listbox(self.movie_frame, width=50, height=10)
        self.movie_listbox.pack(pady=10)

        # Button to trigger the function which will get the data
        fetch_button = tk.Button(self.movie_frame, text="Show Movie Details", command=self.open_movie_details)
        fetch_button.pack(pady=10)

        # Gets the movie data and populates the listbox
        movies = self.fetch_movies_data()
        self.populate_movie_listbox(movies)

    # Function which gets the movie data
    def fetch_movies_data(self):

        # URL to get the data from the API
        url = "https://api.potterdb.com/v1/movies?page[size]=100"  # Assuming there's an endpoint for movies
        
        try:
            # Send GET request to API
            response = requests.get(url)

            # Raised exception
            response.raise_for_status()

            # Parsed JSON response
            data = response.json()

            return data['data']
        
        # If an error occurs during data fetching, a message is show
        except requests.exceptions.RequestException as e:
            messagebox.showerror("API Error", f"Error fetching movie data: {e}")
            return []

    # Function to populate the listbox
    def populate_movie_listbox(self, movies):

        # If data of the movies is returned, each movie will be put into the listbox
        if movies:
            for movie in movies:
                movie_title = movie['attributes']['title']
                self.movie_listbox.insert(tk.END, movie_title)
        
        # If no movies are returned, a message is shown
        else:
            messagebox.showinfo("No Results", "No movies found.")

    # Function when the user wants to know more about a movie
    def open_movie_details(self):

        # Gets the index of the movie from the listbox
        selected_index = self.movie_listbox.curselection()

        # If a movie is selected, the title is taken to get all the details about the movie
        if selected_index:
            movie_title = self.movie_listbox.get(selected_index)
            movie = self.get_movie_by_title(movie_title)

            # If the details are found, they will be displayed in the new window through a different function
            if movie:
                self.create_movie_details(movie)
            # If not, an error is shown
            else:
                messagebox.showinfo("No Results", "Movie details not found.")

        # If no movie was selected
        else:
            messagebox.showwarning("Selection Error", "Please select a movie from the list.")

    # Function which gets the movie's detakls through its title
    def get_movie_by_title(self, movie_title):

        # URL to fetch data from APIR
        url = f"https://api.potterdb.com/v1/movies?filter[title_cont]={movie_title}&page[size]=1"
        
        try:
            # GET request sent to API
            response = requests.get(url)

            # Raised exception
            response.raise_for_status()

            # Parsed JSON response
            data = response.json()

            # If data is found, return the first movie in the data
            if data['data']:
                return data['data'][0]
            
            # If no data is found
            return None
        
        # If an error occurs during data gathering
        except requests.exceptions.RequestException as e:
            messagebox.showerror("API Error", f"Error fetching movie details: {e}")
            return None

    # Function which creates the window for the movie details
    def create_movie_details(self, movie):

        # Create a new window
        movie_window = tk.Toplevel(self.root)
        movie_window.title(movie['attributes']['title']) # Sets the title as the movie name
        movie_window.geometry("600x500")
        movie_window.config(bg="black")

        # Gets each movie detail
        movie_title = movie['attributes']['title']
        movie_release_date = movie['attributes'].get('release_date', '')
        movie_running_time = movie['attributes'].get('running_time', '')
        movie_summary = movie['attributes'].get('summary', 'No summary available.')
        movie_poster_url = movie['attributes'].get('poster', '')

        # Displays the movie title
        tk.Label(movie_window, text=movie_title, font=('Helvetica', 20), fg="white", bg="black").pack(pady=10)

        # Displays movie poster
        if movie_poster_url:
            try:
                img_data = requests.get(movie_poster_url).content 
                img = Image.open(BytesIO(img_data)) # Image from the bytes
                img.thumbnail((150, 200)) # Resized image
                img = ImageTk.PhotoImage(img) # Convert to Tkinter image
                img_label = tk.Label(movie_window, image=img, bg="black")
                img_label.image = img # Creates the reference
                img_label.pack()

            # If no image is taken
            except Exception as e:
                tk.Label(movie_window, text="Poster Not Available").pack(pady=5)

        # Display the movie's release date
        tk.Label(movie_window, text=f"Release Date: {movie_release_date}", font=('Helvetica', 14), fg="white", bg="black").pack(pady=5)

        # Display the movie's running time
        tk.Label(movie_window, text=f"Running Time: {movie_running_time}", font=('Helvetica', 14), fg="white", bg="black").pack(pady=5)

        # Display the movie's summary
        tk.Label(movie_window, text=f"Summary: {movie_summary}", font=('Helvetica', 14), wraplength=500, justify="left", fg="white", bg="black").pack(pady=5)

# Main execution block of code
if __name__ == "__main__":
    # Creates the main Tkinter window to run
    root = tk.Tk()
    app = WizardingWorld(root) # Initializes the app
    root.mainloop() # Initilizes the main loop