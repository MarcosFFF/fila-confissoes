# -*- coding: utf-8 -*-
"""
Fila de Confissões (Streamlit)

Lista única de pessoas; a escolha do padre acontece na hora em que a pessoa vai.
O padre fica ocupado até clicar em "Concluir" (check verde).

Senha (opcional): em Settings > Secrets do Streamlit Cloud, escreva
    senha = "combine-uma-senha"
Quem abrir o link com ?senha=combine-uma-senha entra direto.
"""
import hmac
import json
import re
import threading
import time
import unicodedata
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

import streamlit as st

LOGO = "data:image/jpeg;base64,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"

PADRES_INICIAIS = ["Frei Garcia", "Padre Kleriston", "Padre Rogério", "Dom Lucas", "Padre Augusto"]
DATA_FILE = Path(__file__).with_name("fila_confissoes_dados.json")

try:
    from zoneinfo import ZoneInfo
    TZ = ZoneInfo("America/Sao_Paulo")
except Exception:  # sem base de fusos: Brasília é UTC-3 o ano todo
    TZ = timezone(timedelta(hours=-3))


class Err(Exception):
    """Erro de regra, mostrado ao usuário."""


def ms():
    return int(time.time() * 1000)


def hhmm(t):
    return datetime.fromtimestamp(t / 1000, TZ).strftime("%H:%M") if t else ""


def slug(texto, usados):
    base = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii").lower()
    base = re.sub(r"[^a-z0-9]+", "-", base).strip("-") or "padre"
    novo, n = base, 2
    while novo in usados:
        novo = "%s-%d" % (base, n)
        n += 1
    return novo


def esc(texto):
    """Escapa o markdown: nomes digitados por qualquer pessoa aparecem só como texto."""
    return re.sub(r"([\\`*_{}\[\]()#+\-.!|<>~$&:@^])", r"\\\1", texto or "")


def limpar_nome(raw):
    return " ".join(str(raw or "").split())[:60]


class Store:
    """Lista compartilhada por todas as pessoas que abrirem o app."""

    def __init__(self):
        self.lock = threading.RLock()
        self.state = None
        self._carregar()

    @staticmethod
    def _inicial():
        padres, usados = [], set()
        for i, nome in enumerate(PADRES_INICIAIS):
            pid = slug(nome, usados)
            usados.add(pid)
            padres.append({"id": pid, "name": nome, "order": i + 1})
        return {"v": 0, "priests": padres, "queue": []}

    def _carregar(self):
        try:
            dados = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            if not isinstance(dados.get("priests"), list) or not isinstance(dados.get("queue"), list):
                raise ValueError("formato inválido")
            dados.setdefault("v", 0)
            self.state = dados
        except Exception:
            self.state = self._inicial()

    def _salvar(self):
        try:  # guarda em arquivo quando o servidor deixa; se não deixar, segue só na memória
            tmp = DATA_FILE.with_suffix(".tmp")
            tmp.write_text(json.dumps(self.state, ensure_ascii=False), encoding="utf-8")
            tmp.replace(DATA_FILE)
        except Exception:
            pass

    def foto(self):
        with self.lock:
            return json.loads(json.dumps(self.state))

    # ---- auxiliares (sempre com lock em mãos) ----
    def _pessoa(self, pid):
        for p in self.state["queue"]:
            if p["id"] == pid:
                return p
        raise Err("Essa pessoa não está mais na lista.")

    def _padre(self, pid):
        for p in self.state["priests"]:
            if p["id"] == pid:
                return p
        raise Err("Esse padre não está mais na lista.")

    def _ocupado(self, pid):
        for p in self.state["queue"]:
            if p["status"] == "confessing" and p.get("priestId") == pid:
                return p
        return None

    def _chave_frente(self):
        chaves = [p["sortKey"] for p in self.state["queue"] if p["status"] == "waiting"]
        return min(chaves) - 1 if chaves else ms()

    def _chave_final(self):
        return max([ms()] + [p.get("sortKey", 0) + 1 for p in self.state["queue"]])

    def agir(self, a):
        with self.lock:
            tipo = a.get("action")
            agora = ms()
            q = self.state["queue"]

            if tipo == "addPerson":
                nome = limpar_nome(a.get("name"))
                if not nome:
                    raise Err("Digite um nome.")
                q.append({"id": uuid.uuid4().hex[:8], "name": nome, "status": "waiting",
                          "priestId": None, "priestName": None, "createdAt": agora,
                          "sortKey": self._chave_final(), "startedAt": None, "doneAt": None})

            elif tipo == "start":
                pessoa, padre = self._pessoa(a.get("id")), self._padre(a.get("priestId"))
                if pessoa["status"] != "waiting":
                    raise Err("%s já não está esperando." % pessoa["name"])
                if self._ocupado(padre["id"]):
                    raise Err("%s já está confessando outra pessoa." % padre["name"])
                pessoa.update({"status": "confessing", "priestId": padre["id"],
                               "priestName": padre["name"], "startedAt": agora, "doneAt": None})

            elif tipo == "finish":
                pessoa = self._pessoa(a.get("id"))
                if pessoa["status"] != "confessing":
                    raise Err("%s não está em confissão." % pessoa["name"])
                pessoa.update({"status": "done", "doneAt": agora})

            elif tipo == "back":
                pessoa = self._pessoa(a.get("id"))
                pessoa.update({"status": "waiting", "priestId": None, "priestName": None,
                               "startedAt": None, "doneAt": None, "sortKey": self._chave_frente()})

            elif tipo == "promote":
                pessoa = self._pessoa(a.get("id"))
                if pessoa["status"] != "waiting":
                    raise Err("%s já não está esperando." % pessoa["name"])
                pessoa["sortKey"] = self._chave_frente()

            elif tipo == "removePerson":
                q.remove(self._pessoa(a.get("id")))

            elif tipo == "addPriest":
                nome = limpar_nome(a.get("name"))
                if not nome:
                    raise Err("Digite o nome do padre.")
                usados = {p["id"] for p in self.state["priests"]}
                ordem = max([p.get("order", 0) for p in self.state["priests"]] + [0]) + 1
                self.state["priests"].append({"id": slug(nome, usados), "name": nome, "order": ordem})

            elif tipo == "removePriest":
                padre = self._padre(a.get("id"))
                if self._ocupado(padre["id"]):
                    raise Err("%s está confessando. Conclua antes de remover." % padre["name"])
                self.state["priests"].remove(padre)

            elif tipo == "clearDone":
                self.state["queue"] = [p for p in q if p["status"] != "done"]

            else:
                raise Err("Ação desconhecida.")

            self.state["v"] += 1
            self._salvar()


