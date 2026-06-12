from libraries.Grammar.Grammar import Grammar
from libraries.Grammar.Production import Production
from libraries.Grammar.ProductionBody import ProductionBody
from libraries.Symbol.Epsilon import Epsilon
from libraries.Symbol.NonTerminal import NonTerminal
from libraries.Symbol.Terminal import Terminal, TokenType

lst = []
lst.append(Production(NonTerminal("S\'"), ProductionBody([NonTerminal("S")])))
lst.append(Production(NonTerminal("Num"), ProductionBody([Terminal(TokenType.NUMBER)])))
lst.append(Production(NonTerminal("Num"), ProductionBody([Terminal(TokenType.REAL_NUMBER)])))
lst.append(Production(NonTerminal("S"), ProductionBody([NonTerminal("Command")])))
lst.append(Production(NonTerminal("S"), ProductionBody([NonTerminal("Command"), Terminal(TokenType.SEPARATOR)])))
lst.append(Production(NonTerminal("S"), ProductionBody([NonTerminal("Command"), Terminal(TokenType.SEPARATOR), NonTerminal("S")])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(TokenType.ADD),
                                                        Terminal(TokenType.ID),
                                                        Terminal(TokenType.OPEN_BRACKET),
                                                        NonTerminal("Num"),
                                                        Terminal(TokenType.COMMA),
                                                        NonTerminal("Num"),
                                                        Terminal(TokenType.COMMA),
                                                        NonTerminal("Num"),
                                                        Terminal(TokenType.COMMA),
                                                        NonTerminal("Num"),
                                                        Terminal(TokenType.CLOSE_BRACKET),
                                                        ])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(TokenType.MODIFY),
                                                        Terminal(TokenType.ID),
                                                        Terminal(TokenType.OPEN_BRACKET),
                                                        NonTerminal("Num"),
                                                        Terminal(TokenType.COMMA),
                                                        NonTerminal("Num"),
                                                        Terminal(TokenType.COMMA),
                                                        NonTerminal("Num"),
                                                        Terminal(TokenType.COMMA),
                                                        NonTerminal("Num"),
                                                        Terminal(TokenType.CLOSE_BRACKET),
                                                        ])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(TokenType.REMOVE),
                                                        Terminal(TokenType.ID)])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(TokenType.CREATE),
                                                        Terminal(TokenType.TABLE),
                                                        Terminal(TokenType.ID),
                                                        Terminal(TokenType.OPEN_BRACKET),
                                                        NonTerminal("Columns"),
                                                        Terminal(TokenType.CLOSE_BRACKET)])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(TokenType.ALTER),
                                                              Terminal(TokenType.TABLE),
                                                              Terminal(TokenType.ID),
                                                              Terminal(TokenType.ADD),
                                                              Terminal(TokenType.OPEN_BRACKET),
                                                              NonTerminal("Columns"),
                                                              Terminal(TokenType.CLOSE_BRACKET)])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(TokenType.ALTER),
                                                              Terminal(TokenType.TABLE),
                                                              Terminal(TokenType.ID),
                                                              Terminal(TokenType.MODIFY),
                                                              Terminal(TokenType.OPEN_BRACKET),
                                                              NonTerminal("Columns"),
                                                              Terminal(TokenType.CLOSE_BRACKET)])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(TokenType.ALTER),
                                                              Terminal(TokenType.TABLE),
                                                              Terminal(TokenType.ID),
                                                              Terminal(TokenType.DROP),
                                                              Terminal(TokenType.OPEN_BRACKET),
                                                              NonTerminal("ColumnsID"),
                                                              Terminal(TokenType.CLOSE_BRACKET)])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(TokenType.ALTER),
                                                              Terminal(TokenType.TABLE),
                                                              Terminal(TokenType.ID),
                                                              Terminal(TokenType.RENAME),
                                                              Terminal(TokenType.ID),
                                                              Terminal(TokenType.ID)
                                                              ])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(TokenType.SET),
                                                              Terminal(TokenType.ID),
                                                              NonTerminal("Value")])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(TokenType.INSERT),
                                                              Terminal(TokenType.INTO),
                                                              Terminal(TokenType.ID),
                                                              Terminal(TokenType.OPEN_BRACKET),
                                                              NonTerminal("ColumnsID"),
                                                              Terminal(TokenType.CLOSE_BRACKET),
                                                              Terminal(TokenType.VALUES),
                                                              NonTerminal("InsertValues"),
                                                              ])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(TokenType.INSERT),
                                                              Terminal(TokenType.INTO),
                                                              Terminal(TokenType.ID),
                                                              Terminal(TokenType.VALUES),
                                                              NonTerminal("InsertValues"),
                                                              ])))
# lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(TokenType.INSERT),
#                                                               Terminal(TokenType.INTO),
#                                                               Terminal(TokenType.ID),
#                                                               Terminal(TokenType.VALUES),
#                                                               Terminal(TokenType.OPEN_BRACKET),
#                                                               NonTerminal("Values"),
#                                                               Terminal(TokenType.CLOSE_BRACKET)])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(TokenType.UPDATE),
                                                              Terminal(TokenType.ID),
                                                              Terminal(TokenType.SET),
                                                              NonTerminal("AssigmentList"),
                                                              NonTerminal("SelectWhere"),
                                                              ])))
lst.append(Production(NonTerminal("Assigment"), ProductionBody([NonTerminal("ColumnID"),
                                                              Terminal(TokenType.EQUAL),
                                                              NonTerminal("Expr")
                                                              ])))
lst.append(Production(NonTerminal("AssigmentList"), ProductionBody([NonTerminal("Assigment")
                                                              ])))
lst.append(Production(NonTerminal("AssigmentList"), ProductionBody([NonTerminal("Assigment"),
                                                              Terminal(TokenType.COMMA),
                                                              NonTerminal("AssigmentList")
                                                              ])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(TokenType.DELETE),
                                                              Terminal(TokenType.FROM),
                                                              Terminal(TokenType.ID)])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(TokenType.DELETE),
                                                              Terminal(TokenType.FROM),
                                                              Terminal(TokenType.ID),
                                                              Terminal(TokenType.WHERE),
                                                              NonTerminal("Expr")])))
lst.append(Production(NonTerminal("Command"), ProductionBody([NonTerminal("Select")])))
lst.append(Production(NonTerminal("Select"), ProductionBody([Terminal(TokenType.SELECT),
                                                             Terminal(TokenType.MULTIPLICATION),
                                                             NonTerminal("SelectFrom"),
                                                             NonTerminal("SelectWhere"),
                                                             NonTerminal("SelectOrder")])))
lst.append(Production(NonTerminal("Select"), ProductionBody([Terminal(TokenType.SELECT),
                                                             NonTerminal("ExprList"),
                                                             NonTerminal("SelectFrom"),
                                                             NonTerminal("SelectWhere"),
                                                             NonTerminal("SelectOrder"),
                                                             NonTerminal("SelectWith")])))
lst.append(Production(NonTerminal("SelectWith"), ProductionBody([Epsilon()])))
lst.append(Production(NonTerminal("SelectWith"), ProductionBody([Terminal(TokenType.WITH),
                                                                 NonTerminal("Num")])))
lst.append(Production(NonTerminal("SelectOrder"), ProductionBody([Epsilon()])))
lst.append(Production(NonTerminal("SelectOrder"), ProductionBody([Terminal(TokenType.ORDER),
                                                                  Terminal(TokenType.BY),
                                                                  NonTerminal("OrderList")])))
lst.append(Production(NonTerminal("OrderList"), ProductionBody([NonTerminal("OrderEl"),
                                                                Terminal(TokenType.COMMA),
                                                                NonTerminal("OrderList")])))
lst.append(Production(NonTerminal("OrderList"), ProductionBody([NonTerminal("OrderEl")])))
lst.append(Production(NonTerminal("OrderEl"), ProductionBody([NonTerminal("Expr"),
                                                              NonTerminal("OrderType")])))
