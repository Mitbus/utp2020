#encoding "utf8"

Domen -> Word<wff=/(https?)|(ftp)/> ":" "/" "/"
 AnyWord<wff=/([a-z0-9]{1})((\.[a-z0-9-])|([a-z0-9-]))*\.([a-z]{2,6})/>;
Domen -> AnyWord<wff=/([a-z0-9]{1})((\.[a-z0-9-])|([a-z0-9-]))*\.([a-z]{2,6})/>;

Path -> AnyWord<wff=/((\.[a-zA-Z0-9])|[a-zA-Z0-9-_])*/> ("/");
Path -> AnyWord<wff=/((\.[a-zA-Z0-9])|[a-zA-Z0-9-_])*/> "/" Path;

Addr -> Domen | Domen "/" Path;

S -> Addr interp (url_fact.text);