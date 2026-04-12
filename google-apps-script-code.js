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

function doGet(e) {
  return ContentService.createTextOutput("API Trade Marketing - Sabesp ✅ Funcionando!")
    .setMimeType(ContentService.MimeType.TEXT);
}

function doPost(e) {
  try {
    const ss = SpreadsheetApp.openById("1MM_E9YhOr8n1V3x33_YL3NHl6awPZ-6orIwMUb7MVZ8");
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
    const ss = SpreadsheetApp.openById("1MM_E9YhOr8n1V3x33_YL3NHl6awPZ-6orIwMUb7MVZ8");
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

// ========== FUNÇÃO DE TESTE ==========
// Execute esta função para testar se está gravando corretamente
function testeGravacao() {
  const ss = SpreadsheetApp.openById("1MM_E9YhOr8n1V3x33_YL3NHl6awPZ-6orIwMUb7MVZ8");
  const aba = ss.getSheetByName('Respostas ao formulário 1') || ss.getSheets()[0];
  
  Logger.log("Gravando na aba: " + aba.getName());
  
  aba.appendRow([
    new Date(),
    "teste@email.com",
    "12345",
    "Sim",
    "Loja Teste",
    "Rua Teste",
    "Bairro Teste",
    "Cidade Teste",
    "123",
    "00000-000",
    "(11) 99999-9999",
    "teste@email.com",
    "Promotor Digital",
    "220h",
    "TESTE - Pode Apagar"
  ]);
  
  Logger.log("✅ Gravação de teste concluída! Verifique a planilha.");
}
