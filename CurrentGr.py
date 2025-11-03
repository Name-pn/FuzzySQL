from libraries.Grammar.Grammar import Grammar
from libraries.Grammar.Production import Production
from libraries.Grammar.ProductionBody import ProductionBody
from libraries.Symbol.Epsilon import Epsilon
from libraries.Symbol.NonTerminal import NonTerminal
from libraries.Symbol.Terminal import Terminal, Category

lst = []
lst.append(Production(NonTerminal("S\'"), ProductionBody([NonTerminal("S")])))
lst.append(Production(NonTerminal("Num"), ProductionBody([Terminal(Category.NUMBER)])))
lst.append(Production(NonTerminal("Num"), ProductionBody([Terminal(Category.REAL_NUMBER)])))
lst.append(Production(NonTerminal("S"), ProductionBody([NonTerminal("Command")])))
lst.append(Production(NonTerminal("S"), ProductionBody([NonTerminal("Command"), Terminal(Category.SEPARATOR)])))
lst.append(Production(NonTerminal("S"), ProductionBody([NonTerminal("Command"), Terminal(Category.SEPARATOR), NonTerminal("S")])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(Category.ADD),
                                                        Terminal(Category.ID),
                                                        Terminal(Category.OPEN_BRACKET),
                                                        NonTerminal("Num"),
                                                        Terminal(Category.COMMA),
                                                        NonTerminal("Num"),
                                                        Terminal(Category.COMMA),
                                                        NonTerminal("Num"),
                                                        Terminal(Category.COMMA),
                                                        NonTerminal("Num"),
                                                        Terminal(Category.CLOSE_BRACKET),
                                                        ])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(Category.MODIFY),
                                                        Terminal(Category.ID),
                                                        Terminal(Category.OPEN_BRACKET),
                                                        NonTerminal("Num"),
                                                        Terminal(Category.COMMA),
                                                        NonTerminal("Num"),
                                                        Terminal(Category.COMMA),
                                                        NonTerminal("Num"),
                                                        Terminal(Category.COMMA),
                                                        NonTerminal("Num"),
                                                        Terminal(Category.CLOSE_BRACKET),
                                                        ])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(Category.REMOVE),
                                                        Terminal(Category.ID)])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(Category.CREATE),
                                                        Terminal(Category.TABLE),
                                                        Terminal(Category.ID),
                                                        Terminal(Category.OPEN_BRACKET),
                                                        NonTerminal("Columns"),
                                                        Terminal(Category.CLOSE_BRACKET)])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(Category.ALTER),
                                                              Terminal(Category.TABLE),
                                                              Terminal(Category.ID),
                                                              Terminal(Category.ADD),
                                                              Terminal(Category.OPEN_BRACKET),
                                                              NonTerminal("Columns"),
                                                              Terminal(Category.CLOSE_BRACKET)])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(Category.ALTER),
                                                              Terminal(Category.TABLE),
                                                              Terminal(Category.ID),
                                                              Terminal(Category.MODIFY),
                                                              Terminal(Category.OPEN_BRACKET),
                                                              NonTerminal("Columns"),
                                                              Terminal(Category.CLOSE_BRACKET)])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(Category.ALTER),
                                                              Terminal(Category.TABLE),
                                                              Terminal(Category.ID),
                                                              Terminal(Category.DROP),
                                                              Terminal(Category.OPEN_BRACKET),
                                                              NonTerminal("ColumnsID"),
                                                              Terminal(Category.CLOSE_BRACKET)])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(Category.ALTER),
                                                              Terminal(Category.TABLE),
                                                              Terminal(Category.ID),
                                                              Terminal(Category.RENAME),
                                                              Terminal(Category.ID),
                                                              Terminal(Category.ID)
                                                              ])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(Category.SET),
                                                              Terminal(Category.ID),
                                                              NonTerminal("Value")])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(Category.INSERT),
                                                              Terminal(Category.INTO),
                                                              Terminal(Category.ID),
                                                              Terminal(Category.OPEN_BRACKET),
                                                              NonTerminal("ColumnsID"),
                                                              Terminal(Category.CLOSE_BRACKET),
                                                              Terminal(Category.VALUES),
                                                              NonTerminal("InsertValues"),
                                                              ])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(Category.INSERT),
                                                              Terminal(Category.INTO),
                                                              Terminal(Category.ID),
                                                              Terminal(Category.VALUES),
                                                              NonTerminal("InsertValues"),
                                                              ])))
# lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(Category.INSERT),
#                                                               Terminal(Category.INTO),
#                                                               Terminal(Category.ID),
#                                                               Terminal(Category.VALUES),
#                                                               Terminal(Category.OPEN_BRACKET),
#                                                               NonTerminal("Values"),
#                                                               Terminal(Category.CLOSE_BRACKET)])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(Category.UPDATE),
                                                              Terminal(Category.ID),
                                                              Terminal(Category.SET),
                                                              NonTerminal("AssigmentList"),
                                                              NonTerminal("SelectWhere"),
                                                              ])))
lst.append(Production(NonTerminal("Assigment"), ProductionBody([NonTerminal("ColumnID"),
                                                              Terminal(Category.EQUAL),
                                                              NonTerminal("Expr")
                                                              ])))
lst.append(Production(NonTerminal("AssigmentList"), ProductionBody([NonTerminal("Assigment")
                                                              ])))
lst.append(Production(NonTerminal("AssigmentList"), ProductionBody([NonTerminal("Assigment"),
                                                              Terminal(Category.COMMA),
                                                              NonTerminal("AssigmentList")
                                                              ])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(Category.DELETE),
                                                              Terminal(Category.FROM),
                                                              Terminal(Category.ID)])))
lst.append(Production(NonTerminal("Command"), ProductionBody([Terminal(Category.DELETE),
                                                              Terminal(Category.FROM),
                                                              Terminal(Category.ID),
                                                              Terminal(Category.WHERE),
                                                              NonTerminal("Expr")])))
lst.append(Production(NonTerminal("Command"), ProductionBody([NonTerminal("Select")])))
lst.append(Production(NonTerminal("Select"), ProductionBody([Terminal(Category.SELECT),
                                                             Terminal(Category.MULTIPLICATION),
                                                             NonTerminal("SelectFrom"),
                                                             NonTerminal("SelectWhere"),
                                                             NonTerminal("SelectOrder")])))
lst.append(Production(NonTerminal("Select"), ProductionBody([Terminal(Category.SELECT),
                                                             NonTerminal("ExprList"),
                                                             NonTerminal("SelectFrom"),
                                                             NonTerminal("SelectWhere"),
                                                             NonTerminal("SelectOrder"),
                                                             NonTerminal("SelectWith")])))
lst.append(Production(NonTerminal("SelectWith"), ProductionBody([Epsilon()])))
lst.append(Production(NonTerminal("SelectWith"), ProductionBody([Terminal(Category.WITH),
                                                                 NonTerminal("Num")])))
lst.append(Production(NonTerminal("SelectOrder"), ProductionBody([Epsilon()])))
lst.append(Production(NonTerminal("SelectOrder"), ProductionBody([Terminal(Category.ORDER),
                                                                  Terminal(Category.BY),
                                                                  NonTerminal("OrderList")])))
lst.append(Production(NonTerminal("OrderList"), ProductionBody([NonTerminal("OrderEl"),
                                                                Terminal(Category.COMMA),
                                                                NonTerminal("OrderList")])))
lst.append(Production(NonTerminal("OrderList"), ProductionBody([NonTerminal("OrderEl")])))
lst.append(Production(NonTerminal("OrderEl"), ProductionBody([NonTerminal("Expr"),
                                                              NonTerminal("OrderType")])))
