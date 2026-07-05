# Instagram Downloader (GUI)

Programa com interface gráfica para colar um link do Instagram (post, reel, foto
ou carrossel) e baixar o conteúdo na melhor qualidade disponível, usando
[yt-dlp](https://github.com/yt-dlp/yt-dlp) como motor de download.

⚠️ **Uso responsável:** use apenas para conteúdo próprio ou de terceiros com
autorização explícita. Baixar posts privados ou sem permissão pode violar os
termos de uso do Instagram e direitos autorais do criador.

---

## 1. Rodar direto com Python (mais rápido para testar)

```bash
pip install -r requirements.txt
python instagram_downloader.py
```

Isso abre a janela do programa. Cole a URL, escolha a pasta de destino e
clique em **Baixar**.

## 2. Transformar em .exe autoexecutável (Windows)

Depois de confirmar que o programa funciona com `python instagram_downloader.py`,
gere o executável com PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "InstagramDownloader" instagram_downloader.py
```

- `--onefile`: gera um único arquivo `.exe`
- `--windowed`: não abre janela de console (só a interface gráfica)

O executável final fica em `dist/InstagramDownloader.exe`. Você pode copiar
esse arquivo para qualquer pasta ou pendrive e rodar sem precisar instalar
Python na máquina.

> Rode o comando `pyinstaller` no **Windows** (não no Linux/Mac) se quiser um
> `.exe` para Windows — o PyInstaller empacota para o sistema operacional em
> que ele é executado.

### macOS / Linux
No Mac, o mesmo comando gera um app executável nativo (sem extensão `.exe`).
No Linux, gera um binário executável comum.

## 3. Se o download falhar

- **"Nao foi possivel baixar esse conteudo"**: geralmente é post privado (exige
  login) ou o Instagram mudou algo e o yt-dlp precisa de atualização:
  ```bash
  pip install -U yt-dlp
  ```
- **Conteúdo privado / sua própria conta**: yt-dlp aceita cookies exportados
  do navegador para autenticar. Se precisar disso, me avise que adiciono essa
  opção na interface.

## 4. Gerar o .exe sem Python instalado (GitHub Actions - gratuito)

Se você não tem Python na sua máquina, dá para compilar o `.exe` na nuvem,
num Windows real, usando o GitHub Actions. É grátis para repositórios
públicos (e também funciona em privados, com limite de minutos gratuitos).

Passo a passo:

1. Crie uma conta gratuita em https://github.com (se ainda não tiver).
2. Crie um repositório novo (pode ser privado), por exemplo
   `instagram-downloader`.
3. Envie estes arquivos para o repositório, mantendo a estrutura de pastas:
   - `instagram_downloader.py`
   - `requirements.txt`
   - `.github/workflows/build-exe.yml`

   Isso pode ser feito direto pelo site do GitHub: entre no repositório →
   "Add file" → "Upload files" → arraste os arquivos (o GitHub cria a pasta
   `.github/workflows/` automaticamente se você fizer upload respeitando
   esse caminho).
4. Vá na aba **Actions** do repositório. Você verá o workflow
   "Build Instagram Downloader EXE".
5. Clique nele → **Run workflow** → **Run workflow** (botão verde). Isso
   inicia a compilação num Windows na nuvem (leva ~1-2 minutos).
6. Quando terminar (ícone verde), clique na execução concluída → role até
   **Artifacts** → baixe **InstagramDownloader-Windows** (vem como `.zip`
   contendo o `.exe`).
7. Extraia o `.zip` e pronto: `InstagramDownloader.exe` funciona em qualquer
   Windows, sem precisar instalar Python.

> Toda vez que você quiser gerar uma nova versão do `.exe`, basta repetir o
> passo 5 (ou fazer push de um novo commit, já que o workflow também roda
> automaticamente a cada push na branch `main`).

### Alternativas
- **Replit / Google Colab**: rodam em Linux, então não geram um `.exe` de
  Windows nativo (PyInstaller não faz compilação cruzada de forma confiável).
  Por isso o GitHub Actions com `windows-latest` é a opção mais indicada.
- **Pedir para alguém com Windows rodar os comandos do item 2 localmente**
  também funciona, caso prefira não usar o GitHub.

## Estrutura de arquivos

```
insta_downloader/
├── instagram_downloader.py        # programa principal (GUI)
├── requirements.txt               # dependências
├── README.md                      # este arquivo
└── .github/
    └── workflows/
        └── build-exe.yml          # workflow do GitHub Actions (compila o .exe)
```
