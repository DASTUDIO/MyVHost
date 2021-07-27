from pub.response.wrap import page
from pub.forms.search import form_search_user,form_search_keyword

def search(r,f,p):

    f_userid = form_search_user(r.GET)

    f_keyword = form_search_keyword(r.GET)

    if f_userid.is_valid():
        return page(r, 'search.html', {'s_userid': f_userid.cleaned_data['userid']})
    elif f_keyword.is_valid():
        return page(r, 'search.html', {'s_keyword': f_keyword.cleaned_data['keyword']})
    else:
        return page(r, 'search.html', {})