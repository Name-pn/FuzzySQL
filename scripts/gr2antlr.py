from libraries.Environment import Environment
from libraries.Grammar.Grammar import Grammar
from libraries.Grammar.ProductionBody import ProductionBody
from libraries.Symbol.NonTerminal import NonTerminal
from libraries.Symbol.SymbolType import SymbolType
from libraries.Symbol.Terminal import TokenSpecification, TokenType


def get_noterminal_rules_in_dict(gr:Grammar)->dict[NonTerminal, list[ProductionBody]]:
    res = {}
    non_terminals = gr.get_nonterminals()
    for noterminal in non_terminals:
        res[noterminal] = []
        for rule in gr.dict:
            if rule.head == noterminal:
                res[noterminal].append(rule.body)
    return res

def from_dict_to_str_parser_grammar(d: dict[NonTerminal, list[ProductionBody]])->str:
    res = ""
    for key, value in d.items():
        res += key.value.lower() + " : "
        for body in value:
            for symbol in body.arr:
                if symbol.type == SymbolType.NONTERMINAL:
                    res += symbol.value.lower() + " "
                elif symbol.type == SymbolType.TERMINAL:
                    res += symbol.value.upper() + " "
            res = res[:-1] + "\n|"
        res = res[:-2] + ";\n"
    return res

def get_lexer_str():
    res = ""
    env = Environment()
    env.load("./parser_data/conf.pkl")
    lst = TokenSpecification.get_patterns(env)
    for type, pattern, _, _ in lst:
        if type is TokenType.TYPE:
            res += type.name + " : " + pattern[2:] + "\n"
            continue
        if TokenSpecification.KEYWORDS.get(type, None) is None:
            res += type.name + " : " + pattern + "\n"
        else:
            res += type.name + " : \'" + pattern + "\'\n"

    return res

if __name__ == "__main__":
    gr = Grammar.load("./parser_data/grammar.txt")
    res = "grammar Sql;\n"

    d = get_noterminal_rules_in_dict(gr)
    parser_str = from_dict_to_str_parser_grammar(d)
    parser_str = parser_str.replace("s\'", "start")
    res += parser_str

    lexer_str = get_lexer_str()
    lexer_str = lexer_str.replace("\\b", "")

    print(lexer_str)


