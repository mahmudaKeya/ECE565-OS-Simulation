import tkinter as tk
from tkinter import StringVar, Toplevel, messagebox
import json
from tkinter import ttk


reads=0
writes=0

class BLOCK:
    def __init__(self, file, next_block):
        self.file = file
        self.next_block = next_block

class BlockGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Disk Block Management")
        self.root.geometry("800x500")

        # Instructions label
        label = tk.Label(self.root, text="Block Occupancy (Blue = Occupied, White = Free)")
        label.pack(pady=10)

        # Reads and writes label
        self.read_write_label = tk.Label(self.root, text=f"Reads: {reads} | Writes: {writes}")
        self.read_write_label.pack(pady=5)

        self.blocks = [None] * 32  # Placeholder for BLOCK objects
        
        
        # Display the 32 blocks as labels
        blocks_frame = tk.Frame(self.root)
        blocks_frame.pack(pady=10)

        # Create a 4x8 grid for block entries
        self.block_labels = []
        for i in range(32):
            label = tk.Label(blocks_frame, text=f"Block {i}\nFile: None\nNext: None", borderwidth=1, relief="solid", width=10, height=4)
            label.grid(row=i // 8, column=i % 8, padx=5, pady=5)
            self.block_labels.append(label)
        
        # Load button
        self.load_button = tk.Button(self.root, text="Load block entries from JSON", command=self.load_entries)
        self.load_button.pack(pady=5)

        # Update button (disabled initially)
        self.update_button = tk.Button(self.root, text="Update File", state=tk.DISABLED, command=self.update_file)
        self.update_button.pack(pady=5)

    def load_entries(self):
        try:
            with open("block_entries.json", "r") as file:
                data = json.load(file)

            with open("directory.json", "r") as f:
                self.directory_data = json.load(f)

            # Set to track indexes where file is null
            self.null_file_indexes = set()
            
            # Initialize BLOCK objects from JSON data
            for i in range(32):
                block_data = data.get(str(i), {"file": None, "next_block": None})
                self.blocks[i] = BLOCK(block_data["file"], block_data["next_block"])
                self.update_block_label(i)

                

                # Set background color to light blue after loading
                if block_data["file"] is None:
                    self.null_file_indexes.add(i)
                else:
                    self.block_labels[i].config(bg="light blue")
            
            
            
            # Print indexes with null files
            print("Blocks with null files:")
            print(self.null_file_indexes)

            # Enable the Update button after loading
            self.update_button.config(state=tk.NORMAL)
            # messagebox.showinfo("Success", "Block entries loaded from JSON.")
        
        except FileNotFoundError:
            messagebox.showerror("Error", "block_entries.json file not found.")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format.")

    def update_block_label(self, index):
        block = self.blocks[index]
        self.block_labels[index].config(text=f"Block {index}\nFile: {block.file}\nNext: {block.next_block}")

    def update_read_write_label(self):
        """Update the reads and writes label."""
        self.read_write_label.config(text=f"Reads: {reads} | Writes: {writes}")
    
    def update_file(self):
            # Create a new popup window
        update_window = Toplevel(root)
        update_window.title("Update File")
        update_window.geometry("500x250")  # Adjust window size

        # Dropdown menu for selecting a file (using ttk.Combobox)
        file_names = [entry["file"] for entry in self.directory_data]
        selected_file = StringVar(update_window)
        selected_file.set(file_names[0])  # Default selection

        tk.Label(update_window, text="Select File:").grid(row=0, column=0, pady=5, padx=10, sticky="w")
        file_dropdown = ttk.Combobox(update_window, textvariable=selected_file, values=file_names, state="readonly")
        file_dropdown.grid(row=0, column=1, pady=5, padx=10, sticky="w")

        # Radio buttons for Add/Remove block options
        action = StringVar(value="Add")
        tk.Label(update_window, text="Select Action:").grid(row=1, column=0, pady=5, padx=10, sticky="w")
        tk.Radiobutton(update_window, text="Add Block", variable=action, value="Add").grid(row=1, column=1, sticky="w")
        tk.Radiobutton(update_window, text="Remove Block", variable=action, value="Remove").grid(row=1, column=2, sticky="w")

        # Radio buttons for Position options
        position = StringVar(value="beginning")
        tk.Label(update_window, text="Select Position:").grid(row=2, column=0, pady=5, padx=10, sticky="w")
        tk.Radiobutton(update_window, text="Beginning", variable=position, value="beginning").grid(row=2, column=1, sticky="w")
        tk.Radiobutton(update_window, text="Middle", variable=position, value="middle").grid(row=2, column=2, sticky="w")
        tk.Radiobutton(update_window, text="End", variable=position, value="end").grid(row=2, column=3, sticky="w")

        # Update button to confirm and call add/remove functions
        def confirm_update():
            file_name = selected_file.get()
            pos = position.get()
            action_type = action.get()

            # Find the file entry in the data
            entry = next((item for item in self.directory_data if item["file"] == file_name), None)
            if not entry:
                messagebox.showerror("Error", "File not found.")
                return
            
            start = entry["start"]
            length = entry["length"]

            print(f'start is {start}')
            print(f'length is {length}')

            # Call add or remove function based on action_type
            if action_type == "Add":
                global reads, writes
                add(file_name, start, length, position=pos)  # Parameters are placeholders
            else:
                remove(file_name, start, length, position=pos)  # Parameters are placeholders

            update_window.destroy()  # Close the update window

        update_button = tk.Button(update_window, text="Update File", command=confirm_update)
        update_button.grid(row=3, column=0, columnspan=4, pady=10)  # Adjusted position
        
        def add(file_name, start, length, position):
            global reads, writes
            current_block_index = start

            if position=="beginning":
                # Pick a free block from null_file_indexes
                new_block_index = self.null_file_indexes.pop()
                print(f'new_block_index is {new_block_index}')

                #Add the file and pointer to the new block    
                self.blocks[new_block_index].file = file_name
                self.blocks[new_block_index].next_block = start 

                start = new_block_index
                writes=writes+1

                print(f'Reads: {reads}, Writes {writes}')
                ###Changes to GUI
                self.update_block_label(new_block_index)
                self.block_labels[new_block_index].config(bg="light blue")


            if position=="end":
                while self.blocks[current_block_index].next_block is not None:
                    reads=reads+1
                    print(current_block_index)
                    current_block_index = self.blocks[current_block_index].next_block

                reads=reads+1
                print(f'current_block_index is {current_block_index}')
                print(f'reads is {reads}')


                # Pick the next free block from null_file_indexes
                new_block_index = self.null_file_indexes.pop()
                print(f'Adding block to Block{new_block_index}')

                # Assign file data to the new block
                self.blocks[new_block_index].file = file_name
                self.blocks[new_block_index].next_block = None  # Since it's the end of the list
                writes=writes+1
                # Update the previous block to point to the new block
                self.blocks[current_block_index].next_block = new_block_index
                writes=writes+1

                print(f'Reads: {reads}, Writes {writes}')
                print(self.blocks[new_block_index].next_block)
                print(self.blocks[current_block_index].next_block)

                ###Changes to GUI
                self.update_block_label(new_block_index)
                self.update_block_label(current_block_index)
                self.block_labels[new_block_index].config(bg="light blue")
                

            self.update_read_write_label()

        def remove(file_name, start, length, position):
            global reads,writes
            current_block_index = start
            previous_block_index=None

            if position=="beginning":
                if start is None:
                    # The list is empty, so nothing to remove
                    return None
                
                block_to_remove = start

                # Update the start pointer to the next block
                start = self.blocks[block_to_remove].next_block

                # Free the block file and next_block attributes
                self.blocks[block_to_remove].file = None
                self.blocks[block_to_remove].next_block = None

                # Return the removed block to the free list
                self.null_file_indexes.add(block_to_remove)

                print(f'Reads: {reads}, Writes {writes}')
                ###Changes to GUI
                self.update_block_label(block_to_remove)
                self.update_block_label(start)
                self.block_labels[block_to_remove].config(bg="white")


            if position=="end":

                while self.blocks[current_block_index].next_block is not None:
                    reads=reads+1
                    print(current_block_index)
                    previous_block_index=current_block_index
                    current_block_index = self.blocks[current_block_index].next_block

                # Now, current_block_index is the last block
                # previous_block_index is the second-to-last block

                if previous_block_index is not None:
                    # Update the second-to-last block's next_block to None
                    self.blocks[previous_block_index].next_block = None
                    writes=writes+1

                
                ## Free the last block
                self.blocks[current_block_index].file = None  # Clear the file data (optional)
                self.blocks[current_block_index].next_block = None

                # Return the last block to the free list
                self.null_file_indexes.add(current_block_index)
                print(f'current_block_index is {current_block_index}')
                print(f'reads is {reads}')

                print(f'Reads: {reads}, Writes {writes}')
                ###Changes to GUI
                self.update_block_label(previous_block_index)
                self.update_block_label(current_block_index)
                self.block_labels[current_block_index].config(bg="white")

            self.update_read_write_label()
if __name__ == "__main__":
    root = tk.Tk()
    app = BlockGUI(root)
    root.mainloop()


'''
Some Test CASES:
'''
#add('list',28,4,'beginning', reads, writes) #Ans: reads=0, writes=1
#add('list',28,4,'middle', reads, writes) #Ans: reads=, writes=
#add('list',28,4,'end', reads, writes) #Ans: reads=4 ,writes=2
#remove('list',28,4,'beginning', reads, writes) #Ans: reads=0,writes=0
#remove('list',28,4,'middle', reads, writes) #Ans:reads=, writes
#remove('list',28,4,'end', reads, writes) #Ans: reads=3,writes=1

'''
Test case on count: Please check
'''
#add('count', 0, 2, 'beginning', reads, writes)# Ans: read=0, writes=1
#add('count', 0, 2, 'middle', reads, writes)   #Ans: read= , writes=
#add('count', 0, 2, 'end', reads, writes) # Ans: read=2, writes=2
#remove('count', 0, 2, 'beginning', reads, writes)# Ans: reads=0,writes=0
#remove('count', 0, 2, 'middle', reads, writes)  #Ans: reads=, writes=
#remove('count', 0, 2, 'end', reads, writes) #Ans: reads=1 , writes=1



'''
Test case on f: Please check
'''
#add('f', 6, 2, 'beginning', reads, writes)# Ans: read=0, writes=1
#add('f', 6, 2, 'middle', reads, writes)   #Ans: read= , writes=
#add('f', 6, 2, 'end', reads, writes) # Ans: read=2, writes=2
#remove('f', 6, 2, 'beginning', reads, writes)# Ans: reads=0,writes=0
#remove('f', 6, 2, 'middle', reads, writes)  #Ans: reads=, writes=
#remove('f', 6, 2, 'end', reads, writes) #Ans: reads=1 , writes=1