// ============================================================
// static/js/main.js — SIAT JavaScript
// ============================================================

// ── Máscara CNPJ ──────────────────────────────────────────
function mascaraCNPJ(input) {
  let v = input.value.replace(/\D/g, '').slice(0, 14);
  if (v.length > 12) v = v.replace(/^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/, '$1.$2.$3/$4-$5');
  else if (v.length > 8)  v = v.replace(/^(\d{2})(\d{3})(\d{3})(\d{1,4})/, '$1.$2.$3/$4');
  else if (v.length > 5)  v = v.replace(/^(\d{2})(\d{3})(\d{1,3})/, '$1.$2.$3');
  else if (v.length > 2)  v = v.replace(/^(\d{2})(\d{1,3})/, '$1.$2');
  input.value = v;
}

// ── Máscara CPF ───────────────────────────────────────────
function mascaraCPF(input) {
  let v = input.value.replace(/\D/g, '').slice(0, 11);
  if (v.length > 9) v = v.replace(/^(\d{3})(\d{3})(\d{3})(\d{1,2})$/, '$1.$2.$3-$4');
  else if (v.length > 6) v = v.replace(/^(\d{3})(\d{3})(\d{1,3})/, '$1.$2.$3');
  else if (v.length > 3) v = v.replace(/^(\d{3})(\d{1,3})/, '$1.$2');
  input.value = v;
}

// ── Máscara Telefone ──────────────────────────────────────
function mascaraTelefone(input) {
  let v = input.value.replace(/\D/g, '').slice(0, 11);
  if (v.length > 10) v = v.replace(/^(\d{2})(\d{5})(\d{4})$/, '($1) $2-$3');
  else if (v.length > 6) v = v.replace(/^(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3');
  else if (v.length > 2) v = v.replace(/^(\d{2})(\d{0,5})/, '($1) $2');
  input.value = v;
}

// ── Formatar CNPJ para exibição ───────────────────────────
function formatarCNPJ(cnpj) {
  const d = cnpj.replace(/\D/g, '');
  return d.length === 14
    ? `${d.slice(0,2)}.${d.slice(2,5)}.${d.slice(5,8)}/${d.slice(8,12)}-${d.slice(12)}`
    : cnpj;
}

// ── Modal helpers ─────────────────────────────────────────
function openModal(id) {
  document.getElementById(id).classList.add('open');
}
function closeModal(id) {
  document.getElementById(id).classList.remove('open');
}
// Fechar modal ao clicar fora
document.addEventListener('click', e => {
  if (e.target.classList.contains('modal-overlay')) {
    e.target.classList.remove('open');
  }
});
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-overlay.open').forEach(m => m.classList.remove('open'));
  }
});

// ── Pesquisa em tabela ────────────────────────────────────
function filtrarTabela(inputId, tableId) {
  const input = document.getElementById(inputId);
  if (!input) return;
  input.addEventListener('input', () => {
    const filtro = input.value.toLowerCase();
    const rows = document.querySelectorAll(`#${tableId} tbody tr`);
    rows.forEach(row => {
      row.style.display = row.textContent.toLowerCase().includes(filtro) ? '' : 'none';
    });
  });
}

// ── Consulta de CNPJ via API ──────────────────────────────
async function consultarCNPJ(cnpj, containerId) {
  const cnpjLimpo = cnpj.replace(/\D/g, '');
  if (cnpjLimpo.length !== 14) {
    mostrarErro(containerId, 'CNPJ deve ter 14 dígitos.');
    return;
  }
  mostrarLoading(containerId);
  try {
    const resp = await fetch(`/consultas/cnpj/${cnpjLimpo}`);
    const json = await resp.json();
    if (json.ok) {
      mostrarResultado(containerId, json.data);
    } else {
      mostrarErro(containerId, json.erro || 'Erro desconhecido.');
    }
  } catch (e) {
    mostrarErro(containerId, 'Erro de conexão. Verifique sua internet.');
  }
}

function mostrarLoading(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.innerHTML = `
    <div class="spinner"></div>
    <p class="loading-msg">Consultando Receita Federal...</p>`;
}

function mostrarErro(id, msg) {
  const el = document.getElementById(id);
  if (!el) return;
  el.innerHTML = `<div class="alert alert-error">❌ ${msg}</div>`;
}