lst.append(Production(NonTerminal("OrderType"), ProductionBody([Epsilon()])))
lst.append(Production(NonTerminal("OrderType"), ProductionBody([Terminal(Category.ASC)])))
lst.append(Production(NonTerminal("OrderType"), ProductionBody([Terminal(Category.DESC)])))
lst.append(Production(NonTerminal("SelectFrom"), ProductionBody([Epsilon()])))
lst.append(Production(NonTerminal("SelectFrom"), ProductionBody([Terminal(Category.FROM),
                                                                 NonTerminal("TableRefs")])))
lst.append(Production(NonTerminal("SelectWhere"), ProductionBody([Epsilon()])))
lst.append(Production(NonTerminal("SelectWhere"), ProductionBody([Terminal(Category.WHERE),
                                                                  NonTerminal("Expr")])))
lst.append(Production(NonTerminal("TableRefs"), ProductionBody([NonTerminal("TableRefs"),
                                                                Terminal(Category.COMMA),
                                                                NonTerminal("TableRef")])))
lst.append(Production(NonTerminal("TableRefs"), ProductionBody([NonTerminal("TableRef")])))
lst.append(Production(NonTerminal("TableRef"), ProductionBody([NonTerminal("Name"),
                                                               Terminal(Category.CROSS),
                                                               Terminal(Category.JOIN),
                                                               NonTerminal("TableRef")])))
lst.append(Production(NonTerminal("TableRef"), ProductionBody([NonTerminal("Name")])))
lst.append(Production(NonTerminal("TableRef"), ProductionBody([NonTerminal("Name"),
                                                               Terminal(Category.INNER),
                                                               Terminal(Category.JOIN),
                                                               NonTerminal("TableRef")
                                                               ])))
lst.append(Production(NonTerminal("TableRef"), ProductionBody([NonTerminal("Name"),
                                                               Terminal(Category.LEFT),
                                                               NonTerminal("OptionalOuter"),
                                                               Terminal(Category.JOIN),
                                                               NonTerminal("TableRef")
                                                               ])))
lst.append(Production(NonTerminal("TableRef"), ProductionBody([NonTerminal("Name"),
                                                               Terminal(Category.RIGHT),
                                                               NonTerminal("OptionalOuter"),
                                                               Terminal(Category.JOIN),
                                                               NonTerminal("TableRef")
                                                               ])))
lst.append(Production(NonTerminal("TableRef"), ProductionBody([NonTerminal("Name"),
                                                               Terminal(Category.FULL),
                                                               NonTerminal("OptionalOuter"),
                                                               Terminal(Category.JOIN),
                                                               NonTerminal("TableRef")
                                                               ])))
lst.append(Production(NonTerminal("OptionalOuter"), ProductionBody([Terminal(Category.OUTER)])))
lst.append(Production(NonTerminal("OptionalOuter"), ProductionBody([Epsilon()])))
lst.append(Production(NonTerminal("ExprList"), ProductionBody([NonTerminal("Expr"),
                                                              Terminal(Category.COMMA),
                                                              NonTerminal("ExprList")])))
lst.append(Production(NonTerminal("ExprList"), ProductionBody([NonTerminal("Expr")])))
lst.append(Production(NonTerminal("Expr"), ProductionBody([NonTerminal("Expr"),
                                                              Terminal(Category.OR),
                                                              NonTerminal("T1")])))
lst.append(Production(NonTerminal("Expr"), ProductionBody([NonTerminal("T1")])))
lst.append(Production(NonTerminal("T1"), ProductionBody([NonTerminal("T1"),
                                                              Terminal(Category.AND),
                                                              NonTerminal("T2")])))
lst.append(Production(NonTerminal("T1"), ProductionBody([NonTerminal("T2")])))
lst.append(Production(NonTerminal("T2"), ProductionBody([Terminal(Category.NOT),
                                                              NonTerminal("T2")])))
lst.append(Production(NonTerminal("T2"), ProductionBody([NonTerminal("T3")])))
lst.append(Production(NonTerminal("T3"), ProductionBody([NonTerminal("T3"),
                                                         Terminal(Category.COMPARISON),
                                                         NonTerminal("T4")])))
