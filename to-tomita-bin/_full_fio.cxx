#encoding "utf8"
#GRAMMAR_KWSET ["bank_gram", "geo_gram"]

ExpName -> Word<kwtype=person_name>;
ExpSurname -> Word<kwtype=person_surname>;

FIO -> ExpName<gnc-agr[1]> interp (fio_fact.name::not_norm; fio_fact.normal_name)
 (Word<gram='отч', gnc-agr[1]> interp (fio_fact.middle_name::not_norm; fio_fact.normal_middle_name))
 ExpSurname<gnc-agr[1]> interp (fio_fact.surname::not_norm; fio_fact.normal_surname);
FIO -> ExpSurname<gnc-agr[1]> interp (fio_fact.surname::not_norm; fio_fact.normal_surname)
 ExpName<gnc-agr[1]> interp (fio_fact.name::not_norm; fio_fact.normal_name)
 (Word<gram='отч', gnc-agr[1]> interp (fio_fact.middle_name::not_norm; fio_fact.normal_middle_name));

S -> FIO interp (fio_fact.text::not_norm);