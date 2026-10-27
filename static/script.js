
/* DriveFin - Funcionalidades da interface */

const form = document.getElementById("form-lancamento");
const mensagem = document.getElementById("mensagem");
const historico = document.getElementById("historico");
const botaoContraste = document.getElementById("contraste");

const formatoMoeda = new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL"
});

// Acessibilidade: modo de alto contraste
function atualizarContraste(ativo) {
    document.body.classList.toggle("alto-contraste", ativo);
    botaoContraste.setAttribute("aria-pressed", String(ativo));
    botaoContraste.textContent = ativo
        ? "Desativar alto contraste"
        : "Alto contraste";
}

botaoContraste.addEventListener("click", () => {
    const ativo = !document.body.classList.contains("alto-contraste");
    atualizarContraste(ativo);
});

// Exibir mensagens acessíveis
function mostrarMensagem(texto) {
    mensagem.textContent = texto;
}

// Carregar resumo financeiro
async function carregarResumo() {
    try {
        const resposta = await fetch("/resumo");

        if (!resposta.ok) {
            throw new Error("Erro ao carregar resumo");
        }

        const dados = await resposta.json();

        document.getElementById("receitas").textContent =
            formatoMoeda.format(dados.total_receitas);

        document.getElementById("despesas").textContent =
            formatoMoeda.format(dados.total_despesas);

        document.getElementById("lucro").textContent =
            formatoMoeda.format(dados.lucro_liquido);

    } catch (erro) {
        mostrarMensagem("Não foi possível carregar o resumo financeiro.");
        console.error(erro);
    }
}

// Carregar histórico de lançamentos
async function carregarHistorico() {
    try {
        const resposta = await fetch("/lancamentos");

        if (!resposta.ok) {
            throw new Error("Erro ao carregar histórico");
        }

        const lancamentos = await resposta.json();

        historico.replaceChildren();

        if (lancamentos.length === 0) {
            const item = document.createElement("li");
            item.textContent = "Nenhum lançamento registrado.";
            historico.appendChild(item);
            return;
        }

        lancamentos.forEach((lancamento) => {
            const item = document.createElement("li");

            const descricao = document.createElement("span");
            descricao.textContent = lancamento.descricao;

            const valor = document.createElement("strong");
            valor.textContent = formatoMoeda.format(lancamento.valor);

            valor.className = lancamento.tipo === "receita"
                ? "receita-valor"
                : "despesa-valor";

            item.append(descricao, valor);
            historico.appendChild(item);
        });

    } catch (erro) {
        mostrarMensagem("Não foi possível carregar os lançamentos.");
        console.error(erro);
    }
}

// Cadastrar receita ou despesa
form.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const botaoSalvar = form.querySelector('button[type="submit"]');
    botaoSalvar.disabled = true;

    const tipo = document.getElementById("tipo").value;
    const valor = Number(document.getElementById("valor").value);
    const categoria = document.getElementById("categoria").value;
    const descricao = document.getElementById("descricao").value.trim();

    const dados = {
        tipo,
        valor,
        descricao: descricao || categoria
    };

    if (!Number.isFinite(valor) || valor <= 0) {
        mostrarMensagem("Informe um valor maior que zero.");
        botaoSalvar.disabled = false;
        return;
    }

    try {
        const resposta = await fetch("/lancamentos", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(dados)
        });

        const resultado = await resposta.json();

        if (!resposta.ok) {
            throw new Error(resultado.erro || "Erro ao salvar");
        }

        mostrarMensagem("Lançamento salvo com sucesso!");
        form.reset();

        await Promise.all([
            carregarResumo(),
            carregarHistorico()
        ]);

    } catch (erro) {
        mostrarMensagem(erro.message);
    } finally {
        botaoSalvar.disabled = false;
    }
});

// Inicialização da página
async function iniciarDriveFin() {
    await Promise.all([
        carregarResumo(),
        carregarHistorico()
    ]);
}

iniciarDriveFin();