lst.append(Production(NonTerminal("T3"), ProductionBody([NonTerminal("T3"),
                                                         Terminal(Category.EQUAL),
                                                         NonTerminal("T4")])))
lst.append(Production(NonTerminal("T3"), ProductionBody([NonTerminal("T4")])))
lst.append(Production(NonTerminal("T4"), ProductionBody([NonTerminal("T4"),
                                                         Terminal(Category.PLUS_AND_MINUS),
                                                         NonTerminal("T5")])))
lst.append(Production(NonTerminal("T4"), ProductionBody([NonTerminal("T5")])))
lst.append(Production(NonTerminal("T5"), ProductionBody([NonTerminal("T5"),
                                                         Terminal(Category.OPERATION),
                                                         NonTerminal("T6")])))
lst.append(Production(NonTerminal("T5"), ProductionBody([NonTerminal("T5"),
                                                         Terminal(Category.MULTIPLICATION),
                                                         NonTerminal("T6")])))
lst.append(Production(NonTerminal("T5"), ProductionBody([NonTerminal("T6")])))
lst.append(Production(NonTerminal("T6"), ProductionBody([NonTerminal("T6"),
                                                         Terminal(Category.EXPONENTIATION),
                                                         NonTerminal("Unary")])))
lst.append(Production(NonTerminal("T6"), ProductionBody([NonTerminal("Unary")])))
lst.append(Production(NonTerminal("Unary"), ProductionBody([Terminal(Category.PLUS_AND_MINUS),
                                                         NonTerminal("Unary")])))
lst.append(Production(NonTerminal("Unary"), ProductionBody([NonTerminal("Factor")])))
lst.append(Production(NonTerminal("Factor"), ProductionBody([Terminal(Category.OPEN_BRACKET),
                                                             NonTerminal("Expr"),
                                                             Terminal(Category.CLOSE_BRACKET)])))
lst.append(Production(NonTerminal("Factor"), ProductionBody([NonTerminal("FValue")])))
lst.append(Production(NonTerminal("Factor"), ProductionBody([NonTerminal("FColumn")])))
# lst.append(Production(NonTerminal("Factor"), ProductionBody([Terminal(Category.FUZZY_COLUMN),
#                                                              Terminal(Category.COLON),
#                                                              Terminal(Category.ID)])))
lst.append(Production(NonTerminal("Factor"), ProductionBody([NonTerminal("ValueOrID")])))
lst.append(Production(NonTerminal("Name"), ProductionBody([NonTerminal("Name"),
                                                           Terminal(Category.DOT),
                                                           Terminal(Category.ID)])))
lst.append(Production(NonTerminal("Name"), ProductionBody([Terminal(Category.ID)])))
lst.append(Production(NonTerminal("Columns"), ProductionBody([NonTerminal("Column"),
                                                              Terminal(Category.COMMA),
                                                              NonTerminal("Columns")])))
lst.append(Production(NonTerminal("Columns"), ProductionBody([NonTerminal("Column")])))
lst.append(Production(NonTerminal("Column"), ProductionBody([Terminal(Category.ID),
                                                             NonTerminal("Type"),
                                                             NonTerminal("Attrs")])))
lst.append(Production(NonTerminal("Type"), ProductionBody([Terminal(Category.TYPE)])))
lst.append(Production(NonTerminal("Type"), ProductionBody([Terminal(Category.TYPE),
                                                           Terminal(Category.OPEN_BRACKET),
                                                           Terminal(Category.NUMBER),
                                                           Terminal(Category.CLOSE_BRACKET)])))
lst.append(Production(NonTerminal("Type"), ProductionBody([Terminal(Category.TYPE),
                                                           Terminal(Category.OPEN_BRACKET),
                                                           Terminal(Category.NUMBER),
                                                           Terminal(Category.COMMA),
                                                           Terminal(Category.NUMBER),
                                                           Terminal(Category.CLOSE_BRACKET)])))