lst.append(Production(NonTerminal("OrderType"), ProductionBody([Epsilon()])))
lst.append(Production(NonTerminal("OrderType"), ProductionBody([Terminal(TokenType.ASC)])))
lst.append(Production(NonTerminal("OrderType"), ProductionBody([Terminal(TokenType.DESC)])))
lst.append(Production(NonTerminal("SelectFrom"), ProductionBody([Epsilon()])))
lst.append(Production(NonTerminal("SelectFrom"), ProductionBody([Terminal(TokenType.FROM),
                                                                 NonTerminal("TableRefs")])))
lst.append(Production(NonTerminal("SelectWhere"), ProductionBody([Epsilon()])))
lst.append(Production(NonTerminal("SelectWhere"), ProductionBody([Terminal(TokenType.WHERE),
                                                                  NonTerminal("Expr")])))
lst.append(Production(NonTerminal("TableRefs"), ProductionBody([NonTerminal("TableRefs"),
                                                                Terminal(TokenType.COMMA),
                                                                NonTerminal("TableRef")])))
lst.append(Production(NonTerminal("TableRefs"), ProductionBody([NonTerminal("TableRef")])))
lst.append(Production(NonTerminal("TableRef"), ProductionBody([NonTerminal("Name"),
                                                               Terminal(TokenType.CROSS),
                                                               Terminal(TokenType.JOIN),
                                                               NonTerminal("TableRef")])))
lst.append(Production(NonTerminal("TableRef"), ProductionBody([NonTerminal("Name")])))
lst.append(Production(NonTerminal("TableRef"), ProductionBody([NonTerminal("Name"),
                                                               Terminal(TokenType.INNER),
                                                               Terminal(TokenType.JOIN),
                                                               NonTerminal("TableRef")
                                                               ])))
lst.append(Production(NonTerminal("TableRef"), ProductionBody([NonTerminal("Name"),
                                                               Terminal(TokenType.LEFT),
                                                               NonTerminal("OptionalOuter"),
                                                               Terminal(TokenType.JOIN),
                                                               NonTerminal("TableRef")
                                                               ])))
lst.append(Production(NonTerminal("TableRef"), ProductionBody([NonTerminal("Name"),
                                                               Terminal(TokenType.RIGHT),
                                                               NonTerminal("OptionalOuter"),
                                                               Terminal(TokenType.JOIN),
                                                               NonTerminal("TableRef")
                                                               ])))
lst.append(Production(NonTerminal("TableRef"), ProductionBody([NonTerminal("Name"),
                                                               Terminal(TokenType.FULL),
                                                               NonTerminal("OptionalOuter"),
                                                               Terminal(TokenType.JOIN),
                                                               NonTerminal("TableRef")
                                                               ])))
lst.append(Production(NonTerminal("OptionalOuter"), ProductionBody([Terminal(TokenType.OUTER)])))
lst.append(Production(NonTerminal("OptionalOuter"), ProductionBody([Epsilon()])))
lst.append(Production(NonTerminal("ExprList"), ProductionBody([NonTerminal("Expr"),
                                                              Terminal(TokenType.COMMA),
                                                              NonTerminal("ExprList")])))
lst.append(Production(NonTerminal("ExprList"), ProductionBody([NonTerminal("Expr")])))
lst.append(Production(NonTerminal("Expr"), ProductionBody([NonTerminal("Expr"),
                                                              Terminal(TokenType.OR),
                                                              NonTerminal("T1")])))
lst.append(Production(NonTerminal("Expr"), ProductionBody([NonTerminal("T1")])))
lst.append(Production(NonTerminal("T1"), ProductionBody([NonTerminal("T1"),
                                                              Terminal(TokenType.AND),
                                                              NonTerminal("T2")])))
lst.append(Production(NonTerminal("T1"), ProductionBody([NonTerminal("T2")])))
lst.append(Production(NonTerminal("T2"), ProductionBody([Terminal(TokenType.NOT),
                                                              NonTerminal("T2")])))
