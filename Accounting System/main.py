import datetime as dt
import time
import crud

"""
    CLI Budget App using Postgres

Features:   
    (1) General Journal - contains all transactions using double entry bookkeeping format
    (2) General Ledgers - contains all transactions on a per account basis
    (3) Trial Balance - Summarizes all accounts and their balances
    (4) Balance Sheet - Assets, Liabilities and Net Worth
    (5) Cash Flow Statement - Shows free cash available at the end of the period

"""


class FinanceApp:
    def __init__(self, year):
        self.m_menu = (
            '''What would you like to do today? Please enter the number from below:
                    (1) Enter Journal Entry transaction
                    (2) View Trial Balance
                    (3) Edit Chart of Accounts
                    (4) Generate Balance Sheet
                    (5) Generate Cash Flow Statement
                    (6) Generate Ledger
                    (7) Import Data (in development)
                    (8) Export data (in development)
            ''')
        self.sl_menu = (
            ''' Choose one of the following:
                    (a) GL Accounts - Detailed
                    (b) Subsidiary Ledgers - Detailed
            ''')

        self.year = year

    def run(self):

    # Welcome Screen
        print('Welcome to the Personal Finance Tracker\n')
        time.sleep(1)
        
    # Get user Input. Print the menu once
        print(self.m_menu)    

        while True:
            user_input = int(input('Number:\t'))
            match user_input:
                case 1:     # Go to Journal Section
                    self.journal()
                    break
                case 2:   # Go to TB Section
                    self.accounts(type='tb')
                    break
                case 3:   # Go to CoA Section
                    self.accounts(type='coa')
                    break
                case 4:   # Go to Balance Sheet
                    self.balance_sheet()
                    break
                case 5:   # Go to Cash Flow

                    break
                case 6:   # Go to Ledger options
                    while True:
                        print(self.sl_menu)
                        sl_input = input('Choice:\t')
                        if sl_input == 'a':     # Go to GL Accounts

                            break
                        elif sl_input == 'b':   # Go to Sub Ledger 

                            break
                        else:
                            print('Invalid selection, please choose the letter from the list.')

                    break
                case 7:   # Go to Journal Section

                    break            
                case 8:   # Go to Journal Section

                    break        
                case _: 
                    print('Invalid selection, please enter the number only.')
                
    def exit_prompt(self):
        ans = input("Would you like to exit this app? (y/n)")
        if ans.lower().strip() == 'n':
            self.run()
        else:
            print('Bye!')

    def journal(self):
        pass

    def accounts(self,type='coa'):
        df = crud.get_account()
        df['abs_amt'] = df['Amount'].map(lambda x: abs(x))

        # code, name, category, amount = 200, 'Accounts Receivable', 'Current Assets', 35000
        year_end = dt.datetime(self.year, 12, 31).strftime('%B %d, %Y')

        code_width = 6
        name_width = min(30, df['Description'].str.len().max())
        type_width = 25
        amt_width = 13

        # cell = '|' + {placeholder.center(length)} + '|'

        if type == 'coa':
            title = 'Chart of Accounts'
            amt_width = 0
            extra_cheader = 'Account Type'.center(type_width) + '|'

        elif type == 'tb':
            title = 'Trial Balance'
            type_width = 0
            extra_cheader = 'Amount'.center(amt_width) + '|'
        
        inner_span = code_width + name_width + max(type_width, amt_width) + 2

    # Arrange the top part of the table that contains the title and date
        theader_top = '+' + ('-' * inner_span) + '+'
        title_line = '|' + title.center(inner_span) + '|'
        date_line = '|' + year_end.center(inner_span) + '|'
        border_intersect = '+' + ('-' * code_width) + '+' + ('-' * name_width) + '+' + ('-' * max(type_width, amt_width)) + '+'

    # Arrange the column header section
        cheader_space = '|' + (' ' * code_width) + '|' + (' ' * name_width) + '|' + (' ' * max(type_width, amt_width)) + '|' 
        cheader_names = '|' + ('Code'.center(code_width)) + '|' + ('Account Name'.center(name_width)) + '|' + extra_cheader 
        
    # Print header values
        theader = theader_top + '\n' + title_line + '\n' + date_line + '\n' + border_intersect
        cheader = cheader_space + '\n' + cheader_names + '\n' + border_intersect
        print(theader)
        print(cheader)

    # Fetch data and populate columns
        for i in range(len(df)):
            code = str(df.iloc[i,0])
            name = df.iloc[i,1]
            acc_type = df.iloc[i,2]
            amount = format(int(df.iloc[i,-1]), ',.2f')
            total = sum(df.Amount)
            
            if type == 'coa':
                table_row = '|' + code.center(code_width) + '|' + name.center(name_width) + '|' + acc_type.center(type_width) + '|'

            elif type == 'tb':
                table_row = f'|{code.center(code_width)}|{name.ljust(name_width)}|{amount.rjust(amt_width)}|'
                total_row = '|' + (' ' * code_width) + '|' + 'Total'.ljust(name_width) + '|' + format(int(total), ',.2f').rjust(amt_width) + '|'

            print(table_row)

            if i == len(df)-1:
                print(border_intersect)
                print(total_row)
                print(border_intersect)

    def balance_sheet(self):
        pass

if __name__ == '__main__':
    park = FinanceApp(2022)
    park.run()
