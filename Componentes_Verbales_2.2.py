import requests
from bs4 import BeautifulSoup
from googletrans import Translator
from manual_translations import manual_translations

translator = Translator()

# Función para buscar y mostrar el componente verbal de un hechizo específico
def get_verbal_component(spell_name_input):
    # URL base de la página con la lista de hechizos
    base_url = 'https://www.thievesguild.cc/spells/'
    
    # URL de la lista de hechizos
    list_url = f'{base_url}index'
    
    # Hacemos la solicitud para obtener la página con la lista de hechizos
    response = requests.get(list_url)
    
    # Parseamos el contenido HTML de la página
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Buscamos todas las filas de hechizos
    spell_rows = soup.find_all('tr', class_='contentrow')
    
    # Variable para verificar si encontramos el hechizo
    spell_found = False

    # Normalizamos el nombre del hechizo traducido eliminando espacios y convirtiéndolo a minúsculas
    spell_name_input_normalized = spell_name_input.lower().replace(" ", "")

    # Recorremos cada hechizo para buscar el que coincide con el nombre ingresado
    for row in spell_rows:
        spell_name_tag = row.find('a')  # El enlace que contiene el nombre y la URL del hechizo
        if spell_name_tag:
            spell_name = spell_name_tag.text.strip()
            spell_url = spell_name_tag['href']

            # Normalizamos el nombre del hechizo en la lista de la página eliminando espacios y convirtiéndolo a minúsculas
            spell_name_normalized = spell_name.lower().replace(" ", "")

            # Si encontramos el hechizo ingresado por el usuario (normalizado)
            if spell_name_normalized == spell_name_input_normalized:
                spell_found = True
                # Hacemos la solicitud para obtener la página del hechizo
                spell_response = requests.get(spell_url)
                spell_soup = BeautifulSoup(spell_response.content, 'html.parser')
                
                # Buscamos el componente verbal dentro de la página del hechizo
                verbal_component = spell_soup.find('div', class_='spell-box-compv')
                verbal_component_2 = spell_soup.find('div', class_='spell-box-compv2')
                if verbal_component:
                    # Extraemos el texto del componente verbal
                    verbal_text = verbal_component.find('b').next_sibling.strip()
                    print(f'\nHechizo: {spell_name.capitalize()}\nVerbal Component: {verbal_text.capitalize()}')
                    
                    if verbal_component_2:
                        verbal_text_2 = verbal_component_2.find('b').next_sibling.strip()
                        print(f'Verbal Component (Alternative): {verbal_text_2}\n')
                else:
                    print(f'El hechizo "{spell_name}" no tiene un componente verbal.')
                break
    
    if not spell_found and spell_name_input != "":
        # Traducir el nombre del hechizo a latín como alternativa en caso de no encontrarlo
        traduccion = translator.translate(spell_name_input, dest='la')
        print(f'\nHechizo: {spell_name_input.capitalize()}\nVerbal Component: {traduccion.text.capitalize()}\n')

while True:
    # Pedimos al usuario que ingrese el nombre de un hechizo en español
    spell_name_input = input("Ingresa el nombre del hechizo: ")

    # Si el usuario ingresa una cadena vacía, terminamos el bucle
    if spell_name_input == "":
        break

    # Revisamos si el nombre del hechizo está en el diccionario de traducciones manuales
    if spell_name_input.lower() in manual_translations:
        translated_spell_name = manual_translations[spell_name_input.lower()]
    else:
        # Si no está en el diccionario, utilizamos googletrans para traducir
        traduccion = translator.translate(spell_name_input, src='es', dest='en')
        translated_spell_name = traduccion.text
    
    # Llamamos a la función para buscar el componente verbal del hechizo ingresado (traducido)
    get_verbal_component(translated_spell_name)