@st.cache_resource
def obter_store():
    return Store()


STORE = obter_store()


def agir(a):
    try:
        STORE.agir(a)
    except Err as e:
        st.toast(str(e))


# ---------- ações ligadas aos botões ----------
def cb_add():
    agir({"action": "addPerson", "name": st.session_state.get("nome_novo", "")})


def cb_add_priest():
    agir({"action": "addPriest", "name": st.session_state.get("padre_novo", "")})


def cb_start(pid):
    chave = "sel-" + pid
    padre = st.session_state.get(chave)
    st.session_state[chave] = None
    if padre:
        agir({"action": "start", "id": pid, "priestId": padre})


def cb_simples(acao, pid=None):
    st.session_state["confirmar"] = None
    agir({"action": acao, "id": pid})


def cb_pedir(chave):
    st.session_state["confirmar"] = chave


# ---------- página ----------
st.set_page_config(page_title="Fila de Confissões", layout="wide")
st.markdown(
    """
<style>
button[data-testid="stBaseButton-primary"], div.stButton > button[kind="primary"],
div[data-testid="stFormSubmitButton"] > button[kind="primaryFormSubmit"]{
  background:#4f6b1e; border-color:#4f6b1e; color:#fff;
}
div[data-testid="stMetricValue"]{font-size:1.6rem}
</style>
""",
    unsafe_allow_html=True,
)


def senha_configurada():
    try:
        return str(st.secrets.get("senha", "")).strip()
    except Exception:
        return ""


SENHA = senha_configurada()
if SENHA and not st.session_state.get("ok"):
    na_url = str(st.query_params.get("senha", ""))
    if na_url and hmac.compare_digest(na_url.encode(), SENHA.encode()):
        st.session_state["ok"] = True

if SENHA and not st.session_state.get("ok"):
    st.title("Fila de Confissões")
    with st.form("entrar"):
        digitada = st.text_input("Senha dos organizadores", type="password")
        entrou = st.form_submit_button("Entrar", type="primary")
    if entrou:
        if hmac.compare_digest(digitada.strip().encode(), SENHA.encode()):
            st.session_state["ok"] = True
            st.rerun()
        else:
            st.error("Senha incorreta. Tente de novo.")
    st.stop()

c_logo, c_titulo = st.columns([1, 6], vertical_alignment="center")
with c_logo:
    st.markdown(
        '<img src="%s" alt="Arte do retiro" style="width:84px;height:84px;border-radius:14px;'
        'border:1px solid #e2d8cc;object-fit:cover">' % LOGO,
        unsafe_allow_html=True,
    )
with c_titulo:
    st.title("Fila de Confissões")
    st.caption("Retiro de casais. A lista se atualiza sozinha em todos os aparelhos.")


