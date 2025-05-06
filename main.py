import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
from balanced_bracket import rightmost_derivation, leftmost_derivation

# Color scheme
BG_COLOR = "#f5f5f5"
PRIMARY_COLOR = "#6200ee"
SECONDARY_COLOR = "#03dac6"
TEXT_COLOR = "#333333"  
LIGHT_TEXT = "#666666"
CARD_COLOR = "#ffffff"
ERROR_COLOR = "#b00020"

def input_has_errors(input_string):
    # check if input string is empty
    if input_string == "":
        messagebox.showerror("No Input!", "Please input a string first.")
        return True
    
    # check if the input string is valid (use pyCFG)
    if (rightmost_derivation(input_string)[-1] != ("S => " + input_string)) and (leftmost_derivation(input_string)[-1] != ("S => " + input_string)):
        messagebox.showerror("Invalid Input!", "Grammar cannot generate the string.")
        return True

    return False

def generate_derivations():
    # get input string
    input_str = entry.get()

    # check input
    if input_has_errors(input_str): 
        return

    try:
        left = leftmost_derivation(input_str)
        right = rightmost_derivation(input_str)

        left_output.config(state=tk.NORMAL)
        right_output.config(state=tk.NORMAL)
        
        left_output.delete("1.0", tk.END)
        right_output.delete("1.0", tk.END)

        left_output.insert(tk.END, "\n".join(left))
        right_output.insert(tk.END, "\n".join(right))
        
        left_output.config(state=tk.DISABLED)
        right_output.config(state=tk.DISABLED)
        
        # Clear any previous error styling
        entry.config(style="TEntry")
        status_label.config(text="Derivations generated successfully", foreground="green")
        
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")
        entry.config(style="Error.TEntry")
        status_label.config(text=f"Error: {str(e)}", foreground=ERROR_COLOR)

def show_parse_tree():
    input_str = entry.get()

    # check input
    if input_has_errors(input_str): 
        return

    try:
        tree_root = build_parse_tree(input_str)

        win = tk.Toplevel(root)
        win.title("Parse Tree")
        win.geometry("900x700")
        win.configure(bg=BG_COLOR)
        
        # Add title
        title_frame = ttk.Frame(win)
        title_frame.pack(pady=10, fill=tk.X)
        ttk.Label(title_frame, text="Parse Tree Visualization", font=("Segoe UI", 14, "bold"), foreground=TEXT_COLOR).pack() 
        
        # Add canvas with scrollbars
        canvas_frame = ttk.Frame(win)
        canvas_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
        
        hscroll = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
        vscroll = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL)
        canvas = tk.Canvas(canvas_frame, bg=CARD_COLOR, xscrollcommand=hscroll.set, yscrollcommand=vscroll.set, width=800, height=500)
        
        hscroll.config(command=canvas.xview)
        vscroll.config(command=canvas.yview)
        
        canvas.grid(row=0, column=0, sticky="nsew")
        vscroll.grid(row=0, column=1, sticky="ns")
        hscroll.grid(row=1, column=0, sticky="ew")
        
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)
        
        # Add input display
        ttk.Label(win, text=f"Input: {input_str}", 
                 font=("Segoe UI", 11), 
                 foreground=TEXT_COLOR).pack(pady=(0, 10))

        def draw_tree(node, x, y, dx):
            # Draw node
            canvas.create_oval(x-20, y-20, x+20, y+20, fill=SECONDARY_COLOR, outline=PRIMARY_COLOR, width=2)
            canvas.create_text(x, y, text=node.label, fill=TEXT_COLOR, font=("Segoe UI", 10, "bold"))
            
            # Position children
            cx = x - dx * (len(node.children) - 1) // 2
            for child in node.children:
                # Draw connecting line
                canvas.create_line(x, y+20, cx, y+80-20, fill=PRIMARY_COLOR, width=2)
                draw_tree(child, cx, y+80, max(dx//1.5, 60))
                cx += dx

        draw_tree(tree_root, 450, 50, 120)
        
        # Update scroll region after drawing
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
        # Add zoom controls
        zoom_frame = ttk.Frame(win)
        zoom_frame.pack(pady=(0, 10))
        
        ttk.Button(zoom_frame, text="Zoom In", command=lambda: canvas.scale("all", 0, 0, 1.1, 1.1)).pack(side=tk.LEFT, padx=5)
        ttk.Button(zoom_frame, text="Zoom Out", command=lambda: canvas.scale("all", 0, 0, 0.9, 0.9)).pack(side=tk.LEFT, padx=5)
        ttk.Button(zoom_frame, text="Reset View", command=lambda: canvas.scale("all", 0, 0, 1, 1)).pack(side=tk.LEFT, padx=5)

    except Exception as e:
        messagebox.showerror("Error", f"Could not build parse tree:\n{str(e)}")
        status_label.config(text=f"Error: {str(e)}", foreground=ERROR_COLOR)

def build_parse_tree(s):
    class TreeNode:
        def __init__(self, label):
            self.label = label
            self.children = []

    def helper(sub):
        if not sub:
            return TreeNode("ε")

        if sub[0] == '[':
            depth = 0
            for i in range(len(sub)):
                if sub[i] == '[':
                    depth += 1
                elif sub[i] == ']':
                    depth -= 1
                if depth == 0:
                    inner = sub[1:i]
                    rest = sub[i+1:]
                    node = TreeNode("S")
                    node.children.append(TreeNode("["))
                    node.children.append(helper(inner))
                    node.children.append(TreeNode("]"))
                    node.children.append(helper(rest))
                    return node
        return TreeNode("INVALID")

    return helper(s)

# --- Main GUI Setup ---
root = tk.Tk()
root.title("Square Bracket Derivation Visualizer and Parse Tree Simulator")
root.geometry("1200x800")
root.configure(bg=BG_COLOR)

# Style configuration
style = ttk.Style()
style.theme_use("clam")

# Configure styles
style.configure("TFrame", background=BG_COLOR)
style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR, font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10), padding=6, background=CARD_COLOR, foreground=TEXT_COLOR)
style.configure("Primary.TButton", background=CARD_COLOR, foreground=TEXT_COLOR)  
style.map("Primary.TButton", background=[("active", "#e0e0e0"), ("pressed", "#e0e0e0")])  
style.configure("Secondary.TButton", background=CARD_COLOR, foreground=TEXT_COLOR)  
style.map("Secondary.TButton", background=[("active", "#e0e0e0"), ("pressed", "#e0e0e0")])  
style.configure("TEntry", fieldbackground=CARD_COLOR, foreground=TEXT_COLOR, padding=5)
style.configure("Error.TEntry", fieldbackground="#ffcdd2", foreground=ERROR_COLOR)
style.configure("Card.TFrame", background=CARD_COLOR, relief=tk.RAISED, borderwidth=1)
style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"), foreground=TEXT_COLOR)  
style.configure("Subtitle.TLabel", font=("Segoe UI", 11, "bold"), foreground=TEXT_COLOR) 
style.configure("Output.TText", font=("Consolas", 10), foreground=TEXT_COLOR)

