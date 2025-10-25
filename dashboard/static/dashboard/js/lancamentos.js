
// JS helper for lancamentos page: carregar forms via fetch (expects urls: /lanc_despesas/, /lanc_receitas/, /lanc_investimentos/)
function carregarConteudo(tipo) {
    // map tipo names used in buttons to your endpoint names
    const map = { 'despesa':'lanc_despesas', 'receita':'lanc_receitas', 'investimento':'lanc_investimentos' };
    const url = `/${map[tipo]}/`;
    const container = document.getElementById('formContainer');
    if (!container) return;
    fetch(url)
      .then(r => r.text())
      .then(html => container.innerHTML = html)
      .catch(e => { container.innerHTML = '<p>Erro ao carregar formulario.</p>'; console.error(e); });
}
// expose to global
window.carregarConteudo = carregarConteudo;
