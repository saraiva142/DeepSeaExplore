from wikipedia import page, summary, set_lang, exceptions
import re

def obter_resumo_especie(nome_cientifico, idioma="en"):
    set_lang(idioma)
    try:
        p = page(nome_cientifico)
        resumo = p.summary  # <-- Corrigido aqui

        # Remove seções indesejadas (como "== Espécies ==" e o que vem depois)
        resumo = re.split(r"\n== .*? ==\n", resumo)[0]

        # Remove listas longas de nomes, mantendo só parágrafos com frase completa
        linhas = resumo.splitlines()
        linhas_filtradas = [linha for linha in linhas if len(linha.split()) > 4]
        resumo_limpo = " ".join(linhas_filtradas).strip()

        return {
            "titulo": p.title,
            "resumo": resumo_limpo,
            "url": p.url
        }

    except exceptions.DisambiguationError as e:
        return {"erro": f"O nome '{nome_cientifico}' é ambíguo. Exemplos: {e.options[:3]}"}
    except exceptions.PageError:
        return {"erro": f"Nenhuma página encontrada para '{nome_cientifico}'"}
    except Exception as e:
        return {"erro": f"Erro inesperado: {str(e)}"}
