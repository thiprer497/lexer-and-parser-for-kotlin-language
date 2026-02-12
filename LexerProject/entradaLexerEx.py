
from .lexer import Lexer
from .token_stream import TokenStream

def demo(source_text: str):
    lexer = Lexer(source_text)
    ts = TokenStream(lexer)
    while True:
        t = ts.next()
        print(t)
        if t.tipo == "EOF":
            break

if __name__ == "__main__":
    sample = '''

//#!/usr/bin/env kotlin

/*
 * ================================
 * TESTE COMPLETO DO LEXER
 * ================================
 * Este arquivo cobre:
 * - Shebang
 * - Comentários de linha e bloco (aninhados)
 * - Keywords hard / soft / modifier
 * - Keywords compostas: as?, !in, !is
 * - Identificadores simples e com crase
 * - Literais numéricos (dec, hex, bin, float, sufixos)
 * - Operadores multi-caractere (maximal munch)
 * - Strings simples, interpoladas e escapes
 * - Literais de caractere
 * - Delimitadores
 */

package teste.lexer

import kotlin.math.*

/* -------------------------------
   CLASSE COM MODIFIERS E KEYWORDS
   ------------------------------- */
public final class ExemploLexerTest {

    companion object {
        const val CONST_VALUE = 42
    }

    private lateinit var nome: String
    internal var contador: Int = 0

    /* -------------------------------
       FUNÇÃO PRINCIPAL
       ------------------------------- */
    fun main() {

        // ---------- NUMÉRICOS ----------
        val dec = 123
        val decSep = 1_000_000
        val bin = 0b1010_0110
        val hex = 0xDEAD_BEEF
        val longU = 123UL
        val long = 999L
        val flt = 3.14f
        val dbl = 1.0e-10
        val dbl2 = 2E+3

        // ---------- OPERADORES ----------
        contador++
        contador += 2
        contador -= 1
        contador *= 3
        contador /= 2

        if (contador >= 10 && contador <= 100 || contador != 50) {
            println("contador válido")
        }

        // strict equality
        if (contador === 42 || contador !== 0) {
            println("=== e !== funcionando")
        }

        // ---------- RANGES ----------
        for (i in 0..10) {
            print(i)
        }

        for (j in 0..<5) {
            print(j)
        }

        // ---------- KEYWORDS COMPOSTAS ----------
        val x: Any = "abc"
        if (x !is String) {
            println("!is funcionando")
        }

        val lista = listOf(1, 2, 3)
        if (2 !in lista) {
            println("!in funcionando")
        }

        val cast: String? = x as? String

        // ---------- STRINGS ----------
        val simples = "string simples"
        val escape = "linha\nnova\tcoluna"
        



        // ---------- CHAR ----------
        

        // ---------- IDENTIFICADORES COM CRASE ----------
        val `class` = "keyword como nome"
        val `identificador com espaco` = 100
        val `!in` = "permitido como identificador"

        // ---------- NULL SAFETY ----------
        val tamanho = nome?.length ?: -1
        val naoNulo = nome!!.length

        // ---------- WHEN / TRY / THROW ----------
        when (contador) {
            0 -> println("zero")
            in 1..9 -> println("baixo")
            else -> println("alto")
        }

        try {
            if (contador < 0) {
                throw IllegalStateException("erro")
            }
        } catch (e: Exception) {
            println(e.message)
        } finally {
            println("fim")
        }
    }
}

/* -------------------------------
   COMENTÁRIO DE BLOCO ANINHADO
   /* nível 2 */
   /* nível 3
      /* nível 4 */
   */
*/

'''
    demo(sample)