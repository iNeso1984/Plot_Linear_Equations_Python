import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

# Function to plot lines
def plot_lines(eq1_form, a1, b1, c1, eq2_form, a2, b2, c2, m1=None, m2=None):
    x = sp.symbols('x')
    
    # Parse Equation 1
    if eq1_form == 'Standard':
        eq1_expr = sp.Eq(a1 * x + b1 * sp.symbols('y'), c1)
        y1_expr = sp.solve(eq1_expr, sp.symbols('y'))[0]
    else:
        y1_expr = m1 * x + b1
    
    # Parse Equation 2
    if eq2_form == 'Standard':
        eq2_expr = sp.Eq(a2 * x + b2 * sp.symbols('y'), c2)
        y2_expr = sp.solve(eq2_expr, sp.symbols('y'))[0]
    else:
        y2_expr = m2 * x + b2

    # Generate x values for plotting
    x_vals = np.linspace(-10, 10, 100)

    # Calculate y values using lambdify to convert sympy expressions to numpy functions
    y1_func = sp.lambdify(x, y1_expr)
    y2_func = sp.lambdify(x, y2_expr)

    y1_vals = y1_func(x_vals)
    y2_vals = y2_func(x_vals)

    # Plot the results
    plt.figure(figsize=(8, 6))
    plt.plot(x_vals, y1_vals, label='Line 1', color='blue')
    plt.plot(x_vals, y2_vals, label='Line 2', color='red')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axhline(0, color='black',linewidth=0.5)
    plt.axvline(0, color='black',linewidth=0.5)
    plt.grid(True)
    plt.legend()

    # Display the plot in Streamlit
    st.pyplot(plt)

# Streamlit App
def main():
    st.title('Line Graph Generator')

    # User input for equation 1
    st.header('Equation 1')
    eq1_form = st.selectbox('Select Form for Equation 1', ['Standard', 'Slope-Intercept'])
    if eq1_form == 'Standard':
        a1 = st.number_input('A1', value=1.0)
        b1 = st.number_input('B1', value=1.0)
        c1 = st.number_input('C1', value=0.0)
        m1 = None
    else:
        m1 = st.number_input('Slope (m1)', value=1.0)
        b1 = st.number_input('Y-intercept (b1)', value=0.0)
        a1, c1 = None, None

    # User input for equation 2
    st.header('Equation 2')
    eq2_form = st.selectbox('Select Form for Equation 2', ['Standard', 'Slope-Intercept'])
    if eq2_form == 'Standard':
        a2 = st.number_input('A2', value=2.0)
        b2 = st.number_input('B2', value=1.0)
        c2 = st.number_input('C2', value=0.0)
        m2 = None
    else:
        m2 = st.number_input('Slope (m2)', value=-1.0)
        b2 = st.number_input('Y-intercept (b2)', value=0.0)
        a2, c2 = None, None

    # Plot the lines when the "Plot" button is clicked
    if st.button('Plot'):
        plot_lines(eq1_form, a1, b1, c1, eq2_form, a2, b2, c2, m1, m2)

if __name__ == '__main__':
    main()
