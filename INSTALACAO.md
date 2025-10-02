# 📦 Guia de Instalação - Sistema de Análise GEX

## Passo a Passo para Configurar no GitHub

### 1️⃣ Criar Repositório no GitHub

1. Acesse [GitHub](https://github.com) e faça login
2. Clique no botão **"+"** no canto superior direito
3. Selecione **"New repository"**
4. Dê um nome ao repositório (ex: `gex-analysis` ou `nasdaq-gamma-analysis`)
5. Escolha se será **Público** ou **Privado**
6. **NÃO** marque "Add a README file" (já temos um)
7. Clique em **"Create repository"**

---

### 2️⃣ Fazer Upload dos Arquivos

**Opção A - Via Interface Web (Mais Fácil):**

1. Na página do seu novo repositório, clique em **"uploading an existing file"**
2. Arraste **TODOS** os arquivos e pastas extraídos do ZIP
3. Aguarde o upload completar
4. Role para baixo e clique em **"Commit changes"**

**Opção B - Via Git (Linha de Comando):**

```bash
# Navegue até a pasta extraída
cd caminho/para/gex-analysis-system

# Inicialize o repositório
git init

# Adicione todos os arquivos
git add .

# Faça o primeiro commit
git commit -m "🚀 Configuração inicial do sistema de análise GEX"

# Conecte ao repositório remoto (substitua SEU_USUARIO e SEU_REPO)
git remote add origin https://github.com/SEU_USUARIO/SEU_REPO.git

# Envie os arquivos
git branch -M main
git push -u origin main
```

---

### 3️⃣ Obter Chave de API (Gratuita)

1. Acesse: https://www.alphavantage.co/support/#api-key
2. Preencha o formulário simples
3. Copie a chave de API que aparecerá na tela

---

### 4️⃣ Configurar Secret no GitHub

1. No seu repositório, vá para **Settings** (aba no topo)
2. No menu lateral esquerdo, clique em **Secrets and variables** > **Actions**
3. Clique no botão **"New repository secret"**
4. Preencha:
   - **Name:** `ALPHA_VANTAGE_API_KEY`
   - **Secret:** Cole a chave de API que você copiou
5. Clique em **"Add secret"**

---

### 5️⃣ Ativar GitHub Actions

1. Vá para a aba **Actions** no seu repositório
2. Se aparecer uma mensagem pedindo para habilitar workflows, clique em **"I understand my workflows, go ahead and enable them"**

---

### 6️⃣ Executar Primeira Análise (Opcional)

Para não esperar até o próximo dia útil, você pode executar manualmente:

1. Na aba **Actions**, clique em **"Análise Diária de GEX"** no menu lateral
2. Clique no botão **"Run workflow"** (à direita)
3. Clique novamente em **"Run workflow"** no popup
4. Aguarde alguns minutos
5. Volte para a página principal do repositório e veja o README.md atualizado!

---

## ✅ Pronto!

Seu sistema está configurado e funcionando! A partir de agora, ele executará automaticamente todos os dias úteis às 13:00 UTC (antes da abertura do mercado americano).

---

## 🆘 Problemas Comuns

### "Error: Process completed with exit code 1"

**Causa:** Chave de API não configurada ou inválida  
**Solução:** Verifique se o secret `ALPHA_VANTAGE_API_KEY` foi criado corretamente

### "API rate limit exceeded"

**Causa:** Limite de requisições da API gratuita atingido  
**Solução:** Aguarde 1 minuto e tente novamente. O plano gratuito tem limite de 25 requisições por dia.

### Estrutura de pastas incorreta

**Causa:** Arquivos foram enviados na raiz sem as pastas  
**Solução:** Delete tudo e faça o upload novamente, garantindo que as pastas `.github`, `src`, `data` e `charts` estejam presentes

---

## 📞 Suporte

Se tiver dúvidas, abra uma **Issue** no repositório.
