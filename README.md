# Projeto pessoal: desenvolvimento de um Blog de notícias com Django Framework, HTML, CSS, JavaScript, AWS (MySQL/RDS).

## Projeto: EstampaVersoShop
* **`Acesse o site aqui`:** <a href="https://estampaverso.shop/" target="_blank">https://estampaverso.shop/</a>
- Versão: 1.0

![Demonstração do site](fatosedados\media\images\demonstracao-site.gif)

## Funcionalidades do Blog:
O blog possui as seguintes funcionalidades principais:


**Páginas:**

* **`home`:** Exibe a página inicial do blog, com os posts mais visitados e os posts mais recentes.
* **`contato`:**  Permite que os usuários enviem mensagens através de um formulário de contato.
* **`sobre`:**  Exibe informações sobre o blog e seus autores.
* **`login`:**  Permite que os usuários façam login no blog.
* **`logout`:**  Faz logout do usuário.
* **`register`:**  Permite que novos usuários se cadastrem no blog.
* **`termos`:** Exibe os termos de uso do blog.
* **`privacidade`:** Exibe a política de privacidade do blog.
* **`post_list`:**  Exibe uma lista de todos os posts do blog.
* **`create_post`:** Permite que usuários criem novos posts (apenas usuários autenticados).
* **`post_edit`:** Permite que usuários editem seus próprios posts.
* **`post_delete`:** Permite que usuários excluam seus próprios posts.
* **`post`:** Exibe um post específico, com seu título, autor, conteúdo e imagem.
* **`post_mertics`:** Exibe as métricas de acessos.

**Funcionalidades da API:**
* **`api_post_metrics`:** Gera os relatórios de quantidades de acessos por dia, mês e rank com os 5 Posts mais acessados.

**Outras funcionalidades:**

* **Contador de visitas:**  Cada post possui um contador de visitas que é incrementado a cada visualização.
* **Validação de formulários:** Os formulários de contato e registro possuem validação para garantir a integridade dos dados.
* **Autenticação:** O blog possui um sistema de autenticação para permitir que usuários se cadastrem e façam login.
* **Upload de imagens:**  Os usuários podem fazer upload de imagens para seus posts.
* **Exclusão de imagens:**  As imagens antigas são excluídas automaticamente quando um post é editado e uma nova imagem é enviada.


## Parte 1: Resolvendo problemas de permissão e dependências ( apenas se você estiver utilizando Linux )

Ao realizar o deploy do site em um ambiente Ubuntu, alguns problemas comuns podem surgir relacionados a permissões de arquivos e instalação de dependências. Aqui estão algumas soluções:

**Permissões de arquivos:**

* **Problema:** Erros de permissão ao instalar as dependências do projeto.
* **Solução:** `sudo chown -R $USER:$USER /caminho/para/o/seu/projeto/venv/`

**Instalação do mysqlclient:**

* **Problema:**  Erro ao instalar a biblioteca `mysqlclient`.
* **Solução:** `sudo apt-get install pkg-config`

## Parte 2: Preparando o Ambiente Django

### Instalando as Dependências

O arquivo `requirements.txt` lista todas as bibliotecas Python necessárias. Utilize o comando `pip install -r requirements.txt`.

**Sistemas operacionais:**

* O projeto foi testado em:
    * Produção: Ubuntu 22.04 LTS
    * Desenvolvimento: Windows 11

**Arquivos para criar na raiz do projeto:**

-  .env (necessário para configurações básicas do projeto);
- certificado ssl, exemplo "us-east-2-bundle.pem" (apenas se necessário para conexão com MySQL);

Arquivo .env, bem útil para estados de uma aplicação (PROD/STAGING), armazenar credencias, caminhos de arquivos e etc.

Se você deseja apenas rodar esse projeto na sua máquina sem conectar a serviços externos adicione apenas essas 2 variáveis ao .env:

* DJANGO_DEBUG=True
* DJANGO_SECRET_KEY='crie uma chave hash e armazene aqui com seguraça'

Se for conectar a um serviço externo, como banco de dados por exemplo, siga os passos abaixo:

É uma boa prática armazenar credenciais em arquivos .env pois este arquivo na maioria das vezes possuem dados sensiveis, veja o exemplo de armazenamento de credenciais de uma conexão MySQL:

Variaveis armazenadas no arquivo .env, na raiz do projeto:
```
DB_ENGINE="django.db.backends.mysql"
DB_NAME="nome_do_banco_de_dados"
DB_USER="seu_usuario_DB"
DB_PASSWORD="senha_do_usuario_DB"
DB_HOST="host_do_seu_DB"
DB_PORT="numero_da_porta_DB"
```

## Parte 3: arquivo settings.py
### Configurações do Django (settings.py)

**Middleware:**

* `blog.middleware.VerificarURLMiddleware`: Verifica a existência de URLs.

exemplo da configuração do middleware em settings:
```python
MIDDLEWARE = [
    ...
    'blog.middleware.VerificarURLMiddleware',
]
```

**Banco de dados:**

* Desenvolvimento: SQLite (`db.sqlite3`).
* Produção: Recomenda-se MySQL ou PostgreSQL.

Configuração no arquivo settings.py para casos de conexão com serviços externos de Banco de Dados, neste caso para conexão com MySQL
- foi necessário validar a conexão com certificado ssl pois usei um serviço RDS da AWS, em outros caso pode não haver essa necessidade.
```python
DATABASES = {
    'default': {
        'ENGINE': os.getenv("DB_ENGINE"),
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
        'OPTIONS': {
            'ssl': {'ca': 'us-east-2-bundle.pem'} # utilize a validação de certificado ssl se necessário, utilizei apenas no Ubuntu.
                                                  # este certificado deve estar na raiz do projeto.
        }
    }
}
```

**Boas práticas para Migrations:**

Primeira execução:
```
python manage.py makemigrations blog
python manage.py migrate blog
python manage.py makemigrations
python manage.py migrate
```

Próximas execuções:
```
python manage.py makemigrations
python manage.py migrate
```


Com tudo configurado agora podemos rodar a aplicação com o comando abaixo:
```
python .\fatosedados\manage.py runserver 8000
```