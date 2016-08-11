from communications import uri
import yaolink as y

uri_patterns = [
    uri('^$', y.gen_home),
    uri('^r/', y.get_raw),
    uri('^p/', y.gen_page),
    uri('^favicon.ico', y.get_icon),
    uri('^d/', y.get_download),
    uri('^me/', y.get_prof),
]
