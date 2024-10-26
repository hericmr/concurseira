import os

# Caminho para a pasta downloads
downloads_path = './downloads'

# Crie ou sobrescreva o arquivo index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write('<!DOCTYPE html>\n')
    f.write('<html lang="pt-BR">\n')
    f.write('<head>\n')
    f.write('    <meta charset="UTF-8">\n')
    f.write('    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
    f.write('    <title>Downloads</title>\n')
    f.write('    <style>\n')
    f.write('        body { font-family: Arial, sans-serif; margin: 20px; }\n')
    f.write('        h1 { color: #333; }\n')
    f.write('        ul { list-style-type: none; padding: 0; }\n')
    f.write('        li { margin: 5px 0; }\n')
    f.write('        a { text-decoration: none; color: #007BFF; }\n')
    f.write('        a:hover { text-decoration: underline; }\n')
    f.write('    </style>\n')
    f.write('</head>\n')
    f.write('<body>\n')
    f.write('    <h1>Downloads</h1>\n')
    f.write('    <ul>\n')

    # Listar todos os arquivos na pasta downloads
    for filename in os.listdir(downloads_path):
        if filename.endswith('.pdf'):  # Filtra apenas arquivos PDF
            f.write(f'        <li><a href="{downloads_path}/{filename}">{filename}</a></li>\n')

    f.write('    </ul>\n')
    f.write('</body>\n')
    f.write('</html>\n')

print("Arquivo index.html gerado com sucesso!")
