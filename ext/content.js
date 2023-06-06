chrome.runtime.onMessage.addListener((msg, sender) => {
    switch (msg.type) {
        case "addCart":
            // adicionarProdutoCarrinho(hash, idCategoriaSecundaria)
            // idCategoriaSecundaria = idCategoriaPromocional()
            // string de teste: 185-1-0-0-1;185-1-0-0-1;185-20-0-0-1;1120-96-0-0-1
            // TODO
            // await the completion of adicionarProdutoCarrinho()
            console.log(msg.content)
            var codeInject = `
                var hash = "${msg.content}";
                console.log(hash);
                // Decode base64
                var hashes = hash.split(";");
                for (h of hashes) {
                    console.log(h);
                    adicionarProdutoCarrinho(h);
                };`;
            var script = document.createElement('script');
            script.textContent = codeInject;
            (document.head || document.documentElement).appendChild(script);
            script.remove();
            break;
    }
});
