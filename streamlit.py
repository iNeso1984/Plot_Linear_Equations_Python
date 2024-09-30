import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from matplotlib.backends.backend_pdf import PdfPages

def plot_lines(eq1_form, a1, b1, c1, eq2_form, a2, b2, c2, m1, m2):
    # Parse equations and extract coefficients
    x = sp.symbols('x')

    if eq1_form == 'Standard':
        eq1_expr = sp.Eq(a1 * x + b1 * sp.symbols('y'), c1)
        y1_expr = sp.solve(eq1_expr, sp.symbols('y'))[0]
        equation1 = f'y = {-a1/b1}x + {c1/b1}'  # Slope-Intercept Form
    else:
        y1_expr = m1 * x + b1
        equation1 = f'y = {m1}x + {b1}'

    if eq2_form == 'Standard':
        eq2_expr = sp.Eq(a2 * x + b2 * sp.symbols('y'), c2)
        y2_expr = sp.solve(eq2_expr, sp.symbols('y'))[0]
        equation2 = f'y = {-a2/b2}x + {c2/b2}'  # Slope-Intercept Form
    else:
        y2_expr = m2 * x + b2
        equation2 = f'y = {m2}x + {b2}'

    # Generate x values for plotting
    x_vals = np.linspace(-10, 10, 100)

    # Calculate y values for each equation using sympy's lambdify function
    y1_func = sp.lambdify(x, y1_expr)
    y2_func = sp.lambdify(x, y2_expr)
    y1 = y1_func(x_vals)
    y2 = y2_func(x_vals)

    # Create the plot
    plt.figure(figsize=(10, 10))
    plt.plot(x_vals, y1, label=f'Equation 1: {equation1}', color='blue')
    plt.plot(x_vals, y2, label=f'Equation 2: {equation2}', color='red')
    plt.axhline(0, color='black', lw=0.5, ls='--')
    plt.axvline(0, color='black', lw=0.5, ls='--')
    plt.title('Line Graph of Two Equations')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid()
    plt.legend()
    plt.tight_layout()

    # Set the tick marks for both axes
    plt.xticks(np.arange(-20, 21, 2))  # x ticks from -20 to 20 with a step of 2
    plt.yticks(np.arange(-20, 21, 2))  # y ticks from -20 to 20 with a step of 2

    # Set the aspect ratio to be equal for perfect square grid
    plt.axis('equal')  # This will make the grid squares

    # Show the plot
    st.pyplot(plt)

    return equation1, equation2, x_vals, y1, y2


def save_plot_as_pdf(equation1, equation2, x_vals, y1, y2):
    # Define the filename and path where you want to save the PDF
    pdf_filename = 'line_graph_results.pdf'
    
    try:
        # Create a new figure for the PDF to match the appearance
        plt.figure(figsize=(10, 10))

        # Use the provided data for plotting
        plt.plot(x_vals, y1, label=f'Equation 1: {equation1}', color='blue')
        plt.plot(x_vals, y2, label=f'Equation 2: {equation2}', color='red')
        plt.axhline(0, color='black', lw=0.5, ls='--')
        plt.axvline(0, color='black', lw=0.5, ls='--')
        plt.title('Line Graph of Two Equations')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid()
        plt.legend()
        plt.tight_layout()

        # Set the tick marks for both axes
        plt.xticks(np.arange(-20, 21, 2))  # x ticks from -20 to 20 with a step of 2
        plt.yticks(np.arange(-20, 21, 2))  # y ticks from -20 to 20 with a step of 2

        # Set the aspect ratio to be equal for perfect square grid
        plt.axis('equal')  # This will make the grid squares

        with PdfPages(pdf_filename) as pdf:
            # Save the current plot to the PDF
            pdf.savefig()  
            plt.close()
        
        # Inform the user where the file was saved
        st.success(f"Plot saved as '{pdf_filename}' in the current directory!")

    except Exception as e:
        st.error(f"Error generating PDF: {e}")  # Display error message in Streamlit


def main():
    st.title('Line Graph Generator')
    st.markdown("""
    **Instructions:**
    1. Select the form of the equations you want to plot (Standard or Slope-Intercept).
    2. Enter the coefficients for both equations.
    3. Click the "Plot" button to generate the graph.
    4. The graph will be saved as a PDF file in the current directory.
    """)

    # User input for equation 1
    st.header('Equation 1')
    eq1_form = st.selectbox('Select Form', ['Standard', 'Slope-Intercept'], key='eq1_form')
    if eq1_form == 'Standard':
        a1 = st.number_input('A1', value=1, key='a1')
        b1 = st.number_input('B1', value=1, key='b1')
        c1 = st.number_input('C1', value=0, key='c1')
        m1 = None  # Set m1 to None for Standard form
    else:
        m1 = st.number_input('m1', value=1, key='m1')
        b1 = st.number_input('b1', value=0, key='b1_m1')  # Ensure unique key

    # User input for equation 2
    st.header('Equation 2')
    eq2_form = st.selectbox('Select Form', ['Standard', 'Slope-Intercept'], key='eq2_form')
    if eq2_form == 'Standard':
        a2 = st.number_input('A2', value=2, key='a2')
        b2 = st.number_input('B2', value=1, key='b2')
        c2 = st.number_input('C2', value=0, key='c2')
        m2 = None  # Set m2 to None for Standard form
    else:
        m2 = st.number_input('m2', value=-1, key='m2')
        b2 = st.number_input('b2', value=0, key='b2_m2')  # Ensure unique key

    # Plot the lines when the "Plot" button is clicked
    if st.button('Plot'):
        equation1, equation2, x_vals, y1, y2 = plot_lines(eq1_form, a1, b1, c1, eq2_form, a2, b2, c2, m1 if m1 is not None else 0, m2 if m2 is not None else 0)
        st.markdown(f'**Equation 1:** {equation1}')
        st.markdown(f'**Equation 2:** {equation2}')
        
        # Save the plot as PDF directly
        save_plot_as_pdf(equation1, equation2, x_vals, y1, y2)


if __name__ == '__main__':
    main()
