from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import numpy as np
from scipy.optimize import linprog


class MultiCommoditySolverApp(App):
    def build(self):
        self.title = 'Multi-Commodity Transportation Solver'
        self.layout = GridLayout(cols=2, spacing=10, padding=40)

        self.layout.add_widget(Label(text='Supply Centers'))
        self.supply_centers = TextInput(multiline=False)
        self.layout.add_widget(self.supply_centers)

        self.layout.add_widget(Label(text='Demand Centers'))
        self.demand_centers = TextInput(multiline=False)
        self.layout.add_widget(self.demand_centers)

        self.layout.add_widget(Label(text='Number of Goods'))
        self.goods = TextInput(multiline=False)
        self.layout.add_widget(self.goods)

        self.layout.add_widget(Label(text='Supply Limits'))
        self.supply_limits = TextInput(multiline=False)
        self.layout.add_widget(self.supply_limits)

        self.layout.add_widget(Label(text='Demand Limits'))
        self.demand_amount = TextInput(multiline=False)
        self.layout.add_widget(self.demand_amount)

        self.layout.add_widget(Label(text='Transport Costs'))
        self.transport_costs = TextInput(multiline=False)
        self.layout.add_widget(self.transport_costs)

        self.solve_button = Button(text='Solve', size_hint=(1, None), width=100, height=50)
        self.solve_button.bind(on_press=self.solve_optimization)
        self.layout.add_widget(self.solve_button)

        self.import_button = Button(text='Example', size_hint=(0, None), width=150, height=50)
        self.import_button.bind(on_press=self.import_values)
        self.layout.add_widget(self.import_button)

        self.output_text = TextInput(multiline=True, readonly=True, font_size=16)
        self.scroll_view = ScrollView()
        self.scroll_view.add_widget(self.output_text)
        self.layout.add_widget(self.scroll_view)

        return self.layout

    def import_values(self, instance):
        values = "2 - 2 - 2 - 10,15; 20,5 - 15,10; 15,10 - 2,3:3,2; 4,1:1,4"
        values = values.split(" - ")
        self.supply_centers.text = values[0]
        self.demand_centers.text = values[1]
        self.goods.text = values[2]
        self.supply_limits.text = values[3]
        self.demand_amount.text = values[4]
        self.transport_costs.text = values[5]

    def solve_optimization(self, instance):
        # supply_centers :
        m = int(self.supply_centers.text)
        # demand_centers :
        n = int(self.demand_centers.text)
        # Number of goods :
        p = int(self.goods.text)

        supply_limits_input = self.supply_limits.text.split(';')
        supply_limits = [[float(value) for value in limits.split(',')] for limits in supply_limits_input]

        demand_limits_input = self.demand_amount.text.split(';')
        demand_limits = [[float(value) for value in limits.split(',')] for limits in demand_limits_input]

        transport_costs_input = self.transport_costs.text.split(';')
        transport_costs = [[[float(value) for value in costs.split(',')] for costs in row.split(':')] for row in
                           transport_costs_input]

        # Solver:
        c = []
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    c.append(transport_costs[i][j][k])

        # Inequality constraints (supply constraints)
        A_ub = []
        b_ub = []
        for i in range(m):
            for k in range(p):
                zero = np.zeros((m, n, p))
                for j in range(n):
                    zero[i][j][k] = 1
                zero = zero.reshape(-1).tolist()
                A_ub.append(zero)
                b_ub.append(supply_limits[i][k])

        # equality constraints:
        A_eq = []
        b_eq = []
        for j in range(n):
            for k in range(p):
                zero = np.zeros((m, n, p))
                for i in range(m):
                    zero[i][j][k] = 1
                zero = zero.reshape(-1).tolist()
                A_eq.append(zero)
                b_eq.append(demand_limits[j][k])

        solver = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, method='highs')


        # Displaying the results :
        #output = f"Status: {solver.message}\n"
        output = f"Optimal Value Found: {solver.success}\n"
        output += f"Optimal Value: ${solver.fun}\n"
        output += f"Optimal Solution: {solver.x}"

        self.output_text.text = output

if __name__ == '__main__':
    MultiCommoditySolverApp().run()