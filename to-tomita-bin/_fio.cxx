#encoding "utf8"
#GRAMMAR_KWSET ["full_fio_gram", "bank_gram", "geo_gram"]

// Защита от ложных срабатываний
BaseName -> ExpName<gram='имя'>;
ExpName -> Word<kwtype=person_name>;
BaseSurname -> ExpSurname<gram='фам'>;
ExpSurname -> Word<kwtype=person_surname>;

Initial -> Word<wff=/[А-Я]\./>;
Initials -> Initial (Initial);
FIO -> ExpName interp (fio_fact.name::not_norm; fio_fact.normal_name) Initials;
FIO -> ExpSurname interp (fio_fact.surname::not_norm; fio_fact.normal_surname) Initials;
FIO -> Initials ExpName interp (fio_fact.name::not_norm; fio_fact.normal_name);
FIO -> Initials ExpSurname interp (fio_fact.surname::not_norm; fio_fact.normal_surname);

IO -> ExpName<gnc-agr[1]> interp (fio_fact.name::not_norm; fio_fact.normal_name)
 Word<gram='отч', gnc-agr[1]> interp (fio_fact.middle_name::not_norm; fio_fact.normal_middle_name);
FIO -> (Initial) IO | IO (Initial);

FIO -> BaseName interp (fio_fact.name::not_norm; fio_fact.normal_name);
FIO -> BaseSurname interp (fio_fact.surname::not_norm; fio_fact.normal_surname);

S -> FIO interp (fio_fact.text::not_norm);