function mostrarResultado(id, d) {
  const el = document.getElementById(id);
  if (!el) return;

  const situacao = d.descricao_situacao_cadastral || '—';
  const badgeClass = situacao === 'ATIVA' ? 'badge-green' : 'badge-red';

  const socios = (d.qsa || []).map(s =>
    `<div class="socio-item"><span>👤 ${s.nome_socio}</span><span>${s.qualificacao_socio}</span></div>`
  ).join('');

  const cnaes_sec = (d.cnaes_secundarios || []).slice(0,3).map(c =>
    `<div class="result-field"><div class="result-field-label">CNAE Secundário</div><div class="result-field-value">${c.codigo} · ${c.descricao}</div></div>`
  ).join('');

  const capital = d.capital_social
    ? `R$ ${parseFloat(d.capital_social).toLocaleString('pt-BR',{minimumFractionDigits:2})}`
    : '—';

  el.innerHTML = `
    <div class="result-card">
      <div class="result-company-name">${d.razao_social || '—'} <span class="badge ${badgeClass}">${situacao}</span></div>
      ${d.nome_fantasia ? `<div style="color:var(--text-muted);font-size:.88rem;margin-bottom:6px">${d.nome_fantasia}</div>` : ''}
      <div class="result-cnpj">${formatarCNPJ(d.cnpj || '')}</div>
      <div class="result-grid">
        <div class="result-field"><div class="result-field-label">Natureza Jurídica</div><div class="result-field-value">${d.descricao_natureza_juridica||'—'}</div></div>
        <div class="result-field"><div class="result-field-label">Porte</div><div class="result-field-value">${d.descricao_porte||'—'}</div></div>
        <div class="result-field"><div class="result-field-label">Abertura</div><div class="result-field-value">${formatarData(d.data_inicio_atividade)}</div></div>
        <div class="result-field"><div class="result-field-label">Capital Social</div><div class="result-field-value">${capital}</div></div>
        <div class="result-field"><div class="result-field-label">CNAE Principal</div><div class="result-field-value">${d.cnae_fiscal||'—'} · ${d.cnae_fiscal_descricao||''}</div></div>
        <div class="result-field"><div class="result-field-label">Telefone</div><div class="result-field-value">${d.ddd_telefone_1||'—'}</div></div>
        <div class="result-field"><div class="result-field-label">E-mail</div><div class="result-field-value">${d.email||'—'}</div></div>
        <div class="result-field"><div class="result-field-label">Município / UF</div><div class="result-field-value">${d.municipio||'—'} / ${d.uf||'—'}</div></div>
        <div class="result-field" style="grid-column:1/-1"><div class="result-field-label">Endereço</div><div class="result-field-value">${d.tipo_logradouro||''} ${d.logradouro||''}, ${d.numero||''} ${d.complemento ? '– '+d.complemento : ''} · ${d.bairro||''} · CEP ${d.cep||''}</div></div>
        ${cnaes_sec}
      </div>
      ${socios ? `<div class="result-socios"><h4>Quadro Societário (QSA)</h4>${socios}</div>` : ''}
    </div>`;
}

function formatarData(s) {
  if (!s) return '—';
  try { const d = new Date(s); return d.toLocaleDateString('pt-BR'); } catch { return s; }
}

// ── Gráfico de barras simples ─────────────────────────────
function renderBarChart(canvasId, labels, values, color = '#2563eb') {
  const container = document.getElementById(canvasId);
  if (!container) return;
  const max = Math.max(...values, 1);
  container.innerHTML = `
    <div class="bar-chart">
      ${labels.map((label, i) => `
        <div class="bar-item">
          <div class="bar-value">${values[i]}</div>
          <div class="bar-fill" style="height:${(values[i]/max*100)}px;background:${color}"></div>
          <div class="bar-label">${label}</div>
        </div>`).join('')}
    </div>`;
}

// ── Sidebar toggle no mobile ──────────────────────────────
function toggleSidebar() {
  document.querySelector('.sidebar').classList.toggle('sidebar-open');
}

// ── Init ──────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // Máscaras automáticas
  document.querySelectorAll('[data-mask="cnpj"]').forEach(el => {
    el.addEventListener('input', () => mascaraCNPJ(el));
  });
  document.querySelectorAll('[data-mask="cpf"]').forEach(el => {
    el.addEventListener('input', () => mascaraCPF(el));
  });
  document.querySelectorAll('[data-mask="tel"]').forEach(el => {
    el.addEventListener('input', () => mascaraTelefone(el));
  });

  // Pesquisa
  filtrarTabela('search-input', 'main-table');

  // Auto-fechar alertas após 4s
  document.querySelectorAll('.alert-success, .alert-error, .alert-info').forEach(a => {
    setTimeout(() => { a.style.opacity='0'; a.style.transition='opacity .5s'; setTimeout(()=>a.remove(),500); }, 4000);
  });

  // Formulário de consulta na página de consultas
  const consultaForm = document.getElementById('consulta-form');
  if (consultaForm) {
    consultaForm.addEventListener('submit', async e => {
      e.preventDefault();
      const doc = document.getElementById('doc-input').value;
      await consultarCNPJ(doc, 'consulta-result');
    });
  }
});
