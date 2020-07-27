#encoding "utf8"
#GRAMMAR_KWSET ["fio_gram", "bank_gram", "geo_gram"]

GeoName -> AnyWord<gram='geo'>;

GeoObj -> (AnyWord<kwtype=geo_deskr>) GeoName;
GeoObj -> GeoName (",") (AnyWord<kwtype=geo_deskr>);

GeoFact -> GeoObj | GeoObj "," GeoFact;
S -> GeoFact; //interp (geo_fact.text::not_norm; geo_fact.normal);