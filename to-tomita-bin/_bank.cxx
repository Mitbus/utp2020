#encoding "utf8"

BIK -> Word<wff=/(Б|б)(И|и)(К|к)/> ("банк") ("получатель") (":") AnyWord<wff=/\d{9}/> interp (bank_fact.bik);

Corresp -> Word<wff=/(К|к)ор(респондентский)?/> (".") ("/") (Word<wff=/сч/>) ("счет") (".") ("банк") (":")
 AnyWord<wff=/\d{20}/> interp (bank_fact.corresp);

INN -> Word<wff=/ИНН/> ("юридический") ("физический") ("лицо") ("получатель") (":")
 AnyWord<wff=/\d{10}/> interp (bank_fact.inn);

Ras -> Word<wff=/((Р|р)(ас)?ч?)|((Л|л)(иц)?)/> (".") ("/") (Word<wff=/сч/>) ("счет") (".")
 ("получатель") ("взыскатель") ("платеж") (":") AnyWord<wff=/\d{20}/> interp (bank_fact.ras);
Ras -> "лицевой" ("счет") ("получатель") ("взыскатель") ("платеж") (":")
 AnyWord<wff=/\d{20}/> interp (bank_fact.ras);
Ras -> "расчетный" ("счет") ("получатель") ("взыскатель") ("платеж") (":")
 AnyWord<wff=/\d{20}/> interp (bank_fact.ras);

UserData -> INN (AnyWord<cut>*) Ras | Ras (AnyWord<cut>*) INN;
BankData -> BIK (AnyWord<cut>*) Corresp | Corresp (AnyWord<cut>*) BIK;

S1 -> UserData (AnyWord<cut>*) BankData | BankData (AnyWord<cut>*) UserData | BankData | UserData;
S -> S1 interp (bank_fact.text);