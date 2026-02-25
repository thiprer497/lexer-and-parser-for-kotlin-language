/*
 * Arquivo: estruturas.kt
 * Teste de estruturas sintáticas do Kotlin
 */

package com.exemplo.estruturas;

// Data Class e Construtor Primário
data class Usuario(val id: Int, val nome: String);

// Interface e Generics
interface Repositorio<T> {
    fun buscar(id: Int): T?;
    fun salvar(item: T);
}

fun main() {
    // Listas e Lambdas
    val numeros = listOf(1, 2, 3, 4, 5);
    
    // Teste do token SETA (->) e CHAVES ({ })
    val dobrados = numeros.map { numero ->
        numero * 2;
    };

    // Null Safety e Elvis Operator
    val nulo: String? = null;
    val tamanho = nulo?.length ?: 0;

    // Annotation (O Lexer lê @ como AT e depois o ID)
    @Deprecated("Use a nova funcao");
    fun antiga() { };
}
