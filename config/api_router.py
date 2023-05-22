from rest_framework_extensions.routers import ExtendedDefaultRouter

import users.views

router = ExtendedDefaultRouter()

"""
register(prefix, viewset, base_name)
prefix 该视图集的路由前缀
viewset 视图集
base_name 路由名称的前缀
"""
router.register("user", users.views.UserView, basename="user")
router.register("user/exchange", users.views.UserExchangeAccountView, basename="exchange")
router.register(("accounts"), users.views.GitHubOAuth2LoginView, basename="accounts")

urlpatterns = router.urls + []
