grammar Sql;

// Парсерные правила
start : s;

s : command SEPARATOR s
   | command SEPARATOR
   | command;

command : ADD ID OPEN_BRACKET num COMMA num COMMA num COMMA num CLOSE_BRACKET
        | MODIFY ID OPEN_BRACKET num COMMA num COMMA num COMMA num CLOSE_BRACKET
        | REMOVE ID
        | CREATE TABLE ID OPEN_BRACKET columns CLOSE_BRACKET
        | ALTER TABLE ID ADD OPEN_BRACKET columns CLOSE_BRACKET
        | ALTER TABLE ID MODIFY OPEN_BRACKET columns CLOSE_BRACKET
        | ALTER TABLE ID DROP OPEN_BRACKET columnsid CLOSE_BRACKET
        | ALTER TABLE ID RENAME ID ID
        | SET ID value
        | INSERT INTO ID OPEN_BRACKET columnsid CLOSE_BRACKET VALUES insertvalues
        | INSERT INTO ID VALUES insertvalues
        | UPDATE ID SET assigmentlist selectwhere
        | DELETE FROM ID
        | DELETE FROM ID WHERE expr
        | select
        | DROP TABLE ID
        | fselect;

select : SELECT MULTIPLICATION selectfrom selectwhere selectorder
       | SELECT exprlist selectfrom selectwhere selectorder selectwith;

fselect : FSELECT MULTIPLICATION selectfrom fselectwhere selectorder
        | FSELECT exprlist selectfrom fselectwhere selectorder selectwith;

selectfrom : FROM tablerefs
           | ;

selectwhere : WHERE expr
            | ;

selectorder : ORDER BY orderlist
            | ;

selectwith : WITH num
           | ;

fselectwhere : WHERE fexpr
             | ;

tablerefs : tableref
          | tablerefs COMMA tableref;

tableref : tableref CROSS JOIN name
         | tableref INNER JOIN name ON expr
         | tableref LEFT optionalouter JOIN name ON expr
         | tableref RIGHT optionalouter JOIN name ON expr
         | tableref FULL optionalouter JOIN name ON expr
         | name;

optionalouter : OUTER
              | ;

orderlist : orderel
          | orderel COMMA orderlist;

orderel : expr ordertype;

ordertype : ASC
          | DESC
          | ;

expr : expr OR t1
     | t1;

t1 : t1 AND t2
   | t2;

t2 : NOT t2
   | t3;

t3 : t3 COMPARISON t4
   | t3 EQUAL t4
   | t4;

t4 : t4 PLUS t5
   | t4 MINUS t5
   | t5;

t5 : t5 MULTIPLICATION t6
   | t5 DIVIDE t6
   | t5 MOD t6
   | t6;

t6 : t6 EXPONENTIATION unary
   | unary;

unary : PLUS unary
      | MINUS unary
      | factor;

factor : OPEN_BRACKET expr CLOSE_BRACKET
       | fvalue
       | fcolumn
       | valueorid;

fexpr : fexpr OR ft1
      | ft1;

ft1 : ft1 AND ft2
    | ft2;

ft2 : NOT ft2
    | ft3;

ft3 : fvalue EQUAL name
    | name EQUAL fvalue
    | ffactor;

ffactor : OPEN_BRACKET fexpr CLOSE_BRACKET;

fvalue : FUZZY_VALUE COLON ID;

fcolumn : FUZZY_COLUMN COLON ID;

valueorid : name
          | value;

value : STRING
      | num;

num : NUMBER
    | REAL_NUMBER;

name : name DOT ID
     | ID;

exprlist : expr
         | expr COMMA exprlist;

assigmentlist : assigment
              | assigment COMMA assigmentlist;

assigment : columnid EQUAL expr;

columnid : ID
         | fcolumn;

column : ID column_type attrs;

columns : column
        | column COMMA columns;

columnsid : columnid
          | columnid COMMA columnsid;

attrs : attr attrs
      | ;

attr : UNIQUE
     | NULL
     | NOT NULL
     | PRIMARY KEY
     | DEFAULT valueornull;

column_type : TYPE
     | TYPE OPEN_BRACKET NUMBER CLOSE_BRACKET
     | TYPE OPEN_BRACKET NUMBER COMMA NUMBER CLOSE_BRACKET;

valueornull : value
            | NULL;

insertvalues : insertvalue
              | insertvalue COMMA insertvalues;

insertvalue : OPEN_BRACKET values CLOSE_BRACKET;

values : value
       | value COMMA values;

// Лексерные правила
// Ключевые слова (должны быть перед ID)
ON : 'ON';
ADD : 'ADD';
FSELECT : 'FSELECT';
SELECT : 'SELECT';
FROM : 'FROM';
WHERE : 'WHERE';
GROUP : 'GROUP';
BY : 'BY';
ORDER : 'ORDER';
ASC : 'ASC';
DESC : 'DESC';
OR : 'OR';
AND : 'AND';
NOT : 'NOT';
EXISTS : 'EXISTS';
HAVING : 'HAVING';
WITH : 'WITH';
OUTER : 'OUTER';
CROSS : 'CROSS';
JOIN : 'JOIN';
LEFT : 'LEFT';
RIGHT : 'RIGHT';
TABLE : 'TABLE';
INNER : 'INNER';
FULL : 'FULL';
MODIFY : 'MODIFY';
REMOVE : 'REMOVE';
CREATE : 'CREATE';
SET : 'SET';
INSERT : 'INSERT';
INTO : 'INTO';
VALUES : 'VALUES';
ALTER : 'ALTER';
RENAME : 'RENAME';
DROP : 'DROP';
UNIQUE : 'UNIQUE';
PRIMARY : 'PRIMARY';
KEY : 'KEY';
DEFAULT : 'DEFAULT';
NULL : 'NULL';
UPDATE : 'UPDATE';
DELETE : 'DELETE';

// Специальные литералы
FUZZY_VALUE : 'fv';
FUZZY_COLUMN : 'fc';

// Типы данных
TYPE : 'INT' | 'INTEGER' | 'REAL' | 'DATE' | 'INTERVAL'
     | 'FUZZY' | 'CHARACTER' | 'CHAR' | 'VARCHAR'
     | 'BIT' | 'FLOAT' | 'TIME' | 'TIMESTAMP'
     | 'DEC' | 'DECIMAL' | 'NUMERIC';

// Пробелы и комментарии (пропускаются)
SPACE : [ \t\r\n]+ -> skip;
COMMENT : '--' ~[\r\n]* -> skip;

// Основные токены
ID : [A-Za-z][A-Za-z0-9_]*;
STRING : '\'' ('\'\'' | ~'\'')* '\'';
REAL_NUMBER : [0-9]+ '.' [0-9]+;
NUMBER : [0-9]+;

// Операторы
EQUAL : '=';
COMPARISON : '!=' | '>=' | '<=' | '<<' | '>>' | '<>' | '<' | '>';
PLUS : '+';
MINUS : '-';
MULTIPLICATION : '*';
DIVIDE : '/';
MOD : '%';
EXPONENTIATION : '^';

// Разделители
DOT : '.';
COMMA : ',';
SEPARATOR : ';';
COLON : ':';
OPEN_BRACKET : '(';
CLOSE_BRACKET : ')';