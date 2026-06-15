import os
import wikipediaapi

os.makedirs('bios', exist_ok=True)    # Make bios folder to store player info

folder_name = 'bios'

wiki = wikipediaapi.Wikipedia('NBARAGAgent/1.0', 'en')

players = ['Kobe Bryant', 'Lebron James', 'Derrick Rose', 'Stephen Curry', 'Kyrie Irving', 'Kemba Walker', 'Paul George', 'Michael Jordan', 'Jalen Brunson', 'Jeremy Lin']

for player in players:

    file_path = os.path.join(folder_name, f'{player}.txt')

    if not os.path.exists(file_path):

        page = wiki.page(player)

        if page.exists():
            print(page.text[:500])

            with open(file_path, mode='w', encoding='utf-8') as file:
                file.write(page.text)
                
            print(f'Successfully wrote data to {player}.txt')
            
        else:
            print('Page not found')

    else:
        print('File already exists')   