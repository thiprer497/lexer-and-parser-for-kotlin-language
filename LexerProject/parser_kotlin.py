# parser.py — versão ajustada (corrige ':' seguido por literal e cadeia !! .ident)
from typing import List

class TokenStreamWrapper:
    def __init__(self, ts):
        self._ts = ts
        self._buffer = []

    def _fill(self, n: int):
        while len(self._buffer) <= n:
            t = self._ts.next()
            self._buffer.append(t)

    def peek(self, n: int = 0):
        self._fill(n)
        return self._buffer[n]

    def next(self):
        if self._buffer:
            return self._buffer.pop(0)
        return self._ts.next()

    def eof(self):
        return getattr(self.peek(0), "tipo", None) == "EOF"

class Parser:
    def __init__(self, token_stream):
        self.ts = TokenStreamWrapper(token_stream)
        self.errors: List[str] = []
        self._panic_sync_tokens = {"SEMICOLON", "RBRACE", "EOF"}

    def peek(self, n=0): return self.ts.peek(n)
    def next(self): return self.ts.next()
    def accept(self, tipo):
        if getattr(self.peek(), "tipo", None) == tipo:
            self.next()
            return True
        return False

    def expect(self, tipo, mensagem=None):
        t = self.peek()
        if getattr(t, "tipo", None) == tipo:
            return self.next()
        msg = mensagem or f"Esperado token {tipo}, encontrado {getattr(t,'tipo',None)} ('{getattr(t,'lexema',None)}')"
        self._error_at_token(t, msg)
        self._panic_recover()
        return None

    def _error_at_token(self, token, mensagem):
        linha = getattr(token, "linha", -1)
        coluna = getattr(token, "coluna", -1)
        lex = getattr(token, "lexema", None)
        err = f"Erro sintático na linha {linha}, coluna {coluna}: {mensagem} (token='{lex}')"
        self.errors.append(err)
        print(err)

    def _panic_recover(self):
        try:
            while True:
                t = self.peek()
                if getattr(t, "tipo", None) in self._panic_sync_tokens:
                    if getattr(t, "tipo", None) != "EOF":
                        self.next()
                    return
                self.next()
        except Exception:
            return

    # -------------------------
    # Entrada
    # -------------------------
    def parse(self):
        file_node = {"type": "kotlinFile", "package": None, "imports": [], "declarations": []}
        if getattr(self.peek(), "tipo", None) == "KW_PACKAGE":
            file_node["package"] = self.parse_package_decl()
        while getattr(self.peek(), "tipo", None) in ("SK_IMPORT", "IMPORT"):
            imp = self.parse_import_decl()
            if imp: file_node["imports"].append(imp)
        while getattr(self.peek(), "tipo", None) != "EOF":
            decl = self.parse_top_level_decl()
            if decl:
                file_node["declarations"].append(decl)
            else:
                if getattr(self.peek(), "tipo", None) == "EOF":
                    break
                self._panic_recover()
        return file_node

    # -------------------------
    # package / import
    # -------------------------
    def parse_package_decl(self):
        self.expect("KW_PACKAGE")
        parts = []
        if getattr(self.peek(), "tipo", None) == "IDENTIFIER":
            parts.append(self.next().lexema)
            while self.accept("DOT"):
                if getattr(self.peek(), "tipo", None) == "IDENTIFIER":
                    parts.append(self.next().lexema)
                else:
                    self._error_at_token(self.peek(), "Identificador esperado após '.' no package")
                    break
        self.expect("SEMICOLON", "Ponto-e-vírgula esperado após declaração de package")
        return {"type": "package", "name": ".".join(parts)}

    def parse_import_decl(self):
        self.expect("SK_IMPORT")
        parts = []
        if getattr(self.peek(), "tipo", None) == "IDENTIFIER":
            parts.append(self.next().lexema)
            while self.accept("DOT"):
                if getattr(self.peek(), "tipo", None) == "OP_MUL":
                    parts.append("*"); self.next(); break
                if getattr(self.peek(), "tipo", None) == "IDENTIFIER":
                    parts.append(self.next().lexema)
                else:
                    self._error_at_token(self.peek(), "Identificador esperado no import"); break
        self.expect("SEMICOLON", "Ponto-e-vírgula esperado após import")
        return {"type": "import", "path": ".".join(parts)}

    # -------------------------
    # top-level
    # -------------------------
    def parse_top_level_decl(self):
        mods = self._collect_modifiers()
        t = getattr(self.peek(), "tipo", None)
        if t == "KW_CLASS": return self.parse_class_decl(mods)
        if t == "KW_FUN": return self.parse_function_decl(mods)
        if t in ("KW_VAL","KW_VAR"): return self.parse_property_decl(mods)
        if t == "SEMICOLON": self.next(); return None
        self._error_at_token(self.peek(), "Declaração de topo inválida"); self._panic_recover(); return None

    def _collect_modifiers(self):
        mods=[]
        while getattr(self.peek(), "tipo", None) and getattr(self.peek(), "tipo", None).startswith("MOD_"):
            mods.append(self.next().lexema)
        return mods

    # -------------------------
    # class / object
    # -------------------------
    def parse_class_decl(self, modifiers):
        self.expect("KW_CLASS")
        name_tok = self.expect("IDENTIFIER", "Nome da classe esperado após 'class'")
        name = getattr(name_tok,"lexema",None) if name_tok else "<erro>"
        body=None
        if self.accept("LBRACE"):
            members=[]
            while getattr(self.peek(),"tipo",None) not in ("RBRACE","EOF"):
                if getattr(self.peek(),"tipo",None).startswith("MOD_"):
                    member_mods = self._collect_modifiers()
                    if getattr(self.peek(),"tipo",None) == "KW_OBJECT":
                        members.append(self.parse_object_decl(member_mods)); continue
                    if getattr(self.peek(),"tipo",None) in ("KW_VAL","KW_VAR"):
                        members.append(self.parse_property_decl(member_mods)); continue
                    if getattr(self.peek(),"tipo",None) == "KW_FUN":
                        members.append(self.parse_function_decl(member_mods)); continue
                if getattr(self.peek(),"tipo",None) in ("KW_VAL","KW_VAR"):
                    members.append(self.parse_property_decl([])); continue
                if getattr(self.peek(),"tipo",None) == "KW_FUN":
                    members.append(self.parse_function_decl([])); continue
                if getattr(self.peek(),"tipo",None) == "KW_OBJECT":
                    members.append(self.parse_object_decl([])); continue
                self._error_at_token(self.peek(),"Membro de classe não reconhecido (ignorado)"); self._panic_recover()
            self.expect("RBRACE","Fechamento '}' esperado no corpo da classe")
            body=members
        return {"type":"class","name":name,"modifiers":modifiers,"body":body}

    def parse_object_decl(self, modifiers):
        self.expect("KW_OBJECT")
        name=None
        if getattr(self.peek(),"tipo",None)=="IDENTIFIER": name=self.next().lexema
        members=[]
        if self.accept("LBRACE"):
            while getattr(self.peek(),"tipo",None) not in ("RBRACE","EOF"):
                if getattr(self.peek(),"tipo",None).startswith("MOD_"):
                    mem_mods=self._collect_modifiers()
                    if getattr(self.peek(),"tipo",None) in ("KW_VAL","KW_VAR"):
                        members.append(self.parse_property_decl(mem_mods)); continue
                if getattr(self.peek(),"tipo",None) in ("KW_VAL","KW_VAR"):
                    members.append(self.parse_property_decl([])); continue
                if getattr(self.peek(),"tipo",None) == "KW_FUN":
                    members.append(self.parse_function_decl([])); continue
                self._error_at_token(self.peek(),"Membro do object não reconhecido"); self._panic_recover()
            self.expect("RBRACE","Fechamento '}' esperado no object")
        return {"type":"object","name":name,"modifiers":modifiers,"members":members}

    # -------------------------
    # function
    # -------------------------
    def parse_function_decl(self, modifiers):
        self.expect("KW_FUN")
        name_tok=self.expect("IDENTIFIER","Nome da função esperado")
        name=getattr(name_tok,"lexema",None) if name_tok else "<erro>"
        params=[]
        self.expect("LPAREN","Esperado '(' em declaração de função")
        if getattr(self.peek(),"tipo",None) != "RPAREN":
            while True:
                if getattr(self.peek(),"tipo",None) == "IDENTIFIER":
                    p=self.next().lexema
                    if self.accept("COLON"):
                        if getattr(self.peek(),"tipo",None)=="IDENTIFIER":
                            p_type=self.next().lexema
                            if self.accept("QUESTION"): p_type = p_type + "?"
                        else: p_type=None
                    else: p_type=None
                    params.append({"name":p,"type":p_type})
                else:
                    self._error_at_token(self.peek(),"Parâmetro inválido"); self._panic_recover(); break
                if not self.accept("COMMA"): break
        self.expect("RPAREN","Esperado ')' após parâmetros")
        rettype=None
        if self.accept("COLON"):
            if getattr(self.peek(),"tipo",None)=="IDENTIFIER":
                rettype=self.next().lexema
                if self.accept("QUESTION"): rettype = rettype + "?"
            else:
                self._error_at_token(self.peek(),"Tipo de retorno esperado após ':'")
        body=None
        if self.accept("LBRACE"): body=self.parse_block()
        else:
            if getattr(self.peek(),"tipo",None)=="SEMICOLON": self.next()
        return {"type":"function","name":name,"modifiers":modifiers,"params":params,"return":rettype,"body":body}

    # -------------------------
    # property (destructuring + tolerance for ":" followed by literal)
    # -------------------------
    def parse_property_decl(self, modifiers):
        kind = self.next().tipo  # KW_VAL or KW_VAR

        # destruturação: var (a,b) = expr;
        if getattr(self.peek(),"tipo",None) == "LPAREN":
            self.next()
            parts=[]
            while getattr(self.peek(),"tipo",None) not in ("RPAREN","EOF"):
                if getattr(self.peek(),"tipo",None)=="IDENTIFIER":
                    parts.append(self.next().lexema)
                else:
                    self._error_at_token(self.peek(),"Identificador esperado em destruturação"); self._panic_recover(); break
                if not self.accept("COMMA"): break
            self.expect("RPAREN","')' esperado na destruturação")
            value=None
            if self.accept("OP_ASSIGN"):
                value = self.parse_expression()
            else:
                self._error_at_token(self.peek(),"Atribuição esperada em destruturação"); self._panic_recover()
            self.expect("SEMICOLON","Ponto-e-vírgula esperado ao final da declaração")
            return {"type":"destructuring","kind":kind,"parts":parts,"value":value,"modifiers":modifiers}

        # nome pode ser IDENTIFIER ou Quoted_identifier
        if getattr(self.peek(),"tipo",None) in ("IDENTIFIER","Quoted_identifier"):
            name_tok = self.next()
            name = name_tok.lexema
        else:
            name_tok = None
            self._error_at_token(self.peek(),"Nome da propriedade esperado")
            self._panic_recover()
            name = "<erro>"

        var_type = None
        # se houver ':' — tentar ler tipo; se não for IDENTIFIER, aplicamos tolerância:
        if self.accept("COLON"):
            if getattr(self.peek(),"tipo",None) == "IDENTIFIER":
                var_type = self.next().lexema
                if self.accept("QUESTION"):
                    var_type = var_type + "?"
            else:
                # Caso tolerante: se o próximo token for início de expressão (literal ou identificador ou '('),
                # assumimos que autor digitou ":" por engano e queria escrever "=" (ex: "var dd: 99;")
                t_next = getattr(self.peek(),"tipo",None)
                if t_next in ("INT_LITERAL","FLOAT_LITERAL","STRING_START","CHAR_LITERAL","IDENTIFIER","LPAREN"):
                    # gerar aviso e tratar como se não houvesse tipo, começando expressão aqui
                    self._error_at_token(self.peek(), "Tipo esperado após ':' — assumindo iniacializador (recuperação tolerante).")
                    var_type = None
                    # NOTE: não consumimos um token extra aqui; parse_expression() irá consumir o que for necessário
                else:
                    self._error_at_token(self.peek(), "Tipo esperado após ':' em propriedade")

        # valor (se houver)
        value = None
        if self.accept("OP_ASSIGN"):
            value = self.parse_expression()
        else:
            # Caso em que fizemos recuperação tolerante no ':' (ex: ":" seguido de literal),
            # se o próximo token é um literal/expression, tentamos ler isso como valor automaticamente.
            if var_type is None and getattr(self.peek(),"tipo",None) in ("INT_LITERAL","FLOAT_LITERAL","STRING_START","CHAR_LITERAL","IDENTIFIER","LPAREN"):
                # aviso já emitido acima; aqui consumimos a expressão como value
                value = self.parse_expression()

        # exigir ';'
        if getattr(self.peek(),"tipo",None) == "SEMICOLON":
            self.next()
        else:
            self._error_at_token(self.peek(),"Ponto-e-vírgula esperado ao final da declaração de propriedade")
            self._panic_recover()
        return {"type":"property","kind":kind,"name":name,"var_type":var_type,"value":value,"modifiers":modifiers}

    # -------------------------
    # blocks / statements
    # -------------------------
    def parse_block(self):
        stmts=[]
        while getattr(self.peek(),"tipo",None) not in ("RBRACE","EOF"):
            st=self.parse_statement()
            if st: stmts.append(st)
            else: self._panic_recover()
        self.expect("RBRACE","Fechamento de bloco '}' esperado")
        return {"type":"block","statements":stmts}

    def parse_statement(self):
        t = getattr(self.peek(),"tipo",None)
        if t in ("KW_VAL","KW_VAR"): return self.parse_property_decl([])
        if t == "KW_IF": return self.parse_if()
        if t == "KW_FOR": return self.parse_for()
        if t == "LBRACE": self.next(); return self.parse_block()
        expr = self.parse_expression()
        if getattr(self.peek(),"tipo",None) == "SEMICOLON": self.next()
        else:
            self._error_at_token(self.peek(),"Ponto-e-vírgula esperado ao final da instrução"); self._panic_recover()
        return {"type":"expr_stmt","expr":expr}

    def parse_if(self):
        self.expect("KW_IF")
        self.expect("LPAREN","Esperado '(' após if")
        cond = self.parse_expression()
        self.expect("RPAREN","Esperado ')' após condição do if")
        then_node = None
        if getattr(self.peek(),"tipo",None) == "LBRACE": self.next(); then_node=self.parse_block()
        else: then_node=self.parse_statement()
        else_node=None
        if getattr(self.peek(),"tipo",None)=="KW_ELSE":
            self.next()
            if getattr(self.peek(),"tipo",None)=="LBRACE": self.next(); else_node=self.parse_block()
            else: else_node=self.parse_statement()
        return {"type":"if","cond":cond,"then":then_node,"else":else_node}

    def parse_for(self):
        self.expect("KW_FOR")
        self.expect("LPAREN","Esperado '(' após for")
        var_name=None
        if getattr(self.peek(),"tipo",None)=="IDENTIFIER": var_name=self.next().lexema
        else: self._error_at_token(self.peek(),"Identificador de iteração esperado")
        if self.accept("KW_IN"): rng=self.parse_expression()
        else: rng=None
        self.expect("RPAREN","Esperado ')' após cabeçalho do for")
        body=None
        if self.accept("LBRACE"): body=self.parse_block()
        else: body=self.parse_statement()
        return {"type":"for","var":var_name,"range":rng,"body":body}

    # -------------------------
    # expressões (com elvis)
    # -------------------------
    def parse_expression(self):
        return self.parse_elvis()

    def parse_elvis(self):
        node = self.parse_or()
        while getattr(self.peek(),"tipo",None) == "OP_ELVIS":
            op = self.next().lexema
            right = self.parse_or()
            node = {"type":"binary","op":op,"left":node,"right":right}
        return node

    def parse_or(self):
        node = self.parse_and()
        while getattr(self.peek(),"tipo",None) == "OP_OR":
            op=self.next().lexema; right=self.parse_and(); node={"type":"binary","op":op,"left":node,"right":right}
        return node

    def parse_and(self):
        node=self.parse_equality()
        while getattr(self.peek(),"tipo",None)=="OP_AND":
            op=self.next().lexema; right=self.parse_equality(); node={"type":"binary","op":op,"left":node,"right":right}
        return node

    def parse_equality(self):
        node=self.parse_relational()
        while getattr(self.peek(),"tipo",None) in ("OP_NEQ","OP_EQ","OP_EQ_STRICT","OP_NEQ_STRICT"):
            op_tok=self.next(); right=self.parse_relational(); node={"type":"binary","op":op_tok.lexema,"left":node,"right":right}
        return node

    def parse_relational(self):
        node=self.parse_additive()
        while True:
            t0 = getattr(self.peek(),"tipo",None); t1 = getattr(self.peek(1),"tipo",None)
            op=None
            if t0=="OP_NOT" and t1 in ("KW_IN","KW_IS"):
                self.next(); op_tok=self.next(); op='!'+op_tok.lexema
            elif t0 in ("KW_IN","KW_IS","KW_AS"):
                op_tok=self.next(); op=op_tok.lexema
                if op=="as" and getattr(self.peek(),"tipo",None)=="QUESTION": self.next(); op="as?"
            elif t0 in ("OP_GE","OP_LE","OP_GT","OP_LT","OP_RANGE","OP_RANGE_UNTIL"):
                op_tok=self.next(); op=op_tok.lexema
            else:
                break
            right = self.parse_additive()
            node = {"type":"binary","op":op,"left":node,"right":right}
        return node

    def parse_additive(self):
        node=self.parse_multiplicative()
        while getattr(self.peek(),"tipo",None) in ("OP_PLUS","OP_MINUS","OP_PLUS_ASSIGN","OP_MINUS_ASSIGN"):
            op_tok=self.next(); right=self.parse_multiplicative(); node={"type":"binary","op":op_tok.lexema,"left":node,"right":right}
        return node

    def parse_multiplicative(self):
        node=self.parse_unary()
        while getattr(self.peek(),"tipo",None) in ("OP_MUL","OP_DIV","OP_MOD"):
            op_tok=self.next(); right=self.parse_unary(); node={"type":"binary","op":op_tok.lexema,"left":node,"right":right}
        return node

    def parse_unary(self):
        t = getattr(self.peek(),"tipo",None)
        if t in ("OP_NOT","OP_MINUS"):
            op=self.next().lexema; operand=self.parse_unary(); return {"type":"unary","op":op,"operand":operand}
        node=self.parse_primary()
        if getattr(self.peek(),"tipo",None) in ("OP_INC","OP_DEC"):
            op=self.next().lexema; return {"type":"postfix","op":op,"operand":node}
        return node

    def parse_primary(self):
        t = getattr(self.peek(),"tipo",None)
        if t in ("INT_LITERAL","FLOAT_LITERAL","CHAR_LITERAL"):
            token=self.next(); return {"type":"literal","kind":token.tipo,"value":token.valor}
        if t == "STRING_START": return self.parse_string_literal()
        if t in ("IDENTIFIER","Quoted_identifier"): return self.parse_identifier_or_call_or_member()
        if t == "LPAREN": self.next(); expr=self.parse_expression(); self.expect("RPAREN","')' esperado"); return expr
        tok=self.next(); self._error_at_token(tok,"Expressão primária inválida"); return {"type":"error","token":getattr(tok,"lexema",None)}

    def parse_string_literal(self):
        self.expect("STRING_START")
        parts=[]
        while getattr(self.peek(),"tipo",None) not in ("STRING_END","EOF"):
            t=self.next()
            if getattr(t,"tipo",None)=="STRING_TEXT":
                parts.append({"type":"text","value":t.valor})
            elif getattr(t,"tipo",None)=="STRING_INTERP_ID":
                parts.append({"type":"interp_id","name":t.lexema})
            elif getattr(t,"tipo",None)=="STRING_INTERP_START":
                if getattr(self.peek(),"tipo",None)=="STRING_INTERP_EXPR":
                    expr_tok=self.next(); parts.append({"type":"interp_expr","expr_text":expr_tok.lexema})
                if getattr(self.peek(),"tipo",None)=="STRING_INTERP_END": self.next()
                else: self._error_at_token(self.peek(),"Fim de interpolação esperado ('}')"); self._panic_recover()
            else:
                parts.append({"type":"unknown","token":getattr(t,"lexema",None)})
        self.expect("STRING_END","Fim de string esperado")
        return {"type":"string","parts":parts}

    # -------------------------
    # identificador / chamadas / membros (melhor tratamento de '!! . id')
    # -------------------------
    def parse_identifier_or_call_or_member(self):
        # IDENTIFIER or Quoted_identifier
        if getattr(self.peek(),"tipo",None) in ("IDENTIFIER","Quoted_identifier"):
            node = {"type":"identifier","name":self.next().lexema}
        else:
            tok=self.next(); self._error_at_token(tok,"Identificador esperado"); return {"type":"error","token":getattr(tok,"lexema",None)}

        while True:
            ttype = getattr(self.peek(),"tipo",None)
            if ttype == "LPAREN":
                self.next()
                args=[]
                if getattr(self.peek(),"tipo",None) != "RPAREN":
                    while True:
                        args.append(self.parse_expression())
                        if not self.accept("COMMA"): break
                self.expect("RPAREN","')' esperado após argumentos de chamada")
                node = {"type":"call","callee":node,"args":args}
                continue

            # aceitamos DOT, OP_SAFE_CALL, OP_NOT_NULL
            elif ttype in ("DOT","OP_SAFE_CALL","OP_NOT_NULL"):
                op_tok = self.next()  # consome DOT / ?. / !!
                op = op_tok.lexema

                # Caso tolerante: sequência OP_NOT_NULL seguida de DOT (tokens separados),
                # ex: '!!' then '.' then IDENTIFIER. Se após consumir op o próximo token for DOT,
                # consumimos também esse DOT (para aceitar var!! .length tokenizado como '!!' '.' 'length').
                if op_tok.tipo == "OP_NOT_NULL and getattr(op_tok,'tipo',None)" or op_tok.tipo == "OP_NOT_NULL":
                    # robusto: se próximo token for DOT, consome-o
                    if getattr(self.peek(),"tipo",None) == "DOT":
                        # junta as duas peças visualmente (op passa a ser '!!.' para debug), mas semanticamente
                        # trataremos só como operação de membro seguida pelo '.' já consumido.
                        self.next()  # consome o DOT token

                # agora, o nome do membro deve aparecer (IDENTIFIER ou Quoted_identifier)
                if getattr(self.peek(),"tipo",None) in ("IDENTIFIER","Quoted_identifier"):
                    member = self.next().lexema
                    node = {"type":"member","target":node,"op":op,"member":member}
                    continue
                else:
                    # Erro: membro esperado -- mas tentamos recuperar pegando próximo identificador se possível
                    self._error_at_token(self.peek(),"Nome de membro esperado após '.' ou '?.' etc.")
                    self._panic_recover()
                    break
            else:
                break
        return node