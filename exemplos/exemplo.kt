/*
 * ================================
 * TESTE COMPLETO DO LEXER
 * ================================
 */

package teste.lexer;

import kotlin.math.*;

var (a, b, c, d) = listOf(1, 1, 1, 1);
var cc: Int;
var dd: 99;

public final class ExemploLexerTest {

    companion object {
        const val CONST_VALUE = 42;
    }

    private lateinit var nome: String;
    internal var contador: Int = 0;

    fun main() {

        // ---------- NUMÉRICOS ----------
        val dec = 123;
        val decSep = 1_000_000;
        val bin = 0b1010_0110;
        val hex = 0xDEAD_BEEF;
        val longU = 123UL;
        val flt = 3.14f;
        val dbl = 1.0e-10;

        // ---------- OPERADORES ----------
        contador++;
        contador += 2;

        if (contador >= 10 && contador <= 100 || contador != 50) {
            println("contador válido");
        }

        // strict equality
        if (contador === 42 || contador !== 0) {
            println("=== e !== funcionando");
        }

        // ---------- RANGES ----------
        for (i in 0..10) { print(i); }
        for (j in 0..<5) { print(j); }

        // ---------- KEYWORDS COMPOSTAS ----------
        val x: Any = "abc";
        if (x !is String) { println("!is funcionando"); }
        if (2 !in 0..10) { println("!in funcionando"); }
        val cast: String? = x as? String;

        // ---------- STRINGS ----------
        val simples = "string simples";
        val escape = "linha\nnova\tcoluna";
        val interpolada = "Valor: $contador e soma: ${contador + 1}";

        // ---------- CHAR ----------
        val c = 'a';
        val nl = '\n';

        // ---------- IDENTIFICADORES COM CRASE ----------
        val `class` = "keyword como nome";
        val `identificador com espaco` = 100;

        // ---------- NULL SAFETY ----------
        val tamanho = nome?.length ?: -1;
        val naoNulo = nome!!.length;
    }
}

fun main() {

    // TESTE NOVO: Char e Escapes
    val c1 = 'a';
    val c2 = '\n';
    val c3 = '\'';
    val c4 = '\u0041';

    // TESTE NOVO: Aspas Triplas (Raw String)
    val sql = """
        SELECT * FROM usuarios
        WHERE id = 1
    """;

    // TESTE NOVO: Valores Numéricos
    val x = 0xFF;
    val y = 0b10;
}
