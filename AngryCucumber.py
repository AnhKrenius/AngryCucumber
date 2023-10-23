#Provide sound-playing capabilities
import winsound
#Provide GUI components
from tkinter import *
#Provide video player
from tkVideoPlayer import *
#Used to plot
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
#Used to handle mathematical expression, calculation
from sympy import *
from sympy.parsing.sympy_parser import *
import numpy as np

#Create the MAIN WINDOW of the GUI
root = Tk()
root.title("Angry Cucumber")
root.geometry('800x800')
root.config(bg='skyblue')
#Create label and entry with widget to INPUT A MATHEMATICAL EXPRESSION
input_label = Label(root, text="Enter the mathematical expression:",bg='skyblue')
input_label.pack()
input_entry = Entry(root, width=50,font=("Arial",25),bg='#CCFFFF')
input_entry.pack()
# Set up the DROP-DOWN menu for selecting the type of calculus problem
problem_var = StringVar()
problem_var.set("Limits")  # default value
problem_menu = OptionMenu(root, problem_var, "Limits",
                          "Derivatives","Gradient Descent","Extrema",
                          "Integration","Definite Integration")
problem_menu.pack()
def calculate():
    expression = input_entry.get()
    x = symbols('x')
    try:
        if problem_var.get() == "Limits":
            output_label.pack_forget()
            output_text.pack_forget()
            value = 0  # hardcoded for simplicity
            #Create an ENTRY field to INPUT THE APPROACH VALUE OF LIMIT
            appr_limit_label = Label(root, text="Enter approach of limit:")
            appr_limit_label.pack()
            appr_limit_entry = Entry(root)
            appr_limit_entry.pack()
            result = limit(parse_expr(expression), x, 0)
            def compute_lim():
                if appr_limit_entry.get() == 'oo':
                    appr_limit = oo
                elif appr_limit_entry.get() == '-oo':
                    appr_limit =-oo
                else:
                    appr_limit = float(appr_limit_entry.get())
                resultlimit = limit(parse_expr(expression), x, appr_limit)
                if 'current_output_label' in globals():
                    current_output_label.pack_forget()
                globals()['current_output_label'] = Label(root,
                                                          text=f"Limit: {resultlimit}",
                                                          width=50, height=5, bg='#CCFFFF')
                current_output_label.pack()
            compute_btn = Button(root, text="Compute", command=compute_lim)
            compute_btn.pack()
            def clear_result():
                appr_limit_entry.delete(0, END)
                if 'current_output_label' in globals():
                    current_output_label.pack_forget()
                appr_limit_entry.pack_forget()
                appr_limit_label.pack_forget()
                clear_btn.pack_forget()
                appr_limit_entry.pack_forget()
                compute_btn.pack_forget()
            clear_btn = Button(root, text="Clear Result", command=clear_result)
            clear_btn.pack()
        elif problem_var.get() == "Derivatives":
            output_label.pack()
            output_text.pack()
            result = diff(parse_expr(expression), x)
            #Plot the result expression graph
            fig = Figure(figsize=(5, 4), dpi=100)
            x_vals = np.arange(-1, 1, 0.3)
            y_vals = lambdify(x, result)
            y_vals_vec=np.vectorize(y_vals)
            fig.add_subplot(111).plot(x_vals, y_vals_vec(x_vals))
            def clear_result():
                canvas.get_tk_widget().pack_forget()
                clear_btn.pack_forget()
                toolbar.pack_forget()
                output_text.pack_forget()
            clear_btn = Button(root, text="Clear Result", command=clear_result)
            clear_btn.pack()
            canvas = FigureCanvasTkAgg(fig, master=root)
            canvas.draw()
            canvas.get_tk_widget().pack(side=TOP, padx=10, pady=5)
            toolbar = NavigationToolbar2Tk(canvas, root)
            toolbar.update()
            toolbar.pack(side=TOP, padx=10, pady=5)
        elif problem_var.get() == "Extrema":
            output_label.pack()
            output_text.pack()
            # calculate critical points
            critical_points = solve(diff(parse_expr(expression), x), x)
            # iterate through critical points to determine max/min
            result = []
            for cp in critical_points:
                first_deriv = diff(parse_expr(expression), x)
                second_deriv = diff(first_deriv, x)
                # calculate the value of the second derivative at the critical point
                second_deriv_at_cp = second_deriv.subs(x, cp)
                # use the second derivative test to determine
                # whether the critical point is a maximum or minimum
                if second_deriv_at_cp > 0:
                    rs = f"{cp} is a local minimum"
                elif second_deriv_at_cp < 0:
                    rs = f"{cp} is a local maximum"
                else:
                    rs = f"Cannot determine whether {cp} is a maximum or minimum"
                result.append(rs)
            output_text.insert(END, "\n".join(result))
        elif problem_var.get() == "Gradient Descent":
            output_label.pack_forget()
            output_text.pack_forget()
            input_label2 = Label(root, text="Enter learning rate - alpha: ")
            input_label2.pack()
            alpha_entry = Entry(root)
            alpha_entry.pack()
            input_label3 = Label(root, text="Enter initial guess: ")
            input_label3.pack()
            init_entry = Entry(root)
            init_entry.pack()
            input_label4 = Label(root, text="Enter range: ")
            input_label4.pack()
            a_entry = Entry(root)
            a_entry.pack()
            input_label5 = Label(root, text="Enter step: ")
            input_label5.pack()
            step_entry = Entry(root)
            step_entry.pack()
            def gradient_descent():
                x = symbols('x')
                alpha = float(alpha_entry.get())
                init = float(init_entry.get())
                a = float(a_entry.get())
                step = float(step_entry.get())
                derv = diff(parse_expr(expression), x)
                resultgra = []
                for n in range(int(a)):
                    if (n % int(step)) == 0:
                        resultgra.append((f'{n:>3}', f'{init:>8.4f}', f'{parse_expr(expression).subs(x, init):>8.4f}'))
                    init = init - alpha * derv.evalf(subs={x: init})
                globals()['output3_label1'] = Label(root, width=50, height=50, bg='#CCFFFF')
                globals()['output3_label1'].pack()
                output_str = "Gradient_descent: \n"
                output_str += f"{'n':<3} {'xn':>12} {'f(xn)':>10}\n"
                for t in resultgra:
                    output_str += f"{t[0]:>3} {t[1]:>10} {t[2]:>10} \n"
                globals()['output3_label1'].config(text=output_str)
            compute_btn1 = Button(root, text="Compute", command=gradient_descent)
            compute_btn1.pack()
            def clear_result():
                globals()['output3_label1'].pack_forget()
                input_label2.pack_forget()
                alpha_entry.pack_forget()
                input_label3.pack_forget()
                init_entry.pack_forget()
                input_label4.pack_forget()
                a_entry.pack_forget()
                input_label5.pack_forget()
                step_entry.pack_forget()
                clear_btn.pack_forget()
                compute_btn1.pack_forget()
            clear_btn = Button(root, text="Clear Result", command=clear_result)
            clear_btn.pack()
            result = 'Haha'
        elif problem_var.get() == "Integration":
            if expression == "x*sin(x)+professor_hazem":
                output_label.pack()
                output_text.pack()
                output_text.configure(width=50,height=1)
                def play_sound():
                    winsound.PlaySound("prof.wav",winsound.SND_ASYNC)
                button = Button(root, text="Playsound", command=play_sound)
                button.pack(side="top", pady=3)
                video=TkinterVideo(master=root)
                video.load(r"prof.mp4")
                video.pack(expand=true,fill="both")
                video.play()
                result='Thank Professor Hazem for a wonderful semester'
            else:
                output_label.pack()
                output_text.pack()
                result = integrate(parse_expr(expression), x)
                fig = Figure(figsize=(5, 4), dpi=100)
                x_vals = np.arange(-10, 10, 0.1)
                y_vals = lambdify(x, result)
                fig.add_subplot(111).plot(x_vals, y_vals(x_vals))
                def clear_result():
                    output_label.pack_forget()
                    canvas.get_tk_widget().pack_forget()
                    clear_btn.pack_forget()
                    toolbar.pack_forget()
                    output_text.pack_forget()
                clear_btn = Button(root, text="Clear Result", command=clear_result)
                clear_btn.pack()
                canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
                canvas.draw()
                canvas.get_tk_widget().pack(side=TOP, padx=10, pady=5)

                toolbar = NavigationToolbar2Tk(canvas, root)
                toolbar.update()
                toolbar.pack(side=TOP)
                canvas.get_tk_widget().pack(side=TOP, padx=10, pady=5)
        elif problem_var.get() == "Definite Integration":
            lower_limit_label = Label(root, text="Lower Limit:")
            lower_limit_entry = Entry(root)
            upper_limit_label = Label(root, text="Upper Limit:")
            upper_limit_entry = Entry(root)
            result = limit(parse_expr(expression), x, 0)
            lower_limit_label.pack()
            lower_limit_entry.pack()
            upper_limit_label.pack()
            upper_limit_entry.pack()
            output_label.pack_forget()
            output_text.pack_forget()
            def compute_defintegarion():
                resultdi = integrate(parse_expr(expression),(x, float(lower_limit_entry.get()), float(upper_limit_entry.get())))
                if 'current_output_label' in globals():
                    current_output_label.pack_forget()
                globals()['current_output_label'] = Label(root, text=f"Definite Integral: {resultdi}", width=50, height=5, bg='#CCFFFF')
                current_output_label.pack()
            compute_btn = Button(root, text="Compute", command=compute_defintegarion)
            compute_btn.pack()
            def clear_result():
                clear_btn.pack_forget()
                output_text.pack_forget()
                lower_limit_label.pack_forget()
                lower_limit_entry.pack_forget()
                upper_limit_label.pack_forget()
                upper_limit_entry.pack_forget()
                compute_btn.pack_forget()
                current_output_label.pack_forget()
            clear_btn = Button(root, text="Clear Result", command=clear_result)
            clear_btn.pack()
        output_text.delete("1.0", END)  # clear the previous result
        output_text.insert(END, result)
    except (SympifyError, ValueError,TypeError,SyntaxError,NotImplementedError) as e:
        # Show an error message if the expression is invalid
        main=Tk(className='Error')
        main.configure(background='red')
        main.geometry('800x100')
        labelhaha=Label(main,text="ERRoR: Text expression correctly or I'll kill you 🔪💣",font=("Arial",25))
        labelhaha.pack(side=TOP,pady=25)
        main.mainloop()
#Set up the BUTTON that triggers the CALCULATION
calculate_button = Button(root, text="Calculate", command=calculate)
calculate_button.pack()
# Set up the output field
output_label = Label(root, text="Result:",bg='skyblue')
output_label.pack()
output_text = Text(root, width=50, height=2,font=("Arial",20),bg='#CCFFFF')
output_text.pack()
# Start the GUI event loop
root.mainloop()