lst.append(Production(NonTerminal("T2"), ProductionBody([NonTerminal("T3")])))
lst.append(Production(NonTerminal("T3"), ProductionBody([NonTerminal("T3"),
                                                         Terminal(TokenType.COMPARISON),
                                                         NonTerminal("T4")])))
lst.append(Production(NonTerminal("T3"), ProductionBody([NonTerminal("T3"),
                                                         Terminal(TokenType.EQUAL),
                                                         NonTerminal("T4")])))
lst.append(Production(NonTerminal("T3"), ProductionBody([NonTerminal("T4")])))
lst.append(Production(NonTerminal("T4"), ProductionBody([NonTerminal("T4"),
                                                         Terminal(TokenType.PLUS),
                                                         NonTerminal("T5")])))
lst.append(Production(NonTerminal("T4"), ProductionBody([NonTerminal("T5")])))
lst.append(Production(NonTerminal("T5"), ProductionBody([NonTerminal("T5"),
                                                         Terminal(TokenType.DIVIDE),
                                                         NonTerminal("T6")])))
lst.append(Production(NonTerminal("T5"), ProductionBody([NonTerminal("T5"),
                                                         Terminal(TokenType.MULTIPLICATION),
                                                         NonTerminal("T6")])))
lst.append(Production(NonTerminal("T5"), ProductionBody([NonTerminal("T6")])))
lst.append(Production(NonTerminal("T6"), ProductionBody([NonTerminal("T6"),
                                                         Terminal(TokenType.EXPONENTIATION),
                                                         NonTerminal("Unary")])))
lst.append(Production(NonTerminal("T6"), ProductionBody([NonTerminal("Unary")])))
lst.append(Production(NonTerminal("Unary"), ProductionBody([Terminal(TokenType.PLUS),
                                                         NonTerminal("Unary")])))
lst.append(Production(NonTerminal("Unary"), ProductionBody([NonTerminal("Factor")])))
lst.append(Production(NonTerminal("Factor"), ProductionBody([Terminal(TokenType.OPEN_BRACKET),
                                                             NonTerminal("Expr"),
                                                             Terminal(TokenType.CLOSE_BRACKET)])))
lst.append(Production(NonTerminal("Factor"), ProductionBody([NonTerminal("FValue")])))
lst.append(Production(NonTerminal("Factor"), ProductionBody([NonTerminal("FColumn")])))
# lst.append(Production(NonTerminal("Factor"), ProductionBody([Terminal(TokenType.FUZZY_COLUMN),
#                                                              Terminal(TokenType.COLON),
#                                                              Terminal(TokenType.ID)])))
lst.append(Production(NonTerminal("Factor"), ProductionBody([NonTerminal("ValueOrID")])))
lst.append(Production(NonTerminal("Name"), ProductionBody([NonTerminal("Name"),
                                                           Terminal(TokenType.DOT),
                                                           Terminal(TokenType.ID)])))
lst.append(Production(NonTerminal("Name"), ProductionBody([Terminal(TokenType.ID)])))
lst.append(Production(NonTerminal("Columns"), ProductionBody([NonTerminal("Column"),
                                                              Terminal(TokenType.COMMA),
                                                              NonTerminal("Columns")])))
lst.append(Production(NonTerminal("Columns"), ProductionBody([NonTerminal("Column")])))
lst.append(Production(NonTerminal("Column"), ProductionBody([Terminal(TokenType.ID),
                                                             NonTerminal("Type"),
                                                             NonTerminal("Attrs")])))
lst.append(Production(NonTerminal("Type"), ProductionBody([Terminal(TokenType.TYPE)])))
lst.append(Production(NonTerminal("Type"), ProductionBody([Terminal(TokenType.TYPE),
                                                           Terminal(TokenType.OPEN_BRACKET),
                                                           Terminal(TokenType.NUMBER),
                                                           Terminal(TokenType.CLOSE_BRACKET)])))
