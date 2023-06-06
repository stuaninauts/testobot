chrome.runtime.onMessage.addListener((msg, sender) => {
    switch (msg.type) {
        case "addCart":
            addToCart(msg.content);
            break;
    }
});

function addToCart(hash) {
    // TODO
    console.log(hash)
    // adicionarProdutoCarrinho(hash, idCategoriaSecundaria)
    // idCategoriaSecundaria = idCategoriaPromocional()
}