#lst.append(Production(NonTerminal("Type"), ProductionBody([Terminal(Category.TYPE0)])))
# lst.append(Production(NonTerminal("Type"), ProductionBody([Terminal(Category.TYPE1),
#                                                            Terminal(Category.OPEN_BRACKET),
#                                                            Terminal(Category.NUMBER),
#                                                            Terminal(Category.CLOSE_BRACKET)])))
# lst.append(Production(NonTerminal("Type"), ProductionBody([Terminal(Category.TYPE2),
#                                                            Terminal(Category.OPEN_BRACKET),
#                                                            Terminal(Category.NUMBER),
#                                                            Terminal(Category.COMMA),
#                                                            Terminal(Category.NUMBER),
#                                                            Terminal(Category.CLOSE_BRACKET)
#                                                            ])))
lst.append(Production(NonTerminal("Attrs"), ProductionBody([Epsilon()])))
lst.append(Production(NonTerminal("Attrs"), ProductionBody([NonTerminal("Attr"),
                                                            NonTerminal("Attrs")])))
lst.append(Production(NonTerminal("Attr"), ProductionBody([Terminal(Category.UNIQUE)])))
lst.append(Production(NonTerminal("Attr"), ProductionBody([Terminal(Category.NULL)])))
lst.append(Production(NonTerminal("Attr"), ProductionBody([Terminal(Category.NOT),
                                                           Terminal(Category.NULL)])))
lst.append(Production(NonTerminal("Attr"), ProductionBody([Terminal(Category.PRIMARY), Terminal(Category.KEY)])))
lst.append(Production(NonTerminal("Attr"), ProductionBody([Terminal(Category.DEFAULT), NonTerminal("ValueOrNull")])))
lst.append(Production(NonTerminal("Value"), ProductionBody([Terminal(Category.STRING)])))
lst.append(Production(NonTerminal("Value"), ProductionBody([NonTerminal("Num")])))
lst.append(Production(NonTerminal("ValueOrNull"), ProductionBody([NonTerminal("Value")])))
lst.append(Production(NonTerminal("ValueOrNull"), ProductionBody([Terminal(Category.NULL)])))
lst.append(Production(NonTerminal("Values"), ProductionBody([NonTerminal("Value"),
                                                             Terminal(Category.COMMA),
                                                             NonTerminal("Values")])))
lst.append(Production(NonTerminal("Values"), ProductionBody([NonTerminal("Value")])))
lst.append(Production(NonTerminal("ValueOrID"), ProductionBody([NonTerminal("Name")])))
lst.append(Production(NonTerminal("ValueOrID"), ProductionBody([NonTerminal("Value")])))
lst.append(Production(NonTerminal("FColumn"), ProductionBody([Terminal(Category.FUZZY_COLUMN), Terminal(Category.COLON), Terminal(Category.ID)])))
lst.append(Production(NonTerminal("ColumnID"), ProductionBody([Terminal(Category.ID)])))
lst.append(Production(NonTerminal("ColumnID"), ProductionBody([NonTerminal("FColumn")])))
lst.append(Production(NonTerminal("ColumnsID"), ProductionBody([NonTerminal("ColumnID")])))
lst.append(Production(NonTerminal("ColumnsID"), ProductionBody([NonTerminal("ColumnID"), Terminal(Category.COMMA), NonTerminal("ColumnsID")])))
lst.append(Production(NonTerminal("InsertValue"), ProductionBody([Terminal(Category.OPEN_BRACKET),
                                                                   NonTerminal("Values"),
                                                                   Terminal(Category.CLOSE_BRACKET)])))
lst.append(Production(NonTerminal("InsertValues"), ProductionBody([NonTerminal("InsertValue")])))
lst.append(Production(NonTerminal("InsertValues"), ProductionBody([NonTerminal("InsertValue"),
                                                                   Terminal(Category.COMMA),
                                                                   NonTerminal("InsertValues")])))
lst.append(Production(NonTerminal("FValue"), ProductionBody([Terminal(Category.FUZZY_VALUE),
                                                             Terminal(Category.COLON),
                                                             Terminal(Category.ID)])))

gr = Grammar(lst, NonTerminal("S\'"))