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

function doPost(e) {
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    const dados = JSON.parse(e.postData.contents);
    
    sheet.appendRow([
      new Date(),
      dados.email,
      dados.matricula,
      dados.cargo,
      dados.cargaHoraria,
      dados.interesse,
      dados.loja,
      dados.rua,
      dados.numero,
      dados.bairro,
      dados.cidade,
      dados.cep,
      dados.telefone
    ]);
    
    return ContentService.createTextOutput(JSON.stringify({status: "ok", message: "Dados salvos com sucesso!"}))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (erro) {
    return ContentService.createTextOutput(JSON.stringify({status: "erro", message: erro.toString()}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Função para testar se está funcionando
function doGet(e) {
  return ContentService.createTextOutput("API funcionando! Use POST para enviar dados.")
    .setMimeType(ContentService.MimeType.TEXT);
}
