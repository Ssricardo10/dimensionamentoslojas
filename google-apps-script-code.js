// ===========================================
// CÓDIGO PARA GOOGLE APPS SCRIPT
// ===========================================
// 1. Acesse: https://script.google.com
// 2. Abra o projeto vinculado à sua planilha
// 3. Cole este código no arquivo Code.gs
// 4. Salve e faça: Implantar > Nova implantação
//    - Tipo: App da Web
//    - Executar como: Eu
//    - Quem tem acesso: Qualquer pessoa
// 5. Copie a nova URL gerada e atualize no cadastro.html
// ===========================================

function doGet() {
  return HtmlService.createTemplateFromFile('Index')
    .evaluate()
    .setTitle('Portal Trade Marketing | Sabesp')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

function doPost(e) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const aba = ss.getSheetByName('Respostas ao formulário 1') || ss.getSheets()[0];
    const dados = JSON.parse(e.postData.contents);
    
    // ORDEM EXATA DAS 15 COLUNAS (A até O)
    aba.appendRow([
      new Date(),           // 1. Carimbo de data/hora
      dados.email,          // 2. Endereço de e-mail
      dados.matricula,      // 3. Matricula/RH
      dados.interesse,      // 4. Tem Interesse?
      dados.loja,           // 5. Loja/Interesse
      dados.rua,            // 6. Rua (do Colaborador)
      dados.bairro,         // 7. Bairro (do Colaborador)
      dados.cidade,         // 8. Cidade (do Colaborador)
      dados.numero,         // 9. Número da casa (do Colaborador)
      dados.cep,            // 10. Cep (do Colaborador)
      dados.telefone,       // 11. Telefone (do Colaborador)
      dados.email,          // 12. E-mail (do Colaborador) - Repete o e-mail
      dados.cargo,          // 13. CARGO
      dados.cargaHoraria,   // 14. CARGA HORÁRIA
      dados.nome            // 15. NOME
    ]);
    
    return ContentService.createTextOutput(JSON.stringify({status: "ok", message: "Dados salvos!"}))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (erro) {
    return ContentService.createTextOutput(JSON.stringify({status: "erro", message: erro.toString()}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Para uso com google.script.run (quando HTML é servido pelo Apps Script)
function salvarDados(obj) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const aba = ss.getSheetByName('Respostas ao formulário 1') || ss.getSheets()[0];
    
    aba.appendRow([
      new Date(),
      obj.email,
      obj.matricula,
      obj.interesse,
      obj.loja,
      obj.rua,
      obj.bairro,
      obj.cidade,
      obj.numero,
      obj.cep,
      obj.telefone,
      obj.email,
      obj.cargo,
      obj.cargaHoraria,
      obj.nome
    ]);
    
    return "✅ Cadastro salvo com sucesso!";
  } catch (e) {
    return "❌ Erro: " + e.toString();
  }
}
