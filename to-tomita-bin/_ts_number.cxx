
#encoding "utf8"

rus -> "RUS" | "Rus" | "rus";
RegionNum -> AnyWord<wff=/[0-9]?[0-9]?[0-9]/>;

Region -> ("-") RegionNum (rus);
Region -> AnyWord<wff=/-?[0-9]?[0-9]?[0-9]?-?((RUS)|(Rus)|(rus))/>;

CarNum -> AnyWord<wff=/[а-я, А-Я]-?[0-9][0-9][0-9]-?[а-я, А-Я][а-я, А-Я]-?[0-9]?[0-9]?[0-9]?-?((RUS)|(Rus)|(rus))/>;
CarNum -> AnyWord<wff=/[а-я, А-Я]-?[0-9][0-9][0-9]-?[а-я, А-Я][а-я, А-Я]/> ("|") (Region);
CarNum -> AnyWord<wff=/[а-я, А-Я]/> AnyWord<wff=/[0-9][0-9][0-9]/> AnyWord<wff=/[а-я, А-Я][а-я, А-Я]/> ("|") (Region);

S -> CarNum interp (ts_fact.text);