def espera(t):
    m = int((ms() - t) / 60000)
    if m < 1:
        return "chegou agora"
    if m < 60:
        return "espera há %d min" % m
    return "espera há %d h %d min" % (m // 60, m % 60)


@st.fragment(run_every=3)
def painel():
    snap = STORE.foto()
    padres = sorted(snap["priests"], key=lambda p: p.get("order", 0))
    fila = snap["queue"]
    esperando = sorted((p for p in fila if p["status"] == "waiting"), key=lambda p: (p["sortKey"], p["id"]))
    feitos = sorted((p for p in fila if p["status"] == "done"), key=lambda p: -(p.get("doneAt") or 0))
    ocupados = {p["priestId"]: p for p in fila if p["status"] == "confessing" and p.get("priestId")}
    livres = [p for p in padres if p["id"] not in ocupados]
    confirmar = st.session_state.get("confirmar")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Esperando", len(esperando))
    m2.metric("Confessando", len(ocupados))
    m3.metric("Já foram", len(feitos))
    m4.metric("Padres livres", "%d/%d" % (len(livres), len(padres)))

    # Só aparecem os padres que estão confessando (é neles que fica o botão Concluir).
    if ocupados:
        esq, dir_ = st.columns([1, 2], gap="large")
        with esq:
            st.subheader("Confessando agora")
            for pr in padres:
                b = ocupados.get(pr["id"])
                if not b:
                    continue
                with st.container(border=True):
                    st.markdown("**%s**  :red[OCUPADO]" % esc(pr["name"]))
                    st.markdown("%s  \nconfessando desde %s" % (esc(b["name"]), hhmm(b.get("startedAt"))))
                    st.button("✓ Concluir", key="fin-" + b["id"], type="primary", width="stretch",
                              on_click=cb_simples, args=("finish", b["id"]))
                    st.button("Voltar à fila", key="volta-" + b["id"], width="stretch",
                              on_click=cb_simples, args=("back", b["id"]))
    else:
        dir_ = st.container()

    with dir_:
        st.subheader("Lista de pessoas")
        with st.form("novo", clear_on_submit=True):
            c1, c2 = st.columns([4, 1], vertical_alignment="bottom")
            c1.text_input("Nome de quem vai se confessar", key="nome_novo", max_chars=60,
                          placeholder="Nome de quem vai se confessar", label_visibility="collapsed")
            c2.form_submit_button("Adicionar", type="primary", on_click=cb_add, width="stretch")

        st.markdown("##### Esperando (%d)" % len(esperando))
        if not esperando:
            st.caption("Ninguém esperando.")
        for i, p in enumerate(esperando):
            with st.container(border=True):
                rotulo = "**%d. %s**" % (i + 1, esc(p["name"]))
                if i == 0:
                    rotulo += "  :orange[PRÓXIMO]"
                st.markdown(rotulo)
                st.caption(espera(p["createdAt"]))
                nomes = {pr["id"]: pr["name"] for pr in livres}
                st.selectbox("Padre", options=list(nomes), format_func=lambda x, n=nomes: n.get(x, x),
                             index=None, key="sel-" + p["id"], disabled=not livres,
                             placeholder="Escolher padre…" if livres else "Todos os padres estão ocupados",
                             label_visibility="collapsed", on_change=cb_start, args=(p["id"],))
                if confirmar == "rm:" + p["id"]:
                    st.write("Remover %s da lista?" % esc(p["name"]))
                    s1, s2 = st.columns(2)
                    s1.button("Sim, remover", key="rms-" + p["id"], type="primary", width="stretch",
                              on_click=cb_simples, args=("removePerson", p["id"]))
                    s2.button("Não", key="rmn-" + p["id"], width="stretch",
                              on_click=cb_pedir, args=(None,))
                else:
                    b1, b2 = st.columns(2)
                    if i > 0:
                        b1.button("↑ Passar para próximo", key="up-" + p["id"], width="stretch",
                                  on_click=cb_simples, args=("promote", p["id"]))
                    b2.button("Remover", key="rm-" + p["id"], width="stretch",
                              on_click=cb_pedir, args=("rm:" + p["id"],))

        with st.expander("Já foram (%d)" % len(feitos), expanded=True):
            if not feitos:
                st.caption("Ninguém ainda.")
            for p in feitos:
                with st.container(border=True):
                    st.markdown("**:green[✓] %s**  \ncom %s · %s" % (
                        esc(p["name"]), esc(p.get("priestName") or "padre"), hhmm(p.get("doneAt"))))
                    st.button("Desfazer", key="des-" + p["id"], on_click=cb_simples, args=("back", p["id"]))

    st.divider()
    t1, t2 = st.columns(2)
    with t1:
        with st.expander("Padres (%d)" % len(padres)):
            with st.form("novo_padre", clear_on_submit=True):
                st.text_input("Nome do novo padre", key="padre_novo", max_chars=60, placeholder="Ex.: Padre João")
                st.form_submit_button("Incluir padre", type="primary", on_click=cb_add_priest)
            for pr in padres:
                n1, n2 = st.columns([3, 2], vertical_alignment="center")
                n1.write(pr["name"])
                if confirmar == "rmp:" + pr["id"]:
                    n2.button("Remover mesmo?", key="rpy-" + pr["id"], type="primary",
                              on_click=cb_simples, args=("removePriest", pr["id"]))
                else:
                    n2.button("Remover", key="rp-" + pr["id"], on_click=cb_pedir, args=("rmp:" + pr["id"],))
    with t2:
        st.markdown("**Ao final do retiro**")
        st.caption("Apaga os nomes de quem já foi atendido, para todos.")
        if confirmar == "clr":
            st.button("Apagar o nome de %d pessoa(s)?" % len(feitos), key="clr-sim", type="primary",
                      on_click=cb_simples, args=("clearDone",))
        else:
            st.button("Limpar lista de quem já foi", key="clr", disabled=not feitos,
                      on_click=cb_pedir, args=("clr",))


painel()
