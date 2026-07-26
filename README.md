# 📘 Manual do SoYuAPI
**Cliente HTTP Completo para Testes de API**
`Versão 2.0`

---

## 📖 Navegação Rápida
* [Introdução](#-introdução)
* [Interface](#-interface)
* [Requisição](#-como-fazer-uma-requisição)
* [Parâmetros](#-parâmetros-query-string)
* [Headers](#-headers)
* [Body](#-body)
* [Autenticação](#-autenticação)
* [Resposta](#-resposta)
* [Atalhos](#-atalhos-de-teclado)
* [Dicas](#-dicas-e-truques)

---

## 📖 Introdução
O **SoYuAPI** é um cliente HTTP completo, desenvolvido em Python com Tkinter. Ele permite testar APIs REST de forma fácil e intuitiva, com suporte a todos os métodos HTTP, autenticação, headers personalizados e muito mais.

* ⚡ **Métodos HTTP:** GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS
* 🔗 **Parâmetros:** Query strings com edição inline
* 📋 **Headers:** Personalize cabeçalhos facilmente
* 📦 **Body:** JSON, Form-Data, XML, GraphQL
* 🔐 **Autenticação:** Basic, Bearer Token, API Key
* 💾 **Salvar/Ler:** Salve e carregue requisições

---

## 🖥️ Interface
A interface é dividida em duas áreas principais:

| 📤 Painel Esquerdo (Requisição) | 📥 Painel Direito (Resposta) |
| --- | --- |
| • Barra de ferramentas (método, URL, botões)<br>• Abas: Parâmetros, Headers, Body, Autenticação | • Status, tempo e tamanho da resposta<br>• Abas: Resposta, Headers, Preview |

> 💡 **Dica:** Você pode redimensionar os painéis arrastando a barra divisória no centro da tela.

---

## 📤 Como Fazer uma Requisição
1. **Selecione o Método HTTP:** Escolha entre GET, POST, PUT, DELETE, PATCH, HEAD ou OPTIONS no dropdown da barra de ferramentas.
2. **Digite a URL:** Insira o endereço do endpoint no campo de texto. Exemplo: `https://api.exemplo.com/users`
3. **Configure a Requisição:** Adicione parâmetros, headers, body e autenticação conforme necessário.
4. **Envie:** Clique no botão **🚀 Enviar** ou pressione `Ctrl+Enter`.
5. **Analise a Resposta:** Veja o resultado no painel direito, com status, tempo, corpo e headers da resposta.

> ⚠️ **Atenção:** Certifique-se de que a URL está correta e que o servidor está acessível.

---

## 🔗 Parâmetros (Query String)
Os parâmetros são adicionados automaticamente à URL como query string.

### Como adicionar parâmetros:
1. Vá para a aba **🔗 Parâmetros**
2. Clique em **+ Adicionar Parâmetro**
3. Preencha a **Chave** e o **Valor**
4. Para editar, dê **duplo clique** na célula

```text
// Exemplo: Parâmetros adicionados à URL
[https://api.exemplo.com/users?page=1&limit=10&sort=name](https://api.exemplo.com/users?page=1&limit=10&sort=name)

```

> 💡 **Dica:** Use `Enter` para confirmar a edição e `Esc` para cancelar.

---

## 📋 Headers

Os headers são enviados com a requisição para fornecer informações adicionais ao servidor.

### Headers padrão já configurados:

| Header | Valor | Descrição |
| --- | --- | --- |
| `Content-Type` | `application/x-www-form-urlencoded` | Formato dos dados enviados |
| `Accept` | `*/*` | Aceita qualquer tipo de resposta |
| `User-Agent` | `SoYuAPI/1.0` | Identificação do cliente |

### Como adicionar headers personalizados:

1. Vá para a aba **📋 Headers**
2. Clique em **+ Adicionar Header**
3. Digite a **Chave** e o **Valor**
4. Os headers são enviados automaticamente na requisição

```http
// Exemplo de headers comuns:
Authorization: Bearer seu_token_aqui
X-API-Key: sua_chave_api
Content-Type: application/json

```

---

## 📦 Body

O corpo da requisição contém os dados que você deseja enviar ao servidor.

### Tipos de Body suportados:

* **Form-Data:** `chave1=valor1&chave2=valor2`
* **JSON:** `{"chave": "valor"}`
* **XML:** `<dados><chave>valor</chave></dados>`
* **Raw:** Qualquer texto puro

### Como usar o Body:

1. Vá para a aba **📦 Body**
2. Selecione o formato desejado (JSON, Form-Data, XML, etc.)
3. Digite ou cole o conteúdo na área de texto
4. O header `Content-Type` será atualizado automaticamente

> 💡 **Dica:** Ao selecionar JSON, o SoYuAPI valida a sintaxe e destaca erros.

---

## 🔐 Autenticação

O SoYuAPI suporta os métodos de autenticação mais comuns.

### Tipos de Autenticação:

1. **Basic Auth:** Informar Usuário e Senha
2. **Bearer Token:** Informar o Token JWT ou de acesso
3. **API Key:** Informar Nome da Chave, Valor e Onde enviar (Header ou Query)

---

## 📥 Resposta

O painel direito exibe o retorno do servidor.

### Informações exibidas:

* **Status Code:** ex: `200 OK`, `404 Not Found`, `500 Server Error`
* **Tempo de Resposta:** em milissegundos (ms)
* **Tamanho da Resposta:** em bytes ou KB
* **Abas da Resposta:**
* **Corpo (Response):** Exibe o conteúdo formatado (JSON, HTML, XML, etc.)
* **Headers:** Cabeçalhos retornados pelo servidor
* **Preview:** Visualização renderizada (para respostas HTML)



---

## ⌨️ Atalhos de Teclado

| Atalho | Ação |
| --- | --- |
| `Ctrl + Enter` | Enviar requisição |
| `Ctrl + N` | Nova requisição |
| `Ctrl + S` | Salvar requisição |
| `Ctrl + O` | Abrir requisição salva |
| `Ctrl + L` | Limpar campos |

---

## 💡 Dicas e Truques

* **Diagnóstico de Erros:** Se a requisição falhar, verifique o Status Code no painel de resposta.
* **Salvamento:** As requisições salvas em formato JSON podem ser reutilizadas a qualquer momento.
* **Form-Data:** O formato correto é `chave=valor&outra_chave=outro_valor`, sem espaços desnecessários.

---

*📘 Manual do SoYuAPI • Versão 2.0 • Desenvolvido em Python com Tkinter*
