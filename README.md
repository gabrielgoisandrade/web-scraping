# Serviço de Web Scraping - Secretaria do Estado de São Paulo


## Descrição

**Esse serviço é parte de um projeto da faculdade, que consiste em mapear as regiões com maiores índices de estupro, em São Paulo.  
O serviço é responsável por realizar a captura dos dados referentes a estupro tanto do ano passado, quando do ano atual, 
realizando a junção dos mesmos em um único dado e os enviando diretamente ao Mongodb Atlas.**

### Iniciando o projeto
Dentro do diretório do projeto, no terminal, rode o seguinte comando:

```python
pip install -r requirements.txt
 ``` 

#### Database

Mude as credenciais do database em:
```text
database
|
|__ __init__.py
|
|__ connection_database.py
``` 

Alterando as seguintes variáveis:
```python
__USER: str = 'seu user'
__PSSW: str = 'sua senha'
__CLUSTER: str = 'seu cluster'
__DATABASE: str = 'seu database'
```

#### Estrutura 

```text
web-scraping
|
|__ database
|   |
|   |__ __init__.py
|   |
|   |__ connection_database.py
|
|__ log
|   |
|   |__ __init__.py
|   |
|   |__ log_config.py
|
|__ selector
|   |
|   |__ helper
|   |   |
|   |   |__ __init__.py
|   |   |
|   |   |__ selector_helper.py
|   |   
|   |__ __init__.py
|   |
|   |__ data_selector.py
|
|__ services
|   |
|   |__ helper
|   |   |
|   |   |__ __init__.py
|   |   |
|   |   |__ extractor_helper.py
|   |   |
|   |   |__ send_data_helper.py
|   |   
|   |__ __init__.py
|   |
|   |__ extractor_service.py
|   |
|   |__ selector_service.py
|   |
|   |__ send_data_service.py
|   |
|   |__ update_data_service.py
|
|__ app.py
|
|__ chromedriver.exe
```
---

> *__Caso apareça uma mensagem de erro parecida com essa:__*
```shell script
Selenium message:session not created: This version of ChromeDriver only supports Chrome version XX
```

**Acesse esse [link][chromedriver-url], baixe a versão mais atual do chromedriver (que seja compatível com a versão do seu browser), substitua o antigo e rode o projeto novamente.**

[chromedriver-url]: https://chromedriver.chromium.org/downloads
