console.log("SCRIPT.JS CARREGADO!");
const filtro = document.getElementById("filtro");
const busca = document.getElementById("busca-duvida");

const duvidas = document.querySelectorAll(".duvida");

function filtrarDuvidas() {

    const assuntoEscolhido = filtro ? filtro.value : "todos";
    const textoBusca = busca ? busca.value.toLowerCase().trim() : "";

    duvidas.forEach(function(duvida) {

        const assunto = duvida.dataset.assunto.toLowerCase();
        const texto = duvida.textContent.toLowerCase();

        const combinaAssunto =
            assuntoEscolhido === "todos" ||
            duvida.dataset.assunto === assuntoEscolhido;

        const combinaBusca =
            texto.includes(textoBusca);

        if (combinaAssunto && combinaBusca) {

            duvida.style.display = "block";

        } else {

            duvida.style.display = "none";

        }

    });

}

if (filtro) {
    filtro.addEventListener("change", filtrarDuvidas);
}

if (busca) {
    busca.addEventListener("input", filtrarDuvidas);
}

if (filtro) {

    const duvidas = document.querySelectorAll(".duvida");

    filtro.addEventListener("change", function() {

        const assuntoEscolhido = filtro.value;

        duvidas.forEach(function(duvida) {

            if (
                assuntoEscolhido === "todos" ||
                duvida.dataset.assunto === assuntoEscolhido
            ) {

                duvida.style.display = "block";

            } else {

                duvida.style.display = "none";

            }

        });

    });

}

const ordenacao = document.getElementById("ordenacao");

if (ordenacao) {

    ordenacao.addEventListener("change", function() {

        const container = document.querySelector(".lista-duvidas");

        const duvidasArray = Array.from(
            container.querySelectorAll(".duvida")
        );

        console.log("Ordenação escolhida:", ordenacao.value);

        if (ordenacao.value === "recentes") {

            duvidasArray.sort(function(a, b) {
                return parseInt(b.dataset.id) - parseInt(a.dataset.id);
            });

        }

        if (ordenacao.value === "antigas") {

            duvidasArray.sort(function(a, b) {
                return parseInt(a.dataset.id) - parseInt(b.dataset.id);
            });

        }

        if (ordenacao.value === "respondidas") {

            duvidasArray.sort(function(a, b) {

                const aRespondida =
                    a.dataset.respondida === "sim" ? 1 : 0;

                const bRespondida =
                    b.dataset.respondida === "sim" ? 1 : 0;

                return bRespondida - aRespondida;

            });

        }

        if (ordenacao.value === "sem-resposta") {

            duvidasArray.sort(function(a, b) {

                const aSemResposta =
                    a.dataset.respondida === "nao" ? 1 : 0;

                const bSemResposta =
                    b.dataset.respondida === "nao" ? 1 : 0;

                return bSemResposta - aSemResposta;

            });

        }

        duvidasArray.forEach(function(duvida) {
            container.appendChild(duvida);
        });

    });

}

const limparFiltros = document.getElementById("limpar-filtros");

if (limparFiltros) {

    limparFiltros.addEventListener("click", function() {

        if (busca) {
            busca.value = "";
        }

        if (filtro) {
            filtro.value = "todos";
        }

        if (ordenacao) {
            ordenacao.value = "recentes";
        }

        filtrarDuvidas();

        const container = document.querySelector(".lista-duvidas");

        if (container) {

            const duvidasArray = Array.from(
                container.querySelectorAll(".duvida")
            );

            duvidasArray.sort(function(a, b) {
                return Number(b.dataset.id) - Number(a.dataset.id);
            });

            duvidasArray.forEach(function(duvida) {
                container.appendChild(duvida);
            });

        }

    });

}

const avaliacoes = document.querySelectorAll(".avaliacao");

avaliacoes.forEach(function(avaliacao) {

    const botoes = avaliacao.querySelectorAll("button");

    botoes.forEach(function(botao) {

        botao.addEventListener("click", function() {

            const id = avaliacao.dataset.id;

const disciplina =
    avaliacao.dataset.disciplina;

            const voto = botao.textContent.trim();

fetch("/avaliar/" + disciplina, {

    method: "POST",

    headers: {
        "Content-Type": "application/json"
    },

    body: JSON.stringify({

        id: id,

        voto: voto

    })

})
.then(function(resposta) {

    console.log("Resposta do servidor:", resposta.status);

    return resposta.json();

})
.then(function(dados) {

    console.log("Dados recebidos:", dados);

})
.catch(function(erro) {

    console.error("Erro ao avaliar:", erro);

});

            if (voto === "👍 Sim") {

                const contador =
                    avaliacao.parentElement.querySelector(".contador-sim");

                contador.textContent =
                    Number(contador.textContent) + 1;

            }

            else if (voto === "👎 Não") {

                const contador =
                    avaliacao.parentElement.querySelector(".contador-nao");

                contador.textContent =
                    Number(contador.textContent) + 1;

            }

            botoes.forEach(function(botao) {
                botao.disabled = true;
            });

        });

    });

});