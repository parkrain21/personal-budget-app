from ctypes import alignment
import PySimpleGUI as sg

def calculate_graduated(taxable, mode='itemized'):
    taxable = float(taxable)
    if mode == 'osd':
        taxable = taxable * 0.60

    if taxable <= 250000:
        tax = 0
    elif 250000 < taxable <= 400000:
        tax = 0 + (taxable - 250000) * 0.15
    elif 400000 < taxable <= 800000:
        tax = 22500 + (taxable - 400000) * 0.20
    elif 800000 < taxable <= 2000000:
        tax = 102500 + (taxable - 800000) * 0.25
    elif 2000000 < taxable <= 8000000:
        tax = 402500 + (taxable - 2000000) * 0.30
    elif taxable > 8000000:
        tax = 2202500 + (taxable - 8000000) * 0.35
    
    return f'P {tax:,.2f}'

def calculate_special(gross):
    gross = float(gross)
    tax = max(0, (gross - 250000) * 0.08)
    return f'P {tax:,.2f}'

result_leyout = [ 
            [sg.Text('8% Special Rate: ', size=15, p=((50,0),(0,0))), sg.Text('P xx,xxx.xx', size=15, p=((50,0),(0,0)), key='-GRT-RESULT')],
            [sg.Text('Graduated - OSD: ', size=15, p=((50,0),(0,0))), sg.Text('P xx,xxx.xx', size=15, p=((50,0),(0,0)), key='-OSD-RESULT')],
            [sg.Text('Graduated - Itemized: ', size=15, p=((50,0),(0,0))), sg.Text('P xx,xxx.xx', size=15, p=((50,0),(0,0)), key='-ITEMIZED-RESULT')]
        ]

layout = [  
            [sg.Push(), sg.Text('PH Tax Calculator', font='Arial'), sg.Push()],
            [sg.Text('Gross Receipts', size=15), sg.InputText(key='-GROSS-', size=35, default_text='0.00')],
            [sg.Text('Total Deductions', size=15), sg.InputText(key='-DEDUCTIONS-', size=35, default_text='0.00')],
            [sg.Text('Taxable Income', size=15), sg.InputText(key='-TAXABLE-', size=35, default_text='0.00', readonly=True)],
            [sg.Push(), sg.Button('Calculate', size=(14, 1), bind_return_key=True), sg.Button('Reset', size=(14, 1)), sg.Push()], 
            [sg.VPush()],
            [sg.Frame('Results', result_leyout, title_location='n', size=(380,100))]
            
        ]

# Create the Window
window = sg.Window('Window Title', layout=layout,)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    print(values)
    if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
        break

    if event == 'Reset':
        for key in values:
            window[key]('')

    if event == 'Calculate':
        taxable = float(values['-GROSS-']) - float(values['-DEDUCTIONS-'])
        window['-TAXABLE-'](f'{taxable:,.2f}')

        special_tax = calculate_special(values['-GROSS-'])
        osd_tax = calculate_graduated(float(values['-GROSS-']) * 0.6, mode='osd')
        itemized_tax = calculate_graduated(taxable, mode='itemized')

        window['-GRT-RESULT'](special_tax)
        window['-OSD-RESULT'](osd_tax)
        window['-ITEMIZED-RESULT'](itemized_tax)
    
window.close()