lst.append(Production(NonTerminal("Type"), ProductionBody([Terminal(TokenType.TYPE),
                                                           Terminal(TokenType.OPEN_BRACKET),
                                                           Terminal(TokenType.NUMBER),
                                                           Terminal(TokenType.COMMA),
                                                           Terminal(TokenType.NUMBER),
                                                           Terminal(TokenType.CLOSE_BRACKET)])))
#lst.append(Production(NonTerminal("Type"), ProductionBody([Terminal(TokenType.TYPE0)])))
# lst.append(Production(NonTerminal("Type"), ProductionBody([Terminal(TokenType.TYPE1),
#                                                            Terminal(TokenType.OPEN_BRACKET),
#                                                            Terminal(TokenType.NUMBER),
#                                                            Terminal(TokenType.CLOSE_BRACKET)])))
# lst.append(Production(NonTerminal("Type"), ProductionBody([Terminal(TokenType.TYPE2),
#                                                            Terminal(TokenType.OPEN_BRACKET),
#                                                            Terminal(TokenType.NUMBER),
#                                                            Terminal(TokenType.COMMA),
#                                                            Terminal(TokenType.NUMBER),
#                                                            Terminal(TokenType.CLOSE_BRACKET)
#                                                            ])))
lst.append(Production(NonTerminal("Attrs"), ProductionBody([Epsilon()])))
lst.append(Production(NonTerminal("Attrs"), ProductionBody([NonTerminal("Attr"),
                                                            NonTerminal("Attrs")])))
lst.append(Production(NonTerminal("Attr"), ProductionBody([Terminal(TokenType.UNIQUE)])))
lst.append(Production(NonTerminal("Attr"), ProductionBody([Terminal(TokenType.NULL)])))
lst.append(Production(NonTerminal("Attr"), ProductionBody([Terminal(TokenType.NOT),
                                                           Terminal(TokenType.NULL)])))
lst.append(Production(NonTerminal("Attr"), ProductionBody([Terminal(TokenType.PRIMARY), Terminal(TokenType.KEY)])))
lst.append(Production(NonTerminal("Attr"), ProductionBody([Terminal(TokenType.DEFAULT), NonTerminal("ValueOrNull")])))
lst.append(Production(NonTerminal("Value"), ProductionBody([Terminal(TokenType.STRING)])))
lst.append(Production(NonTerminal("Value"), ProductionBody([NonTerminal("Num")])))
lst.append(Production(NonTerminal("ValueOrNull"), ProductionBody([NonTerminal("Value")])))
lst.append(Production(NonTerminal("ValueOrNull"), ProductionBody([Terminal(TokenType.NULL)])))
lst.append(Production(NonTerminal("Values"), ProductionBody([NonTerminal("Value"),
                                                             Terminal(TokenType.COMMA),
                                                             NonTerminal("Values")])))
lst.append(Production(NonTerminal("Values"), ProductionBody([NonTerminal("Value")])))
lst.append(Production(NonTerminal("ValueOrID"), ProductionBody([NonTerminal("Name")])))
lst.append(Production(NonTerminal("ValueOrID"), ProductionBody([NonTerminal("Value")])))
lst.append(Production(NonTerminal("FColumn"), ProductionBody([Terminal(TokenType.FUZZY_COLUMN), Terminal(TokenType.COLON), Terminal(TokenType.ID)])))
lst.append(Production(NonTerminal("ColumnID"), ProductionBody([Terminal(TokenType.ID)])))
lst.append(Production(NonTerminal("ColumnID"), ProductionBody([NonTerminal("FColumn")])))
lst.append(Production(NonTerminal("ColumnsID"), ProductionBody([NonTerminal("ColumnID")])))
lst.append(Production(NonTerminal("ColumnsID"), ProductionBody([NonTerminal("ColumnID"), Terminal(TokenType.COMMA), NonTerminal("ColumnsID")])))
lst.append(Production(NonTerminal("InsertValue"), ProductionBody([Terminal(TokenType.OPEN_BRACKET),
                                                                   NonTerminal("Values"),
                                                                   Terminal(TokenType.CLOSE_BRACKET)])))
