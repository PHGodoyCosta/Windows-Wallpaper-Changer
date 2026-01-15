# Trocador de Automático de Wallpaper

Quando estava no seminário em 2025, meu amigo Marcos, me pediu uma forma de trocar seu wallpaper do windows aleatoriamente com suas imagens.

E que trocasse sozinho tambem, automaticamente quando ligasse o computador.

Então montei esse script python simples para windows.

É necessário fazer o build com PyInstaller:

```bash
python -m PyInstaller server.spec --clean
```

## Instruções para configuração:

* No construtor da classe, seto essas duas variáveis:
```python
self.pathImagens = str(Path.home() / "OneDrive" / "Documentos" / "Wallpapers" / "Imagens")

self.logPath = str(Path.home() / "OneDrive" / "Documentos" / "Wallpapers" / "log.json")
```

* o pathImagens é o caminho para a pasta onde você pode colocar todas as imagens que quer usar no wallpaper.

* logPath é o arquivo que vai manter o nome do wallpaper atual. Recomendo manter na pasta de Wallpapers.

## Instruções para uso:

* Recomendado manter o arquivo buildado .exe em algum lugar visível, como a Área de trabalho, para fácil uso.

* Após as configurações iniciais, basta executar ele quando quiser trocar de wallpaper.

* Se quiser que o wallpaper seja trocado ao inicializar o computador, copie o programa para o path:

```txt
C:\Users\<USUÁRIO>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```

