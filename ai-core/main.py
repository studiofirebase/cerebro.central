from __future__ import annotations

import os

from config import LLM_PROVIDER
from indexer import rebuild_index
from rag import RAGEngine, active_model_name, ask_llm, llm_available


def build_prompt(question: str, context: str) -> str:
    return f"""
Você é especialista em React, Next.js e arquitetura web.
Seu foco é sugerir código limpo, performático e offline-friendly.

Contexto do projeto:
{context}

Pergunta:
{question}

Responda com passos curtos e código otimizado.
""".strip()


def _ansi_enabled() -> bool:
    term = os.getenv("TERM", "")
    return term != "dumb"


def _style(text: str, code: str) -> str:
    if not _ansi_enabled():
        return text
    return f"\033[{code}m{text}\033[0m"


def _print_header() -> None:
    title = _style("CEREBRO CENTRAL", "1;95")
    subtitle = _style("Assistente local • RAG", "2;37")
    print("\n" + _style("=" * 54, "95"))
    print(f" {title}")
    print(f" {subtitle}")
    print(_style("=" * 54, "95"))


def run() -> int:
    _print_header()

    indexed_docs = rebuild_index()
    engine = RAGEngine()
    print(f"{_style('Índice:', '1;94')} {indexed_docs} chunks carregados.")

    if not llm_available():
        print("Modelo indisponível no momento. Verifique as credenciais/configuração.")

    while True:
        try:
            question = input(f"\n{_style('✦ Você', '1;96')} > ").strip()
        except EOFError:
            break

        if not question:
            continue
        if question == "/exit":
            break
        if question == "/reindex":
            indexed_docs = rebuild_index()
            engine.reload()
            print(f"{_style('✔', '1;92')} Reindexado com {indexed_docs} chunks.")
            continue

        results = engine.search(question)
        context = engine.context_from_results(results)
        prompt = build_prompt(question, context)

        try:
            answer = ask_llm(prompt)
        except Exception as exc:  # noqa: BLE001
            print(f"{_style('Erro LLM:', '1;91')} {exc}")
            continue

        print(f"\n{_style('✦ Cerebro', '1;95')}\n")
        print(answer)

    print(_style("Encerrado.", "2;37"))
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
