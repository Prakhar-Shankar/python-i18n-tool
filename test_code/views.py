import gettext

lang = gettext.translation("messages", localedir="locales", languages=["fr"])
lang.install()
_ = lang.gettext

def welcome_user():
    print(_("user.name"))
    print(_("user.age"))

welcome_user()
