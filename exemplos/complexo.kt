/*
 * Arquivo: complexo.kt
 * Teste de regras léxicas avançadas
 */

// 1. Comentários Aninhados (O Lexer deve ignorar tudo isso)
/*
   Inicio do nivel 1
   /*
      Nivel 2 (interno)
      /* Nivel 3 */
      Fim do nivel 2
   */
   Fim do nivel 1
*/

fun main() {
    // 2. Strings Raw (Múltiplas linhas sem escape)
    val query = """
        SELECT * FROM "tabela"
        WHERE nome = 'O''Neal'
        AND id > 0
    """;

    // 3. Ambiguidade de Operadores (Maximal Munch)
    var a = 10;
    var b = 20;
    val soma = a+++b;    // Deve ser lido como: a ++ + b
    val range = 0..<10;  // Operador rangeUntil

    // 4. Identificadores Soft Keywords (podem ser nomes de var)
    val file = 1;
    val field = 2;
    val get = 3;
    val set = 4;
    
    // 5. Unicode e Escapes
    val unicodeChar = '\u00A9'; // Copyright symbol
    val citacao = "Ele disse: \"Olá!\"";
}
