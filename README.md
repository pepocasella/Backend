

# Frontend

### Como subir o frontend
- nvm use 20
- npm run dev

### Informações
- Frontend: http://localhost:5173/

# Backend

### Como subir o backend
- pyenv install 3.12.5
- pyenv global 3.12.5
- python3 -m venv est
- source est/bin/activate
- pip install requirements.txt
- python manage.py runserver 0.0.0.0:8000

### Informações

- Django Ninja: http://127.0.0.1:8000/api/docs 
- Django Admin http://127.0.0.1:8000/admin/login/?next=/admin/ 



# Projeto Fase 2

1. Criar endpoints no Django Ninja para:
    - Listar todas as estações
    - Recuperar uma estação específica
    - Criar uma nova estação
    - Atualizar uma estação existente
    - Deletar uma estação  

2. Gerar schemas Pydantic para validação do request e response.  

3. Criar o front-end em Vue.js com:
    - Tela para listar todas as estações
    - Formulário para criar e editar estações
    - Botão para deletar uma estação
    - Integração completa com os endpoints do Django Ninja usando fetch ou axios  

4. Gerar código limpo e organizado, usando boas práticas de Django Ninja e Vue.js, incluindo tratamento de erros e mensagens de sucesso.  
