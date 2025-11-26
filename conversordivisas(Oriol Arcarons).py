import tkinter as tk
from tkinter import ttk, messagebox
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Divisas (BCE)")
        self.root.geometry("600x500")
        
        self.rates = {'EUR': 1.0}
        self.update_date = ""
        
        self.create_widgets()
        
        self.load_data()

    def create_widgets(self):
        title_label = tk.Label(self.root, text="Conversor de Divisas (BCE)", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        desc_label = tk.Label(self.root, 
                             text="Esta aplicación consume XML en tiempo real del Banco Central Europeo",
                             font=("Arial", 10))
        desc_label.pack(pady=5)
        
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=20)
        
        tk.Label(control_frame, text="Cantidad:").grid(row=0, column=0, padx=5, pady=5)
        self.amount_entry = tk.Entry(control_frame, width=15)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(control_frame, text="De:").grid(row=1, column=0, padx=5, pady=5)
        self.from_currency = ttk.Combobox(control_frame, width=12, state="readonly")
        self.from_currency.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(control_frame, text="A:").grid(row=2, column=0, padx=5, pady=5)
        self.to_currency = ttk.Combobox(control_frame, width=12, state="readonly")
        self.to_currency.grid(row=2, column=1, padx=5, pady=5)
        
        convert_btn = tk.Button(control_frame, text="Calcular Conversión", 
                               command=self.convert_currency, bg="#4CAF50", fg="white")
        convert_btn.grid(row=3, column=0, columnspan=2, pady=10)
        

        self.result_label = tk.Label(self.root, text="Valor: ", font=("Arial", 12, "bold"))
        self.result_label.pack(pady=10)
        
        self.rate_label = tk.Label(self.root, text="", font=("Arial", 10))
        self.rate_label.pack(pady=5)
        
        self.date_label = tk.Label(self.root, text="", font=("Arial", 9), fg="blue")
        self.date_label.pack(pady=5)
        
        self.create_rates_table()

    def create_rates_table(self):
        table_frame = tk.Frame(self.root)
        table_frame.pack(pady=20, fill="both", expand=True)
        
        tk.Label(table_frame, text="Tabla de Tipos de Cambio (Base EUR)", 
                font=("Arial", 11, "bold")).pack()
        
        columns = ("Moneda", "Tasa")
        self.rates_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
        
        self.rates_tree.heading("Moneda", text="Moneda")
        self.rates_tree.heading("Tasa", text="Tasa")
        self.rates_tree.column("Moneda", width=100)
        self.rates_tree.column("Tasa", width=100)
        
        self.rates_tree.pack(pady=10)

    def load_data(self):
        try:
            url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
            response = requests.get(url)
            
            if response.status_code == 200:
                self.parse_xml(response.content)
                self.update_interface()
                messagebox.showinfo("Éxito", "Datos cargados correctamente del BCE")
            else:
                messagebox.showerror("Error", "No se pudo conectar con el servidor del BCE")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")

    def parse_xml(self, xml_content):
        try:
            root = ET.fromstring(xml_content)
            
            namespaces = {
                'gesmes': 'http://www.gesmes.org/xml/2002-08-01',
                '': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'
            }
            
            cube_time = root.find('.//{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube[@time]', namespaces)
            if cube_time is not None:
                self.update_date = cube_time.get('time')
            
            self.rates = {'EUR': 1.0}
            
            currency_cubes = cube_time.findall('{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube', namespaces)
            
            for cube in currency_cubes:
                currency = cube.get('currency')
                rate = cube.get('rate')
                if currency and rate:
                    self.rates[currency] = float(rate)
                    
        except ET.ParseError as e:
            raise Exception(f"Error parsing XML: {str(e)}")

    def update_interface(self):
        currencies = sorted(self.rates.keys())
        self.from_currency['values'] = currencies
        self.to_currency['values'] = currencies
        
        if 'EUR' in currencies:
            self.from_currency.set('EUR')
        if 'USD' in currencies:
            self.to_currency.set('USD')
        
        self.date_label.config(text=f"Datos cargados. Fecha oficial: {self.update_date}")
        
        self.update_rates_table()

    def update_rates_table(self):
        for item in self.rates_tree.get_children():
            self.rates_tree.delete(item)
        
        self.rates_tree.insert("", "end", values=("EUR", "1.0"))
        
        for currency in sorted(self.rates.keys()):
            if currency != 'EUR':
                rate = self.rates[currency]
                self.rates_tree.insert("", "end", values=(currency, f"{rate:.4f}"))

    def convert_currency(self):
        try:
            amount = float(self.amount_entry.get().replace(',', '.'))
            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()
            
            if not from_curr or not to_curr:
                messagebox.showerror("Error", "Seleccione monedas de origen y destino")
                return
            
            if from_curr == to_curr:
                result = amount
            else:
                amount_in_eur = amount / self.rates[from_curr]
                result = amount_in_eur * self.rates[to_curr]
            
            self.result_label.config(text=f"Valor en {to_curr}: {result:.2f} {to_curr}")
            
            exchange_rate = self.rates[to_curr] / self.rates[from_curr]
            self.rate_label.config(text=f"Tipo de cambio: 1 {from_curr} = {exchange_rate:.4f} {to_curr}")
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese una cantidad válida")
        except KeyError as e:
            messagebox.showerror("Error", f"Moneda no encontrada: {e}")

def main():
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()