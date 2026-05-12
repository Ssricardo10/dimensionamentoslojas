// ==========================================
// CONFIGURAÇÕES - ALTERE AQUI
// ==========================================
const SS_ID = 'SEU_ID_DA_PLANILHA_AQUI'; // ID da planilha (pegar da URL)
const FOLDER_ID = 'SEU_ID_DA_PASTA_DE_FOTOS_AQUI'; // ID da pasta do Drive

// ==========================================
// FUNÇÕES PRINCIPAIS
// ==========================================

function doGet() {
  return HtmlService.createHtmlOutputFromFile('FormularioMapeamento')
    .setTitle('Mapeamento de Estrutura | Sabesp')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function processarFormulario(dados) {
  try {
    const sheet = SpreadsheetApp.openById(SS_ID).getSheets()[0];
    const pasta = DriveApp.getFolderById(FOLDER_ID);
    
    // 1. Tratamento de Fotos (Evidências)
    let linksFotos = [];
    if (dados.fotos && dados.fotos.length > 0) {
      dados.fotos.forEach((fotoBase64, index) => {
        // Decodifica base64 e cria arquivo
        const blob = Utilities.newBlob(
          Utilities.base64Decode(fotoBase64.split(',')[1]),
          'image/jpeg',
          `${dados.nomeLoja}_${dados.dataVisita}_foto${index + 1}.jpg`
        );
        const arquivo = pasta.createFile(blob);
        linksFotos.push(arquivo.getUrl());
      });
    }

    // 2. Organização da Linha
    const novaLinha = [
      new Date(),                      // Timestamp
      dados.nomeLoja,                  // Nome da Loja
      dados.codigoLoja || '-',         // Código da Loja
      dados.cidadeUf,                  // Cidade/UF
      dados.dataVisita,                // Data da Visita
      dados.nomePesquisador,           // Nome do Pesquisador
      dados.tamanhoEspaco,             // Tamanho do Espaço
      dados.estadoConservacao,         // Estado de Conservação
      dados.organizacaoAmbiente,       // Organização do Ambiente
      dados.qtdPAs,                    // Quantidade de PAs
      dados.espacoOcioso,              // Espaço Ocioso
      dados.podeExpandir,              // Pode Expandir?
      dados.observacoes || '-',        // Observações
      linksFotos.join(", ")            // Links das Fotos
    ];

    sheet.appendRow(novaLinha);
    
    return {
      sucesso: true,
      mensagem: "✅ Dados enviados com sucesso!",
      fotos: linksFotos.length
    };
    
  } catch (erro) {
    return {
      sucesso: false,
      mensagem: "❌ Erro ao processar: " + erro.message
    };
  }
}

function criarPlanilhaModelo() {
  const ss = SpreadsheetApp.create('Sabesp - Mapeamento de Estrutura');
  const sheet = ss.getSheets()[0];
  
  // Cabeçalhos
  const cabecalhos = [
    'Timestamp',
    'Nome da Loja',
    'Código da Loja',
    'Cidade/UF',
    'Data da Visita',
    'Nome do Pesquisador',
    'Tamanho do Espaço',
    'Estado de Conservação',
    'Organização do Ambiente',
    'Qtd de PAs',
    'Espaço Ocioso',
    'Pode Expandir',
    'Observações',
    'Links das Fotos'
  ];
  
  sheet.getRange(1, 1, 1, cabecalhos.length).setValues([cabecalhos]);
  sheet.getRange(1, 1, 1, cabecalhos.length).setFontWeight('bold').setBackground('#4285f4').setFontColor('#ffffff');
  sheet.setFrozenRows(1);
  
  Logger.log('Planilha criada: ' + ss.getUrl());
  Logger.log('ID da planilha: ' + ss.getId());
  
  return ss.getId();
}
