# Web Scraping - Secretaria do Estado de São Paulo

## Descrição
[ssp-url]: https://www.ssp.sp.gov.br/

**Extração de dados referentes a estupro, diretamente da _[Secretaria do Estado de São Paulo][ssp-url]_.  
Os dados que estão sendo extraídos são tanto do ano passado, quanto do ano atual.**

**Os dados são tratados, estruturados e, por fim, enviados para o banco de dados.  
O tipo de banco de dados escolhido foi um NoSQL (MongoDB).**

**Esse serviço conta com uma verificação de dados.   
Ou seja, cada vez que o for detectada uma alteração e/ou inclusão de algum dado, por parte da SSP, os dados   
(já armazenados no banco de dados) serão atualizados.**

### Iniciando o projeto
Dentro do diretório do projeto, no terminal, rode o seguinte comando:

```shell script
pip install -r requirements.txt
 ``` 

#### Estrutura 

```text
web-scraping
|
|__ driver
|   |
|   |__ chromedriver.exe
|
|__ logs
|   |
|   |__ app.log
|
|__ src
|   |
|   |__ database
|   |   |
|   |   |__ __init__.py
|   |   |
|   |   |__ connectionDatabase.py
|   |   |
|   |   |__ operationsDatabase.py
|   |
|   |__ log
|   |   |
|   |   |__ __init__.py
|   |   |
|   |   |__ logConfig.py
|   |   
|   |__ selector
|   |   |
|   |   |__ __init__.py
|   |   |
|   |   |__ dataSelector.py
|   |
|   |__services
|   |   |
|   |   |__ __init__.py
|   |   |
|   |   |__ extractorService.py
|   |   |
|   |   |__ selectorService.py
|   |   |
|   |   |__ sendDataService.py
|   |
|   |__ __init__.py
|
|__ app.py

```
---

> *__Caso apareça uma mensagem de erro parecida com essa:__*
```shell script
Selenium message:session not created: This version of ChromeDriver only supports Chrome version XX
```

> **Acesse esse [link][chromedriver-url], baixe a versão mais atual do chromedriver (que seja compatível com a versão do seu browser), substitua o antigo e rode o projeto novamente.**

[chromedriver-url]: https://chromedriver.chromium.org/downloads

> ### O.B.S.: PROJETO COM FINALIDADE ACADÊMICA. 