# Header frame
header_frame = ttk.Frame(root, padding=(20, 10))
header_frame.pack(fill=tk.X)

# MAIN TITLE
ttk.Label(header_frame, text="Square Bracket Derivation Visualizer", style="Title.TLabel").pack(side=tk.LEFT)

# Input frame
input_frame = ttk.Frame(root, padding=20)
input_frame.pack(fill=tk.X)

ttk.Label(input_frame, text="Enter Bracket String:", style="Subtitle.TLabel").grid(row=0, column=0, padx=5, pady=5, sticky="w")

entry = ttk.Entry(input_frame, width=60, style="TEntry")
entry.grid(row=1, column=0, padx=5, pady=5, sticky="we")

button_frame = ttk.Frame(input_frame)
button_frame.grid(row=1, column=1, padx=10)

generate_btn = ttk.Button(button_frame, text="Generate Derivations", style="Primary.TButton", command=generate_derivations)
generate_btn.pack(side=tk.LEFT, padx=5)

parse_tree_btn = ttk.Button(button_frame, text="Show Parse Tree", style="Secondary.TButton", command=show_parse_tree)
parse_tree_btn.pack(side=tk.LEFT, padx=5)

# Output frame
output_frame = ttk.Frame(root)
output_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=(0, 20))

# Left derivation frame
left_frame = ttk.Frame(output_frame, style="Card.TFrame")
left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)

ttk.Label(left_frame, text="Leftmost Derivation", style="Subtitle.TLabel").pack(pady=(10, 5), padx=10, anchor="w")

left_output = tk.Text(left_frame, height=25, width=60, wrap=tk.WORD,  bg=CARD_COLOR, fg=TEXT_COLOR, font=("Consolas", 10), padx=10, pady=10, relief=tk.FLAT)
left_output.pack(expand=True, fill=tk.BOTH, padx=10, pady=(0, 10))
left_output.config(state=tk.DISABLED)

# Right derivation frame
right_frame = ttk.Frame(output_frame, style="Card.TFrame")
right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5)

ttk.Label(right_frame, text="Rightmost Derivation", style="Subtitle.TLabel").pack(pady=(10, 5), padx=10, anchor="w")

right_output = tk.Text(right_frame, height=25, width=60, wrap=tk.WORD,  bg=CARD_COLOR, fg=TEXT_COLOR, font=("Consolas", 10), padx=10, pady=10, relief=tk.FLAT)
right_output.pack(expand=True, fill=tk.BOTH, padx=10, pady=(0, 10))
right_output.config(state=tk.DISABLED)

# Status bar
status_bar = ttk.Frame(root, height=25)
status_bar.pack(fill=tk.X, side=tk.BOTTOM)
status_label = ttk.Label(status_bar, text="Ready", foreground=LIGHT_TEXT, font=("Segoe UI", 8))
status_label.pack(side=tk.LEFT, padx=10)

# Start app
root.mainloop()