lst.append(Production(NonTerminal("InsertValues"), ProductionBody([NonTerminal("InsertValue")])))
lst.append(Production(NonTerminal("InsertValues"), ProductionBody([NonTerminal("InsertValue"),
                                                                   Terminal(TokenType.COMMA),
                                                                   NonTerminal("InsertValues")])))
lst.append(Production(NonTerminal("FValue"), ProductionBody([Terminal(TokenType.FUZZY_VALUE),
                                                             Terminal(TokenType.COLON),
                                                             Terminal(TokenType.ID)])))
lst.append(Production(NonTerminal("Unary"), ProductionBody([Terminal(TokenType.MINUS),
                                                         NonTerminal("Unary")])))
lst.append(Production(NonTerminal("T4"), ProductionBody([NonTerminal("T4"),
                                                         Terminal(TokenType.MINUS),
                                                         NonTerminal("T5")])))
lst.append(Production(NonTerminal("T5"), ProductionBody([NonTerminal("T5"),
                                                         Terminal(TokenType.MOD),
                                                         NonTerminal("T6")])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(TokenType.DROP),
                                                         Terminal(TokenType.TABLE),
                                                         Terminal(TokenType.ID)])))
lst.append(Production(NonTerminal("Command"), ProductionBody([NonTerminal("FSelect")])))
lst.append(Production(NonTerminal("FSelect"), ProductionBody([Terminal(TokenType.FSELECT),
                                                             Terminal(TokenType.MULTIPLICATION),
                                                             NonTerminal("SelectFrom"),
                                                             NonTerminal("FSelectWhere"),
                                                             NonTerminal("SelectOrder")])))
lst.append(Production(NonTerminal("FSelect"), ProductionBody([Terminal(TokenType.FSELECT),
                                                             NonTerminal("ExprList"),
                                                             NonTerminal("SelectFrom"),
                                                             NonTerminal("FSelectWhere"),
                                                             NonTerminal("SelectOrder"),
                                                             NonTerminal("SelectWith")])))
lst.append(Production(NonTerminal("FSelectWhere"), ProductionBody([Epsilon()])))
lst.append(Production(NonTerminal("FSelectWhere"), ProductionBody([Terminal(TokenType.WHERE),
                                                                  NonTerminal("FExpr")])))
lst.append(Production(NonTerminal("FExpr"), ProductionBody([NonTerminal("FExpr"),
                                                              Terminal(TokenType.OR),
                                                              NonTerminal("FT1")])))
lst.append(Production(NonTerminal("FExpr"), ProductionBody([NonTerminal("FT1")])))
lst.append(Production(NonTerminal("FT1"), ProductionBody([NonTerminal("FT1"),
                                                              Terminal(TokenType.AND),
                                                              NonTerminal("FT2")])))
lst.append(Production(NonTerminal("FT1"), ProductionBody([NonTerminal("FT2")])))
lst.append(Production(NonTerminal("FT2"), ProductionBody([Terminal(TokenType.NOT),
                                                              NonTerminal("FT2")])))
lst.append(Production(NonTerminal("FT2"), ProductionBody([NonTerminal("FT3")])))
lst.append(Production(NonTerminal("FT3"), ProductionBody([NonTerminal("FValue"),
                                                         Terminal(TokenType.EQUAL),
                                                         NonTerminal("Name")])))
lst.append(Production(NonTerminal("FT3"), ProductionBody([NonTerminal("Name"),
                                                         Terminal(TokenType.EQUAL),
                                                         NonTerminal("FValue")])))
lst.append(Production(NonTerminal("FT3"), ProductionBody([NonTerminal("FFactor")])))
lst.append(Production(NonTerminal("FFactor"), ProductionBody([Terminal(TokenType.OPEN_BRACKET),
                                                             NonTerminal("FExpr"),
                                                             Terminal(TokenType.CLOSE_BRACKET)])))

gr = Grammar(lst, NonTerminal("S\'"))